# todo(maximsmol): add a "trace_class_function" decorator that adds path, flags, etc. to all
# todo(maximsmol): custom instrumentation for aiohttp
# todo(maximsmol): instrument pathlib + os functions

import asyncio
import errno
import json
import mimetypes
import os
import stat
import sys
import time
import traceback
from collections import defaultdict
from collections.abc import Callable, Coroutine, Iterator
from concurrent.futures import Future
from contextlib import AbstractAsyncContextManager, asynccontextmanager, contextmanager
from datetime import datetime
from functools import wraps
from io import BufferedRandom
from math import ceil, floor
from pathlib import Path, PurePosixPath
from threading import Barrier, Condition, RLock, Semaphore, Thread, get_ident
from typing import Any, ClassVar, TypedDict, TypeVar

import aiohttp
import fuse
from fuse import Fuse
from latch_o11y.o11y import app_tracer, dict_to_attrs, trace_app_function
from opentelemetry.trace import Context, Status, StatusCode, get_current_span
from typing_extensions import ParamSpec

import queries_lib.main as qlib
from graphql_generate.support import (
    GqlContext,
    GqlError,
    GqlSubscriptionData,
    GqlSubscriptionErrors,
    GqlWebSocketContext,
    WebSocketClosedException,
)
from queries_lib.schema import LdataNodeType

from .config import config

sys.stdout.reconfigure(line_buffering=True)  # type: ignore

fuse.fuse_python_api = (0, 2)


def always_true():
    return True


P = ParamSpec("P")
R = TypeVar("R")

ws_id: str = "not_set"
pod_id: str = "not_set"


def syscall_impl(f: Callable[P, R]) -> Callable[P, R | int]:
    @wraps(f)
    @trace_app_function
    def inner(*args: P.args, **kwargs: P.kwargs) -> R | int:
        span = get_current_span()
        span.update_name(f"syscall:{f.__name__}")
        span.set_attributes({"ws_id": ws_id, "pod_id": pod_id})

        try:
            res = f(*args, **kwargs)

            if isinstance(res, int) and res < 0:
                err = errno.errorcode[-res]
                span.set_status(Status(StatusCode.ERROR, err))

            span.set_status(Status(StatusCode.OK))
            return res
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, "EIO"))
            span.record_exception(e)
            traceback.print_exc()
            return -errno.EIO

    return inner


class LatchStat(fuse.Stat):
    def __init__(self):
        # https://linux.die.net/man/2/stat
        self.st_dev = 0  # id of device containing file
        self.st_ino = 0  # inode number
        self.st_mode = 0  # protection
        self.st_nlink = 0  # number of hard links
        self.st_uid = 0  # user id of owner
        self.st_gid = 0  # group id of owner
        self.st_size = 0  # total size in bytes
        self.st_atime = 0  # time of last access
        self.st_mtime = 0  # time of last modification
        self.st_ctime = 0  # time of last status change


T = TypeVar("T")


class RequestThread:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self._run)

    def run(self):
        self.thread.start()

    @trace_app_function
    def stop(self):
        helper_task = None

        async def helper():
            to_cancel = [
                x
                for x in asyncio.tasks.all_tasks(asyncio.get_event_loop())
                if x.get_coro() is not helper_task
            ]
            for t in to_cancel:
                t.cancel("Requester thread shutting down")

            results = await asyncio.gather(*to_cancel, return_exceptions=True)
            for res in results:
                if not isinstance(res, Exception):
                    continue

                print("Uncaught exception at requester thread async loop shutdown:")
                traceback.print_exception(res)

            await self.loop.shutdown_asyncgens()
            await self.loop.shutdown_default_executor()

        stop_barrier = Barrier(2)

        def stop_helper():
            self.loop.stop()
            stop_barrier.wait()

        try:
            helper_task = helper()
            self.call(helper_task)

            self.loop.call_soon_threadsafe(stop_helper)
            stop_barrier.wait()
        finally:
            self.loop.close()

    def _run(self):
        self.loop.run_forever()

    @trace_app_function
    def call_as_future(self, cb: Coroutine[Any, Any, T]) -> Future:
        span = get_current_span()
        span.set_attribute("callback", cb.__qualname__)
        return asyncio.run_coroutine_threadsafe(cb, self.loop)

    @trace_app_function
    def call(self, cb: Coroutine[Any, Any, T], timeout: float | None = None) -> T:
        span = get_current_span()
        span.set_attributes({"callback": cb.__qualname__, "timeout": str(timeout)})
        res = self.call_as_future(cb)
        return res.result(timeout)


def ldata_node_type_to_flag(x: LdataNodeType) -> int:
    if x in {
        LdataNodeType.dir,
        LdataNodeType.account_root,
        LdataNodeType.mount,
        LdataNodeType.mount_gcp,
        LdataNodeType.mount_azure,
    }:
        return stat.S_IFDIR

    if x == LdataNodeType.obj:
        return stat.S_IFREG

    return 0


open_flags = {
    # https://man7.org/linux/man-pages/man2/open.2.html
    os.O_RDONLY: "O_RDONLY",
    os.O_WRONLY: "O_WRONLY",
    os.O_RDWR: "O_RDWR",
    os.O_APPEND: "O_APPEND",
    os.O_ASYNC: "O_ASYNC",
    os.O_CLOEXEC: "O_CLOEXEC",
    os.O_CREAT: "O_CREAT",  # 1
    # os.O_DIRECT: "O_DIRECT", # 2
    os.O_DIRECTORY: "O_DIRECTORY",
    os.O_DSYNC: "O_DSYNC",
    os.O_EXCL: "O_EXCL",  # 1
    # os.O_LARGEFILE: "O_LARGEFILE", # 2
    # os.O_NOATIME: "O_NOATIME", # 2
    os.O_NOCTTY: "O_NOCTTY",  # 1
    os.O_NOFOLLOW: "O_NOFOLLOW",
    os.O_NONBLOCK: "O_NONBLOCK",
    os.O_NDELAY: "O_NDELAY",
    # os.O_PATH: "O_PATH", # 2
    os.O_SYNC: "O_SYNC",
    # os.O_TMPFILE: "O_TMPFILE", # 2
    os.O_TRUNC: "O_TRUNC",
    # 1 filtered out by the kernel according to libFUSE docs
    # https://libfuse.github.io/doxygen/structfuse__operations.html#a08a085fceedd8770e3290a80aa9645ac
    # 2 not on mac
}


def human_readable_open_flags(flags: int):
    res: list[str] = []
    for k, v in open_flags.items():
        if (k & flags) == 0:
            continue

        res.append(v)

    return " | ".join(res)


mode_flags = {
    stat.S_IFBLK: "S_IFBLK",
    stat.S_IFCHR: "S_IFCHR",
    stat.S_IFIFO: "S_IFIFO",
    stat.S_IFREG: "S_IFREG",
    stat.S_IFDIR: "S_IFDIR",
    stat.S_IFLNK: "S_IFLNK",
    stat.S_IRUSR: "S_IRUSR",
    stat.S_IWUSR: "S_IWUSR",
    stat.S_IXUSR: "S_IXUSR",
    stat.S_IRGRP: "S_IRGRP",
    stat.S_IWGRP: "S_IWGRP",
    stat.S_IXGRP: "S_IXGRP",
    stat.S_IROTH: "S_IROTH",
    stat.S_IWOTH: "S_IWOTH",
    stat.S_IXOTH: "S_IXOTH",
}


def human_readable_mode(mode: int):
    res: list[str] = []
    for k, v in mode_flags.items():
        if (k & mode) == 0:
            continue

        res.append(v)

    return " | ".join(res)


MAXIMUM_UPLOAD_SIZE = 5 * 2**40  # 5 TiB
MAXIMUM_UPLOAD_PARTS = 10000


class LDataFile:
    upload_part_size: ClassVar[int] = (
        256 * 2**20
    )  # Minimum upload part size is 5MiB, cannot set less than that

    download_part_size: ClassVar[int] = 1 * 2**20

    keep_cache = False

    workfile: BufferedRandom
    cached: qlib.NodeInfoFragment

    @trace_app_function
    def __init__(self, fs: "LDataFS", path: str, flags: int, mode: int):
        self.fs = fs
        self.path = PurePosixPath(path)
        self.flags = flags
        self.mode = mode

        self.io_lock = RLock()
        self.part_finished_cv = Condition()
        self.download_futures: list[Future] = []

        self.max_concurrent_downloads = 10
        self.concurrent_downloads = Semaphore(self.max_concurrent_downloads)
        self.cv_bins = 1000
        self.download_failed = False

        self.content_size = 0

        self.wrote_anything = False

    @trace_app_function
    def _download(self):
        span = get_current_span()
        span.set_attribute("path", str(self.path))
        self.download_failed = False

        @trace_app_function
        async def get_signed_url():
            span = get_current_span()
            span.set_attribute("path", str(self.path))

            path = f"latch://{str(self.path)}"

            async with self.fs.nucleus_sess.post(
                "/ldata/get-signed-url",
                json={
                    "path": path,
                    "egress_event_data": {"purpose": "ldata-fuse"},
                },
            ) as res:
                json_data = await res.json()
                if "data" not in json_data:
                    raise RuntimeError(
                        f"could not get download url for {path}: {json_data}"
                    )
                return json_data["data"]["url"]

        @trace_app_function
        async def schedule_downloads(content_size: int):
            span = get_current_span()
            span.set_attributes({"path": str(self.path), "content_size": content_size})

            download_jobs = []

            for i in range(ceil(content_size / self.download_part_size)):
                download_jobs.append(download_part(presigned, i))
                if len(download_jobs) >= self.max_concurrent_downloads:
                    await asyncio.gather(*download_jobs)
                    download_jobs = []

            await asyncio.gather(*download_jobs)

        @trace_app_function
        async def download_part(url: str, i: int):
            span = get_current_span()
            span.update_name("download_part")
            span.set_attributes({"part": i, "path": str(self.path)})
            headers = {
                "Range": (
                    f"bytes={i * self.download_part_size}-{(i+1) * self.download_part_size}"
                )
            }
            try:
                async with self.fs.generic_sess.get(url, headers=headers) as res:
                    if not res.ok:
                        raise RuntimeError(
                            f"could not download ({res.status}): [part {i}] {self.path}"
                        )

                    offset = i * self.download_part_size
                    with app_tracer.start_as_current_span("write"):
                        async for chunk in res.content.iter_any():
                            os.pwrite(self.workfile.fileno(), chunk, offset)
                            offset += len(chunk)
                        self.workfile.flush()
            except Exception as e:
                self.download_failed = True
                span.record_exception(e)
                raise e
            finally:
                with self.part_finished_cv:
                    self.bitmap |= 1 << i
                    self.part_finished_cv.notify_all()

        presigned = self.fs.req_thread.call(get_signed_url(), 60)

        meta = self.cached["ldataObjectMeta"]
        self.content_size = 0
        if meta is not None and meta["contentSize"] is not None:
            self.content_size = int(meta["contentSize"])

        self.bitmap = 0
        self.fs.req_thread.call_as_future(schedule_downloads(self.content_size))

    @syscall_impl
    def open(self):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {
                    "path": str(self.path),
                    "flags": human_readable_open_flags(self.flags),
                    "flags.raw": self.flags,
                    "mode": human_readable_mode(self.mode),
                    "mode.raw": self.mode,
                },
                "args",
            )
        )

        parent_cached = self.fs.load_subtree(str(self.path.parent))
        if parent_cached is None:
            return -errno.ENOENT

        cached = parent_cached.get(self.path.name)
        if cached is None:
            return -errno.ENOENT

        flt = cached["finalLinkTarget"]
        assert flt is not None
        self.cached = flt

        node_id = self.cached["id"]
        self.fs.ldata_path_to_node_cache[str(self.path)] = node_id
        self.fs.ldata_node_to_path_cache[node_id].add(str(self.path))
        workfile_p = self.fs.workdir_path / node_id

        # need write and create to download the file
        # need read because we need to read the file out again to upload it
        flags = self.flags
        flags &= ~os.O_RDONLY
        flags &= ~os.O_WRONLY
        flags |= os.O_RDWR | os.O_CREAT

        with self.io_lock:
            # for truncate/new files this will succeed without downloading
            fd = os.open(str(workfile_p), flags, self.mode)

            # afaik mode here doesn't matter beyond the binary specifier
            self.workfile = os.fdopen(fd, "rb+")
            # todo(maximsmol): unbuffer here? shouldn't matter I think

            if (flags & os.O_TRUNC) == 1:
                return

            with app_tracer.start_as_current_span(
                "Path.tell",
                attributes={
                    "path": str(self.workfile),
                },
            ):
                # if not truncating, ensure the file is downloaded
                pos = self.workfile.tell()
                if pos != 0:
                    return
            self._download()
            self.workfile.seek(0, os.SEEK_SET)

    @classmethod
    @trace_app_function
    async def upload(
        cls,
        fs: "LDataFS",
        path: PurePosixPath,
        size: int,
        get_reader: Callable[[int], Iterator[bytes]] | None,
    ):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {
                    "path": str(path),
                    "size": size,
                },
                "args",
            )
        )

        if size > 0 and get_reader is None:
            raise ValueError("get_reader must be provided for files of size > 0")

        if size > MAXIMUM_UPLOAD_SIZE:
            raise ValueError(
                f"File {path} is {size} bytes which exceeds the maximum upload size"
                " (5TiB)"
            )

        chunk_size = max(
            cls.upload_part_size,
            ceil(size / MAXIMUM_UPLOAD_PARTS),
        )
        nrof_parts = ceil(float(size) / chunk_size)

        content_type = mimetypes.guess_type(path, strict=False)[0]
        if content_type is None:
            content_type = "application/octet-stream"

        span.set_attributes(
            {
                "content_type": content_type,
                "part_count": nrof_parts,
                "chunk_size": chunk_size,
            }
        )

        # todo(maximsmol): aiofile
        # todo(maximsmol): use data_validation
        async with fs.nucleus_sess.post(
            "/ldata/start-upload",
            json={
                "path": f"latch://{str(path)}",
                "content_type": content_type,
                "part_count": nrof_parts,
            },
        ) as start_res:
            start_data = await start_res.json()

            if "error" in start_data:
                raise RuntimeError(repr(start_data))

            start_res.raise_for_status()

        if "urls" not in start_data["data"]:
            # file of size 0, we're done
            return

        # todo(maximsmol): pararellize this
        # todo(maximsmol): aiofile
        assert get_reader is not None
        reader = get_reader(chunk_size)

        parts = []
        for i, url in enumerate(start_data["data"]["urls"]):
            data = next(reader)
            cur = await fs.generic_sess.put(url, data=data)
            cur.raise_for_status()
            parts.append({"ETag": cur.headers["ETag"], "PartNumber": i + 1})

        # todo(maximsmol): use data_validation
        async with await fs.nucleus_sess.post(
            "/ldata/end-upload",
            json={
                "path": f"latch://{str(path)}",
                "upload_id": start_data["data"]["upload_id"],
                "parts": parts,
            },
        ) as end_res:
            end_data = await end_res.json()
            if "error" in end_data:
                raise RuntimeError(repr(end_data))

            end_res.raise_for_status()

    @syscall_impl
    def fsync(self):
        span = get_current_span()
        span.set_attributes(dict_to_attrs({"path": str(self.path)}, "args"))

        if self.download_failed:
            span.set_attribute("download_failed", True)
            return -errno.EIO

        with self.io_lock:
            span.set_attribute("wrote_anything", self.wrote_anything)
            if not self.wrote_anything:
                # fixme(maximsmol): this would likely be wrong semantics, need to examine
                # what native filesystems do

                # self.fs.schedule_refresh(str(self.path.parent))
                # self._download()
                return

            self.workfile.flush()
            os.fsync(self.workfile)

            # need to upload
            async def helper():
                pos = self.workfile.tell()
                try:
                    self.workfile.seek(0, os.SEEK_END)
                    size = self.workfile.tell()
                    self.workfile.seek(0, os.SEEK_SET)

                    def read_part(chunk_size: int) -> Iterator[bytes]:
                        def _read_part():
                            while True:
                                res = self.workfile.read(chunk_size)
                                if len(res) == 0:
                                    break

                                yield res

                        return _read_part()

                    await LDataFile.upload(self.fs, self.path, size, read_part)
                finally:
                    self.workfile.seek(pos, os.SEEK_SET)

        def ensure_not_pending():
            cache = self.fs.load_subtree_from_cache(str(self.path.parent))
            if cache is None:
                return False

            return cache[self.path.name]["pending"] is False

        # todo(maximsmol): scale timeout with content size?
        # note(taras): needs refresh since has to go through ribosome. Should we just update the cached size in-place?
        with self.fs.ensure_refresh(
            str(self.path.parent),
            subscription_timeout=30,
            timeout=60 * 5,
            refresh_filter=ensure_not_pending,
        ):
            self.fs.req_thread.call(helper(), 60 * 5)

        # our version is authoritative, no need to re-download
        self.wrote_anything = False

    @syscall_impl
    def flush(self):
        # note(taras): this function is called on `close` (each time) and so it needs to sync the file to ldata
        span = get_current_span()
        span.set_attributes(dict_to_attrs({"path": str(self.path)}, "args"))

        self.fsync()

        parent_id = self.fs.ldata_path_to_node_cache.get(str(self.path.parent))
        if parent_id is not None and parent_id in self.fs.ldata_node_cache:
            self.fs.ldata_node_cache.pop(parent_id, None)

    @syscall_impl
    def release(self):
        # note(taras): release is asynchronous, so script can start executing next commands before this is finished. For operations that need to block the `close` call use `flush`.
        span = get_current_span()
        span.set_attributes(dict_to_attrs({"path": str(self.path)}, "args"))

        with self.io_lock:
            for future in self.download_futures:
                if not future.done():
                    future.cancel()

            self.workfile.close()

            node_id = self.cached["id"]
            workfile_p = self.fs.workdir_path / node_id

            # UNIX semantics let us unlink even when other open descriptors exist
            # the descriptors will work as if nothing happened but
            # the file will not be resolvable by path anymore
            # I'm doing it here to make sure the next open() re-downloads the file from S3
            try:
                workfile_p.unlink()
                span.set_attribute("workfile.already_unlinked", False)
            except FileNotFoundError:
                span.set_attribute("workfile.already_unlinked", True)

    @syscall_impl
    def read(self, size, offset):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": str(self.path), "size": size, "offset": offset}, "args"
            )
        )

        start = floor(offset / self.download_part_size)
        end = ceil(min(size + offset, self.content_size) / self.download_part_size)

        span.set_attributes({"start_chunk": start, "end_chunk": end})

        mask = 1 << (end - start)
        mask -= 1
        mask = mask << start

        with self.part_finished_cv:
            while (self.bitmap & mask) != mask:
                self.part_finished_cv.wait()

        if self.download_failed:
            span.set_attribute("download_failed", True)
            return -errno.EIO

        res = os.pread(self.workfile.fileno(), size, offset)
        return res

    @syscall_impl
    def write(self, data: bytes, offset: int):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": str(self.path), "data.len": len(data), "offset": offset},
                "args",
            )
        )
        if self.download_failed:
            span.set_attribute("download_failed", True)
            return -errno.EIO

        # todo(maximsmol): the semantics here are very suspect
        # 1. since we locally share a buffer, the semantics within one computer are the same as
        # the underlying FS
        # 2. cross-system we get close-to-open consistency but everything else is different
        # e.g. on a normal FS, with concurrent writes, the resulting file can be made
        # of mixed parts, for us one of the systems wins
        # 3. this means cross-system semantics are different from local semantics
        # because locally we do get the possible mixing of parts of the file
        # while cross-system we do not

        with self.io_lock:
            self.wrote_anything = True
            res = os.pwrite(self.workfile.fileno(), data, offset)
            self.workfile.flush()
            return res


P = ParamSpec("P")
R = TypeVar("R")


class NodeCacheEntry(TypedDict):
    path: str | None
    children: dict[
        str,
        qlib.LDataSubtreeByPathQueryResult_LdataResolvePathData_ChildLdataTreeEdges_Nodes_Child,
    ]


class LDataFS(Fuse):
    gql_ctx: GqlContext
    ws_ctx: GqlWebSocketContext
    ws_ctx_manager: AbstractAsyncContextManager
    sub_poller: asyncio.Task

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exiting = False
        self.cache_lock = RLock()

        self.ldata_node_cache: dict[str, NodeCacheEntry] = {}
        self.ldata_path_to_node_cache: dict[str, str] = {}
        self.ldata_node_to_path_cache: dict[str, set[str]] = defaultdict(set)

        self.truncated_files: set[str] = set()

        self.req_thread = RequestThread()

        # todo(maximsmol): switch to map between node id and list of callbacks?
        self.node_update_callbacks: dict[int, tuple[str, Callable]] = {}

        self.parser.add_option("--token", help="Latch SDK token for authorization")
        self.parser.add_option(
            "--pod-id", help="Latch Pod ID for tracing", default="unset"
        )

        # self.parser.add_option(
        #     "--workdir-path",
        # )
        self.workdir_path = Path("./workdir")

        # on to async init

    # todo(maximsmol): flush everything on unmount/destroy()

    async def async_init(self):
        print("init http session", get_ident())
        sess = aiohttp.ClientSession(
            headers={"Authorization": f"Latch-SDK-Token {self.token}"}
        )
        await sess.__aenter__()

        self.gql_ctx = GqlContext(sess, config.gql_endpoint)

        # todo(maximsmol): merge all aiohttps sessions
        self.nucleus_sess = aiohttp.ClientSession(
            headers={"Authorization": f"Latch-SDK-Token {self.token}"},
            base_url=config.nucleus_endpoint,
        )
        await self.nucleus_sess.__aenter__()

        # todo(maximsmol): merge all aiohttps sessions
        self.generic_sess = aiohttp.ClientSession()
        await self.generic_sess.__aenter__()

        print("scheduling poller task")
        self.sub_poller = asyncio.create_task(self.poll_subscriptions())

        print("ready")

    async def poll_subscriptions(self):
        last_died = None
        while not self.exiting:
            self.ws_ctx_manager = self.gql_ctx.ws_connect()
            self.ws_ctx = await self.ws_ctx_manager.__aenter__()

            print("  setting up subscriptions")
            basic_info = await qlib.query_basic_info_query(self.gql_ctx)
            assert basic_info["accountInfoCurrent"] is not None

            print("  current workspace:", basic_info["accountInfoCurrent"]["id"])
            print("  current pod:", pod_id)
            global ws_id
            ws_id = basic_info["accountInfoCurrent"]["id"]

            await qlib.subscribe_latch_data_subscription(
                self.ws_ctx,
                operation_id="node_subscription",
                callback=self.handle_latch_data_notification,
                variables={"workspaceId": basic_info["accountInfoCurrent"]["id"]},
            )

            # todo(maximsmol): die fully if it keeps crashing very frequently
            while not self.ws_ctx.sock.closed:
                try:
                    await self.ws_ctx.poll()
                except WebSocketClosedException as e:
                    print(f"<<< WebSocket poller exited: {repr(e)}")
                    self.ldata_node_cache = {}
                    self.ldata_path_to_node_cache = {}
                    self.ldata_node_to_path_cache = defaultdict(set)
                    self.truncated_files = set()
                    break
                except Exception:
                    traceback.print_exc()

            if last_died is not None and (time.monotonic() - last_died) < 1:
                # died in under a second
                print("\n\n\n[!!!] WebSocket poller keeps dying")
                sys.exit(1)

            last_died = time.monotonic()
            if not self.exiting:
                # we probably crashed for some reason
                await self.ws_ctx_manager.__aexit__(None, None, None)
                print("<<< Restarting WebSocket poller")

    async def handle_latch_data_notification(
        self,
        sub: (
            GqlSubscriptionData[qlib.LatchDataSubscriptionResult]
            | GqlSubscriptionErrors
        ),
    ):
        fn = self.handle_latch_data_notification
        with app_tracer.start_as_current_span(
            fn.__qualname__,
            context=Context(),
            attributes={"code.function": fn.__name__, "code.namespace": fn.__module__},
        ) as span:
            if isinstance(sub, GqlSubscriptionErrors):
                span.set_status(Status(StatusCode.ERROR, json.dumps(sub.errors)))
                return

            span.set_attribute("data", json.dumps(sub.data))

            data = sub.data["consoleLdataNode"]
            assert data is not None

            row_ids = data["rowIds"]
            assert row_ids is not None

            async with asyncio.TaskGroup() as g:
                for x in row_ids:
                    g.create_task(self.fetch_subtree_by_path_async(f"{x}.node"))

    async def async_cleanup(self):
        self.exiting = True

        await self.gql_ctx.sess.__aexit__(None, None, None)
        await self.nucleus_sess.__aexit__(None, None, None)
        await self.generic_sess.__aexit__(None, None, None)
        await self.ws_ctx_manager.__aexit__(None, None, None)
        await self.sub_poller

    def run(self):
        self.parse(errex=1)
        self.token = self.cmdline[0].token

        global pod_id
        pod_id = self.cmdline[0].pod_id

        self.workdir_path.mkdir(parents=True, exist_ok=True)

        self.req_thread.run()
        print("  done")

    @trace_app_function
    def load_subtree_from_cache(self, path: str):
        span = get_current_span()
        span.set_attributes({"path": path})

        res = None

        node_id = self.ldata_path_to_node_cache.get(path)
        if node_id is not None:
            res = self.ldata_node_cache.get(node_id)
            res = res["children"] if res is not None else None

        span.set_attribute("cache_hit", res is not None)
        return res

    @trace_app_function
    async def fetch_subtree_by_path_async(self, path: str):
        span = get_current_span()
        span.set_attributes({"path": path})

        query_res = await qlib.query_l_data_subtree_by_path_query(
            self.gql_ctx, {"path": f"latch://{path}"}
        )

        data = query_res["ldataResolvePathData"]

        with self.cache_lock:
            if data is None:
                self.invalidate_cache(path)
                return None

            node_id = data["id"]
            node_path = data["path"]

            if node_path is not None:
                # get the actual path to always be able to translate path to node id
                node_path = "/" + "/".join(node_path.split("/")[2:])
                self.ldata_path_to_node_cache[node_path] = node_id
                self.ldata_node_to_path_cache[node_id].add(node_path)

            self.ldata_path_to_node_cache[path] = node_id
            self.ldata_node_to_path_cache[node_id].add(path)
            self.ldata_node_cache[node_id] = {
                "path": node_path,
                "children": {
                    x["child"]["name"]: x["child"]
                    for x in data["childLdataTreeEdges"]["nodes"]
                    if x["child"] is not None
                },
            }

            span.set_attributes(
                dict_to_attrs(
                    {
                        "id": node_id,
                        "path": node_path if node_path else "none",
                        "children.len": len(self.ldata_node_cache[node_id]["children"]),
                    },
                    "res",
                )
            )

        num_notified = 0
        for cur_node_id, cb in self.node_update_callbacks.values():
            if node_id != cur_node_id:
                continue

            num_notified += 1
            cb()

        span.set_attribute("waiters_notified", num_notified)

        return self.ldata_node_cache[node_id]["children"]

    @trace_app_function
    def load_subtree(self, path: str, *, use_cache: bool = True):
        get_current_span().set_attributes({"path": path, "use_cache": use_cache})

        if use_cache:
            res = self.load_subtree_from_cache(path)
            if res is not None:
                return res

        return self.req_thread.call(
            self.fetch_subtree_by_path_async(path),
            30,
        )

    # todo(maximsmol): trace this. probably need to propagate spans/context between the threads
    @asynccontextmanager
    async def ensure_refresh_async(
        self,
        path: str,
        *,
        subscription_timeout: float | None = 15,
        refresh_filter: Callable[[], bool] = always_true,
    ):
        node_id = self.ldata_path_to_node_cache.get(path)
        if node_id is None:
            raise RuntimeError(f"cannot ensure refresh of unknown path: {path}")

        ev = asyncio.Event()

        def callback():
            # span.add_event("subscription hit")
            ev.set()

        # this is the pessimistic case that will sometimes miss notifications
        # and retry manually when it happens too fast after the operation commits
        #
        # this is explicitly chosen over the case that sometimes gets a
        # random notification that happened in-between us starting to listen
        # and the operation completing
        # todo(maximsmol): rewrite everything to use filters and the optimistic case instead
        yield

        rejected_subscription_count = 0

        try:
            self.node_update_callbacks[id(callback)] = (node_id, callback)

            try:
                done = False
                while not done:
                    await asyncio.wait_for(ev.wait(), timeout=subscription_timeout)
                    rejected_subscription_count += 1

                    done = refresh_filter()
                    # if not done:
                    #     span.add_event("rejected by refresh filter")

                    # span.set_attribute("refresh.outcome", "subscription hit")
            except TimeoutError:
                # span.add_event("did not refresh in time")
                await self.fetch_subtree_by_path_async(path)
                # span.add_event("refreshed maually")

                # if rejected_subscription_count:
                #     span.set_attribute(
                #         "refresh.outcome", "all subscription hits rejected"
                #     )
                # else:
                #     span.set_attribute("refresh.outcome", "subscription timeout")
            # finally:
            #     span.set_attribute(
            #         "refresh.outcome.num_rejected", rejected_subscription_count
            #     )
        finally:
            del self.node_update_callbacks[id(callback)]

    @contextmanager
    def ensure_refresh(
        self,
        path: str,
        *,
        subscription_timeout: float | None = 15,
        timeout: float | None = 15,
        refresh_filter: Callable[[], bool] = always_true,
    ):
        ctx = self.ensure_refresh_async(
            path,
            subscription_timeout=subscription_timeout,
            refresh_filter=refresh_filter,
        )

        self.req_thread.call(ctx.__aenter__(), timeout=timeout)
        try:
            yield
        finally:
            self.req_thread.call(ctx.__aexit__(*sys.exc_info()), timeout=timeout)

    @syscall_impl
    def getattr(self, path: str):
        # todo(maximsmol): this does not work properly with symlinks
        span = get_current_span()

        span.set_attributes(
            dict_to_attrs(
                {"path": path},
                "args",
            )
        )

        st = LatchStat()
        st.st_mode |= stat.S_IRWXU
        st.st_mode |= stat.S_IRWXG
        st.st_mode |= stat.S_IRWXO

        if path == "/":
            st.st_mode |= ldata_node_type_to_flag(LdataNodeType.account_root)
            return st

        p = PurePosixPath(path)
        parent_cached = self.load_subtree(str(p.parent))
        if parent_cached is None:
            return -errno.ENOENT

        cached = parent_cached.get(p.name)
        if cached is None:
            return -errno.ENOENT

        flt = cached["finalLinkTarget"]
        assert flt is not None
        st.st_mode |= ldata_node_type_to_flag(flt["type"])

        meta = cached["ldataObjectMeta"]
        if meta is not None:
            size = meta["contentSize"]
            if size is not None:
                st.st_size = int(size)

            mtime = meta["modifyTime"]
            if mtime is None:
                # todo(maximsmol): report creation time somehow where supported?
                mtime = meta["birthTime"]
            if mtime is not None:
                st.st_mtime = int(datetime.fromisoformat(mtime).timestamp())

            st.st_atime = st.st_mtime
            st.st_ctime = st.st_mtime

        span.set_attributes(
            dict_to_attrs(
                {
                    "node.id": cached["id"],
                    "node.flt.id": flt["id"],
                    "node.flt.type": flt["type"].name,
                    "st.mode": st.st_mode,
                    "st.size": st.st_size,
                    "st.mtime": st.st_mtime,
                },
                "res",
            )
        )

        return st

    @syscall_impl
    def readdir(self, path: str, offset: int):
        # todo(maximsmol): support offset
        # todo(maximsmol): benchmark stateful listing
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "offset": offset},
                "args",
            )
        )

        data = self.load_subtree(path)
        if data is None:
            return -errno.ENOENT

        yield fuse.Direntry(".")
        yield fuse.Direntry("..")

        span.set_attribute("res.len", len(data))

        count = 0
        for cur in data.values():
            if cur["pending"]:
                continue

            if cur["removed"]:
                continue

            if cur["name"] == "":
                continue

            flt = cur["finalLinkTarget"]
            assert flt is not None

            res = fuse.Direntry(
                cur["name"],
                type=ldata_node_type_to_flag(flt["type"]),
            )

            if count < 10:
                span.set_attribute(f"res.{count}", f"{res.name}-{res.type}")
                count += 1

            yield res

        return -errno.ENOENT

    @syscall_impl
    def mkdir(self, path: str, mode: int):
        span = get_current_span()
        # semantics: we ignore mode
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "mode": human_readable_mode(mode), "mode.raw": mode},
                "args",
            )
        )

        if not path.endswith("/"):
            path = path + "/"

        try:
            self.req_thread.call(
                qlib.query_mkdir_mutation(self.gql_ctx, {"path": f"latch://{path}"}),
                10,
            )

            self.invalidate_parent_cache(path)

        except GqlError as e:
            first = e.errors[0]
            if first["message"] == "Node already exists":
                return -errno.EEXIST

            if first["message"] == "Parent directory does not exist":
                return -errno.ENOENT

            raise e

    @syscall_impl
    def rmdir(self, path: str):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {
                    "path": path,
                },
                "args",
            )
        )

        if not path.endswith("/"):
            path = path + "/"

        try:
            self.req_thread.call(
                qlib.query_rmdir_mutation(self.gql_ctx, {"path": f"latch://{path}"}),
                5,
            )
        except GqlError as e:
            first = e.errors[0]
            if first["message"] == "Node does not exist or signer lacks permissions":
                return -errno.ENOENT

            if first["message"] == "Node is not a directory":
                # todo(maximsmol): support mounts/account roots/etc.
                return -errno.ENOTDIR

            if first["message"] == "Directory is not empty":
                return -errno.ENOTEMPTY

            raise e
        finally:
            self.invalidate_cache(path)

    @trace_app_function
    def invalidate_parent_cache(self, path: str):
        # invalidate the parent, so that if someone needs to use this node, they have to refresh cache
        with self.cache_lock:
            parent_id = self.ldata_path_to_node_cache.get(
                str(PurePosixPath(path).parent)
            )
            if parent_id is not None:
                self.ldata_node_cache.pop(parent_id, None)

    @trace_app_function
    def invalidate_cache(self, path: str):
        span = get_current_span()
        path = str(PurePosixPath(path))
        span.set_attributes(
            dict_to_attrs(
                {
                    "path": path,
                },
                "args",
            )
        )

        with self.cache_lock:
            node_id = self.ldata_path_to_node_cache.get(path)
            if node_id is None:
                return

            def invalidate_parent(node_id: str):
                node_cache = self.ldata_node_cache.get(node_id)
                if node_cache is None or node_cache["path"] is None:
                    return

                node_path = PurePosixPath(node_cache["path"])

                parent_id = self.ldata_path_to_node_cache.get(str(node_path.parent))
                if parent_id is None:
                    return

                parent_cache = self.ldata_node_cache.get(parent_id)
                if (
                    parent_cache is None
                    or parent_cache["children"].get(node_path.name) is None
                ):
                    return

                del parent_cache["children"][node_path.name]

            def invalidate_children(node_id: str):
                to_process = [node_id]

                while len(to_process) > 0:
                    node_id = str(to_process.pop())

                    for path in self.ldata_node_to_path_cache[node_id]:
                        self.ldata_path_to_node_cache.pop(path, None)

                    if node_id in self.ldata_node_cache:
                        for child in self.ldata_node_cache[node_id][
                            "children"
                        ].values():
                            to_process.append(child["id"])
                        self.ldata_node_cache.pop(node_id, None)

                    self.ldata_node_to_path_cache.pop(node_id, None)

            invalidate_parent(node_id)
            invalidate_children(node_id)

    @syscall_impl
    def unlink(self, path: str):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {
                    "path": path,
                },
                "args",
            )
        )

        # semantics are not the same as on a normal FS
        # if somebody unlinks a file after its been opened, the file will
        # be recreated when `close` gets called. a normal FS would end up with no file instead
        #
        # basically we act as if all unclosed opens happen after unlink even if that's not true
        #
        # a `close` is still a barrier that `open` cannot move past

        try:
            self.req_thread.call(
                qlib.query_unlink_mutation(self.gql_ctx, {"path": f"latch://{path}"}),
                5,
            )
        except GqlError as e:
            first = e.errors[0]
            if first["message"] == "Node does not exist or signer lacks permissions":
                return -errno.ENOENT

            if first["message"] == "Node is not a file":
                # todo(maximsmol): not necessarily a directory
                return -errno.EISDIR

            raise e
        finally:
            self.invalidate_cache(path)

    @trace_app_function
    def open(self, path: str, flags: int, mode: int = 0o777):
        res = LDataFile(self, path, flags, mode)

        errno = res.open()
        if errno is not None:
            return errno

        # todo(maximsmol): support kernel cache
        # self.Invalidate(path)

        return res

    @trace_app_function
    def fsync(self, path: str, datasync: int, f: LDataFile):
        # todo(maximsmol): semantics:
        # > If the datasync parameter is non-zero, then only the user data should be flushed, not the meta data.
        # we don't care probably since uploading user data would trigger a ribo sync anyway
        return f.fsync()

    @trace_app_function
    def flush(self, path: str, f: LDataFile):
        if path in self.truncated_files:
            f.wrote_anything = True
            self.truncated_files.remove(path)
        return f.flush()

    @trace_app_function
    def release(self, path: str, flags: int, f: LDataFile):
        return f.release()

    @trace_app_function
    def read(self, path: str, size: int, offset: int, f: LDataFile):
        return f.read(size, offset)

    @trace_app_function
    def write(self, path: str, data: bytes, offset: int, f: LDataFile):
        return f.write(data, offset)

    @syscall_impl
    def mknod(self, path: str, mode: int, device: int):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {
                    "path": path,
                    "mode": human_readable_mode(mode),
                    "mode.raw": mode,
                    "device": device,
                },
                "args",
            )
        )

        # semantics: we are violating the mode here since we ignore perms bits

        if device != 0 or stat.S_IFMT(mode) != stat.S_IFREG:
            # todo(maximsmol): only supporting the most common case of creating regular files
            return -errno.ENOSYS

        p = PurePosixPath(path)

        self.req_thread.call(LDataFile.upload(self, p, 0, None), 5)

        self.invalidate_parent_cache(path)

    @trace_app_function
    def create(self, path, flags: int, mode: int):
        get_current_span().set_attributes(
            dict_to_attrs(
                {
                    "path": path,
                    "flags": human_readable_open_flags(flags),
                    "flags.raw": flags,
                    "mode": human_readable_mode(mode),
                    "mode.raw": mode,
                },
                "args",
            )
        )

        return -errno.ENOSYS

    @syscall_impl
    def truncate(self, path, size):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "size": size},
                "args",
            )
        )

        if size != 0:
            # todo(maximsmol): currently only support the most common case of emptying the file
            return -errno.ENOSYS

        self.truncated_files.add(path)

        node_id = self.ldata_path_to_node_cache.get(path)
        span.set_attribute("node_id", str(node_id))
        if node_id is None:
            return

        workfile = self.workdir_path / node_id
        span.set_attribute("workfile", str(workfile))
        try:
            os.truncate(str(workfile), 0)
            span.set_attribute("workfile.truncated", True)
        except FileNotFoundError:
            span.set_attribute("workfile.truncated", False)

    @syscall_impl
    def chmod(self, path: str, mode: int):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "mode": human_readable_mode(mode), "mode.raw": mode},
                "args",
            )
        )
        # unsupported, noop
        return

    @syscall_impl
    def chown(self, path: str, uid: int, gid: int):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "uid": uid, "gid": gid},
                "args",
            )
        )
        # unsupported, noop
        return

    @syscall_impl
    def utimens(self, path: str, a_time: float, m_time: float):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "a_time": a_time, "m_time": m_time},
                "args",
            )
        )
        # unsupported, noop
        return

    @syscall_impl
    def utime(self, path: str, a_time: float, m_time: float):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"path": path, "a_time": a_time, "m_time": m_time},
                "args",
            )
        )
        # unsupported, noop
        return

    @syscall_impl
    def rename(self, src: str, dst: str):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {
                    "src": src,
                    "dst": dst,
                },
                "args",
            )
        )

        src_path = f"latch://{src}"
        dst_path = f"latch://{dst}"

        try:
            # note(taras): needs refresh since this needs to go through ribosome for copies/metadata updates
            with self.ensure_refresh(str(PurePosixPath(dst).parent)):
                self.req_thread.call(
                    qlib.query_l_data_rename_fuse_mutation(
                        self.gql_ctx,
                        {
                            "srcPath": str(src_path),
                            "destPath": str(dst_path),
                        },
                    ),
                    5,
                )
                self.invalidate_cache(src)
        except GqlError as e:
            first = e.errors[0]
            if (
                first["message"]
                == "Source node does not exist or signer lacks permissions"
            ):
                return -errno.ENOENT

            if (
                first["message"]
                == "Destination parent node does not exist or signer lacks permissions"
            ):
                return -errno.ENOENT

            if first["message"] == "Refusing to make node its own parent":
                return -errno.EINVAL

            if (
                first["message"]
                == "Destination node is a directory but source node is not"
            ):
                return -errno.EISDIR

            if first["message"] == "Destination node is not empty":
                return -errno.ENOTEMPTY

            raise e

        return

    @syscall_impl
    def fallocate(self, fd: int, mode: int, offset: int, len: int):
        span = get_current_span()
        span.set_attributes(
            dict_to_attrs(
                {"fd": fd, "mode": mode, "offset": offset, "len": len}, "args"
            )
        )
        # nothing to do
        # todo(maximsmol): is that so?
        return

    @syscall_impl
    def statfs(self):
        res = fuse.StatVfs()

        # todo(maximsmol): idk
        res.f_bsize = 128 * 1024
        res.f_frsize = 128 * 1024

        res.f_blocks = 1000_000_000
        res.f_bfree = res.f_blocks
        res.f_bavail = res.f_blocks

        res.f_files = 1000_000_000
        res.f_ffree = res.f_files
        res.f_favail = res.f_files

        res.f_namemax = 1024  # AWS S3 limit (we only care about this for mounts)

        return res


def main():
    with app_tracer.start_as_current_span("Write PID"):
        Path("fuse.pid").write_text(str(os.getpid()) + "\n")

    with app_tracer.start_as_current_span("Create FS instance"):
        server = LDataFS(
            version="%prog " + fuse.__version__,
            usage=Fuse.fusage,
            dash_s_do="setsingle",
        )
    try:
        with app_tracer.start_as_current_span("Initialize"):
            server.run()
            server.req_thread.call(server.async_init())

        print("Mounting")
        server.main()
        print("Exiting")
    finally:
        with app_tracer.start_as_current_span("Cleanup"):
            server.req_thread.call(server.async_cleanup())

            server.req_thread.stop()
            server.req_thread.thread.join()

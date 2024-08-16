import json
from collections import defaultdict
from pathlib import PurePosixPath

path_cache = {
    "/": "71256333",
    "71909694.node": "71909694",
    "71897518.node": "71897518",
    "71909706.node": "71909706",
}
node_cache = {
    "71256333": {
        "fusedir": {"id": "71897518", "name": "fusedir", "type": "LdataNodeType.dir"}
    },
    "71909694": {
        "a.txt": {"id": "71909706", "name": "a.txt", "type": "LdataNodeType.obj"}
    },
    "71897518": {
        "dir3": {"id": "71909499", "name": "dir3", "type": "LdataNodeType.dir"},
        "dir4": {"id": "71909694", "name": "dir4", "type": "LdataNodeType.dir"},
    },
    "71909706": {},
}
"""
algo
- get node id from path
- get dir from the node id with the child ids
- delete node id key from the node_cache
- search and delete all keys in path cache with the node id
"""
from copy import deepcopy


def print_node_cache():
    cache = deepcopy(node_cache)
    for key in cache.keys():
        for child_key, v in cache[key].items():
            cache[key][child_key] = {
                "id": v["id"],
                "name": v["name"],
                "type": str(v["type"]),
            }
    print(json.dumps(cache, indent=2))


def invalidate_cache(path):
    node_id = path_cache.get(path)
    if node_id is None:
        return

    reverse_lookup = defaultdict(list)
    for k, v in path_cache.items():
        reverse_lookup[v].append(k)

    real_path = [p for p in reverse_lookup[node_id] if ".node" not in p][0]
    parent_path = str(PurePosixPath(real_path).parent)
    parent_id = path_cache.get(parent_path)

    to_process = [node_id]

    while to_process:
        node_id = str(to_process.pop())
        for path in reverse_lookup[node_id]:
            path_cache.pop(path, None)
        for child_id in node_cache[node_id].values():
            to_process.append(child_id)
        node_cache.pop(node_id, None)

    if parent_id is not None:
        for path in reverse_lookup[parent_id]:
            path_cache.pop(path, None)
        node_cache.pop(parent_id, None)


invalidate_cache("71909694.node")

path_cache = {
    "/": "71256333",
    "71909694.node": "71909694",
    "71897518.node": "71897518",
    "71909706.node": "71909706",
}
node_cache = {
    "71256333": {
        "fusedir": {"id": "71897518", "name": "fusedir", "type": "LdataNodeType.dir"}
    },
    "71909694": {
        "a.txt": {"id": "71909706", "name": "a.txt", "type": "LdataNodeType.obj"}
    },
    "71897518": {
        "dir3": {"id": "71909499", "name": "dir3", "type": "LdataNodeType.dir"},
        "dir4": {"id": "71909694", "name": "dir4", "type": "LdataNodeType.dir"},
    },
    "71909706": {},
}

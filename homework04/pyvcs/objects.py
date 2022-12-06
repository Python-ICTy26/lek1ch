import hashlib
import pathlib
import re
import typing as tp
import zlib

from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    hashed = hashlib.sha1(store).hexdigest()
    if write:
        gitdir = repo_find(".")
        path = gitdir / "objects" / hashed[:2]
        if not path.exists():
            path.mkdir()
        with open(path / hashed[2:], "wb") as f:
            f.write(zlib.compress(store))
    return hashed


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    files = (gitdir / "objects" / obj_name[:2]).iterdir()
    res = [obj_name[:2] + el.name for el in files if el.name.startswith(obj_name[2:])]
    if not (4 <= len(obj_name) <= 40) or len(res) == 0:
        raise Exception(f"Not a valid object name {obj_name}")
    return res


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    with open(gitdir / "objects" / sha[:2] / sha[2:], "rb") as f:
        data = zlib.decompress(f.read())
    content = data[data.find(b"\x00") + 1 :]
    fmt = data[: data.find(b" ")].decode()
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[str, str, str]]:
    files = [f for f in re.split(rb"\d{5,6} ", data) if len(f) > 0]
    res = []
    for file in files:
        mode, ft = ("100644", "blob") if b"." in file else ("040000", "tree")
        filename = re.findall(b"[a-zA-z]{1,15}[.]?[a-zA-Z]{1,5}", file)[0]
        hash_ = file[len(filename) :].hex().lstrip("0")
        res.append((mode, ft, f"{hash_}\t{filename.decode()}"))
    return res


def cat_file(obj_name: str, pretty: bool = True) -> None:
    fmt, data = read_object(obj_name, repo_find("."))
    if fmt == "tree":
        for obj in read_tree(data):
            print(" ".join(obj))
    else:
        print(data.decode())


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    return re.findall("tree .{40}", data.decode())[0].removeprefix("tree ")

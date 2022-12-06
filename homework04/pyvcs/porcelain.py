import pathlib
import typing as tp
import zlib

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, read_tree
from pyvcs.tree import commit_tree, write_tree

PATHS: list[pathlib.Path] = []


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    global PATHS
    if len(PATHS) == 3:
        PATHS = []
    PATHS.extend(paths)
    update_index(gitdir, PATHS, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree_hash = write_tree(gitdir, read_index(gitdir))
    commit_hash = commit_tree(gitdir, tree_hash, message, author=author)
    return commit_hash


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    with open(gitdir / "objects" / obj_name[:2] / obj_name[2:], "rb") as fi:
        data = fi.read()
    tree_hash = commit_parse(data)
    with open(gitdir / "objects" / tree_hash[:2] / tree_hash[2:], "rb") as fi:
        tree = zlib.decompress(fi.read())
    files = read_tree(tree)[1:]
    filenames = {f[-1].split("\t")[1] for f in files}
    tracked = {f.name for f in PATHS}
    for file in gitdir.parent.iterdir():
        if file.name not in ("Users", ".git"):
            if file.name not in filenames and file.name in tracked:
                file.unlink()
            if file.is_dir() and file.name not in filenames:
                for f in file.iterdir():
                    f.unlink()
                file.rmdir()

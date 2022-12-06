import os
import pathlib
import time
import typing as tp

from pyvcs.index import GitIndexEntry, form_tree
from pyvcs.objects import hash_object


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    if len(index) > 1:
        index = [file for file in index if "/" not in file.name]
    return hash_object(form_tree(index), "tree")


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    timest = int(time.mktime(time.localtime()))
    data = f"tree {tree}\nauthor {author} {timest} +0300\ncommitter {author} {timest} +0300\n\n{message}\n"
    return hash_object(data.encode(), "commit", True)

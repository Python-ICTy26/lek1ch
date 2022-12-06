import os
import pathlib
import re
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(
            f"!LLLLLLLLLL20sh{len(self.name)}sxxx",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        filename_len = len(data[62:]) - 3
        values = struct.unpack(f"!LLLLLLLLLL20sh{filename_len}sxxx", data)
        new_values = list(values)
        new_values[-1] = "".join([chr(b) for b in values[-1]])
        return GitIndexEntry(*new_values)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not (gitdir / "index").exists():
        return []
    with open(gitdir / "index", "rb") as f:
        data = f.read()[12:-20]
    pattern = re.compile(
        b".{62}[a-zA-Z/]{1,25}[.]?[a-zA-Z]{1,9}\x00\x00\x00",
        flags=re.DOTALL,
    )
    entries = pattern.findall(data)
    return [GitIndexEntry.unpack(entry) for entry in entries]


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / "index", "wb") as f:
        f.write(b"DIRC\x00\x00\x00\x02")
        f.write(len(entries).to_bytes(4, "big"))
        for entry in entries:
            f.write(entry.pack())
        f.write(b"k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11")


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    if not details:
        print("\n".join(entry.name for entry in entries), end="")
    else:
        for index, entry in enumerate(entries):
            if index > 0:
                print()
            print(f"100644 {entry.sha1.hex()} 0\t{entry.name}", end="")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = False) -> None:
    entries = []
    for path in paths:
        with open(path, "rb") as f:
            hash_ = hash_object(f.read(), "blob", write)
            entries.append(create_entry(path, hash_))
            if not (hash_path := gitdir / "objects" / hash_[:2]).exists():
                hash_path.mkdir()
            if not path.is_dir():
                (hash_path / hash_[2:]).touch()
    if write:
        files = set(p.name for p in gitdir.parent.iterdir())
        for path in paths:
            if "/" in str(path):
                entries.append(create_tree(path.parent, entries))
        entries.append(
            create_tree(
                pathlib.Path("."),
                sorted([e for e in entries if e.name in files], key=lambda e: e.name),
            )
        )
    write_index(gitdir, sorted(entries, key=lambda e: e.name))


def form_tree(index: tp.List[GitIndexEntry], prefix: str = "") -> bytes:
    content = b""
    for entry in index:
        name = entry.name.removeprefix(prefix)
        content += f"{oct(entry.mode)[2:]} {name}\0".encode()
        content += entry.sha1
    return content


def create_tree(path: pathlib.Path, entries: list[GitIndexEntry]) -> GitIndexEntry:
    entries = [e for e in entries if e.name.startswith(path.name)]
    hash_ = hash_object(form_tree(entries, path.name + "/"), "tree", True)
    return create_entry(path, hash_, 16384)


def create_entry(path: pathlib.Path, hash_: str, mode: int = 33188) -> GitIndexEntry:
    stat = os.stat(path)
    entry = GitIndexEntry(
        int(stat.st_ctime),
        0,
        int(stat.st_mtime),
        0,
        stat.st_dev,
        stat.st_ino,
        mode,
        stat.st_uid,
        stat.st_gid,
        stat.st_size,
        bytes.fromhex(hash_),
        0,
        str(path).replace("\\", "/"),
    )
    return entry

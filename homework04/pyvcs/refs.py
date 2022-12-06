import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with open(gitdir / ref, "w") as f:
        f.write(new_value)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    with open(gitdir / refname) as f:
        data = f.read().strip()
    if data.startswith("ref: "):
        data = data.removeprefix("ref: ")
        with open(gitdir / data) as f:
            data = f.read().strip()
    return data


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if (path := gitdir / "refs" / "heads" / "master").exists():
        with open(path) as f:
            return f.read()
    return None


def is_detached(gitdir: pathlib.Path) -> bool:
    with open(gitdir / "HEAD") as f:
        data = f.read().strip()
    return not data.startswith("ref: ")


def get_ref(gitdir: pathlib.Path) -> str:
    return "refs/heads/master"

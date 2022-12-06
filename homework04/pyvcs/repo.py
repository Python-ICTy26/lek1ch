import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    current_dir = set(el.name for el in workdir.iterdir())
    parent_dir = set(el.name for el in workdir.parent.iterdir())
    git_dir = None
    if ".git" in current_dir:
        git_dir = workdir
    elif ".git" in parent_dir:
        git_dir = workdir.parent
    elif workdir.parent.name == ".git":
        git_dir = workdir.parent.parent
    else:
        raise Exception("Not a git repository")
    return git_dir / ".git"


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    git_dir = pathlib.Path(os.environ.get("GIT_DIR", ".git"))
    workdir = pathlib.Path(workdir)
    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")
    if not workdir.exists():
        workdir.mkdir()
    if not git_dir.exists():
        git_dir.mkdir()
    for sub_dir in ("refs", "refs/heads", "refs/tags", "objects"):
        if not (p := git_dir / sub_dir).exists():
            p.mkdir()
    write("ref: refs/heads/master\n", git_dir / "HEAD")
    write(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
        git_dir / "config",
    )
    write("Unnamed pyvcs repository.\n", git_dir / "description")
    return pathlib.Path(git_dir)


def write(content: str, path: pathlib.Path) -> None:
    with open(path, "w", encoding="u8") as f:
        f.write(content)

from pathlib import Path


def resolve_project_root() -> str:
    filesystem_root = Path("/")
    project_root = Path.cwd()

    while not project_root.joinpath("pyproject.toml").exists() and project_root != filesystem_root:
        project_root = project_root.parent

    if project_root == filesystem_root:
        raise FileNotFoundError("Cannot resolve project root directory")

    return project_root.as_posix()

import sys
from pathlib import Path
from typing import Union

def get_root_path() -> Path:
    root_path = Path(".")
    if getattr(sys, "frozen", False):
        root_path = Path(sys.executable).parent
    else:
        root_path = Path(sys.argv[0]).parent
    if len(sys.argv) > 1:
        arg_path = Path(sys.argv[1])
        if arg_path.is_dir():
            root_path = arg_path
        elif arg_path.is_file():
            root_path = arg_path.parent
    return root_path.resolve()

def get_resource_path(path: Union[str | Path] | None = None) -> Path:
    resource_path = Path(getattr(sys, "_MEIPASS", ".")).joinpath("resources")
    if path is None:
        return resource_path.resolve()
    else:
        return resource_path.joinpath(path).resolve()
    
def quote(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
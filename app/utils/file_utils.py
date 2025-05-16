import sys
import ctypes
from pathlib import Path
from typing import Union
import mimetypes

def get_default_root_path() -> Path:
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
    return root_path.absolute()

def get_resource_path(path: Union[str | Path] | None = None) -> Path:
    resource_path = Path(getattr(sys, "_MEIPASS", ".")).joinpath("resources")
    if path is None:
        return resource_path.absolute()
    else:
        return resource_path.joinpath(path).absolute()
    
def is_hidden(path: Path) -> bool:
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        if attrs == -1:
            return 
        return bool(attrs & 2)
    except Exception:
        return False


def get_mimetype_head(name):
    mime_type, _ = mimetypes.guess_type(name)
    if mime_type is None:
        return None
    return mime_type.split('/')[0]

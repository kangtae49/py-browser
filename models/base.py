from pydantic import BaseModel
from typing import List
from enum import Enum

class ContentTemplate(Enum):
    CONTENT = "CONTENT"
    GALLERY = "GALLERY"

class WidgetId(Enum):
    PY_BROWSER = "PY_BROWSER"
    WIDGET_FOLDER = "WIDGET_FOLDER"
    WIDGET_CONTENT = "WIDGET_CONTENT"
    WIDGET_CONSOLE = "WIDGET_CONSOLE"

class BaseMsg(BaseModel):
    sender_id: WidgetId
    receiver_id: WidgetId
    action: str
    callback: str | None = None


class FolderReq(BaseMsg):
    path: str | None = None
    is_root: bool

class OpenFileReq(BaseMsg):
    path: str

class PathItem(BaseModel):
    is_folder: bool
    name: str
    path: str
    mtime: str
    size: int


class FolderRes(BaseMsg):
    path: str | None = None
    is_root: bool
    items: List[PathItem]




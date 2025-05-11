from pydantic import BaseModel
from typing import List
from enum import Enum

class WidgetId(Enum):
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


class PathItem(BaseModel):
    is_folder: bool
    name: str
    path: str


class FolderListRes(BaseMsg):
    path: str | None = None
    items: List[PathItem]


class ConsoleReq(BaseMsg):
    msg: str
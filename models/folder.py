from pydantic import BaseModel
from typing import TypeVar, List

class FolderReq(BaseModel):
    widget_id: str
    action: str
    target: str
    path: str | None = None
    callback: str | None = None

class FolderItem(BaseModel):
    is_folder: bool
    name: str
    path: str

class FolderListRes(BaseModel):
    widget_id: str
    action: str
    target: str
    parent: str | None = None
    data: List[FolderItem]


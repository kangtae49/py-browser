from pydantic import BaseModel
from typing import List
from app.enums import WidgetId, ActionId, StateKey, ContentTemplate, GalleryType


class BaseMsg(BaseModel):
    sender_id: WidgetId
    receiver_id: WidgetId
    action: ActionId


class FolderReq(BaseMsg):
    path: str | None = None
    is_root: bool

class OpenPathReq(BaseMsg):
    path: str

class OpenPathRes(BaseMsg):
    path: str

class PathItem(BaseModel):
    is_folder: bool
    name: str
    path: str
    has_children: bool = False
    mtime: str
    size: int


class FolderRes(BaseMsg):
    path: str | None = None
    is_root: bool
    items: List[PathItem]

class GetStateReq(BaseMsg):
    key: StateKey

class GetStateRes(BaseMsg):
    key: StateKey
    value: ContentTemplate | GalleryType | str

class SetStateReq(BaseMsg):
    key: StateKey
    value: ContentTemplate | GalleryType | str

class SetStateRes(BaseMsg):
    key: StateKey
    value: ContentTemplate | GalleryType | str




def createFolderReq (
        sender=WidgetId.PY_BROWSER,
        receiver_id=WidgetId.WIDGET_FOLDER,
        action=ActionId.LIST_DIRECTORY,
        path=None,
        is_root=True
    ):
    return FolderReq(
        sender_id=WidgetId.PY_BROWSER,
        receiver_id=WidgetId.WIDGET_FOLDER,
        action=ActionId.LIST_DIRECTORY,
        path=path,
        is_root=True,
    )

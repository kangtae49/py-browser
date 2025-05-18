from pydantic import BaseModel
from typing import List
from app.enums import WidgetId, ActionId, StateKey, ContentTemplate, GalleryType, OpenPathType


class BaseMsg(BaseModel):
    sender_id: WidgetId
    receiver_id: WidgetId
    action: ActionId


class FolderReq(BaseMsg):
    path: str | None = None
    select_path: str | None = None
    depth: int

class OpenPathReq(BaseMsg):
    open_path_type: OpenPathType = OpenPathType.AUTO
    path: str

class OpenPathRes(BaseMsg):
    open_path_type: OpenPathType
    path: str

class PathItem(BaseModel):
    is_dir: bool
    name: str
    path: str
    ext: str
    mime: str
    mtime: float
    size: int
    tot: int
    items: List["PathItem"]


class FolderRes(BaseMsg):
    path: str | None = None
    select_path: str | None = None
    depth: int
    page_no: int
    page_size: int = 20
    item: PathItem

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

class Link(BaseModel):
    key: str
    value: str

class GetLinkReq(BaseMsg):
    pass

class GetLinkRes(BaseMsg):
    items: List[Link]


def createFolderReq (
        sender=WidgetId.PY_BROWSER,
        receiver_id=WidgetId.WIDGET_FOLDER,
        action=ActionId.LIST_DIRECTORY,
        path=None,
        select_path=None,
        depth=0
    ):
    return FolderReq(
        sender_id=WidgetId.PY_BROWSER,
        receiver_id=WidgetId.WIDGET_FOLDER,
        action=ActionId.LIST_DIRECTORY,
        path=path,
        select_path=select_path,
        depth=depth,
    )

from enum import Enum

class ContentTemplate(Enum):
    CONTENT_LIST = "CONTENT_LIST"         # "widget_content.html"
    CONTENT_GALLERY = "CONTENT_GALLERY"   #"widget_content_gallery.html"

class FolderTemplate(Enum):
    FOLDER = "FOLDER"  # "widget_folder.html"

class OpenPathType(Enum):
    AUTO = "AUTO"
    WEBVIEW = "WEBVIEW"
    APPLICATION = "APPLICATION"
    BROWSER = "BROWSER"

class GalleryType(Enum):
    LAYOUT_LIST = "LAYOUT_LIST"
    LAYOUT_GALLERY = "LAYOUT_GALLERY"

class StateKey(Enum):
    TEMPLATE = "TEMPLATE"
    GALLERY_TYPE = "GALLERY_TYPE"
    PATH = "PATH"
    SLIDER_VAL = "SLIDER_VAL"

class WidgetId(Enum):
    PY_BROWSER = "PY_BROWSER"
    WIDGET_FOLDER = "WIDGET_FOLDER"
    WIDGET_CONTENT = "WIDGET_CONTENT"
    WIDGET_CONSOLE = "WIDGET_CONSOLE"

class ActionId(Enum):
    APP_ACTION = "APP_ACTION"
    ON_LOAD = "ON_LOAD"
    LIST_DIRECTORY = "LIST_DIRECTORY"
    OPEN_PATH = "OPEN_PATH"
    GET_STATE = "GET_STATE"
    SET_STATE = "SET_STATE"
    GET_LINK = "GET_LINK"
    
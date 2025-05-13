from app.models.base import WidgetId, FolderReq

def createFolderReq (
        sender=WidgetId.PY_BROWSER,
        receiver_id=WidgetId.WIDGET_FOLDER,
        action="api_list_directory",
        callback="Pb.callbacks.appendData",
        path=None,
        is_root=True
    ):
    return FolderReq(
        sender_id=WidgetId.PY_BROWSER,
        receiver_id=WidgetId.WIDGET_FOLDER,
        action="api_list_directory",
        callback="Pb.callbacks.appendData",
        path=path,
        is_root=True,
    )

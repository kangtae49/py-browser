from pathlib import Path
from utils.file_utils import get_root_path, get_resource_path
from models.base import BaseMsg, FolderReq, FolderListRes, PathItem
import wx
from models.base import WidgetId

class WidgetFolderHandler:
    def __init__(self, browser, webview, widget_id: WidgetId):
        self._browser = browser
        self._webview = webview
        self._widget_id = widget_id

        self._webview.AddScriptMessageHandler(self._widget_id.name)
        self._browser._register_widget(self._widget_id, self._webview, self._on_message_received)

        self._browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self._on_load_folder, self._webview)
        self._browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self._browser._on_message_received, self._webview)
        self._webview.LoadURL(get_resource_path(f"{self._widget_id.name.lower()}.html").as_uri())

    def _on_load_folder(self, event):
        self._webview.RunScriptAsync(f"Pb.addScriptMessageHandler('{self._widget_id.name}')")

    def _on_message_received(self, event):
        param = event.GetString()
        base = BaseMsg.model_validate_json(param)

        action = getattr(self, base.action, None)
        if action:
            action(param)

    def open_file(self, param: str):
        req = FolderReq.model_validate_json(param)
        self._browser._webview_content.LoadURL(Path(req.path).as_uri())


    def list_directory(self, param: str):
        req = FolderReq.model_validate_json(param)
        if req.path is None:
            root_path = get_root_path()
            res = FolderListRes(
                sender_id=req.sender_id,
                receiver_id=req.receiver_id,
                action=req.callback,
                callback=None,
                path=None,
                items=[
                    PathItem(
                        is_folder=True,
                        name=root_path.name or root_path.resolve().as_posix(),
                        path=root_path.as_posix()
                    )
                ]
            )
        else:
            parent_path = Path(req.path)
            items = []
            for item in parent_path.iterdir():
                if item.is_dir():
                    items.append(PathItem(
                        is_folder=True,
                        name=item.name,
                        path=item.as_posix()
                    ))
                else:
                    items.append(PathItem(
                        is_folder=False,
                        name=item.name,
                        path=item.as_posix()
                    ))
            res = FolderListRes(
                sender_id=req.sender_id,
                receiver_id=req.receiver_id,
                action=req.callback,
                callback=None,
                path=parent_path.as_posix(),
                items=items
            )
        webview = self._browser._widgets.get(req.receiver_id)
        if res.action is not None:
            script = f"{res.action}({repr(res.model_dump_json())})"
            webview.RunScriptAsync(script)
        

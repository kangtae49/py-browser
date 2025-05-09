from pathlib import Path
from utils.file_utils import get_root_path, get_resource_path, quote
from models.folder import FolderReq, FolderListRes, FolderItem
import wx

class WidgetFolderHandler:
    def __init__(self, browser, webview, widget_id):
        self._browser = browser
        self._webview = webview
        self._widget_id = widget_id

        self._webview.AddScriptMessageHandler(self._widget_id)
        self._browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self._on_load_folder, self._webview)
        self._browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self._on_message_received, self._webview)
        self._webview.LoadURL(get_resource_path(f"{self._widget_id}.html").as_uri())

    def _on_load_folder(self, event):
        self._webview.RunScriptAsync(f"set_widget_id('{self._widget_id}')")
        self._webview.RunScriptAsync(f"onload_widget()")

    def _on_message_received(self, event):
        param = event.GetString()
        req = FolderReq.model_validate_json(param)

        method = getattr(self, req.action, None)
        if method:
            method(req)

    def open_file(self, req: FolderReq):
        self._browser._webview_content.LoadURL(Path(req.path).as_uri())


    def list_directory(self, req: FolderReq):
        if req.path is None:
            root_path = get_root_path()
            res = FolderListRes(
                widget_id=self._widget_id,
                action=req.action,
                target=req.target,
                parent=None,
                data=[
                    FolderItem(
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
                    items.append(FolderItem(
                        is_folder=True,
                        name=item.name,
                        path=item.as_posix()
                    ))
                else:
                    items.append(FolderItem(
                        is_folder=False,
                        name=item.name,
                        path=item.as_posix()
                    ))
            res = FolderListRes(
                widget_id=self._widget_id,
                action=req.action,
                target=req.target,
                parent=parent_path.as_posix(),
                data=items
            )
        
        self.run_script(req.callback, res)
    
    def run_script(self, callback: str, res: FolderListRes):
        param = res.model_dump_json()
        script_param = quote(param)
        self._webview.RunScriptAsync(f"{callback}('{script_param}')")


import os
from pathlib import Path
from datetime import datetime
import wx
from wx.html2 import WebView
from utils.file_utils import get_default_root_path, get_resource_path
from models.base import BaseMsg, FolderReq, OpenFileReq, FolderRes, PathItem
from models.base import WidgetId

class WidgetFolderHandler:
    def __init__(self, browser, webview: WebView, widget_id: WidgetId):
        self._browser = browser
        self._webview: WebView = webview
        self._widget_id: WidgetId = widget_id
        self.log = self._browser.log
        self._root_path: Path = get_default_root_path()

        self._webview.EnableAccessToDevTools(True)
        self._webview.MSWSetModernEmulationLevel(True)
        self._webview.AddScriptMessageHandler(self._widget_id.name)
        self._browser._register_widget(self._widget_id, self._webview, self)

        self._browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self._on_load, self._webview)
        self._browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self._browser._on_message_received, self._webview)
        self._webview.LoadURL(get_resource_path(f"{self._widget_id.name.lower()}.html").as_uri())

    def _on_load(self, event):
        self._browser.runScriptAsync(BaseMsg(
            sender_id=self._widget_id,
            receiver_id=self._widget_id,
            action="_on_load",
            callback="Pb.init",
        ))

    def _on_message_received(self, event):
        param = event.GetString()
        base = BaseMsg.model_validate_json(param)

        action = getattr(self, base.action, None)
        if action:
            action(param)

    def get_root_path(self):
        return self._root_path
    
    def set_root_path(self, path):
        self._root_path = path

    def api_open_file(self, param: str):
        req = OpenFileReq.model_validate_json(param)
        path = Path(req.path)
        # self.log(f"{path}: {path.suffix}")
        # openable_suffix = {
        #     ".html", ".htm", ".mht", ".mhtml", ".txt", ".pdf",
        #     ".odt", ".ods", ".odp", ".csv", ".tsv", ".json", ".xml",
        #     ".md", ".rtf", ".epub", 
        #     ".js", ".cpp", ".c", ".py", ".rs", ".hs", ".jsp", ".sh", ".bat", ".ps1",
        #     ".php", ".asp", "jsp"
        #     ".ini", ".ipynb", ".kml", ".cif", ".pdb", ".xyz",
        #     ".reg", ".toml", ".gitignore", ".cfg", ".log",
        #     ".bmp", ".jpg", ".jpeg", ".png", ".gif", ".svg", 
        #     ".webp", ".ico", ".otf",
        #     ".mp3", ".mp4", ".webm", ".ogg", ".ogv", ".mov", ".avi", ".wmv", ".flv",
        #     ".wav", ".m4a", ".wma",
        # }
        # if path.suffix.lower() in openable_suffix:
        # wx.LaunchDefaultApplication(str(path.absolute()))
        # wx.LaunchDefaultBrowser(str(path.absolute()))
        exclude_suffix = {
            ".exe", ".lnk", ".com",
        }
        if path.suffix.lower() not in exclude_suffix:
            self._browser._webview_content.LoadURL(path.as_uri())


    def api_list_directory(self, param: str):
        req = FolderReq.model_validate_json(param)
        root_path = req.path
        if root_path is None:
            root_path = self.get_root_path()
        else:
            root_path = Path(root_path)
        print(req)
        if req.is_root:
            res = FolderRes(
                sender_id=req.sender_id,
                receiver_id=req.receiver_id,
                action=req.action,
                callback=req.callback,
                path=root_path.absolute().as_posix(),
                is_root=True,
                items=[
                    PathItem(
                        is_folder=True,
                        name=root_path.name or root_path.absolute().as_posix(),
                        path=root_path.absolute().as_posix(),
                        size=root_path.stat().st_size,
                        mtime=datetime.fromtimestamp(root_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    )
                ]
            )
        else:
            items = []
            for item in root_path.iterdir():
                # if not item.exists():
                #     continue
                # if item.is_junction():
                #     continue
                # if item.is_symlink():
                #     continue
                if not os.access(item.absolute(), os.R_OK):
                    continue
                if item.is_dir():
                    items.append(PathItem(
                        is_folder=True,
                        name=item.name,
                        path=item.absolute().as_posix(),
                        size=item.stat().st_size,
                        mtime=datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    ))
                else:
                    items.append(PathItem(
                        is_folder=False,
                        name=item.name,
                        path=item.absolute().as_posix(),
                        size=item.stat().st_size,
                        mtime=datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    ))
            res = FolderRes(
                sender_id=req.sender_id,
                receiver_id=req.receiver_id,
                action=req.action,
                callback=req.callback,
                path=root_path.resolve().as_posix(),
                is_root=req.is_root,
                items=items
            )
        self._browser.runScriptAsync(res)
        

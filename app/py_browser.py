import os
import math
import wx
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import wx.aui as aui
from wx.html2 import WebView 

from app.utils.file_utils import get_default_root_path, get_resource_path, get_mimetype_head, get_mimetype
from app.utils.file_utils import count_path

from app.enums import WidgetId, ContentTemplate, GalleryType, StateKey, OpenPathType
from app.models import createFolderReq
from app.models import BaseMsg, State
from app.models import FolderReq, FolderRes, PathItem
from app.models import GetStateReq, GetStateRes
from app.models import SetStateReq, SetStateRes
from app.models import OpenPathReq, OpenPathRes
from app.models import GetLinkReq, GetLinkRes, Link
from app.widgets.widget_folder import WidgetFolder
from app.widgets.widget_content import WidgetContent
from app.widgets.widget_base import WidgetBase




# @dataclass
# class State:
#     template: ContentTemplate = ContentTemplate.CONTENT_LIST
#     gallery_type: GalleryType = GalleryType.LAYOUT_LIST
#     slider_val: str = "20"
#     path: str = ""
#     is_dir: bool = False

class PyBrowser(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._webviews = {}
        self._widgets = {}

        self._state = State()

        # -----------
        # Menu
        # -----------
        menubar = wx.MenuBar()
        # Open Folder
        menu_open_folder = wx.Menu()
        self._menu_open_folder = menu_open_folder.Append(wx.ID_ANY, "Open Folder")
        menubar.Append(menu_open_folder, "File")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self._on_open_folder, self._menu_open_folder)

        # Console
        # menu_consoler = wx.Menu()
        # self._menu_console = menu_consoler.Append(wx.ID_ANY, "Console", kind=wx.ITEM_CHECK)
        # menubar.Append(menu_consoler, "View")
        # self.SetMenuBar(menubar)
        # self.Bind(wx.EVT_MENU, self._on_toggle_console, self._menu_console)
        # self.Bind(aui.EVT_AUI_PANE_CLOSE, self._on_close_console)

        
        # -----------
        # Folder
        # -----------
        self._webview_folder = WidgetFolder(self, browser=self, widget_id=WidgetId.WIDGET_FOLDER)
        self._mgr.AddPane(self._webview_folder, 
                          aui.AuiPaneInfo()
                            .Name(WidgetId.WIDGET_FOLDER.name)
                            .Left()
                            .BestSize((300, -1))
                            .CloseButton(False)
                            .CaptionVisible(False)
        )
        
        # -----------
        # Content
        # -----------
        self._webview_content = WidgetContent(self, browser=self, widget_id=WidgetId.WIDGET_CONTENT)

        self._mgr.AddPane(self._webview_content, 
                          aui.AuiPaneInfo()
                            .Name(WidgetId.WIDGET_CONTENT.name)
                            .Top()
                            .Center()
                            .BestSize((600, -1))
                            .CloseButton(False)
                            .CaptionVisible(False)
        )

        # -----------
        # Debug Console
        # -----------
        # self._webview_console = WidgetConsole(self, browser=self, widget_id=WidgetId.WIDGET_CONSOLE)
        # self._mgr.AddPane(self._webview_console, 
        #                   aui.AuiPaneInfo()
        #                     .Name(WidgetId.WIDGET_CONSOLE.name)
        #                     .Caption("Console")
        #                     .Bottom()
        #                     .BestSize((-1, 100))
        #                     .CloseButton(True)
        #                     .CaptionVisible(True)
        #                     .Hide()
        # )

        self._mgr.Update()

    def _get_state(self) -> State:
        return self._state

    def _register_widget(self, widget_id: WidgetId, webview: WebView, widget: WidgetBase):
        self._webviews.update({widget_id: webview})
        self._widgets.update({widget_id: widget})

    def _on_toggle_console(self, event):
        pane = self._mgr.GetPane(WidgetId.WIDGET_CONSOLE.name)
        if self._menu_console.IsChecked():
            pane.Show()
        else:
            pane.Hide()
        self._mgr.Update()

    def _on_close_console(self, event):
        self._menu_console.Check(False)
        event.Skip()

    def on_close(self, event):
        self._mgr.UnInit()
        self.Destroy()

    def _on_open_folder(self, event):
        with wx.DirDialog(None, "Select Folder:",
                      style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                selected_path = dlg.GetPath()
                self.runApi(createFolderReq(path=selected_path, depth=0))

    def getWebview(self, widget_id: WidgetId) -> WebView:
        return self._webviews.get(widget_id)

    def getWidget(self, widget_id: WidgetId) -> WidgetBase:
        return self._widgets.get(widget_id)


    def runApi(self, req: BaseMsg):
        getattr(self, req.action.value.lower())(req.model_dump_json())

    def runScriptAsync(self, res: BaseMsg):
        script = f"Pb.listener({repr(res.model_dump_json())})"
        print(f"runScriptAsync: {script}")
        # https://docs.wxpython.org/wx.html2.WebView.html#wx.html2.WebView.RunScriptAsync
        self.getWebview(res.receiver_id).RunScriptAsync(javascript=script)
        

    def _on_message_received(self, event):
        param = event.GetString()
        print(f"_on_message_received: {param}")
        base_msg: BaseMsg = BaseMsg.model_validate_json(param)
        func = getattr(self, f"{base_msg.action.value.lower()}")
        if func:
            func(param)
        else:
            print(f"Router.route action: {base_msg.action}")


    def list_directory(self, param: str | FolderReq) -> FolderRes:
        print("list_directory")
        if isinstance(param, str):
            req = FolderReq.model_validate_json(param)
        else:
            req = param
        root_path = None
        
        if req.path is None:
            root_path = self.getWidget(WidgetId.WIDGET_FOLDER).get_root_path()
        else:
            root_path = Path(req.path)

        select_path = None
        if req.select_path is not None:
            select_path = Path(req.select_path)
        else:
            select_path = req.select_path

        tot = count_path(root_path)
        page_size = 5000
        res = FolderRes(
            sender_id=req.sender_id,
            receiver_id=req.receiver_id,
            action=req.action,
            path=root_path.absolute().as_posix(),
            select_path=select_path.absolute().as_posix() if select_path is not None else None,
            depth=req.depth,
            page_no=0,
            page_size=page_size,
            item= PathItem(
                is_dir=True,
                name=root_path.name or root_path.absolute().as_posix(),
                path=root_path.absolute().as_posix(),
                ext=root_path.suffix.lower(),
                mime=get_mimetype(root_path.name),
                size=root_path.stat().st_size,
                mtime=root_path.stat().st_mtime,
                tot=tot,
                items = []
            )
        )
        if tot == 0 or res.depth == 0:
            self.runScriptAsync(res)
            return
  
        
        items = []
        idx = 0
        for item in root_path.iterdir():
            # if not item.exists():
            #     continue
            # if item.is_junction():
            #     continue
            # if item.is_symlink():
            #     continue
            # if is_hidden(item):
            #     continue
            # if not os.access(item.absolute(), os.R_OK):
            #     continue
            page_no, rem = divmod(idx, page_size)

            items.append(PathItem(
                is_dir=item.is_dir(),
                name=item.name,
                path=item.absolute().as_posix(),
                ext=item.suffix.lower(),
                mime=get_mimetype(item.name),
                size=item.stat().st_size,
                mtime=item.stat().st_mtime,
                tot=count_path(item),
                items=[],
            ))
            if rem == page_size-1:
                res.page_no = page_no
                res.item.items = items
                self.runScriptAsync(res)
                items = []
            idx += 1
        if items:
            page_no = math.ceil(res.item.tot / page_size) - 1 
            res.page_no = page_no
            res.item.items = items
            self.runScriptAsync(res)
            items = []


    def open_path(self, param: str | OpenPathReq):
        print("open_path")
        if isinstance(param, str):
            req = OpenPathReq.model_validate_json(param)
        else:
            req = param

        path = Path(req.path)

        if req.open_path_type == OpenPathType.BROWSER:
            wx.LaunchDefaultBrowser(str(path.absolute()))
            return
        elif req.open_path_type == OpenPathType.APPLICATION:
            wx.LaunchDefaultApplication(str(path.absolute()))
            return
        elif req.open_path_type == OpenPathType.WEBVIEW:
            self.getWebview(WidgetId.WIDGET_CONTENT).LoadURL(str(path.absolute()))
            return
        elif req.open_path_type == OpenPathType.AUTO:
            pass

        # OpenPathType.AUTO
        if path.is_file():
            ext = path.suffix.lower()
            if get_mimetype_head(path.name) in {"image", "text", "audio", "video"} or ext in {".pdf", ".md", ".toml"}: 
                self.SetTitle(f"PyBrowser - {path.absolute().as_posix()}")
                self._state.path = path.absolute().as_posix()
                self._state.is_dir = False
                self.getWebview(WidgetId.WIDGET_CONTENT).LoadURL(path.as_uri())
                return
            else:
                self.getWebview(WidgetId.WIDGET_CONTENT).LoadURL("about:blank")
            # else:
            #     wx.LaunchDefaultApplication(str(path.absolute()))

        elif path.is_dir():
            self.SetTitle(f"PyBrowser - {path.absolute().as_posix()}")
            self._state.path = path.absolute().as_posix()
            self._state.is_dir = True
            cur_url = self.getWebview(WidgetId.WIDGET_CONTENT).GetCurrentURL()
            new_url = get_resource_path(f"{WidgetId.WIDGET_CONTENT.value.lower()}.html").as_uri()
            if cur_url != new_url:
                self.getWebview(WidgetId.WIDGET_CONTENT).LoadURL(new_url)
            else:
                res = OpenPathRes(
                    sender_id=req.sender_id,
                    receiver_id=WidgetId.WIDGET_CONTENT,
                    action=req.action,
                    open_path_type=req.open_path_type,
                    path=req.path,
                )
                self.runScriptAsync(res)


    def get_state(self, param: str | GetStateReq):
        if isinstance(param, str):
            req = GetStateReq.model_validate_json(param)
        else:
            req = param
        if req.key == StateKey.TEMPLATE:
            value = self._state.template
        elif req.key == StateKey.GALLERY_TYPE:
            value = self._state.gallery_type
        elif req.key == StateKey.PATH:
            value = self._state.path
        elif req.key == StateKey.SLIDER_VAL:
            value = self._state.slider_val
        res = GetStateRes(
            sender_id=req.sender_id,
            receiver_id=req.receiver_id,
            action=req.action,
            key=req.key,
            value=value
        )
        self.runScriptAsync(res)

    def set_state(self, param: str | SetStateReq):
        if isinstance(param, str):
            req = SetStateReq.model_validate_json(param)
        else:
            req = param
        if req.key == StateKey.TEMPLATE:
            self._state.template = req.value
            value = self._state.template
        elif req.key == StateKey.GALLERY_TYPE:
            self._state.gallery_type = req.value
            value = self._state.gallery_type
        elif req.key == StateKey.PATH:
            self._state.path = req.value
            value = self._state.path
        elif req.key == StateKey.SLIDER_VAL:
            self._state.slider_val = req.value
            value = self._state.slider_val

        res = SetStateRes(
            sender_id=req.sender_id,
            receiver_id=req.receiver_id,
            action=req.action,
            key=req.key,
            value=value
        )
        self.runScriptAsync(res)

    def get_link(self, param: str | GetLinkReq):
        if isinstance(param, str):
            req = GetLinkReq.model_validate_json(param)
        else:
            req = param
        home = Path.home()
        
        items = [
            Link(key="root", value=Path("/").absolute().as_posix()),
            Link(key="home", value=home.absolute().as_posix()),
            Link(key="down", value=home.joinpath("Downloads").absolute().as_posix()),
            Link(key="docs", value=home.joinpath("Documents").absolute().as_posix()),
        ]

        res = GetLinkRes(
            sender_id=req.sender_id,
            receiver_id=req.receiver_id,
            action=req.action,
            items=items
        )
        self.runScriptAsync(res)

def main():
    app = wx.App(False)
    frame = PyBrowser(None, "PyBrowser")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()

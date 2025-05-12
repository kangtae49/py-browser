from pathlib import Path
import wx
import wx.html2
import wx.aui as aui

from models.base import WidgetId, BaseMsg, FolderReq
from handlers.widget_folder_handler import WidgetFolderHandler
from handlers.widget_content_handler import WidgetContentHandler
from handlers.widget_console_handler import WidgetConsoleHandler
from handlers import api

class PyBrowser(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._webviews = {}
        self._handlers = {}
        self._console_handler = None

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
        menu_consoler = wx.Menu()
        self._menu_console = menu_consoler.Append(wx.ID_ANY, "Console", kind=wx.ITEM_CHECK)
        menubar.Append(menu_consoler, "View")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self._on_toggle_console, self._menu_console)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self._on_close_console)


        # -----------
        # Folder
        # -----------
        self._webview_folder = wx.html2.WebView.New(self)
        
        WidgetFolderHandler(self, self._webview_folder, WidgetId.WIDGET_FOLDER)
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
        self._webview_content = wx.html2.WebView.New(self)
        WidgetContentHandler(self, self._webview_content, WidgetId.WIDGET_CONTENT)
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
        self._webview_console = wx.html2.WebView.New(self)
        self._console_handler = WidgetConsoleHandler(self, self._webview_console, WidgetId.WIDGET_CONSOLE)
        self._mgr.AddPane(self._webview_console, 
                          aui.AuiPaneInfo()
                            .Name(WidgetId.WIDGET_CONSOLE.name)
                            .Caption("Console")
                            .Bottom()
                            .BestSize((-1, 100))
                            .CloseButton(True)
                            .CaptionVisible(True)
                            .Hide()
        )
        self._mgr.Update()

    def _on_message_received(self, event):
        param = event.GetString()
        base = BaseMsg.model_validate_json(param)
        self.getHandler(base.receiver_id)._on_message_received(event)


    def _register_widget(self, widget_id: WidgetId, webview, handler):
        self._webviews.update({widget_id: webview})
        self._handlers.update({widget_id: handler})

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

    def _on_open_folder(self, event):
        with wx.DirDialog(None, "Select Folder:",
                      style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                selected_path = dlg.GetPath()
                self.runApi(api.createFolderReq(path=selected_path, is_root=True))

    def getWebview(self, widget_id: WidgetId):
        return self._webviews.get(widget_id)

    def getHandler(self, widget_id: WidgetId):
        return self._handlers.get(widget_id)


    def runApi(self, req: BaseMsg):
        getattr(self.getHandler(req.receiver_id), req.action)(req.model_dump_json())

    def runScriptAsync(self, res: BaseMsg):
        script = f"Pb.listener({repr(res.model_dump_json())})"
        self.getWebview(res.receiver_id).RunScriptAsync(script)
        
    def log(self, msg: str):
        self._console_handler._console_log(msg)

    def on_close(self, event):
        self._mgr.UnInit()
        self.Destroy()


def main():
    app = wx.App(False)
    frame = PyBrowser(None, "PyBrowser")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()

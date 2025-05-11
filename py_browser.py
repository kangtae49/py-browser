import wx
import wx.html2
import wx.aui as aui
from utils.file_utils import get_root_path, get_resource_path

from models.base import WidgetId, BaseMsg
from handlers.widget_folder_handler import WidgetFolderHandler
from handlers.widget_content_handler import WidgetContentHandler
from handlers.widget_console_handler import WidgetConsoleHandler


class PyBrowser(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        print(get_root_path())
        print(get_resource_path())
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._widgets = {}
        self._handlers = {}

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
                            # .Center()
                            # .CenterPane()
                            .CloseButton(False)
                            .CaptionVisible(False)
        )

        # -----------
        # Debug Console
        # -----------
        self._webview_console = wx.html2.WebView.New(self)
        WidgetConsoleHandler(self, self._webview_console, WidgetId.WIDGET_CONSOLE)
        self._mgr.AddPane(self._webview_console, 
                          aui.AuiPaneInfo()
                            .Name(WidgetId.WIDGET_CONSOLE.name)
                            .Bottom()
                            .BestSize((-1, 100))
                            .CloseButton(False)
                            .CaptionVisible(False)
        )

        
        self._mgr.Update()

    def _on_message_received(self, event):
        param = event.GetString()
        base = BaseMsg.model_validate_json(param)
        handler = self._handlers.get(base.receiver_id)
        handler(event)

    def _register_widget(self, widget_id: WidgetId, webview, handler):
        self._widgets.update({widget_id: webview})
        self._handlers.update({widget_id: handler})

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

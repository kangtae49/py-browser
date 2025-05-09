import wx
import wx.html2
import wx.aui as aui

from utils.file_utils import get_root_path, get_resource_path

from enum import Enum
from handlers.widget_folder_handler import WidgetFolderHandler
from handlers.widget_content_handler import WidgetContentHandler

class WidgetId(Enum):
    FOLDER = "widget_folder"
    CONTENT = "widget_content"

class PyBrowser(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        print(get_root_path())
        print(get_resource_path())
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # -----------
        # Folder
        # -----------
        self._webview_folder = wx.html2.WebView.New(self)
        WidgetFolderHandler(self, self._webview_folder, WidgetId.FOLDER.value)
        self._mgr.AddPane(self._webview_folder, aui.AuiPaneInfo()
                            .Name(WidgetId.FOLDER.value)
                            .Left()
                            .BestSize((300, -1))
                            .CloseButton(False)
                            .CaptionVisible(False)
        )
        
        # -----------
        # Content
        # -----------
        self._webview_content = wx.html2.WebView.New(self)
        WidgetContentHandler(self, self._webview_content, WidgetId.CONTENT.value)
        self._mgr.AddPane(self._webview_content, aui.AuiPaneInfo()
                            .Name(WidgetId.CONTENT.value)
                            .Center()
                            .CenterPane()
                            .CloseButton(False)
                            .CaptionVisible(False)
        )
        
        self._mgr.Update()


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

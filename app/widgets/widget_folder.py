from pathlib import Path
import wx
from wx.html2 import WebView
from app.utils.file_utils import get_default_root_path, get_resource_path
from app.models import BaseMsg
from app.models import WidgetId
from app.enums import ActionId
from app.widgets.widget_base import WidgetBase, WidgetMeta

class WidgetFolder(wx.Panel, WidgetBase, metaclass=WidgetMeta):
    def __init__(self, *args, **kwargs):
        from app.py_browser import PyBrowser
        self._browser: PyBrowser = kwargs.pop("browser", None)
        self._widget_id: WidgetId = kwargs.pop("widget_id", None)
        
        super().__init__(*args, **kwargs)

        self._webview: WebView = WebView.New(self)
        self._root_path: Path = get_default_root_path()

        self._webview.EnableAccessToDevTools(True)
        self._webview.MSWSetModernEmulationLevel(True)
        self._webview.AddScriptMessageHandler(self._widget_id.name)
        self._browser._register_widget(self._widget_id, self._webview, self)

        self._browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self._on_load, self._webview)
        self._browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self._browser._on_message_received, self._webview)
        self._browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_RESULT, self.on_script_result)
        self._webview.LoadURL(get_resource_path(f"{self._widget_id.name.lower()}.html").as_uri())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._webview, 1, wx.EXPAND)
        self.SetSizer(sizer)
    
    def get_original(self):
        return self
    
    def _on_load(self, event):
        print("_on_load")
        self._browser.runScriptAsync(BaseMsg(
            sender_id=self._widget_id,
            receiver_id=self._widget_id,
            action=ActionId.ON_LOAD,
        ))
    
    def on_script_result(self, event):
        if event.IsError():
            print("err(WidgetFolder):", event.GetString())

    def get_root_path(self):
        return self._root_path
    
    def set_root_path(self, path):
        self._root_path = path




        

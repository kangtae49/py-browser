import json
import wx
from utils.file_utils import  get_resource_path

import wx

class WidgetContentHandler:
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
        message = event.GetString()
        jmessage = json.loads(message)
        print("json", jmessage)

    
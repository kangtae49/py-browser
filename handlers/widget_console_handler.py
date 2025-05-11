from utils.file_utils import get_resource_path
from models.base import ConsoleReq
import wx
from models.base import WidgetId, BaseMsg


class WidgetConsoleHandler:
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
    
    def console_log(self, param: str):
        req = ConsoleReq.model_validate_json(param)

        webview = self._browser._widgets.get(req.receiver_id)
        script = f"{req.callback}({repr(req.model_dump_json())})"
        webview.RunScriptAsync(script)
    

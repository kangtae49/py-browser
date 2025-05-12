from utils.file_utils import get_resource_path
import wx
from models.base import BaseMsg, ContentTemplate


class WidgetContentHandler:
    def __init__(self, browser, webview, widget_id):
        self._browser = browser
        self._webview = webview
        self._widget_id = widget_id
        self._template = ContentTemplate.CONTENT
        self.log = self._browser.log

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
    
    def change_template(self, template: ContentTemplate):
        if self._template == template:
            return
        self._template = template
        if template == ContentTemplate.GALLERY:
            self._webview.LoadURL(get_resource_path(f"widget_content_gallery.html").as_uri())
        else:
            self._webview.LoadURL(get_resource_path(f"widget_content.html").as_uri())




    
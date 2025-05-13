
from abc import ABC, ABCMeta, abstractmethod
import wx

class WidgetBase(ABC):
    @abstractmethod
    def _on_load(self, event): ...

    @abstractmethod
    def _on_message_received(self, event): ...

    @abstractmethod
    def get_original(self): ...

class WidgetMeta(type(wx.Panel), ABCMeta): pass    
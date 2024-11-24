from abc import ABC, abstractmethod

from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager


class TextManager(Manager, ABC):
    name = "TextManager"

    def __init__(self):
        super().__init__(self.name)

    @abstractmethod
    def initialize(self, wPos: LiveData, wSize: LiveData):
        """弹出位置和锚点窗口的大小，位置有关"""
        pass

    @abstractmethod
    def popup(self, chara: str, text: str, delay: float = 2):
        pass

    @abstractmethod
    def isFinished(self):
        pass

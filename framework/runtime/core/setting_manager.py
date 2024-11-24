from abc import ABC, abstractmethod
from enum import Enum

from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager
from framework.handler.handler import Handler
from framework.handler.message import Message
from framework.handler.looper import Looper


class SystrayOption(Enum):
    VISIBLE = 1
    STAY_ON_TOP = 2
    TRACK_ENABLE = 3
    CLICK_ENABLE = 4
    CLICK_TRANSPARENT = 5
    OPEN_SETTING = 6
    EXIT = 7


class SettingManager(Manager, ABC):
    name = "SystrayManager"

    def __init__(self):
        super().__init__(self.name)
        self.__mainHandler = Handler(Looper.mainLooper())
        self.__mainHandler.handle = self.__handleSystrayMessage

        self.visible: LiveData | None = None
        self.stayOnTop: LiveData | None = None
        self.trackEnable: LiveData | None = None
        self.clickEnable: LiveData | None = None
        self.clickTransparent: LiveData | None = None

    def initialize(
            self,
            clickTransparent: LiveData,
            clickEnable: LiveData,
            trackEnable: LiveData,
            stayOnTop: LiveData,
            visible: LiveData,
    ):
        self.clickTransparent = clickTransparent
        self.clickEnable = clickEnable
        self.trackEnable = trackEnable
        self.stayOnTop = stayOnTop
        self.visible = visible

        self.doInitialize()

    @abstractmethod
    def doInitialize(self):
        pass

    @staticmethod
    def __handleSystrayMessage(msg: Message):
        e = msg.data
        if e == SystrayOption.EXIT:
            Looper.mainLooper().shutdown()

    def handleEvent(self, event):
        if event == SystrayOption.CLICK_ENABLE:
            self.clickEnable.value = not self.clickEnable.value
        elif event == SystrayOption.CLICK_TRANSPARENT:
            self.clickTransparent.value = not self.clickTransparent.value
        elif event == SystrayOption.VISIBLE:
            self.visible.value = not self.visible.value
        elif event == SystrayOption.TRACK_ENABLE:
            self.trackEnable.value = not self.trackEnable.value
        elif event == SystrayOption.STAY_ON_TOP:
            self.stayOnTop.value = not self.stayOnTop.value
        elif event == SystrayOption.EXIT:
            msg = Message.obtain()
            msg.data = event
            self.__mainHandler.post(msg)

    @abstractmethod
    def dispose(self):
        pass

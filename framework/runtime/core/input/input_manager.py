from abc import ABC, abstractmethod

from framework.constant import Mouse
from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager
from framework.handler.handler import Handler
from framework.handler.message import Message
from framework.handler.looper import Looper
from framework.runtime.core.input.clickable import Clickable


class MouseEvent:

    def __init__(self):
        self.type: Mouse.Event | None = None
        self.x = 0
        self.y = 0
        self.button: Mouse.Button | None = None

    def __str__(self):
        return f"{self.type}"


class InputManager(Manager, ABC):
    name = "InputManager"

    def __init__(self):
        super().__init__(self.name)
        self.__rootClickable: Clickable | None = None
        self.__handler: Handler | None = None
        self.wPos: LiveData | None = None
        self.clickEnable: LiveData | None = None
        self.trackEnable: LiveData | None = None

    def initialize(self,
                   looper: Looper,
                   wPos: LiveData,
                   clickEnable: LiveData,
                   clickTransparent: LiveData,
                   trackEnable: LiveData):
        self.doInitialize()

        # 窗口位置通过鼠标事件来设置
        self.wPos = wPos
        self.clickEnable = clickEnable
        self.trackEnable = trackEnable
        clickTransparent.observe(self.makeTransparent)

        self.__handler = Handler(looper)
        self.__handler.handle = self.__handleMouseEventMsg

    @abstractmethod
    def doInitialize(self):
        pass

    def __handleMouseEventMsg(self, msg: Message):
        if type(msg.data) != MouseEvent:
            raise RuntimeError(f"invalid mouse event {type(msg.data)}")

        e = msg.data
        if e.type == Mouse.Event.PRESS:
            self.performPress(e)
        elif e.type == Mouse.Event.RELEASE:
            self.performRelease(e)
        elif e.type == Mouse.Event.DOUBLE_CLICK:
            self.performDoubleClick(e)
        elif e.type == Mouse.Event.MOVE:
            self.performMove(e)

        del e

    def performPress(self, mouseEvent):
        if self.__rootClickable:
            self.__rootClickable.onPressed(mouseEvent.button, mouseEvent.x, mouseEvent.y)

    def performRelease(self, mouseEvent):
        if self.__rootClickable:
            self.__rootClickable.onReleased(mouseEvent.button, mouseEvent.x, mouseEvent.y)

    def performDoubleClick(self, mouseEvent):
        if self.__rootClickable:
            self.__rootClickable.onDoubleClicked(mouseEvent.button, mouseEvent.x, mouseEvent.y)

    def performMove(self, mouseEvent):
        if self.__rootClickable:
            self.__rootClickable.onMoved(mouseEvent.x, mouseEvent.y)

    def pushClickable(self, c: Clickable):
        self.__rootClickable = c

    @abstractmethod
    def makeTransparent(self, value):
        pass

    @abstractmethod
    def processInput(self):
        """
        在此处提交鼠标事件
        """
        pass

    def dispatchMouseEvent(self, event: MouseEvent):
        # 过滤鼠标移动事件
        if event.type == Mouse.Event.MOVE and not self.trackEnable.value:
            return

        # 过滤鼠标点击事件
        if (event.type == Mouse.Event.PRESS or event.type == Mouse.Event.RELEASE) and not self.clickEnable.value:
            return

        msg = Message.obtain()
        msg.data = event
        self.__handler.post(msg)

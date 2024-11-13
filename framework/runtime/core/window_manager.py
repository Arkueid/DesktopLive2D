from abc import ABC, abstractmethod

from framework.runtime.core.manager import Manager


class Window(ABC):

    def __init__(self, title: str):
        self.title = title
        self.handle = None
        self.ww = None
        self.wh = None
        self.views = list()

    def addView(self, v):
        self.views.append(v)
        v.onAttach(self)

    @abstractmethod
    def performMove(self, x: int, y: int):
        pass

    @abstractmethod
    def performResize(self, ww: int, wh: int):
        pass

    @abstractmethod
    def performShow(self):
        pass

    @abstractmethod
    def performHide(self):
        pass

    @abstractmethod
    def performStayOnTop(self):
        pass

    @abstractmethod
    def cancelStayOnTop(self):
        pass

    @abstractmethod
    def performClose(self):
        pass


class WindowManager(Manager, ABC):
    name = "WindowManager"

    def __init__(self):
        super().__init__(self.name)
        self.__windows: dict[str, Window] = dict()

    def register(self, w: Window):
        self.__windows[w.title] = w

    @abstractmethod
    def initialize(self):
        pass

    def dispose(self):
        for w in self.__windows.values():
            w.performClose()

        self.__windows.clear()
        self.doDispose()

    @abstractmethod
    def doDispose(self):
        pass

    def move(self, name, x, y):
        self.getWindow(name).performMove(x, y)

    def show(self, name):
        self.getWindow(name).performShow()

    def hide(self, name):
        self.getWindow(name).performHide()

    def resize(self, name, ww, wh):
        self.getWindow(name).performResize(ww, wh)

    def getWindow(self, name) -> Window:
        return self.__windows[name]

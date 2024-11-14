from abc import ABC, abstractmethod

from framework.runtime.core.manager import Manager
from framework.ui.window import Window


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

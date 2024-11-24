from abc import ABC, abstractmethod


class Window(ABC):

    def __init__(self, title: str):
        self.title = title
        self.handle = None
        self.width = None
        self.height = None
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

from abc import abstractmethod

from framework.ui.clickable import Clickable
from framework.ui.drawable import Drawable


class View(Drawable, Clickable):

    def __init__(self):
        self.window = None

    @abstractmethod
    def onResize(self, w: int, h: int):
        pass

    def onUpdate(self):
        pass

    def onDraw(self):
        pass

    def onPressed(self, button: int, x: int, y: int) -> bool:
        pass

    def onReleased(self, button: int, x: int, y: int) -> bool:
        pass

    def onDoubleClicked(self, button: int, x: int, y: int) -> bool:
        pass

    def onMoved(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def onAttach(self, w):
        pass

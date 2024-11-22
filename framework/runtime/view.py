from abc import abstractmethod, ABC

from framework.runtime.core.input.clickable import Clickable
from framework.runtime.core.draw.drawable import Drawable


class View(Drawable, Clickable, ABC):

    def __init__(self):
        self.window = None

    @abstractmethod
    def onResize(self, w: int, h: int):
        pass

    @abstractmethod
    def onAttach(self, w):
        pass

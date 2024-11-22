from abc import ABC, abstractmethod


class Drawable(ABC):

    @abstractmethod
    def onUpdate(self):
        pass

    @abstractmethod
    def onDraw(self):
        pass

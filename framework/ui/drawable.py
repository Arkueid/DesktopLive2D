from abc import ABC, abstractmethod


class Drawable(ABC):

    @abstractmethod
    def onInitialize(self):
        pass

    @abstractmethod
    def onUpdate(self):
        pass

    @abstractmethod
    def onDraw(self):
        pass

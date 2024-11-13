from abc import abstractmethod, ABC

from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager
from framework.ui.drawable import Drawable


class DrawManager(Manager, ABC):
    name = "DrawManager"

    def __init__(self):
        super().__init__(self.name)
        self.fps: LiveData | None = None
        self.__drawables: list[Drawable] = list()

    def initialize(self, fps: LiveData):
        self.fps = fps

        self.doInitialize()
        for d in self.__drawables:
            d.onInitialize()

    @abstractmethod
    def dispose(self):
        pass

    @abstractmethod
    def doInitialize(self):
        pass

    @abstractmethod
    def clearBuffer(self):
        pass

    def addDrawable(self, d: Drawable):
        # not thread safe
        self.__drawables.append(d)

    def beforeDraw(self):
        for d in self.__drawables:
            d.onUpdate()

    def onDraw(self):
        for d in self.__drawables:
            d.onDraw()

    @abstractmethod
    def doDraw(self):
        pass

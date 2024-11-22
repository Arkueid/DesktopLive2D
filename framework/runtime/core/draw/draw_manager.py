from abc import abstractmethod, ABC

from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager
from framework.runtime.core.draw.drawable import Drawable


class DrawManager(Manager, ABC):
    name = "DrawManager"

    def __init__(self):
        super().__init__(self.name)
        self.fps: LiveData | None = None
        self.__drawables: list[Drawable] = list()

    def initialize(self, fps: LiveData):
        self.fps = fps

        self.doInitialize()

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

    def update(self):
        """更新参数"""
        for d in self.__drawables:
            d.onUpdate()

    def doDraw(self):
        """绘制"""
        for d in self.__drawables:
            d.onDraw()

    @abstractmethod
    def postDraw(self):
        """刷新缓冲区，提醒窗口更新……"""
        pass

from abc import ABC, abstractmethod

from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager


class SoundManager(Manager, ABC):
    name = "SoundManager"

    def __init__(self):
        super().__init__(self.name)

    def initialize(self, volume: LiveData):
        self.doInitialize()
        volume.observe(self.setVolume)

    @abstractmethod
    def doInitialize(self):
        pass

    @abstractmethod
    def play(self, audioPath) -> None:
        pass

    @abstractmethod
    def isFinished(self) -> bool:
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def setVolume(self, v: int):
        pass

    @abstractmethod
    def getRsm(self):
        pass

from abc import ABC, abstractmethod


class Clickable(ABC):

    @abstractmethod
    def onPressed(self, button: int, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def onReleased(self, button: int, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def onDoubleClicked(self, button: int, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def onMoved(self, x: int, y: int) -> bool:
        pass

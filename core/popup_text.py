import time
from abc import ABC, abstractmethod

from qfluentwidgets import TeachingTip, TeachingTipTailPosition, TeachingTipView

from core.lock import Lockable
from utils import log


class IPopupText(ABC):

    @abstractmethod
    def popup(self, text: str, title: str = ''):
        pass


class PopupText(IPopupText, Lockable):
    current: TeachingTip | None

    def __init__(self, target):
        super().__init__()
        self.target = target
        self.current = None

    @Lockable.lock_decor
    def popup(self, text: str, title=''):
        view = TeachingTipView(
            icon=None,
            title=title,
            content=text,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
        )

        self.current = TeachingTip.make(
            target=self.target,
            view=view,
            duration=-1,  # 关闭自动消失
            tailPosition=TeachingTipTailPosition.BOTTOM,
            parent=self.target,
            isDeleteOnClose=True,
        )

        view.closed.connect(self.__delete)

    @Lockable.lock_decor
    def fadeOut(self):
        if self.current is not None:
            self.__delete()

    def __delete(self):
        self.current.close()
        self.current = None
        log.info("text finished")

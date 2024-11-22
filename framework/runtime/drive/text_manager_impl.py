import live2d.utils.log as log
from framework.handler.handler import Handler
from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.live_data.live_data import LiveData
from framework.runtime.core.text_manager import TextManager
from framework.runtime.drive.looper.looper_impl_tk import TkLooper
from framework.runtime.drive.window.gal_dialog_tk import TkGalDialog


class TextManagerImpl(TextManager):
    """
    管理弹出对话框（Motion对应的文本）
    """

    def __init__(self):
        super().__init__()

        self.__tkHandler = None
        self.dialog: TkGalDialog | None = None
        self.popupX = None
        self.popupY = None

        self.anchorX = None
        self.anchorY = None
        self.anchorW = None
        self.anchorH = None

    def initialize(self, wPos: LiveData, wSize: LiveData):
        looper = Looper.getLooper(TkLooper.name)
        self.__tkHandler = Handler(looper)
        self.__tkHandler.handle = self.setDialog
        self.__tkHandler.post(Message.obtain())

        wPos.observe(lambda v: self.adjustPopupPos(v, None), False)
        wSize.observe(lambda v: self.adjustPopupPos(None, v), False)
        self.adjustPopupPos(wPos.value, wSize.value)

    def setDialog(self, dialog):
        self.dialog = dialog

    def adjustPopupPos(self, wPos, wSize):
        if wPos:
            self.anchorX, self.anchorY = wPos
        if wSize:
            self.anchorW, self.anchorH = wSize

        if self.dialog:
            self.__tkHandler.post(
                lambda: self.dialog.move_from_thread(self.anchorX, self.anchorY, self.anchorW, self.anchorH))

    def popup(self, chara: str, text: str, delay: float = 2, lock=False):
        self.__tkHandler.post(
            lambda: self.dialog.trigger_from_thread(text, self.anchorX, self.anchorY, self.anchorW, self.anchorH,
                                                    lock=lock))
        log.Info(f"[TextManager] popup")

    def isFinished(self):
        return self.dialog is not None and not self.dialog.isVisible()

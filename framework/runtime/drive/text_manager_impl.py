import live2d.utils.log as log
from framework.live_data.live_data import LiveData
from framework.runtime.core.text_manager import TextManager
from framework.runtime.drive.window.gal_dialog import GalDialog
from framework.runtime.drive.looper.looper_impl_tk import TkLooper
from framework.handler.handler import Handler
from framework.handler.message import Message
from framework.handler.looper import Looper


class TextManagerImpl(TextManager):
    def __init__(self):
        super().__init__()

        self.handler = None
        self.dialog: GalDialog | None = None
        self.popupX = None
        self.popupY = None

        self.anchorX = None
        self.anchorY = None
        self.anchorW = None
        self.anchorH = None

    def initialize(self, wPos: LiveData, wSize: LiveData):
        # 启动 tk 线程
        looper = Looper.getLooper(TkLooper.name)
        self.handler = Handler(looper)
        self.handler.handle = self.setDialog

        self.handler.post(Message.obtain())

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

        self.popupX, self.popupY = (
            self.anchorX + self.anchorW // 2 - GalDialog.MAX_WIDTH // 2,
            self.anchorY + self.anchorH // 2
        )
        if self.dialog:
            self.dialog.move_from_thread(self.popupX, self.popupY)

    def popup(self, chara: str, text: str, delay: float = 2):
        self.dialog.trigger_from_thread(text, self.popupX, self.popupY)
        log.Info(f"[TextManager] popup")

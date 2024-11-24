from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.runtime.drive.window.gal_dialog_qt import GalDialog
from framework.runtime.drive.window.glfw_window import GlfwWindow
from framework.runtime.drive.window.kizuna_link import KizunaLink
from framework.runtime.drive.window.qglw import QGLW
from framework.runtime.drive.window.settings.settings import Settings
from framework.utils import log


class QtLooper(Looper):
    name = "qt"

    def __init__(self):
        super().__init__(self.name, manualStart=True)
        self.app: QApplication | None = None

    def shutdown(self):
        msg = Message.obtain()
        msg.handle = lambda _: self.app.quit()
        self.mq.put(msg)

    def handleMessages(self):
        msg = self.mq.get()
        while msg:
            if msg.handle:
                msg.handle(msg)

            msg.recycle()

            msg = self.mq.get()

    def loop(self, appConfig):
        self.app = QApplication()

        kizuna_init_msg = self.mq.getOrBlock()
        kl = KizunaLink()
        kl.receiver = kizuna_init_msg.data
        kizuna_init_msg.handle(kl)
        kizuna_init_msg.recycle()

        log.Info("[QtLooper] Kizuna link init")

        dialog = GalDialog()
        dialog_init_msg = self.mq.getOrBlock()
        dialog_init_msg.handle(dialog)
        dialog_init_msg.recycle()

        log.Info("[QtLooper] GalDialog init")

        mm_init_fi_msg = self.mq.getOrBlock()
        mm_init_fi_msg.recycle()

        setting = Settings(appConfig)
        setting_init_msg = self.mq.getOrBlock()
        setting_init_msg.handle(setting)
        setting_init_msg.recycle()

        log.Info("[QtLooper] Setting init")

        # 开启事件处理
        timer = QTimer()
        timer.timeout.connect(self.handleMessages)
        timer.start(100)

        self.app.exec()

        timer.stop()

        log.Info("[QtLooper] shutdown")

import sys
import threading

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from pygame.threads import Thread

from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.runtime.drive.window.kizuna_link import KizunaLink
from framework.runtime.drive.window.settings.settings import Settings
from framework.utils import log


class QtLooper(Looper):
    name = "QtLooper"

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
        self.app = QApplication(sys.argv)

        kizuna_init_msg = self.mq.getOrBlock()

        kl = KizunaLink()
        kl.receiver = kizuna_init_msg.data
        kizuna_init_msg.handle(kl)
        kizuna_init_msg.recycle()

        log.Info("[QtLooper]Kizuna init")

        setting = Settings(appConfig)
        setting_init_msg = self.mq.getOrBlock()
        setting_init_msg.handle(setting)
        setting_init_msg.recycle()

        log.Info("[QtLooper]Setting init")

        # 开启事件处理
        timer = QTimer()
        timer.timeout.connect(self.handleMessages)
        timer.start(100)

        self.app.exec()

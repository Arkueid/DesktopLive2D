from typing import Callable

from framework.runtime.core.draw_manager import DrawManager
from framework.runtime.core.input_manager import InputManager
from framework.handler.looper import Looper
from framework.utils import log


class MainLooper(Looper):

    def __init__(self):
        super().__init__("main", True)
        self.shouldExit = False

    def start(self,
              im: InputManager,
              dm: DrawManager,
              beforeStart: Callable | None = None,
              afterEnd: Callable | None = None):
        super().start(im, dm, beforeStart, afterEnd)

    def loop(self,
             im: InputManager,
             dm: DrawManager,
             beforeStart=None,
             afterEnd=None):

        if beforeStart:
            beforeStart()

        while not self.shouldExit:
            dm.beforeDraw()
            im.processInput()

            self.handleMessages()

            dm.clearBuffer()
            dm.onDraw()
            dm.doDraw()

        if afterEnd:
            afterEnd()

        log.Info("[MainLooper] shutdown")

    def shutdown(self):
        self.shouldExit = True

    def handleMessages(self):
        msg = self.mq.get()
        while msg:
            if msg.handle is not None:
                msg.handle(msg)
            msg.recycle()
            msg = self.mq.get()

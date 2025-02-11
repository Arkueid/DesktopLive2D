import time

import glfw

import live2d.v3 as l2d_v3
import live2d.v2 as l2d_v2
from framework.runtime.core.draw_manager import DrawManager
from framework.runtime.core.manager import Manager
from framework.runtime.core.window_manager import WindowManager


class DrawManagerImpl(DrawManager):

    def __init__(self):
        super().__init__()
        self.window = None

    def dispose(self):
        pass

    def doInitialize(self):
        self.window = Manager.getManager(WindowManager.name).getWindow("scene").handle
        l2d_v3.glewInit()
        l2d_v2.glewInit()

    def clearBuffer(self):
        l2d_v3.clearBuffer()

    def doDraw(self):
        glfw.swap_buffers(self.window)
        time.sleep(1 / self.fps.value)  # 60 帧

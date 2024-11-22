import time

import glfw

import live2d.v3 as l2d_v3
from framework.runtime.core.draw.draw_manager import DrawManager
from framework.runtime.core.manager import Manager
from framework.runtime.core.window.window_manager import WindowManager


class DrawManagerImpl(DrawManager):

    def __init__(self):
        super().__init__()
        self.window = None

    def dispose(self):
        pass

    def doInitialize(self):
        self.window = Manager.getManager(WindowManager.name).getWindow("scene").handle
        l2d_v3.glewInit()
        l2d_v3.setGLProperties()

    def clearBuffer(self):
        l2d_v3.clearBuffer()

    def postDraw(self):
        glfw.swap_buffers(self.window)
        time.sleep(1 / self.fps.value)  # 60 帧

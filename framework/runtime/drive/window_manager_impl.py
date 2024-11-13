import glfw

from framework.runtime.core.window_manager import WindowManager


class WindowManagerImpl(WindowManager):
    def doDispose(self):
        glfw.terminate()

    def initialize(self):
        if not glfw.init():
            raise RuntimeError("cannot init glfw")


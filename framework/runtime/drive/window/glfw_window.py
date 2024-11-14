import glfw
from OpenGL.raw.GL.VERSION.GL_1_0 import glViewport

from framework.handler.handler import Handler
from framework.live_data.live_data import LiveData
from framework.ui.window import Window
from framework.handler.looper import Looper


class GlfwWindow(Window):
    def __init__(self, wSize: LiveData, wPos: LiveData, wVisible: LiveData, stayOnTop: LiveData):
        super().__init__("scene")
        self.handler = Handler(Looper.mainLooper())
        wSize.observe(lambda x: self.performResize(x[0], x[1]))

        # 透明窗体支持
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        self.handle = glfw.create_window(self.width, self.height, self.title, None, None)
        glfw.make_context_current(self.handle)
        glfw.set_window_attrib(self.handle, glfw.DECORATED, glfw.FALSE)
        glfw.set_window_close_callback(self.handle,
                                       lambda w: glfw.destroy_window(self.handle) and Looper.mainLooper().shutdown())

        wPos.observe(lambda x: self.performMove(x[0], x[1]))
        wVisible.observe(lambda v: self.performShow() if v else self.performHide())
        stayOnTop.observe(lambda v: self.performStayOnTop() if v else self.cancelStayOnTop())

    def performMove(self, x: int, y: int):
        if self.handle is None:
            return

        glfw.set_window_pos(self.handle, x, y)

    def performResize(self, ww: int, wh: int):
        self.width = ww
        self.height = wh
        if self.handle is None:
            return

        self.handler.post(self.__doResize)

        for v in self.views:
            v.onResize(self.width, self.height)

    def __doResize(self):
        glViewport(0, 0, self.width, self.height)
        glfw.set_window_size(self.handle, self.width, self.height)

    def performShow(self):
        if self.handle is None:
            return

        glfw.show_window(self.handle)

    def performHide(self):
        if self.handle is None:
            return

        glfw.hide_window(self.handle)

    def performStayOnTop(self):
        if self.handle is None:
            return

        glfw.set_window_attrib(self.handle, glfw.FLOATING, glfw.TRUE)

    def cancelStayOnTop(self):
        if self.handle is None:
            return

        glfw.set_window_attrib(self.handle, glfw.FLOATING, glfw.FALSE)

    def performClose(self):
        if self.handle is None:
            return

        glfw.hide_window(self.handle)
        glfw.destroy_window(self.handle)

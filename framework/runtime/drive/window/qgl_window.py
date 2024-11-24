from PySide6.QtCore import Qt

from framework.handler.handler import Handler
from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.live_data.live_data import LiveData
from framework.runtime.drive.looper.looper_impl_qt import QtLooper
from framework.runtime.drive.window.qglw import QGLW
from framework.ui.window import Window


class QGLWindow(Window):

    def __init__(self, wSize: LiveData, wPos: LiveData, wVisible: LiveData, stayOnTop: LiveData):
        super().__init__("scene")
        self.__qglw: QGLW | None = None
        self.__qtLooper = Looper.getLooper(QtLooper.name)
        self.__qtHandler = Handler(self.__qtLooper)
        self.__qtHandler.handle = lambda qglw: self.init(qglw, wSize, wPos, wVisible, stayOnTop)
        self.__qtHandler.post(Message.obtain())

    def init(self, qglw, wSize: LiveData, wPos: LiveData, wVisible: LiveData, stayOnTop: LiveData):
        self.setQGLW(qglw)

        wSize.observe(lambda x: self.performResize(x[0], x[1]))
        wSize.observeOn(self.__qtLooper)
        wPos.observe(lambda x: self.performMove(x[0], x[1]))
        wPos.observeOn(self.__qtLooper)
        wVisible.observe(lambda v: self.performShow() if v else self.performHide())
        wVisible.observeOn(self.__qtLooper)
        stayOnTop.observe(lambda v: self.performStayOnTop() if v else self.cancelStayOnTop())
        stayOnTop.observeOn(self.__qtLooper)

    def setQGLW(self, qglw):
        self.__qglw = qglw
        # self.__qglw.makeCurrent()
        # self.__qglw.closed.connect(self.onClose)

    def onClose(self):
        Looper.mainLooper().shutdown()

    def performMove(self, x: int, y: int):
        self.__qglw.move(x, y)

    def performResize(self, ww: int, wh: int):
        self.__qglw.resize(ww, wh)

        for v in self.views:
            v.onResize(ww, wh)

    def performShow(self):
        self.__qglw.show()

    def performHide(self):
        self.__qglw.hide()

    def performStayOnTop(self):
        self.__qglw.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

    def cancelStayOnTop(self):
        self.__qglw.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)

    def performClose(self):
        self.__qglw.close()

from PySide6.QtCore import Signal
from PySide6.QtOpenGLWidgets import QOpenGLWidget

import live2d.v3 as l2d_v3


class QGLW(QOpenGLWidget):
    closed = Signal()

    def initializeGL(self):
        self.makeCurrent()
        l2d_v3.glewInit()
        l2d_v3.setGLProperties()

    def resizeGL(self, w, h):
        pass

    def paintGL(self):
        pass

    def closeEvent(self, event):
        self.closed.emit()

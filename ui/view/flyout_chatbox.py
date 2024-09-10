from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QKeySequence, QAction, QShortcut
from PySide6.QtWidgets import QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from qfluentwidgets import isDarkTheme, FlyoutViewBase, LineEdit, ToolButton, PrimaryToolButton, FluentIcon

from config import Configuration

class FlyoutChatView(FlyoutViewBase):

    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout(self)
        self.lineEdit = LineEdit()
        self.lineEdit.setFixedWidth(200)
        self.sendBtn = PrimaryToolButton()
        self.sendBtn.setIcon(FluentIcon.SEND)
        self.closeBtn = ToolButton()
        self.closeBtn.setIcon(FluentIcon.CLOSE)
        hbox.addWidget(self.lineEdit)
        hbox.addWidget(self.sendBtn)
        hbox.addWidget(self.closeBtn)


class FlyoutChatBox(QWidget):
    config: Configuration
    sent = Signal(str)

    def __init__(self, config: Configuration, parent: QWidget):
        super().__init__(parent)
        self.shadowEffect = None

        self.view = FlyoutChatView()

        self.config = config

        self.hBoxLayout = QHBoxLayout(self)

        self.hBoxLayout.addWidget(self.view)
        self.setShadowEffect()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)

        self.view.closeBtn.released.connect(self.hide)
        self.view.sendBtn.released.connect(self.__sendMsg)
        self.view.lineEdit.returnPressed.connect(self.__sendMsg)

    def setShadowEffect(self, blurRadius=35, offset=(0, 8)):
        color = QColor(0, 0, 0, 80 if isDarkTheme() else 30)
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(self.shadowEffect)

    def show(self):
        self.setVisible(True)
        self.move(self.config.lastX.value + self.config.width.value // 2 - self.width() // 2,
                  self.config.lastY.value + self.config.height.value + 10)
        self.activateWindow()

    def fadeOut(self):
        self.hide()

    def clearText(self):
        self.view.lineEdit.clear()

    def disable(self):
        self.view.sendBtn.setEnabled(False)

    def enable(self):
        self.view.sendBtn.setEnabled(True)

    def __sendMsg(self):
        if len(self.view.lineEdit.text()) > 0:
            self.sent.emit(self.view.lineEdit.text())

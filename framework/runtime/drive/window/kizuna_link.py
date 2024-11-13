from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from qfluentwidgets import isDarkTheme, FlyoutViewBase, LineEdit, ToolButton, PrimaryToolButton, FluentIcon


class KizunaLinkView(FlyoutViewBase):

    def __init__(self):
        super().__init__()
        self.hbox = QHBoxLayout(self)
        self.lineEdit = LineEdit()
        self.lineEdit.setFixedWidth(200)
        self.sendBtn = PrimaryToolButton()
        self.sendBtn.setIcon(FluentIcon.SEND)
        self.closeBtn = ToolButton()
        self.closeBtn.setIcon(FluentIcon.CLOSE)
        self.hbox.addWidget(self.lineEdit)
        self.hbox.addWidget(self.sendBtn)
        self.hbox.addWidget(self.closeBtn)


class KizunaLink(QWidget):

    def __init__(self):
        super().__init__()
        self.shadowEffect = None

        self.view = KizunaLinkView()

        self.hBoxLayout = QHBoxLayout(self)

        self.hBoxLayout.addWidget(self.view)
        self.setShadowEffect()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)

        self.view.closeBtn.released.connect(self.hide)
        self.view.sendBtn.released.connect(self.__sendMsg)
        self.view.lineEdit.returnPressed.connect(self.__sendMsg)
        self.receiver = None

    def setShadowEffect(self, blurRadius=35, offset=(0, 8)):
        color = QColor(0, 0, 0, 80 if isDarkTheme() else 30)
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(self.shadowEffect)

    def activate_from_thread(self, x, y, w, h):
        self.setVisible(True)
        self.move(x + w // 2 - self.width() // 2,
                  y + h + 10)
        self.activateWindow()

    def clearText(self):
        self.view.lineEdit.clear()

    def disable(self):
        self.view.lineEdit.setEnabled(False)
        self.view.sendBtn.setEnabled(False)

    def enable(self):
        self.view.lineEdit.setEnabled(True)
        self.view.sendBtn.setEnabled(True)
        # 看情况，先直接清空了
        self.view.lineEdit.clear()

    def __sendMsg(self):
        if len(self.view.lineEdit.text()) > 0 and self.receiver:
            self.receiver.value = self.view.lineEdit.text()
            self.disable()

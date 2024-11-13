from PySide6.QtGui import QPainter, QColor, QPainterPath, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import StrongBodyLabel, BodyLabel, ComboBox, ToolButton, FluentIcon, PrimaryToolButton, MessageBox

from framework.live_data.live_data import LiveData
from framework.runtime.drive.window.settings.components.base_designs import ScrollDesign


class MessageItemView(QWidget):

    def __init__(self, sender: str, content: str):
        super().__init__()
        self.vBoxLayout = QVBoxLayout()

        title = StrongBodyLabel()
        title.setText(sender)
        body = BodyLabel()
        body.setWordWrap(True)
        body.setText(content)

        self.vBoxLayout.addWidget(title)
        self.vBoxLayout.addWidget(body)

        self.setLayout(self.vBoxLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 10, 10)
        painter.fillPath(path, QBrush(QColor(255, 255, 255, 255)))


class MessageList(ScrollDesign):

    def __init__(self):
        super().__init__()
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def addMessageItem(self, itemView: MessageItemView):
        self.vBoxLayout.addWidget(itemView)

    def clearMessageItems(self):
        item = self.vBoxLayout.takeAt(0)
        while item:
            if item.widget():
                self.vBoxLayout.removeWidget(item.widget())
                item.widget().deleteLater()
            del item
            item = self.vBoxLayout.takeAt(0)

    def addBottomStretch(self):
        self.vBoxLayout.addStretch(1)


class MessageArchive(QWidget):

    def __init__(self, waifu: LiveData):
        super().__init__()
        self.setMinimumHeight(450)
        self.setStyleSheet("QWidget{background-color: white}")
        vbox = QVBoxLayout()
        line1 = QHBoxLayout()
        lbl_chat_selector = BodyLabel()
        lbl_chat_selector.setText("current moment")
        lbl_chat_selector.setStyleSheet("padding: 5px")
        self.chatSelector = ComboBox()
        line1.addWidget(lbl_chat_selector)
        line1.addWidget(self.chatSelector)
        self.messageList = MessageList()
        self.addBtn = PrimaryToolButton()
        self.addBtn.setIcon(FluentIcon.ADD)
        self.deleteBtn = ToolButton()
        self.deleteBtn.setIcon(FluentIcon.DELETE)
        line1.addWidget(self.addBtn)
        line1.addWidget(self.deleteBtn)
        vbox.addLayout(line1)
        vbox.addWidget(self.messageList)
        self.setLayout(vbox)

        self.setObjectName("messageArchive")

        self.chatSelector.currentTextChanged.connect(self.onMomentChange)
        self.addBtn.released.connect(self.onAddMoment)
        self.deleteBtn.released.connect(self.onDeleteMoment)

        waifu.observe(self.onMomentsChanged)

        self.waifu = waifu.value

    def onMomentsChanged(self, waifu):
        self.chatSelector.currentTextChanged.disconnect(self.onMomentChange)
        self.chatSelector.clear()

        self.waifu = waifu

        for i in waifu.mids:
            self.chatSelector.addItem(i, None)

        # TODO remove unnecessary `if`
        mid = '' if len(waifu.mids) == 0 else waifu.mids[0]
        self.chatSelector.setCurrentText(mid)
        self.onMomentChange(mid)

        self.chatSelector.currentTextChanged.connect(self.onMomentChange)

    def addItem(self, itemView: MessageItemView):
        self.messageList.addMessageItem(itemView)

    def clearItems(self):
        """清空消息"""
        self.messageList.clearMessageItems()

    def onMomentChange(self, v):
        self.messageList.clearMessageItems()

        if v not in self.waifu.mids:
            return
        self.waifu.recall(v)

        for h in self.waifu.currentMoment.hitokotos:
            view = MessageItemView(h.who, h.words)
            self.messageList.addMessageItem(view)
        self.messageList.addBottomStretch()

    def onAddMoment(self):
        mid = self.waifu.newMoment()
        self.chatSelector.addItem(mid)
        self.chatSelector.setCurrentText(mid)

    def onDeleteMoment(self):
        """well, it's hard to forget the moment"""
        mb = MessageBox(f"{self.waifu.name}", "このバカ!", self)
        mb.cancelButton.hide()
        mb.exec()

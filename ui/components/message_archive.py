import uuid

from PySide6.QtGui import QPainter, QColor, QPainterPath, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import StrongBodyLabel, BodyLabel, ComboBox, ToolButton, FluentIcon, PrimaryToolButton, Dialog

from chat.data.entity import Message
from config import Configuration
from ui.components.design.base_designs import ScrollDesign


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
    messageSource: callable

    def __init__(self, config: Configuration):
        super().__init__()
        self.setMinimumHeight(450)
        self.setStyleSheet("QWidget{background-color: white}")
        self.config = config
        self.messageSource = None
        vbox = QVBoxLayout()
        line1 = QHBoxLayout()
        lbl_chatSelector = BodyLabel()
        lbl_chatSelector.setText("当前对话")
        lbl_chatSelector.setStyleSheet("padding: 5px")
        self.chatSelector = ComboBox()
        line1.addWidget(lbl_chatSelector)
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

        self.chatSelector.currentTextChanged.connect(self.onChatIdChanged)
        self.addBtn.released.connect(self.onAddChat)
        self.deleteBtn.released.connect(self.onDeleteChat)

    def setChatIds(self, chatIds: list[str], messageSource: callable):
        self.chatSelector.currentTextChanged.disconnect(self.onChatIdChanged)

        self.messageSource = messageSource
        self.chatSelector.clear()
        if self.config.chatId.value not in chatIds:
            chatIds.append(self.config.chatId.value)
        self.chatSelector.addItems(chatIds)
        self.onChatIdChanged(self.config.chatId.value)
        self.chatSelector.setCurrentText(self.config.chatId.value)

        self.chatSelector.currentTextChanged.connect(self.onChatIdChanged)

    def addItem(self, itemView: MessageItemView):
        self.messageList.addMessageItem(itemView)

    def clearItems(self):
        self.messageList.clearMessageItems()
        self.messages.clear()

    def onChatIdChanged(self, v):
        if self.config.chatId.value != v:
            self.config.chatId.value = v

        self.messageList.clearMessageItems()
        for i in self.messageSource(v):
            view = MessageItemView(i.src, i.text)
            self.messageList.addMessageItem(view)
        self.messageList.addBottomStretch()

    def onAddChat(self):
        chatId = str(uuid.uuid4())
        self.chatSelector.addItem(chatId)
        self.chatSelector.setCurrentText(chatId)

    def onDeleteChat(self):
        dialog = Dialog('删除对话',
                        f"是否删除对话{self.config.chatId.value}", self)
        if dialog.exec():
            Message.delete().where(Message.chatId == self.config.chatId.value).execute()

            chatIds = Message.chatIds()
            if len(chatIds) > 0:
                self.config.chatId.value = chatIds[0]
            self.setChatIds(chatIds, Message.DataSource)

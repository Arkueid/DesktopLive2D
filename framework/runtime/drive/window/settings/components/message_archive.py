from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem
from qfluentwidgets import StrongBodyLabel, BodyLabel, ComboBox, ToolButton, FluentIcon, PrimaryToolButton, MessageBox, \
    ListWidget

from framework.handler.looper import Looper
from framework.live_data.live_data import LiveData


class MessageItemView(QWidget):

    def __init__(self, sender: str, content: str):
        super().__init__()
        self.vBoxLayout = QVBoxLayout()

        title = StrongBodyLabel()
        title.setText(sender)
        title.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        body = BodyLabel()
        body.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        body.setWordWrap(True)
        body.setText(content)

        self.vBoxLayout.addWidget(title)
        self.vBoxLayout.addWidget(body)

        self.setLayout(self.vBoxLayout)


class MessageList(ListWidget):

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

    def addMessageItem(self, itemView: MessageItemView):
        item = QListWidgetItem()
        self.addItem(item)
        item.setSizeHint(itemView.vBoxLayout.sizeHint())
        self.setItemWidget(item, itemView)

    def clearMessageItems(self):
        self.clear()


class MessageArchive(QWidget):

    def __init__(self, waifu: LiveData):
        super().__init__()
        self.setFixedHeight(450)
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

        self.waifu = waifu.value

        waifu.observe(self.onMomentsChanged)

    def onMomentsChanged(self, waifu):
        if self.waifu:
            self.waifu.onTell.unobserve(self.addMsg)
            self.waifu.onRethink.unobserve(self.addMsg)

        self.chatSelector.currentTextChanged.disconnect(self.onMomentChange)
        self.chatSelector.clear()

        self.waifu = waifu
        self.waifu.onTell.observeOn(Looper.getLooper("qt"))
        self.waifu.onTell.observe(self.addMsg, False)
        self.waifu.onRethink.observeOn(Looper.getLooper("qt"))
        self.waifu.onRethink.observe(self.addMsg, False)

        for i in waifu.mids:
            self.chatSelector.addItem(i, None)

        # TODO remove unnecessary `if`
        mid = '' if len(waifu.mids) == 0 else waifu.mids[0]
        self.chatSelector.setCurrentText(mid)
        self.onMomentChange(mid)

        self.chatSelector.currentTextChanged.connect(self.onMomentChange)

    def addMsg(self, msg):
        self.addItem(MessageItemView(msg[0], msg[1]))

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

    def onAddMoment(self):
        mid = self.waifu.newMoment()
        self.chatSelector.addItem(mid)
        self.chatSelector.setCurrentText(mid)

    def onDeleteMoment(self):
        """well, it's hard to forget the moment"""
        mb = MessageBox(f"{self.waifu.name}", "このバカ!", self)
        mb.cancelButton.hide()
        mb.exec()

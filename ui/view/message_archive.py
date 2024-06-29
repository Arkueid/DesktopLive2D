import sys

from PySide2.QtGui import QPainter, QColor, QPainterPath, QBrush
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import StrongBodyLabel, BodyLabel, ComboBox

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

    def __init__(self):
        super().__init__()
        self.messageSource = None
        vbox = QVBoxLayout()
        self.dateSelector = ComboBox()
        self.messageList = MessageList()
        vbox.addWidget(self.dateSelector)
        vbox.addWidget(self.messageList)
        self.setLayout(vbox)

    def setDates(self, dates: list[str], messageSource: callable):
        self.dateSelector.clear()
        self.dateSelector.addItems(dates)
        self.messageSource = messageSource
        self.dateSelector.currentTextChanged.connect(self.onDateChanged)
        self.onDateChanged(dates[0])

    def addItem(self, itemView: MessageItemView):
        self.messageList.addMessageItem(itemView)

    def clearItems(self):
        self.messageList.clearMessageItems()
        self.messages.clear()

    def onDateChanged(self, v):
        self.messageList.clearMessageItems()
        for i in self.messageSource(v):
            view = MessageItemView(i.src, i.text)
            self.messageList.addMessageItem(view)
        self.messageList.addBottomStretch()


if __name__ == '__main__':
    from chat.cache.database import Message

    dates = list(sorted(set([i.ct.strftime("%Y-%m-%d") for i in Message.select()])))

    app = QApplication(sys.argv)
    win = MessageArchive()
    win.setDates(dates, Message.DataSource)
    win.show()
    app.exec_()

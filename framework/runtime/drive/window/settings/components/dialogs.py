from tkinter import Label

from PySide6.QtWidgets import QMessageBox
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, BodyLabel


class InputDialog(MessageBoxBase):
    """ Custom message box """
    res: QMessageBox.StandardButton

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel()
        self.lineEdit = LineEdit()

        self.lineEdit.setClearButtonEnabled(True)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.lineEdit)

        self.widget.setMinimumWidth(350)

    @staticmethod
    def getText(parent, title, default=""):
        w = InputDialog(parent)
        w.titleLabel.setText(title)
        w.lineEdit.setText(default)

        ok = w.exec()
        res = (w.lineEdit.text(), ok)
        w.deleteLater()

        return res


class Dialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel()
        self.contentLabel = BodyLabel()

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)

        self.widget.setMinimumWidth(350)
        self.button = None

        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def accept(self):
        self.button = True
        super().accept()

    def reject(self):
        self.button = False
        super().reject()

    @staticmethod
    def getButton(parent, title, content):
        w = Dialog(parent)
        w.titleLabel.setText(title)
        w.contentLabel.setText(content)

        w.exec()
        res = w.button
        w.deleteLater()

        return res
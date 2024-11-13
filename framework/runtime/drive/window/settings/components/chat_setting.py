from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ExpandGroupSettingCard, MessageBox
from qfluentwidgets import FluentIcon, BodyLabel, ComboBox, PrimaryToolButton, ToolButton, LineEdit, TextEdit

from framework.handler.message import Message
from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.waifu import Waifu
from framework.runtime.drive.window.settings.components.base_designs import ScrollDesign
from framework.runtime.drive.window.settings.components.dialogs import Dialog, InputDialog
from framework.runtime.drive.window.settings.components.icon_design import IconDesign
from framework.runtime.drive.window.settings.components.message_archive import MessageArchive


class WaifuSettings(ScrollDesign, IconDesign):
    def __init__(self, waifu: LiveData):
        super().__init__()

        self.waifu = waifu

        frame = QWidget()
        line1 = QHBoxLayout()
        self.lbl_charaSelector = BodyLabel()
        self.lbl_charaSelector.setText("current waifu")
        self.charaSelector = ComboBox()

        for i in Waifu.waifus():
            self.charaSelector.addItem(i, None, i)

        self.charaSelector.setCurrentIndex(self.charaSelector.findData(waifu.value.name))
        self.addBtn = PrimaryToolButton()
        self.addBtn.setIcon(FluentIcon.ADD)
        self.deleteBtn = ToolButton()
        self.deleteBtn.setIcon(FluentIcon.DELETE)
        line1.addWidget(self.lbl_charaSelector)
        line1.addWidget(self.charaSelector)
        line1.addWidget(self.addBtn)
        line1.addWidget(self.deleteBtn)

        vbox = QVBoxLayout()
        vbox.addLayout(line1)
        frame.setLayout(vbox)

        self.label_charaId = BodyLabel("name")
        self.label_charaProfile = BodyLabel("desc")
        self.label_charaGreeting = BodyLabel("greeting")
        self.charaName = BodyLabel()
        self.charaName.setFixedHeight(60)
        self.charaProfile = TextEdit()
        self.charaProfile.setFixedHeight(200)
        self.charaProfile.textChanged.connect(self.onCharaProfileChanged)
        self.charaGreeting = TextEdit()
        self.charaGreeting.setFixedHeight(200)
        self.charaGreeting.textChanged.connect(self.onCharaGreetingChanged)

        setting_card = ExpandGroupSettingCard(FluentIcon.COMMAND_PROMPT, "Waifu Info")
        vbox.addWidget(self.label_charaId)
        vbox.addWidget(self.charaName)
        vbox.addWidget(self.label_charaProfile)
        vbox.addWidget(self.charaProfile)
        vbox.addWidget(self.label_charaGreeting)
        vbox.addWidget(self.charaGreeting)
        setting_card.addGroupWidget(frame)

        setting_card2 = ExpandGroupSettingCard(FluentIcon.HISTORY, "Moments")

        self.messageArchive = MessageArchive(waifu)

        setting_card2.addGroupWidget(self.messageArchive)

        self.vBoxLayout.addWidget(setting_card)
        self.vBoxLayout.addWidget(setting_card2)
        self.vBoxLayout.addStretch(0)

        self.addBtn.released.connect(self.onAddChara)
        self.deleteBtn.released.connect(self.onDeleteChara)

        self.onCharaChanged(waifu.value.name)

        self.charaSelector.currentTextChanged.connect(self.onCharaChanged)

    def onCharaChanged(self, v):
        self.charaProfile.textChanged.disconnect(self.onCharaProfileChanged)
        self.charaGreeting.textChanged.disconnect(self.onCharaGreetingChanged)

        if not v:
            self.charaName.setText('')
            self.charaProfile.setText('')
            self.charaGreeting.setText('')
        else:
            v = self.charaSelector.currentData()

            waifu: Waifu = Waifu.waifus()[v]
            self.charaName.setText(waifu.name)
            self.charaProfile.setText(waifu.desc)
            self.charaGreeting.setText(waifu.greeting)

            self.waifu.value = waifu

        self.charaProfile.textChanged.connect(self.onCharaProfileChanged)
        self.charaGreeting.textChanged.connect(self.onCharaGreetingChanged)

    def onCharaProfileChanged(self):
        self.waifu.value.desc = self.charaProfile.toPlainText()

    def onCharaGreetingChanged(self):
        self.waifu.value.greeting = self.charaGreeting.toPlainText()

    def onAddChara(self):
        name, ok = InputDialog.getText(self, "Waifu Setting", "waifu name")
        if not ok:
            return

        if name in Waifu.waifus():
            MessageBox(f"{name}", f"I'm already here!!!", self).exec()
            return

        Waifu.create(
            name=name,
            desc="You are an AI assistant.",
            greeting="OK, I got it."
        )
        self.charaSelector.addItem(name, None, name)

        MessageBox(name, "よろしく!", self).exec()

    def onDeleteChara(self):
        if self.waifu.value.name == Waifu.default().name:
            mb = MessageBox("Waifu Setting", "このバカ!", self)
            mb.cancelButton.hide()
            mb.exec()
            return

        res = Dialog.getButton(self, f'{self.charaSelector.currentText()}',
                               f"connection lost!!! ")
        if not res:
            return

        self.charaSelector.currentTextChanged.disconnect(self.onCharaChanged)

        Waifu.lostConnection(self.waifu.value)

        self.charaSelector.removeItem(self.charaSelector.currentIndex())

        new = Waifu.waifus().get(self.charaSelector.currentText())

        self.onCharaChanged(new.name)

        self.charaSelector.currentTextChanged.connect(self.onCharaChanged)

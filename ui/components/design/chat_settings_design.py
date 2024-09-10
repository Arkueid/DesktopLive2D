import uuid

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ExpandGroupSettingCard
from qfluentwidgets import FluentIcon, BodyLabel, ComboBox, PrimaryToolButton, ToolButton, LineEdit, TextEdit, Dialog

from chat.data.entity import Character
from config import Configuration
from ui.components.design.base_designs import ScrollDesign
from ui.components.design.icon_design import IconDesign
from ui.components.message_archive import MessageArchive


class ChatSettingsDesign(ScrollDesign, IconDesign):
    def __init__(self, config: Configuration):
        super().__init__()
        self.config = config

        frame = QWidget()
        line1 = QHBoxLayout()
        self.lbl_charaSelector = BodyLabel()
        self.lbl_charaSelector.setText("当前角色")
        self.charaSelector = ComboBox()

        for i in Character.idNames():
            self.charaSelector.addItem(i[0], None, i[1])

        self.charaSelector.setCurrentIndex(self.charaSelector.findData(self.config.charaId.value))
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

        self.label_charaId = BodyLabel("角色ID")
        self.label_charaProfile = BodyLabel("角色设定")
        self.label_charaGreeting = BodyLabel("问候语")
        self.charaName = LineEdit()
        self.charaName.setFixedHeight(60)
        self.charaName.textChanged.connect(self.onCharaNameChanged)
        self.charaProfile = TextEdit()
        self.charaProfile.setFixedHeight(200)
        self.charaProfile.textChanged.connect(self.onCharaProfileChanged)
        self.charaGreeting = TextEdit()
        self.charaGreeting.setFixedHeight(200)
        self.charaGreeting.textChanged.connect(self.onCharaGreetingChanged)

        settingCard = ExpandGroupSettingCard(FluentIcon.COMMAND_PROMPT, "角色设置")
        vbox.addWidget(self.label_charaId)
        vbox.addWidget(self.charaName)
        vbox.addWidget(self.label_charaProfile)
        vbox.addWidget(self.charaProfile)
        vbox.addWidget(self.label_charaGreeting)
        vbox.addWidget(self.charaGreeting)
        settingCard.addGroupWidget(frame)

        settingCard2 = ExpandGroupSettingCard(FluentIcon.HISTORY, "聊天记录")

        self.messageArchive = MessageArchive(config)

        settingCard2.addGroupWidget(self.messageArchive)

        self.vBoxLayout.addWidget(settingCard)
        self.vBoxLayout.addWidget(settingCard2)
        self.vBoxLayout.addStretch(0)

        self.addBtn.released.connect(self.onAddChara)
        self.deleteBtn.released.connect(self.onDeleteChara)

        self.onCharaChanged(self.config.charaId.value)

        self.charaSelector.currentTextChanged.connect(self.onCharaChanged)

    def onCharaNameChanged(self):
        Character.update(name=self.charaName.text()).where(Character.charaId == self.config.charaId.value).execute()

    def onCharaChanged(self, v):
        """
        更换模型
        """
        self.charaName.textChanged.disconnect(self.onCharaNameChanged)
        self.charaProfile.textChanged.disconnect(self.onCharaProfileChanged)
        self.charaGreeting.textChanged.disconnect(self.onCharaGreetingChanged)

        if not v:
            self.charaName.setText('')
            self.charaProfile.setText('')
            self.charaGreeting.setText('')
        else:
            v = self.charaSelector.currentData()

            chara: Character = Character.get_by_id(v)
            self.charaName.setText(chara.name)
            self.charaProfile.setText(chara.profile)
            self.charaGreeting.setText(chara.greeting)

            self.config.charaId.value = chara.charaId

        self.charaName.textChanged.connect(self.onCharaNameChanged)
        self.charaProfile.textChanged.connect(self.onCharaProfileChanged)
        self.charaGreeting.textChanged.connect(self.onCharaGreetingChanged)

    def onCharaProfileChanged(self):
        (Character.update(profile=self.charaProfile.toPlainText())
         .where(Character.charaId == self.config.charaId.value).execute())

    def onCharaGreetingChanged(self):
        (Character.update(greeting=self.charaGreeting.toPlainText())
         .where(Character.charaId == self.config.charaId.value).execute())

    def onAddChara(self):
        charaId = str(uuid.uuid4())
        name = "assistant"
        Character.create(charaId=charaId,
                         name=name,
                         profile="You are an AI assistant.",
                         greeting="OK, I got it.")
        self.charaSelector.addItem(name, None, charaId)

    def onDeleteChara(self):
        dialog = Dialog('删除角色',
                        f"是否删除角色{self.charaSelector.currentText()}({self.config.charaId.value})", self)
        if not dialog.exec():
            return

        self.charaSelector.currentTextChanged.disconnect(self.onCharaChanged)

        Character.delete().where(Character.charaId == self.config.charaId.value).execute()

        self.charaSelector.currentTextChanged.connect(self.onCharaChanged)

        self.charaSelector.removeItem(self.charaSelector.currentIndex())

        self.config.charaId.value = self.charaSelector.currentText()

import uuid

from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon, BodyLabel, ComboBox, PrimaryToolButton, ToolButton, LineEdit, TextEdit, Dialog, \
    InfoBarIcon, FlyoutAnimationType
from qfluentwidgets import SettingCard, ExpandGroupSettingCard, Flyout

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
        self.charaSelector.addItems(Character.charaIds())
        self.charaSelector.setCurrentText(self.config.chara.value)
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
        self.charaId = LineEdit()
        self.charaId.setFixedHeight(60)
        self.charaId.textChanged.connect(self.onEditCharaId)
        self.charaProfile = TextEdit()
        self.charaProfile.setFixedHeight(200)
        self.charaProfile.textChanged.connect(self.onCharaProfileChanged)
        self.charaGreeting = TextEdit()
        self.charaGreeting.setFixedHeight(200)
        self.charaGreeting.textChanged.connect(self.onCharaGreetingChanged)

        settingCard = ExpandGroupSettingCard(FluentIcon.COMMAND_PROMPT, "角色设置")
        vbox.addWidget(self.label_charaId)
        vbox.addWidget(self.charaId)
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

        self.onCharaIdChanged(self.config.chara.value)

        self.charaSelector.currentTextChanged.connect(self.onCharaIdChanged)

    def onEditCharaId(self):
        self.charaSelector.currentTextChanged.disconnect(self.onCharaIdChanged)

        try:
            Character.update(charaId=self.charaId.text()).where(Character.charaId == self.config.chara.value).execute()
            self.config.chara.value = self.charaId.text()
        except Exception as e:
            Flyout.create(
                icon=InfoBarIcon.ERROR,
                title='角色ID',
                content="角色ID已存在!",
                target=self,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.PULL_UP,
                isDeleteOnClose=True
            )

        self.charaSelector.removeItem(self.charaSelector.currentIndex())
        self.charaSelector.addItem(self.config.chara.value)
        self.charaSelector.setCurrentText(self.config.chara.value)

        self.charaSelector.currentTextChanged.connect(self.onCharaIdChanged)

    def onCharaIdChanged(self, v):
        self.charaId.textChanged.disconnect(self.onEditCharaId)
        self.charaProfile.textChanged.disconnect(self.onCharaProfileChanged)
        self.charaGreeting.textChanged.disconnect(self.onCharaGreetingChanged)

        chara: Character = Character.get_by_id(v)
        self.charaId.setText(chara.charaId)
        self.charaProfile.setText(chara.profile)
        self.charaGreeting.setText(chara.greeting)

        self.config.chara.value = self.charaId.text()

        self.charaId.textChanged.connect(self.onEditCharaId)
        self.charaProfile.textChanged.connect(self.onCharaProfileChanged)
        self.charaGreeting.textChanged.connect(self.onCharaGreetingChanged)

    def onCharaProfileChanged(self):
        (Character.update(profile=self.charaProfile.toPlainText())
         .where(Character.charaId == self.charaId.text()).execute())

    def onCharaGreetingChanged(self):
        (Character.update(greeting=self.charaGreeting.toPlainText())
         .where(Character.charaId == self.charaId.text()).execute())

    def onAddChara(self):
        charaId = str(uuid.uuid4())
        Character.create(charaId=charaId,
                         profile="",
                         greeting="")
        self.charaSelector.addItem(charaId)

    def onDeleteChara(self):
        dialog = Dialog('删除角色',
                        f"是否删除角色{self.config.chara.value}", self)
        if not dialog.exec():
            return

        if self.charaSelector.currentText() == "toyama kasumi":
            return

        self.charaSelector.currentTextChanged.disconnect(self.onCharaIdChanged)

        Character.delete().where(Character.charaId == self.config.chara.value).execute()

        self.charaSelector.removeItem(self.charaSelector.currentIndex())

        self.config.chara.value = self.charaSelector.currentText()

        self.charaSelector.currentTextChanged.connect(self.onCharaIdChanged)

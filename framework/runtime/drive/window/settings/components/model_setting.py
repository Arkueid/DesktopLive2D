from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, PrimaryPushButton, MessageBox

from framework.live_data.live_data import LiveData
from framework.runtime.drive.window.settings.components.base_designs import ScrollDesign
from framework.runtime.drive.window.settings.components.icon_design import IconDesign
from framework.runtime.drive.window.settings.components.motion_editor import MotionEditor
from framework.runtime.drive.window.settings.components.setting_cards import ChangeModelSettingCard


class ModelSetting(ScrollDesign, IconDesign):

    def __init__(self, modelInfo: LiveData):
        super().__init__()
        self.card_changeModel = ChangeModelSettingCard(modelInfo,
                                                       modelInfo.value.mm.modelInfoList,
                                                       FluentIcon.PEOPLE,
                                                       "模型")

        expandable = ExpandGroupSettingCard(FluentIcon.PLAY, "动作组")
        self.motionEditor = MotionEditor(modelInfo)
        self.btn_save = PrimaryPushButton("保存")
        expandable.addGroupWidget(self.motionEditor)
        expandable.addGroupWidget(self.btn_save)

        self.vBoxLayout.addWidget(self.card_changeModel)
        self.vBoxLayout.addWidget(expandable)
        self.vBoxLayout.addStretch(1)

        self.modelInfo = modelInfo
        self.btn_save.clicked.connect(self.save)

    def save(self):
        self.modelInfo.value.modelJson.save()
        MessageBox("模型设置", self.modelInfo.value.modelJson.src_file() + "保存成功!", self).exec()

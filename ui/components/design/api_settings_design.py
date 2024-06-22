from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import LineEdit, BodyLabel, ConfigItem, Icon, FluentIcon

from config import Configuration
from ui.components.design.icon_design import IconDesign
from ui.components.setting_cards import TextSettingCard


class ApiSettingsDesign(QWidget, IconDesign):
    def __init__(self, config: Configuration):
        super().__init__()

        # Initialize fields

        # Layout
        vbox = QVBoxLayout()

        self.serverCard = TextSettingCard(config.chatServer, FluentIcon.SETTING, "服务器地址")
        self.textPathCard = TextSettingCard(config.textPath, FluentIcon.SETTING, "文本处理地址")
        self.voicePathCard = TextSettingCard(config.voicePath, FluentIcon.SETTING, "语音识别接口")

        vbox.addWidget(self.serverCard)
        vbox.addWidget(self.textPathCard)
        vbox.addWidget(self.voicePathCard)
        vbox.addStretch(1)

        # Set layout
        self.setLayout(vbox)

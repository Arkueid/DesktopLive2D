from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon

from framework.runtime.app_config import Configuration
from framework.runtime.drive.window.settings.components.app_setting import AppSetting
from framework.runtime.drive.window.settings.components.chat_setting import WaifuSettings
from framework.runtime.drive.window.settings.components.icon_design import IconDesign
from framework.runtime.drive.window.settings.components.model_setting import ModelSetting


class Settings(FluentWindow, IconDesign):

    def __init__(self, appConfig: Configuration):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.SubWindow, True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setResizeEnabled(False)
        self.resource_dir = appConfig.resourceDir.value
        self.appSettings = AppSetting(appConfig)
        self.modelSettings = ModelSetting(appConfig.modelInfo)
        self.waifuSetting = WaifuSettings(appConfig.waifu)

        self.appSettings.setObjectName("appSetting")
        self.modelSettings.setObjectName("modelSetting")
        self.waifuSetting.setObjectName("waifuSetting")

        self.addSubInterface(self.appSettings, FluentIcon.APPLICATION, "应用设置")
        self.addSubInterface(self.modelSettings, FluentIcon.BRUSH, "模型设置")
        self.addSubInterface(self.waifuSetting, FluentIcon.MESSAGE, "Waifus")
        self.setMinimumSize(700, 500)

    def show(self):
        self.hide()
        size = QApplication.primaryScreen().size()
        self.move(size.width() // 2 - self.width() // 2, size.height() // 2 - self.height() // 2)
        self.setVisible(True)
        self.adjustSize()
        self.setMicaEffectEnabled(True)

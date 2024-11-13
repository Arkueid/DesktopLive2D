import sys

from PySide6.QtWidgets import QApplication

from framework.runtime.app_config import Configuration
from framework.runtime.core.kizuna.waifu import Waifu
from framework.runtime.drive.model_manager_impl import ModelManagerImpl
from framework.runtime.drive.window.settings.settings import Settings

if __name__ == '__main__':
    Waifu.link()
    app = QApplication(sys.argv)
    appConfig = Configuration()
    appConfig.load("config.json")

    mm = ModelManagerImpl()
    mm.initialize(appConfig.resourceDir.value, appConfig.modelInfo)
    # model info
    # waifu info
    win = Settings(appConfig)
    win.show()

    app.exec()

    appConfig.save()

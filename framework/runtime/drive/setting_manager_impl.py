import os.path

from PIL import Image
from pystray import MenuItem, Menu, Icon

from framework.constant.app import APP_NAME
from framework.live_data.live_data import LiveData
from framework.runtime.core.setting.setting_manager import SettingManager, SystrayOption
from framework.utils import log

icon_path = os.path.join("./Resources", "tray.ico")


def create_image():
    image = Image.open(icon_path)
    return image


class CheckableData:

    def __init__(self, liveData: LiveData):
        self.liveData = liveData

    def __call__(self, *args, **kwargs):
        return self.liveData.value


class SettingManagerImpl(SettingManager):
    def __init__(self):
        super().__init__()
        self.icon = None
        self.handler = None
        self.setting = None

    def setSetting(self, setting):
        self.setting = setting

    def doInitialize(self):
        image = create_image()
        self.icon = Icon(
            APP_NAME,
            image,
            menu=Menu(
                MenuItem("Visible", lambda: self.handleEvent(SystrayOption.VISIBLE),
                         checked=CheckableData(self.visible)),
                MenuItem("Stay On Top", lambda: self.handleEvent(SystrayOption.STAY_ON_TOP),
                         checked=CheckableData(self.stayOnTop)),
                MenuItem("Track Enable", lambda: self.handleEvent(SystrayOption.TRACK_ENABLE),
                         checked=CheckableData(self.trackEnable)),
                MenuItem("Click Enable", lambda: self.handleEvent(SystrayOption.CLICK_ENABLE),
                         checked=CheckableData(self.clickEnable)),
                MenuItem("Click Transparent", lambda: self.handleEvent(SystrayOption.CLICK_TRANSPARENT),
                         checked=CheckableData(self.clickTransparent)),
                MenuItem("Open Setting", lambda: self.handleEvent(SystrayOption.OPEN_SETTING)),
                MenuItem("Quit", lambda: self.handleEvent(SystrayOption.EXIT)),
            )
        )
        self.icon.run_detached()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event == SystrayOption.OPEN_SETTING:
            log.Info("[SettingManager] open setting")
            self.handler.post(self.setting.show)

    def dispose(self):
        self.icon.stop()

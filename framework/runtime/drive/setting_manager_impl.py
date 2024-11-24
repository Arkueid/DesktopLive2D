from PIL import Image
from pystray import MenuItem, Menu, Icon

from framework.constant.app import APP_NAME
from framework.handler.handler import Handler
from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.live_data.live_data import LiveData
from framework.runtime.app_config import Configuration
from framework.runtime.core.setting.setting_manager import SettingManager, SystrayOption
from framework.runtime.drive.looper.looper_impl_tk import TkLooper
from framework.utils import log


class CheckableData:

    def __init__(self, liveData: LiveData):
        self.liveData = liveData

    def __call__(self, *args, **kwargs):
        return self.liveData.value


class SettingManagerImpl(SettingManager):
    def __init__(self):
        super().__init__()
        self.icon = None
        self.tkHandler = None
        self.setting = None

    def setSetting(self, setting):
        self.setting = setting

    def doInitialize(self, config: Configuration):
        self.tkHandler = Handler(Looper.getLooper(TkLooper.name))
        self.tkHandler.handle = self.setSetting
        self.tkHandler.post(Message.obtain())

        image = Image.open(config.iconPath.value)
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
            self.tkHandler.post(self.setting.show)

    def dispose(self):
        self.icon.stop()

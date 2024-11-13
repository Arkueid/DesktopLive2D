from PIL import Image, ImageDraw
from pystray import MenuItem, Menu, Icon

from framework.constant.app import APP_NAME
from framework.handler.handler import Handler
from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.live_data.live_data import LiveData
from framework.runtime.core.setting_manager import SettingManager, SystrayOption
from framework.runtime.drive.looper.looper_impl_qt import QtLooper
from framework.utils import log


def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill=(0, 0, 255))
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
        self.handler = Handler(Looper.getLooper(QtLooper.name))
        self.handler.handle = self.setSetting
        self.handler.post(Message.obtain())

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

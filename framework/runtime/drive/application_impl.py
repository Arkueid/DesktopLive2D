from framework.runtime.app_config import Configuration
from framework.runtime.application import Application
from framework.runtime.core.draw_manager import DrawManager
from framework.runtime.core.input_manager import InputManager
from framework.runtime.core.kizuna.kizuna import Kizuna
from framework.runtime.core.kizuna.waifu import Waifu
from framework.runtime.core.model.model_manager import ModelManager
from framework.runtime.core.sound_manager import SoundManager
from framework.runtime.core.setting_manager import SettingManager
from framework.runtime.core.text_manager import TextManager
from framework.runtime.core.window_manager import WindowManager
from framework.runtime.drive.draw_manager_impl import DrawManagerImpl
from framework.runtime.drive.kizuna.kizuna_impl import KizunaImpl
from framework.runtime.drive.looper.looper_impl_qt import QtLooper
from framework.runtime.drive.window.glfw_window import GlfwWindow
from framework.runtime.drive.input_manager_impl import InputManagerImpl
from framework.runtime.drive.model.model_manager_impl import ModelManagerImpl
from framework.runtime.drive.sound_manager_impl import SoundManagerImpl
from framework.runtime.drive.setting_manager_impl import SettingManagerImpl
from framework.runtime.drive.text_manager_impl import TextManagerImpl
from framework.runtime.drive.window_manager_impl import WindowManagerImpl
from framework.runtime.main_looper import MainLooper
from framework.runtime.scene import Scene


class ApplicationImpl(Application):
    def __init__(self):
        self.stm: SettingManager | None = None
        self.dm: DrawManager | None = None
        self.mm: ModelManager | None = None
        self.im: InputManager | None = None
        self.wm: WindowManager | None = None
        self.sm: SoundManager | None = None
        self.tm: TextManager | None = None
        self.kizuna: Kizuna | None = None
        self.mainLooper: MainLooper | None = None
        self.qtLooper: QtLooper | None = None
        self.appConfig: Configuration | None = None

    def initialize(self):
        # 初始化本地存储
        Waifu.link()

        self.appConfig = Configuration()
        self.appConfig.load("config.json")

        # 创建主循环
        self.mainLooper = MainLooper()
        # 创建qt线程
        self.qtLooper = QtLooper()

        # 创建服务
        self.dm = DrawManagerImpl()
        self.im = InputManagerImpl()
        self.mm = ModelManagerImpl()
        self.wm = WindowManagerImpl()
        self.sm = SoundManagerImpl()
        self.tm = TextManagerImpl()
        self.stm = SettingManagerImpl()
        self.kizuna = KizunaImpl()

    def beforeStart(self):
        """有些工作不得不在主线程完成"""
        self.kizuna.initialize(
            self.appConfig.waifu,
            self.appConfig.windowPos,
            self.appConfig.windowSize
        )

        self.wm.initialize()  # 初始化窗口服务
        self.sm.initialize(self.appConfig.volume)  # 初始化音频服务
        self.tm.initialize(self.appConfig.windowPos, self.appConfig.windowSize)  # 初始化对话框服务

        scene = Scene(
            self.appConfig.motionInterval,
            self.appConfig.drawPos,
            self.appConfig.lipSyncN,
            self.appConfig.scale
        )
        window = GlfwWindow(
            self.appConfig.windowSize,
            self.appConfig.windowPos,
            self.appConfig.visible,
            self.appConfig.stayOnTop
        )
        self.wm.register(window)

        window.addView(scene)

        scene.install(self.mm)
        scene.install(self.im)
        scene.install(self.dm)
        scene.install(self.sm)
        scene.install(self.tm)
        scene.install(self.kizuna)

        self.dm.initialize(self.appConfig.fps)
        # 模型文件夹不能更改，传固定值
        self.mm.initialize(self.appConfig.resourceDir.value, self.appConfig.modelInfo)
        # 依赖 mm
        self.stm.initialize(
            self.appConfig.clickTransparent,
            self.appConfig.clickEnable,
            self.appConfig.trackEnable,
            self.appConfig.stayOnTop,
            self.appConfig.visible
        )

        self.im.initialize(
            self.mainLooper,
            self.appConfig.windowPos,
            self.appConfig.clickEnable,
            self.appConfig.clickTransparent,
            self.appConfig.trackEnable,
        )

    def afterEnd(self):
        """主线程中，主循环结束后执行"""
        self.wm.dispose()
        self.mm.dispose()
        self.stm.dispose()
        self.qtLooper.shutdown()

    def start(self):
        # 实际上是叫做 main looper 的子线程
        # 在此我们称为主循环
        self.mainLooper.start(self.im, self.dm, self.beforeStart, self.afterEnd)

        # 实际上是当前进程的直接子线程，也就是主线程
        # 依赖 model manager
        self.qtLooper.loop(self.appConfig)

        self.exit()

    def exit(self):
        self.appConfig.save()

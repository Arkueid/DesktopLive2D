import os
import sys
import threading as td

from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QApplication
from qfluentwidgets import qconfig, Flyout

from app import live2d, settings
from chat.client.baidu.qianfan import Qianfan
from config.configuration import Configuration
from core.audio_device import AudioDevice
from core.chat_delegate import ChatDelegate
from core.lipsync import globalWavHandler
from core.model import Model, find_model_dir
from core.popup_text import PopupText
from ui.components.app_settings import AppSettings
from ui.components.model_settings import ModelSettings
from ui.view.flyout_chatbox import FlyoutChatBox
from ui.view.scene import Scene
from ui.view.settings import Settings
from ui.view.systray import Systray


class Signals(QObject):
    sentSucceeded = Signal(str, str)


class Application(
    Systray.CallbackSet,
    AppSettings.CallBackSet,
    ModelSettings.CallbackSet,
    Model.CallbackSet
):
    app: QApplication

    systray: Systray

    scene: Scene

    model: Model

    config: Configuration

    settings: Settings

    audioDevice: AudioDevice

    popupText: PopupText

    flyoutChatBox: FlyoutChatBox

    chatDelegate: ChatDelegate

    signals: Signals

    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        self.signals = Signals()
        self.config = Configuration()

    def load_config(self):
        qconfig.load(settings.CONFIG_PATH, self.config)
        self.config.model_list.extend(find_model_dir(self.config.resource_dir.value))
        self.config.model3Json.load(os.path.join(
            self.config.resource_dir.value,
            self.config.model_name.value,
            self.config.model_name.value + settings.MODEL_JSON_SUFFIX
        ))

    def save_config(self) -> None:
        self.config.save()
        self.config.model3Json.save()

    def start(self) -> None:
        self.systray.start()
        self.scene.start()

        self.app.exec_()

    def exit(self) -> None:
        self.systray.hide()
        self.scene.hide()

        live2d.dispose()

        self.app.exit()

    def setup(self):
        self.systray = Systray()
        self.scene = Scene()
        self.settings = Settings(self.config)
        self.model = Model()
        self.popupText = PopupText(self.scene)
        self.audioDevice = AudioDevice(self.config, self.model.setTextFinished)
        self.flyoutChatBox = FlyoutChatBox(self.config, self.scene)
        self.chatDelegate = ChatDelegate()

        self.flyoutChatBox.sent.connect(self.chat)

        self.chatDelegate.setup(self.config, Qianfan(settings.API_KEY, settings.SECRET_KEY))
        self.signals.sentSucceeded.connect(self.chatCallback)

        live2d.init()

        self.systray.setup(self.config, self)
        self.model.setup(self.config, self)
        self.scene.setup(self.config, self.model)
        self.settings.setup(self.config, self, self)

    def toggleCharacterVisibility(self):
        self.config.visible.value = not self.config.visible.value
        self.scene.show()

    def setCharacterVisible(self):
        self.scene.activateWindow()

    def toggleEyeTracking(self):
        self.config.track_enable.value = not self.config.track_enable.value
        self.scene.setMouseTracking(self.config.track_enable.value)
        if not self.config.track_enable.value:
            self.model.onMouseMoved(self.scene.width() // 2, self.scene.height() // 2)

    def toggleClickTransparent(self):
        self.config.click_transparent.value = not self.config.click_transparent.value

    def lockWindow(self):
        self.config.enable.value = not self.config.enable.value

    def stickWindowToTop(self):
        self.config.stay_on_top.value = not self.config.stay_on_top.value
        self.scene.show()

    def openSettings(self):
        self.settings.show()

    def exitApplication(self):
        self.exit()

    def onChangeModel(self, callback):
        self.model.loadModel()
        self.config.model3Json.load(
            os.path.join(self.config.resource_dir.value,
                         self.config.model_name.value,
                         self.config.model_name.value + settings.MODEL_JSON_SUFFIX)
        )
        self.model.onResize(self.config.width.value, self.config.height.value)
        callback(self.config.model3Json)

    def onModel3JsonChanged(self):
        self.config.model3Json.save()
        self.model.loadModel()
        self.config.model3Json.load(
            os.path.join(self.config.resource_dir.value, self.config.model_name.value,
                         self.config.model_name.value + settings.MODEL_JSON_SUFFIX)
        )

    def onPlayMotion(self, group, no):
        if self.config.visible.value:
            self.model.startMotion(group, no, live2d.MotionPriority.FORCE.value)
        else:
            Flyout.create(
                title="播放动作",
                content="角色未显示，无法播放动作",
                target=self.settings,
                parent=self.settings,
                isClosable=True
            )

    def onPlayText(self, group, no):
        text: str = self.config.model3Json.motion_groups().group(group).motion(no).text()
        if text is None or len(text.strip()) == 0: return
        self.popupText.fadeOut()
        self.popupText.popup(text)

    def onMotionSoundFinished(self):
        self.popupText.fadeOut()

    def onPlaySound(self, group: str, no: int):
        soundFile = self.config.model3Json.motion_groups().group(group).motion(no).sound()
        if not soundFile:
            return
        path = os.path.join(self.config.model3Json.src_dir(), soundFile)
        if not os.path.exists(path):
            return
        self.audioDevice.play(path)
        globalWavHandler.Start(path)

    def isSoundFinished(self) -> bool:
        return self.audioDevice.isFinished()

    def onChatOpen(self):
        self.flyoutChatBox.show()

    def chatCallback(self, text, sound):
        self.popupText.unlock()
        self.audioDevice.unlock()
        self.flyoutChatBox.clearText()
        if text:
            self.popupText.popup(text)
            timer = QTimer(self.popupText.current)
            timer.timeout.connect(self.popupText.fadeOut)
            timer.start(200 * len(text))
        if sound:
            self.audioDevice.play(sound)

        self.settings.chatSettings.updateArchive()

    def chatTask(self, text: str):
        try:
            self.chatDelegate.chat(text, self.signals.sentSucceeded.emit)
        finally:
            self.popupText.unlock()
            self.audioDevice.unlock()
            self.flyoutChatBox.enable()

    def chat(self, text: str):
        self.popupText.fadeOut()
        self.audioDevice.stop()
        self.popupText.lock()
        self.audioDevice.lock()
        self.flyoutChatBox.disable()
        td.Thread(None, self.chatTask, "chat-task", (text,)).start()

import os
from abc import abstractmethod, ABC

from app import live2d, settings
from config.configuration import Configuration
from core.lipsync import globalWavHandler
from live2d.utils.lipsync import WavHandler
from live2d.v3.params import StandardParams
from ui.view.scene import Scene
from utils import log


def find_model_dir(path: str) -> list[str]:
    ls: list[str] = list()
    dirs = os.listdir(path)
    for i in dirs:

        if i == '.' or i == '..':
            continue

        dirName = os.path.join(path, i)
        if not os.path.isdir(dirName):
            continue

        modelJson = os.path.join(dirName, i + settings.MODEL_JSON_SUFFIX)
        if os.path.exists(modelJson):
            ls.append(i)
    return ls


class Model(Scene.CallBackSet):
    class CallbackSet(ABC):

        @abstractmethod
        def onPlayText(self, group: str, no: int):
            pass

        @abstractmethod
        def onPlaySound(self, group: str, no: int):
            pass

        @abstractmethod
        def onMotionSoundFinished(self):
            pass

        @abstractmethod
        def isSoundFinished(self) -> bool:
            pass

        @abstractmethod
        def onChatOpen(self):
            pass

    def onInitialize(self):
        self.initialize = True
        self.loadModel()

    def onUpdate(self, ww: int, wh: int):
        self.model.SetScale(self.config.scale.value)
        self.model.SetOffset(self.config.drawX.value, self.config.drawY.value)

        live2d.clearBuffer()
        self.model.Update()
        if globalWavHandler.Update():
            self.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                         globalWavHandler.GetRms() * self.config.lip_sync.value, 1)
        self.model.Draw()

    def onResize(self, ww: int, wh: int):
        self.model.Resize(ww, wh)

    def onLeftClick(self, rx: int, ry: int):
        self.model.Touch(rx, ry, self.onStartMotionHandler, self.setMotionFinished)

    def onRightClick(self, rx: int, ry: int):
        self.callbackSet.onChatOpen()

    def onMouseMoved(self, mx: int, my: int):
        self.model.Drag(mx, my)

    def onIntervalReached(self):
        self.startRandomMotion(live2d.MotionGroup.IDLE.value, live2d.MotionPriority.IDLE.value)

    def IsFinished(self):
        return self.motionFinished and self.soundFinished

    config: Configuration
    model: live2d.LAppModel | None
    motionFinished: bool
    initialize: bool
    callbackSet: CallbackSet

    def __init__(self):
        self.model = None
        self.motionFinished = True
        self.soundFinished = True
        self.initialize = False

    def setup(self, config: Configuration, callbackSet: CallbackSet):
        self.config = config
        self.callbackSet = callbackSet

    def loadModel(self):
        if not self.initialize:
            return

        if self.model is not None:
            del self.model

        self.model = live2d.LAppModel()

        self.model.LoadModelJson(
            os.path.join(self.config.resource_dir.value, self.config.model_name.value,
                         self.config.model_name.value + settings.MODEL_JSON_SUFFIX)
        )

        self.motionFinished = True

    def startMotion(self, group, no, priority):
        self.model.StartMotion(group, no, priority,
                               self.onStartMotionHandler, self.setMotionFinished)

    def startRandomMotion(self, group, priority):
        self.model.StartRandomMotion(group, priority, self.onStartMotionHandler, self.setMotionFinished)

    def setMotionFinished(self):
        self.motionFinished = True
        log.info("motion finished")
        self.setTextFinished()

    def setTextFinished(self):
        if self.motionFinished and self.callbackSet.isSoundFinished():
            self.callbackSet.onMotionSoundFinished()

    def onStartMotionHandler(self, group, no):
        self.motionFinished = False
        self.callbackSet.onPlaySound(group, no)
        self.callbackSet.onPlayText(group, no)

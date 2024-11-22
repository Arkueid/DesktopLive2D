import os.path
from abc import ABC, abstractmethod

import framework.constant as constants
from framework.constant import Live2DVersion
from framework.handler.looper import Looper
from framework.live_data.live_data import LiveData
from framework.runtime.core.manager import Manager
from framework.runtime.core.model.model import Model
from framework.runtime.core.model.model_info import ModelInfo
from framework.runtime.core.model.model_scene import ModelScene


def find_model_dir(version: Live2DVersion, path: str) -> list[ModelInfo]:
    ls: list[ModelInfo] = list()
    dirs = os.listdir(path)
    for i in dirs:

        if i == '.' or i == '..':
            continue

        dir_name = os.path.join(path, i)
        if not os.path.isdir(dir_name):
            continue

        if Live2DVersion.V3 == version:
            model_json = os.path.join(dir_name, i + constants.MODEL3_JSON_SUFFIX)
        elif Live2DVersion.V2 == version:
            model_json = os.path.join(dir_name, i + constants.MODEL_JSON_SUFFIX)
        else:
            raise RuntimeError(f"unknown live2d version {version}")
        if os.path.exists(model_json):
            ls.append(ModelInfo(
                name=i,
                jsonPath=model_json,
                version=version
            ))
    return ls


class ModelManager(Manager, ABC):
    name = "ModelManager"

    def __init__(self):
        super().__init__(self.name)
        self.__resourceDir: str | None = None
        self.__modelInfos = None
        self.__scene = None
        self.__currentModel: Model | None = None
        self.__currentModelInfo: LiveData | None = None

    @property
    def currentModel(self):
        return self.__currentModel

    def setScene(self, scene : ModelScene):
        self.__scene = scene

    def startMotion(self, group, no, priority):
        self.__currentModel.StartMotion(group, no, priority)
        self.__scene.onMotionStart(group, no)

    def initialize(self, resourceDir: str, modelInfo: LiveData):
        self.doInitialize()

        self.__resourceDir = resourceDir
        if not os.path.exists(resourceDir):
            self.__makeResourceDir(resourceDir)

        self.__findModels()

        modelInfo.observe(self.changeModel)
        modelInfo.observeOn(Looper.mainLooper())
        # handler = Handler(Looper.getLooper(QtLooper.name))
        # handler.post(Message.obtain())

    @abstractmethod
    def doInitialize(self):
        pass

    @abstractmethod
    def dispose(self):
        pass

    @property
    def modelInfoList(self):
        return self.__modelInfoList

    def __findModels(self):
        ls = find_model_dir(Live2DVersion.V2, os.path.join(self.__resourceDir, "v2"))
        ls.extend(find_model_dir(Live2DVersion.V3, os.path.join(self.__resourceDir, "v3")))
        self.__modelInfoList = ls

    @staticmethod
    def __makeResourceDir(resourceDir: str):
        os.makedirs(resourceDir)
        os.mkdir(os.path.join(resourceDir, "v2"))
        os.mkdir(os.path.join(resourceDir, "v3"))

    @abstractmethod
    def createModel(self, modelInfo: ModelInfo) -> Model:
        pass

    def changeModel(self, modelInfo: ModelInfo):
        model = self.createModel(modelInfo)

        if self.__scene:  # TODO for test
            self.__scene.changeModel(model)

        if self.__currentModel is not None:
            del self.__currentModel
        self.__currentModel = model

        modelInfo.mm = self

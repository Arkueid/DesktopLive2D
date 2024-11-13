import live2d.v3 as l2d_v3
from framework.runtime.core.model import Model
from framework.runtime.core.model_manager import ModelManager
from framework.runtime.drive.model_impl import ModelImpl
from framework.runtime.model_info import ModelInfo


class ModelManagerImpl(ModelManager):

    def doInitialize(self):
        l2d_v3.init()

    def createModel(self, modelInfo: ModelInfo) -> Model:
        # TODO 区别不同版本
        m = l2d_v3.LAppModel()
        return ModelImpl(modelInfo.modelJson, m)

    def dispose(self):
        l2d_v3.dispose()

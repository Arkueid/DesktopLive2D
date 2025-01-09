import live2d.v3 as l2d_v3
import live2d.v2 as l2d_v2
from framework.constant import Live2DVersion
from framework.runtime.core.model.model import Model
from framework.runtime.core.model.model_manager import ModelManager
from framework.runtime.drive.model.model_impl import ModelImpl
from framework.runtime.core.model.model_info import ModelInfo


class ModelManagerImpl(ModelManager):

    def doInitialize(self):
        l2d_v3.init()
        l2d_v2.init()
        l2d_v2.clearBuffer()

    def createModel(self, modelInfo: ModelInfo) -> Model:
        if modelInfo.version == Live2DVersion.V3:
            m = l2d_v3.LAppModel()
        elif modelInfo.version == Live2DVersion.V2:
            m = l2d_v2.LAppModel()
        else:
            raise RuntimeError("Unsupported version")
        return ModelImpl(modelInfo.modelJson, m)

    def dispose(self):
        l2d_v3.dispose()
        l2d_v2.dispose()

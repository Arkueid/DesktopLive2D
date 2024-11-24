import live2d.v3 as l2d_v3
import live2d.v2 as l2d_v2
from framework.constant import Live2DVersion
from framework.runtime.core.model.model import Model
from framework.runtime.core.model.model_manager import ModelManager
from framework.runtime.drive.model.model_v2_impl import ModelV2Impl
from framework.runtime.drive.model.model_v3_impl import ModelV3Impl
from framework.runtime.core.model.model_info import ModelInfo


class ModelManagerImpl(ModelManager):

    def doInitialize(self):
        l2d_v3.init()
        l2d_v2.init()

    def createModel(self, modelInfo: ModelInfo) -> Model:
        # TODO 区别不同版本
        if modelInfo.modelJson.version == Live2DVersion.V3:
            m = l2d_v3.LAppModel()
            return ModelV3Impl(modelInfo.modelJson, m)
        elif modelInfo.modelJson.version == Live2DVersion.V2:
            m = l2d_v2.LAppModel()
            return ModelV2Impl(modelInfo.modelJson, m)
        raise RuntimeError(f"Unsupported Version {modelInfo.modelJson.version}")

    def dispose(self):
        l2d_v3.dispose()
        l2d_v2.dispose()

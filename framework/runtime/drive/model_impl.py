from framework.runtime.core.model import Model
from framework.utils.model_json import ModelJson
from live2d.v3.params import StandardParams


# TODO: ModelImpl 内部根据模型版本的不同，分别使用不同的加载库

class ModelImpl(Model):

    def __init__(self, modelJson: ModelJson, model):
        super().__init__(modelJson)
        self._model = model

    def init(self):
        self._model.LoadModelJson(self.modelJson.src_file())

    def Resize(self, ww: int, wh: int):
        self._model.Resize(ww, wh)

    def Draw(self) -> None:
        self._model.Draw()

    def StartMotion(self, group: str, no: int, priority: int, onStartMotionHandler=None,
                    onFinishMotionHandler=None):
        self._model.StartMotion(group, no, priority, onStartMotionHandler, onFinishMotionHandler)

    def StartRandomMotion(self, group: str, priority: int, onStartMotionHandler=None,
                          onFinishMotionHandler=None):
        self._model.StartRandomMotion(group, priority, onStartMotionHandler, onFinishMotionHandler)

    def SetExpression(self, expressionID: str):
        self._model.SetExpression(expressionID)

    def SetRandomExpression(self):
        self._model.SetRandomExpression()

    def Touch(self, x: float, y: float, onStartMotionHandler=None, onFinishMotionHandler=None) -> None:
        self._model.Touch(x, y, onStartMotionHandler, onFinishMotionHandler)

    def Drag(self, x: float, y: float):
        self._model.Drag(x, y)

    def IsMotionFinished(self) -> bool:
        return self._model.IsMotionFinished()

    def SetOffset(self, dx: float, dy: float):
        self._model.SetOffset(dx, dy)

    def SetScale(self, scale: float) -> None:
        self._model.SetScale(scale)

    def SetParameterValue(self, paramId: str, value: float, weight: float):
        self._model.SetParameterValue(paramId, value, weight)

    def AddParameterValue(self, paramId: str, value: float):
        self._model.AddParameterValue(paramId, value)

    def Update(self) -> None:
        self._model.Update()

    def SetAutoBreathEnable(self, enable: bool):
        self._model.SetAutoBreathEnable(enable)

    def SetAutoBlinkEnable(self, enable: bool):
        self._model.SetAutoBlinkEnable(enable)

    def SetLipSync(self, value):
        self._model.SetParameterValue(StandardParams.ParamMouthOpenY, value, 1.0)

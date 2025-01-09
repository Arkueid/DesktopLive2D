from abc import ABC, abstractmethod

from framework.utils.model_json import ModelJson


# 不同版本模型使用 ModelBase 统一接口
class ModelBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def Resize(self, ww: int, wh: int):
        pass

    @abstractmethod
    def Draw(self) -> None:
        pass

    @abstractmethod
    def StartMotion(self, group: str, no: int, priority: int, onStartMotionHandler=None,
                    onFinishMotionHandler=None):
        pass

    @abstractmethod
    def StartRandomMotion(self, group: str, priority: int, onStartMotionHandler=None,
                          onFinishMotionHandler=None):
        pass

    @abstractmethod
    def SetExpression(self, expressionID: str):
        pass

    @abstractmethod
    def SetRandomExpression(self):
        pass

    @abstractmethod
    def Touch(self, x: float, y: float, onStartMotionHandler=None, onFinishMotionHandler=None) -> None:
        pass

    @abstractmethod
    def Drag(self, x: float, y: float):
        pass

    @abstractmethod
    def IsMotionFinished(self) -> bool:
        pass

    @abstractmethod
    def SetOffset(self, dx: float, dy: float):
        pass

    @abstractmethod
    def SetScale(self, scale: float) -> None:
        pass

    @abstractmethod
    def SetParameterValue(self, paramId: str, value: float, weight: float):
        pass

    @abstractmethod
    def AddParameterValue(self, paramId: str, value: float):
        pass

    @abstractmethod
    def Update(self) -> None:
        pass

    @abstractmethod
    def SetAutoBreathEnable(self, enable: bool):
        pass

    @abstractmethod
    def SetAutoBlinkEnable(self, enable: bool):
        pass

    @abstractmethod
    def SetLipSync(self, value):
        pass


class Model(ModelBase, ABC):

    def __init__(self, modelJson: ModelJson):
        super().__init__()
        self.modelJson = modelJson

    @abstractmethod
    def init(self):
        pass

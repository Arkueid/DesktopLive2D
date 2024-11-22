from abc import ABC, abstractmethod

from framework.runtime.core.model.model import Model


class ModelScene(ABC):

    @abstractmethod
    def changeModel(self, model: Model):
        pass

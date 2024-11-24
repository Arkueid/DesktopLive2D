from framework.constant import Live2DVersion
from framework.utils.model_json import ModelJson


class ModelInfo:
    mm = None

    def __init__(self, name: str, jsonPath: str, version: Live2DVersion):
        self.name = name
        self.jsonPath = jsonPath
        self.version = version
        self.__modelJson = None

    def __str__(self):
        return f"ModelInfo(name={self.name}, jsonPath={self.jsonPath}, version={self.version})"

    @property
    def modelJson(self):
        if self.__modelJson is None:
            self.__modelJson = ModelJson(self.version)
            self.__modelJson.load(self.jsonPath)
        return self.__modelJson

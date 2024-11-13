from enum import Enum

MODEL_JSON_SUFFIX = ".model.json"
MODEL3_JSON_SUFFIX = ".model3.json"


class Live2DVersion(Enum):
    V2 = 2
    V3 = 3

    @staticmethod
    def parse(value: int):
        if value == 2:
            return Live2DVersion.V2
        elif value == 3:
            return Live2DVersion.V3
        else:
            raise RuntimeError(f"unknown live2d version int {value}")

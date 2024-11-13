from pprint import pprint

from framework.constant import Live2DVersion
from framework.utils.model_json import ModelJson, __Keys3, MotionGroup, Motion, __Keys2

if __name__ == '__main__':
    m = ModelJson(Live2DVersion.V2)
    m.load("../../../Resources/v2/kasumi2/kasumi2.model.json")
    mg = MotionGroup(m.version)
    mg.add(Motion(m.version, {
        "file": "123.motion3.json"
    }))
    m.motion_groups().add("123", mg)
    pprint(m.meta())

    m = ModelJson(Live2DVersion.V3)
    m.load("../../../Resources/v3/Haru/Haru.model3.json")
    mg = MotionGroup(m.version)
    mg.add(Motion(m.version, {
        "File": "123.motion3.json"
    }))
    m.motion_groups().add("123", mg)
    pprint(m.meta())
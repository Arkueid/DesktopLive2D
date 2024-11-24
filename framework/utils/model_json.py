import json
import os.path
from abc import ABC

from framework.constant import Live2DVersion


class Keys(ABC):
    FILE_REFERENCES: str
    MOTIONS: str
    FILE: str
    SOUND: str
    TEXT: str


class __Keys3(Keys):
    FILE_REFERENCES = "FileReferences"
    MOTIONS = "Motions"
    FILE = "File"
    SOUND = "Sound"
    TEXT = "Text"


KEYS3 = __Keys3()


class __Keys2(Keys):
    FILE_REFERENCES = "FileReferences"
    MOTIONS = "motions"
    FILE = "file"
    SOUND = "sound"
    TEXT = "sound"


KEYS2 = __Keys2()


class VersionedJson:

    def __init__(self, version: Live2DVersion):
        self.__version = version
        if version == Live2DVersion.V3:
            self.__keys = KEYS3
        elif version == Live2DVersion.V2:
            self.__keys = KEYS2
        else:
            raise RuntimeError(f"unknown live2d version {version}")

    @property
    def keys(self) -> Keys:
        return self.__keys

    @property
    def version(self) -> Live2DVersion:
        return self.__version


class Motion(VersionedJson):

    def __init__(self, version: Live2DVersion, d: dict):
        super().__init__(version)
        self.__meta = d
        if self.keys.FILE not in self.__meta:
            self.__meta[self.keys.FILE] = ""
        if self.keys.SOUND not in self.__meta:
            self.__meta[self.keys.SOUND] = ""
        if self.keys.TEXT not in self.__meta:
            self.__meta[self.keys.TEXT] = ""

    def file(self):
        return self.__meta[self.keys.FILE]

    def sound(self):
        return self.__meta[self.keys.SOUND]

    def text(self):
        return self.__meta[self.keys.TEXT]

    def set_file(self, value: str):
        self.__meta[self.keys.FILE] = value

    def set_sound(self, value: str):
        self.__meta[self.keys.SOUND] = value

    def set_text(self, value: str):
        self.__meta[self.keys.TEXT] = value

    def meta(self):
        return self.__meta


class MotionGroup(VersionedJson):

    def __init__(self, version: Live2DVersion, ls=None):
        super().__init__(version)
        if ls is None:
            ls = []
        self.__meta = ls

    def __iter__(self):
        for i in self.__meta:
            yield Motion(self.version, i)

    def motion(self, nr: int):
        return Motion(self.version, self.__meta[nr])

    def add(self, motion: Motion):
        self.__meta.append(motion.meta())

    def remove(self, motion: Motion):
        self.__meta.remove(motion.meta())

    def pop(self, no: int):
        self.__meta.pop(no)

    def meta(self):
        return self.__meta


class MotionGroups(VersionedJson):

    def __init__(self, version: Live2DVersion, d: dict):
        super().__init__(version)
        self.__meta = d

    def __iter__(self):
        for key, value in self.__meta.items():
            yield key, MotionGroup(self.version, value)

    def group(self, name: str) -> MotionGroup:
        return MotionGroup(self.version, self.__meta[name])

    def add(self, name: str, motionGroup: MotionGroup):
        self.__meta[name] = motionGroup.meta()

    def remove(self, name: str):
        self.__meta.pop(name)

    def meta(self):
        return self.__meta

    def set_meta(self, meta):
        self.__meta = meta

    def group_names(self):
        return tuple(self.__meta.keys())


class ModelJson(VersionedJson):

    def __init__(self, version: Live2DVersion, d=None):
        super().__init__(version)
        self.__meta: dict | None = None
        self.__src_file: str | None = None
        self.__src_dir: str | None = None

        if d is None:
            d = {}
        self.__meta = d

    def motion_groups(self) -> MotionGroups:
        if self.keys == KEYS2:
            return MotionGroups(self.version, self.__meta[self.keys.MOTIONS])
        else:
            return MotionGroups(self.version,
                                self.__meta[self.keys.FILE_REFERENCES].get(self.keys.MOTIONS, {}))

    def src_dir(self):
        return self.__src_dir

    def src_file(self):
        return self.__src_file

    def load(self, fileName):
        self.__src_file = fileName
        self.backup()
        with open(fileName, 'r', encoding='utf-8') as f:
            self.__meta = json.loads(f.read())
        self.__src_dir = os.path.split(fileName)[0]

    def __write_to(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__meta, ensure_ascii=False, indent=4))

    def backup(self):
        if os.path.exists(self.__src_file + ".bak"):
            return
        self.__write_to(self.__src_file + ".bak")

    def save(self):
        self.__write_to(self.__src_file)

    def meta(self):
        return self.__meta

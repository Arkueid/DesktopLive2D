import json
import os
import uuid

from framework.runtime.core.kizuna.hitokoto import Hitokoto


class Moment:

    def __init__(self):
        self.mid = None
        self.srcFile = None
        self.hitokotos: list[Hitokoto] | None = None

    @classmethod
    def create(cls, homeDir):
        obj = cls()
        obj.mid = uuid.uuid4().hex
        obj.srcFile = os.path.join(homeDir, "moments", f"{obj.mid}.jsonlines")
        obj.hitokotos = list()
        return obj

    @classmethod
    def load(cls, mf):
        self = cls()
        self.srcFile = mf
        self.mid = mf.replace(".jsonlines", "")
        with open(self.srcFile, "r", encoding="utf-8") as jlf:
            self.hitokotos = [Hitokoto.create(json.loads(line)) for line in jlf.readlines()]
        return self

    def save(self):
        with open(self.srcFile, "w", encoding="utf-8") as jlf:
            jlf.writelines([json.dumps(h.json, ensure_ascii=False) + "\n" for h in self.hitokotos])

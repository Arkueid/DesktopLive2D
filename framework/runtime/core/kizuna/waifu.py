import json
import os
import time
from logging import warning
from threading import RLock

from framework.constant.waifu import DefaultWaifu
from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.hitokoto import Hitokoto
from framework.runtime.core.kizuna.moment import Moment


class Waifu:
    WAIFUS_HOME = "waifus"

    __waifus: dict | None = None
    __lock: RLock = RLock()
    __default = None

    def __init__(self):
        self.name = None
        self.desc = None
        self.greeting = None
        self.home = None

        self.moments: dict[str, Moment] | None = None

        # runtime attr
        # current moment
        self.cMid = None
        self.onTell = LiveData(None)
        self.onRethink = LiveData(None)

    def __str__(self):
        return (f"Waifu(\n\tname={self.name},\n"
                f"\tdesc={self.desc},\n"
                f"\tgreeting={self.greeting},\n"
                f"\tmoments={[k for k in self.moments]}\n"
                f"\tcMid={self.cMid}"
                f")")

    @property
    def mids(self):
        return tuple(self.moments.keys())

    def recall(self, mid: str):
        self.cMid = mid

    def tell(self, words):
        if self.cMid is None:
            raise RuntimeError("current moment not set, call `recall` first")

        self.moments[self.cMid].hitokotos.append(
            Hitokoto(
                self.cMid,
                "me",
                words,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                False
            )
        )

        self.onTell.value = ("me", words)

    def rethink(self, words):
        if self.cMid is None:
            raise RuntimeError("current moment not set, call `recall` first")

        self.moments[self.cMid].hitokotos.append(
            Hitokoto(
                self.cMid,
                self.name,
                words,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                True
            )
        )

        self.onRethink.value = (self.name, words)

    @classmethod
    def __initDirs(cls, obj):
        init_home = os.path.exists(obj.home)
        if not init_home:
            os.makedirs(obj.home)

        mm_dir = os.path.join(obj.home, "moments")
        init_mm = os.path.exists(mm_dir)
        if not init_mm:
            os.makedirs(mm_dir)
            obj.cMid = obj.newMoment()

        if init_home and init_mm:
            return False, mm_dir
        else:
            obj.save()
            return True, mm_dir

    @classmethod
    def __create(cls, name, desc, greeting, home=None):
        obj = cls()
        obj.name = name
        obj.desc = desc
        obj.greeting = greeting
        if home:
            obj.home = home
        else:
            obj.home = os.path.join(Waifu.WAIFUS_HOME, name)
        obj.moments = dict()

        ret, mm_dir = Waifu.__initDirs(obj)

        if ret:
            return obj

        for i in os.listdir(mm_dir):
            if i.endswith(".jsonlines"):
                key = i.replace(".jsonlines", "")
                obj.moments[key] = Moment.load(os.path.join(mm_dir, i))
        return obj

    @classmethod
    def __load(cls, homeDir):
        info_path = os.path.join(homeDir, "info.json")
        with open(info_path, "r", encoding="utf-8") as f:
            d = json.load(f)
            obj = Waifu.__create(d["name"], d["desc"], d["greeting"], homeDir)
            obj.cMid = d.get("cMid", obj.cMid)
        return obj

    @classmethod
    def create(cls, name, desc, greeting, home=None):
        if name == Waifu.__default.name:
            return Waifu.__default

        obj = cls()
        obj.name = name

        with Waifu.__lock:
            if Waifu.__waifus is None:
                raise RuntimeError("waifus not connected!!! call `link` first")
            if obj.name not in Waifu.__waifus:
                Waifu.__waifus[obj.name] = obj
            else:
                warning(f"waifu `{obj.name}` already connected!!!")
                return Waifu.__waifus[obj.name]

        obj.desc = desc
        obj.greeting = greeting
        if home:
            obj.home = home
        else:
            obj.home = os.path.join(cls.WAIFUS_HOME, name)
        obj.moments = dict()

        ret, mm_dir = Waifu.__initDirs(obj)

        if ret:
            return obj

        for i in os.listdir(mm_dir):
            if i.endswith(".jsonlines"):
                key = i.replace(".jsonlines", "")
                obj.moments[key] = Moment.load(os.path.join(mm_dir, i))
        return obj

    @classmethod
    def load(cls, homeDir):
        info_path = os.path.join(homeDir, "info.json")
        with open(info_path, "r", encoding="utf-8") as f:
            d = json.load(f)
            obj = cls.create(d["name"], d["desc"], d["greeting"], homeDir)
            obj.cMid = d.get("cMid", obj.cMid)
        return obj

    def save(self):
        d = {
            "name": self.name,
            "desc": self.desc,
            "greeting": self.greeting,
            "cMid": self.cMid,
        }
        if not os.path.exists(self.home):
            os.makedirs(self.home)
        with open(os.path.join(self.home, "info.json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

        for mm in self.moments.values():
            mm.save()

    def newMoment(self):
        mm = Moment.create(self.home)
        self.moments[mm.mid] = mm
        return mm.mid

    @property
    def currentMoment(self):
        if self.cMid is None:
            raise RuntimeError("current moment not set, call `recall` first")

        return self.moments[self.cMid]

    @staticmethod
    def link():
        if not os.path.exists(Waifu.WAIFUS_HOME):
            os.makedirs(Waifu.WAIFUS_HOME)

        with Waifu.__lock:
            Waifu.__waifus = dict()
            dw = Waifu.__create(DefaultWaifu.NAME, DefaultWaifu.DESC, DefaultWaifu.GREETING)
            Waifu.__waifus[dw.name] = dw
            Waifu.__default = dw
            Waifu.__find_waifus(Waifu.WAIFUS_HOME)

    @staticmethod
    def waifus():
        return Waifu.__waifus

    @staticmethod
    def default():
        return Waifu.__default

    @staticmethod
    def __find_waifus(waifu_home):
        dic = Waifu.__waifus
        for d in os.listdir(waifu_home):
            dp = os.path.join(waifu_home, d)
            if os.path.isdir(dp):
                jf = os.path.join(dp, "info.json")
                if os.path.exists(jf):
                    wf = Waifu.__load(dp)
                    dic[wf.name] = wf

    @staticmethod
    def lostConnection(waifu):
        with Waifu.__lock:
            if waifu.name != Waifu.__default.name:
                Waifu.__waifus.pop(waifu.name)
            else:
                return

        jp = os.path.join(waifu.home, "info.json")
        if os.path.exists(jp):
            os.rename(jp, jp + ".lost." + time.strftime("%Y.%m.%m.%H.%M.%S"))

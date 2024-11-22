import json
import os.path

from framework.constant import Live2DVersion
from framework.constant.waifu import DefaultWaifu
from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.waifu import Waifu
from framework.runtime.core.model.model_info import ModelInfo


# LiveData change --> UI
# change by UI --> LiveData --> saved file
class ConfigMeta:
    def __init__(self):
        # model manager
        self.modelInfo = LiveData(ModelInfo("nn",
                                            "./Resources/v3/nn/nn.model3.json",
                                            Live2DVersion.V3))
        self.resourceDir = LiveData("./Resources")

        # scene
        self.motionInterval = LiveData(10)  # 小于0 禁用，单位秒
        self.drawPos = LiveData((0, 0))  # -2.0 ~ 2.0
        self.lipSyncN = LiveData(1.0)  # >0
        self.scale = LiveData(1.0)  # >0

        # input manager
        self.clickTransparent = LiveData(False)
        self.clickEnable = LiveData(False)
        self.trackEnable = LiveData(True)

        # window manager
        self.stayOnTop = LiveData(False)
        self.visible = LiveData(True)
        self.windowSize = LiveData((200, 300))
        self.windowPos = LiveData((600, 800))

        # draw manager
        self.fps = LiveData(30)

        # TODO: systray manager
        self.iconPath = LiveData(None)

        # sound manager
        self.volume = LiveData(100)  # 0 - 100

        # waifu
        self.waifu = LiveData(Waifu.create(DefaultWaifu.NAME, DefaultWaifu.DESC, DefaultWaifu.GREETING))

        self.jsonPath = None

    @property
    def json(self):
        d = dict()
        for i in self.__dict__:
            if i == "jsonPath":
                continue

            if i == "modelInfo":
                mf = self.modelInfo.value
                d[i] = {
                    "name": mf.name,
                    "version": mf.version.value,
                    "jsonPath": mf.jsonPath
                }
            elif i == "waifu":
                d[i] = self.waifu.value.home
                self.waifu.value.save()
            else:
                d[i] = self.__dict__[i].value
        return d


class Configuration(ConfigMeta):

    def load(self, path: str):
        self.jsonPath = path

        if not os.path.exists(path):
            self.save()
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            for i in d:
                if i == "modelInfo":
                    mf = d[i]
                    self.__dict__[i] = LiveData(
                        ModelInfo(mf["name"], mf["jsonPath"], Live2DVersion.parse(mf["version"])))
                elif i == "waifu":
                    home_dir = d[i]
                    self.waifu = LiveData(Waifu.load(home_dir))
                else:
                    self.__dict__[i] = LiveData(d[i])
        except Exception as e:
            raise RuntimeError(e)

    def save(self, jsonPath=None):
        if jsonPath is None:
            p = self.jsonPath
        else:
            p = jsonPath
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(self.json, f, ensure_ascii=False, indent=4)

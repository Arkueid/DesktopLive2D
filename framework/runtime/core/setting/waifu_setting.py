from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.waifu import Waifu


class WaifuSetting:

    def __init__(self, current_waifu: LiveData):
        self.currentWaifu = current_waifu

    def selectWaifu(self, name: str):
        self.currentWaifu.value = Waifu.waifus().get(name)

    @staticmethod
    def newWaifu(name: str, desc: str, greeting: str):
        Waifu.create(name, desc, greeting)

    @staticmethod
    def getWaifus() -> list[str]:
        return Waifu.waifus().keys()

    def getMoments(self) -> list[str]:
        return self.currentWaifu.value.mids()

    def getCurrentMoment(self) -> Waifu:
        return self.currentWaifu.value.currentMoment()

    def selectMoment(self, mid: str):
        self.currentWaifu.value.recall(mid)

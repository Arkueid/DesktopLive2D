from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.moment import Moment
from framework.runtime.core.kizuna.waifu import Waifu


class WaifuSettingViewModel:

    def __init__(self, current_waifu: LiveData):
        self.__currentWaifu = current_waifu

    @property
    def currentWaifu(self) -> LiveData:
        return self.__currentWaifu

    def selectWaifu(self, name: str) -> None:
        self.__currentWaifu.value = Waifu.waifus().get(name)

    @staticmethod
    def newWaifu(name: str, desc: str, greeting: str) -> Waifu:
        return Waifu.create(name, desc, greeting)

    @staticmethod
    def getWaifuNames() -> list[str]:
        return list(Waifu.waifus().keys())

    def getMoments(self) -> list[Moment]:
        return self.__currentWaifu.value.moments

    def getCurrentMoment(self) -> Waifu:
        return self.__currentWaifu.value.currentMoment()

    def selectMoment(self, mid: str) -> None:
        self.__currentWaifu.value.recall(mid)

    def newMoment(self) -> str:
        return self.__currentWaifu.value.newMoment()

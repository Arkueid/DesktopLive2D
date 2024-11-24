from framework.live_data.live_data import BiasRangeLiveData, RangeLiveData
from framework.runtime.app_config import Configuration


class AppSettingViewModel:

    def __init__(self, config: Configuration):
        self.windowWidth = BiasRangeLiveData(config.windowSize, (0, 65535), 0)
        self.windowHeight = BiasRangeLiveData(config.windowSize, (0, 65535), 1)
        self.drawX = BiasRangeLiveData(config.drawPos, (-2.0, 2.0), 0)
        self.drawY = BiasRangeLiveData(config.drawPos, (-2.0, 2.0), 1)
        self.scale = RangeLiveData(config.scale, (0.01, 65535))
        self.fps = RangeLiveData(config.fps, (30, 120))
        self.motionInterval = RangeLiveData(config.motionInterval, (-1, 65535))
        self.lipSyncN = RangeLiveData(config.lipSyncN, (0, 65535))
        self.volume = RangeLiveData(config.volume, (0, 100))

    def getMotionInterval(self) -> int:
        return self.motionInterval.value

    def setMotionInterval(self, interval: int) -> None:
        self.motionInterval.value = interval

    def getDrawX(self) -> float:
        return self.drawX.value

    def setDrawX(self, x: float) -> None:
        self.drawX.value = x

    def getDrawY(self) -> float:
        return self.drawY.value

    def setDrawY(self, y: float) -> None:
        self.drawY.value = y

    def getWindowWidth(self) -> int:
        return self.windowWidth.value

    def setWindowWidth(self, width: int) -> None:
        self.windowWidth.value = width

    def getWindowHeight(self) -> int:
        return self.windowHeight.value

    def setWindowHeight(self, height: int) -> None:
        self.windowHeight.value = height

    def getLipSyncN(self) -> float:
        return self.lipSyncN.value

    def setLipSyncN(self, lipSyncN: float) -> None:
        self.lipSyncN.value = lipSyncN

    def getScale(self) -> float:
        return self.scale.value

    def setScale(self, scale: float) -> None:
        self.scale.value = scale

    def getFps(self) -> int:
        return self.fps.value

    def setFps(self, fps: int) -> None:
        self.fps.value = fps

    def getVolume(self) -> int:
        return self.volume.value

    def setVolume(self, volume: int) -> None:
        self.volume.value = volume

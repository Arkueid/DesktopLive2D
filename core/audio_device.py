import time
from abc import ABC, abstractmethod

from PySide2.QtCore import QUrl, QCoreApplication
from PySide2.QtMultimedia import QMediaPlayer

from config import Configuration
from core.lock import Lockable


class IAudioDevice(ABC):

    finished: bool

    @abstractmethod
    def play(self, audioPath: str) -> None:
        pass

    @abstractmethod
    def isFinished(self) -> bool:
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def setVolume(self, v: int):
        pass


class AudioDevice(IAudioDevice, Lockable):

    def __init__(self, volumeConfig: Configuration, onFinishCallback: callable):
        super().__init__()
        self.audioPlayer = QMediaPlayer()
        self.finished = True
        self.onFinishCallback = onFinishCallback
        self.audioPlayer.mediaStatusChanged.connect(self.__onFinished)
        self.audioPlayer.setVolume(volumeConfig.volume.value)
        volumeConfig.volume.valueChanged.connect(self.setVolume)

    def isFinished(self) -> bool:
        return not self.isLocked() and self.finished

    def __onFinished(self, state):
        if state == QMediaPlayer.EndOfMedia:
            self.finished = True
            info = time.strftime("[INFO  %Y-%m-%d %H:%M:%S] sound finished", time.localtime(time.time()))
            print(info)
            self.onFinishCallback()

    @Lockable.lock_decor
    def play(self, audioPath: str) -> None:
        self.stop()
        self.finished = False
        self.audioPlayer.setMedia(QUrl.fromLocalFile(audioPath))
        self.audioPlayer.play()
        print(f"[INFO  {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] play audio: {audioPath}")

    @Lockable.lock_decor
    def stop(self):
        if self.audioPlayer.state() == QMediaPlayer.PlayingState:
            self.audioPlayer.stop()
            QCoreApplication.processEvents()
            self.finished = True

    def setVolume(self, v: int):
        self.audioPlayer.setVolume(v)

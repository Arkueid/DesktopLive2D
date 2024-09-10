from abc import ABC, abstractmethod

from PySide6.QtCore import QUrl, QCoreApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from config import Configuration
from core.lock import Lockable
from utils import log


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
        self.audioOutput = QAudioOutput()
        self.audioPlayer.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(volumeConfig.volume.value / 100)
        volumeConfig.volume.valueChanged.connect(self.setVolume)

    def isFinished(self) -> bool:
        return not self.isLocked() and self.finished

    def __onFinished(self, state):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.finished = True
            log.info("sound finished")
            self.onFinishCallback()

    @Lockable.lock_decor
    def play(self, audioPath: str) -> None:
        self.stop()
        self.finished = False
        self.audioPlayer.setSource(QUrl.fromLocalFile(audioPath))
        self.audioPlayer.play()
        log.info(f"play audio: {audioPath}")

    @Lockable.lock_decor
    def stop(self):
        if self.audioPlayer.playbackRate() == QMediaPlayer.PlaybackState.PlayingState:
            self.audioPlayer.stop()
            QCoreApplication.processEvents()
            self.finished = True

    def setVolume(self, v: int):
        self.audioOutput.setVolume(v / 100)

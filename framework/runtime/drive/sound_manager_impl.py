import os.path

from pygame import mixer

from framework.runtime.core.sound_manager import SoundManager

import live2d.utils.log as log
from live2d.utils.lipsync import WavHandler


class SoundManagerImpl(SoundManager):
    def getRsm(self):
        return self.wavHandler.Update(), self.wavHandler.GetRms()

    def __init__(self):
        super().__init__()
        self.wavHandler = WavHandler()

    def doInitialize(self):
        mixer.init()

    def play(self, audioPath: str) -> None:
        if not self.isFinished():
            self.stop()

        if os.path.isfile(audioPath):
            mixer.music.load(audioPath)
            mixer.music.play()
            log.Info(f"[SoundManager] play: {audioPath}")
            self.wavHandler.Start(audioPath)

    def isFinished(self) -> bool:
        return not mixer.music.get_busy()

    def stop(self):
        mixer.music.stop()

    def setVolume(self, v: int):
        mixer.music.set_volume(v / 100)

import os.path

import pygame.mixer

from framework.runtime.core.sound_manager import SoundManager

from live2d.utils.lipsync import WavHandler
from live2d.utils import log


class SoundManagerImpl(SoundManager):
    def getRsm(self):
        return self.wavHandler.Update(), self.wavHandler.GetRms()

    def __init__(self):
        super().__init__()
        self.wavHandler = WavHandler()

    def doInitialize(self):
        pygame.mixer.init()

    def play(self, audioPath: str) -> None:
        if not self.isFinished():
            self.stop()

        if os.path.exists(audioPath):
            pygame.mixer.music.load(audioPath)
            pygame.mixer.music.play()
            log.Info(f"[SoundManager] play: {audioPath}")
            self.wavHandler.Start(audioPath)

    def isFinished(self) -> bool:
        return not pygame.mixer.music.get_busy()

    def stop(self):
        pygame.mixer.music.stop()

    def setVolume(self, v: int):
        pygame.mixer.music.set_volume(v / 100)

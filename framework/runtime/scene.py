import os
import time

from framework.constant import Mouse
from framework.live_data.live_data import LiveData
from framework.runtime.core.draw_manager import DrawManager
from framework.runtime.core.input_manager import InputManager
from framework.runtime.core.kizuna.kizuna import Kizuna
from framework.runtime.core.model import Model
from framework.runtime.core.model_manager import ModelManager
from framework.runtime.core.sound_manager import SoundManager
from framework.runtime.core.text_manager import TextManager
from framework.ui.window import Window
from framework.ui.view import View


class Scene(View):

    def __init__(
            self,
            motionInterval: LiveData,
            drawPos: LiveData,
            lipSyncN: LiveData,
            scale: LiveData
    ):
        super().__init__()
        self.model: Model | None = None
        self.ww = None
        self.wh = None

        self.sm: SoundManager | None = None
        self.tm: TextManager | None = None
        self.kzn: Kizuna | None = None

        self.lastMotionEndAt = time.time()
        self.motionInterval = motionInterval
        self.lipSyncN = lipSyncN

        drawPos.observe(lambda pos: self.model.SetOffset(pos[0], pos[1]) if self.model else None)
        scale.observe(lambda s: self.model.SetScale(s) if self.model else None)

    def install(self, m):
        if isinstance(m, ModelManager):
            m.setScene(self)
        elif isinstance(m, InputManager):
            m.pushClickable(self)
        elif isinstance(m, DrawManager):
            m.addDrawable(self)
        elif isinstance(m, SoundManager):
            self.sm = m
        elif isinstance(m, TextManager):
            self.tm = m
        elif isinstance(m, Kizuna):
            self.kzn = m

    def changeModel(self, model: Model):
        self.model = model
        self.model.init()
        self.model.Resize(self.ww, self.wh)

    def onResize(self, ww: int, wh: int):
        self.ww = ww
        self.wh = wh

        if self.model is None:
            return

        self.model.Resize(ww, wh)

    def onUpdate(self):
        if self.model is None:
            return

        self.model.Update()

        updated, rms = self.sm.getRsm()
        if updated:
            self.model.SetLipSync(rms * self.lipSyncN.value)

        # 自动播放 idle 动作组
        # -1 禁止自动播放
        if self.motionInterval.value < 0:
            return

        ct = time.time()
        if self.isFinished() and self.lastMotionEndAt < 0:
            self.lastMotionEndAt = time.time()

        if self.lastMotionEndAt > 0 and ct - self.lastMotionEndAt > self.motionInterval.value:
            self.lastMotionEndAt = -1
            self.model.StartRandomMotion("Idle", 1, self.onMotionStart)

    def onDraw(self):
        if self.model is None:
            return

        self.model.Draw()

    def onPressed(self, button, x: int, y: int) -> bool:
        return True

    def isFinished(self):
        """动作、音频、文本全部播放完毕"""
        return self.model.IsMotionFinished() and self.tm.isFinished() and self.sm.isFinished()

    def onMotionStart(self, name: str, nr: int):
        motion = self.model.modelJson.motion_groups().group(name).motion(nr)
        sound = motion.sound()
        audio_path = os.path.join(self.model.modelJson.src_dir(), sound)
        self.sm.play(audio_path)

        text = motion.text()
        self.tm.popup("", text, 5)

    def onReleased(self, button, x: int, y: int) -> bool:
        if self.model is None:
            return False

        if button == Mouse.Button.LEFT:
            self.model.Touch(x, y, self.onMotionStart)
            return True

        if button == Mouse.Button.RIGHT:
            self.kzn.tell()
            return True

        return False

    def onDoubleClicked(self, button, x: int, y: int) -> bool:
        return True

    def onMoved(self, x: int, y: int) -> bool:
        if self.model is None:
            return False

        self.model.Drag(x, y)
        return True

    def onAttach(self, w: Window):
        self.onResize(w.width, w.height)

import os.path
from abc import ABC, abstractmethod

from framework.handler.handler import Handler
from framework.handler.looper import Looper
from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.waifu import Waifu
from framework.runtime.core.manager import Manager
from framework.runtime.core.text_manager import TextManager

"""
缩进代表函数内部调用

Kizuna.ruleBreak 选择当前对话的 waifu
Kizuna.recall 选择当前对话的 上下文（历史记录）
Kizuna.tell 
    同步调用 -> Kizuna.prepare 激活输入或者什么都不干（交给具体实现考虑）
    
    ...
    
    等待 Kizuna.receiver 被赋值
        触发 -> Kizuna.doTell
            Kizuna.beforeTell 预处理输入 
            同步调用，但切换到 io 线程执行 -> Kizuna.getReaction
                同步调用，但切换到 main looper 所在线程（不是主线程） -> Kizuna.onReaction
                    完成一次 对话 
"""


class Kizuna(Manager, ABC):
    name = "Kizuna"

    def __init__(self):
        super().__init__(self.name)
        # setup mana source first ~
        self.__looper = Looper(self.name)
        self.__kHandler = Handler(self.__looper)
        self.__mainHandler = Handler(Looper.mainLooper())

        self.__receiver = LiveData(None)
        self.__receiver.observe(self.doTell, False)

        self.waifus: dict[str, Waifu] | None = None

        self.currentWaifu = None

        self.words = LiveData(None)

    def initialize(self, waifu: LiveData, wPos: LiveData, wSize: LiveData):
        self.doInitialize(wPos, wSize)
        self.waifus = Waifu.waifus()

        self.currentWaifu = waifu
        self.ruleBreak(waifu.value)

        tm = Manager.getManager(TextManager.name)
        self.words.observe(lambda v: tm.popup(self.currentWaifu.value.name, v, lock=True), False)

    @property
    def receiver(self):
        return self.__receiver

    def recall(self, mid):
        if self.currentWaifu.value is None:
            raise RuntimeError("no link established, call `ruleBreak` first!!!")

        self.currentWaifu.value.recall(mid)

    @abstractmethod
    def doInitialize(self, wPos: LiveData, wSize: LiveData):
        pass

    def ruleBreak(self, waifu):
        """create a connection ignoring the rule the real world"""
        self.currentWaifu.value = self.waifus[waifu.name]

    def tell(self):
        self.prepare()

    def doTell(self, words):
        name = self.currentWaifu.value.name
        words = self.beforeTell(words)
        waifu = self.waifus[name]
        waifu.tell(words)
        # 切换到io进程执行
        self.__kHandler.post(lambda: self.getReaction(waifu, words))

    @abstractmethod
    def beforeTell(self, words) -> str:
        pass

    def getReaction(self, waifu, words):
        words = self.doReaction(waifu, words)
        # ツンデレでしょう
        waifu.rethink(words)
        # 切换到主线程，执行一些回调
        # 主要是方便操作模型弹出对话框
        self.__mainHandler.post(lambda: self.onReaction(words))

    @abstractmethod
    def doReaction(self, waifu, words) -> str:
        pass

    @abstractmethod
    def onReaction(self, reaction: str):
        pass

    @abstractmethod
    def prepare(self) -> str:
        pass

    def suspend(self):
        for w in self.waifus.values():
            w.save()
        self.doSuspend()

    @abstractmethod
    def doSuspend(self):
        pass

from framework.handler.handler import Handler
from framework.handler.looper import Looper
from framework.handler.message import Message
from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.kizuna import Kizuna
from framework.runtime.core.kizuna.moment import Moment
from framework.runtime.drive.kizuna import qianfan_token
from framework.runtime.drive.kizuna.qianfan import Qianfan
from framework.runtime.drive.looper.looper_impl_tk import TkLooper
from framework.runtime.drive.window.kizuna_link_tk import TkKizunaLink
from framework.utils import log


class KizunaImpl(Kizuna):

    def __init__(self):
        super().__init__()
        self.anchorY = None
        self.anchorH = None
        self.anchorW = None
        self.anchorX = None
        self.qianfan: Qianfan | None = None
        self.__tkHandler: Handler | None = None
        self.__link: TkKizunaLink | None = None

        self.popupX = None
        self.popupY = None

    def doInitialize(self, wPos: LiveData, wSize: LiveData):
        self.__tkHandler = Handler(Looper.getLooper(TkLooper.name))
        self.__tkHandler.handle = self.__setLink
        msg = Message.obtain()
        msg.data = self.receiver
        self.__tkHandler.post(msg)

        self.qianfan = Qianfan(
            qianfan_token.API_KEY,
            qianfan_token.SECRET_KEY
        )

        wPos.observe(lambda v: self.adjustPopupPos(v, None))
        wSize.observe(lambda v: self.adjustPopupPos(None, v))

    def adjustPopupPos(self, wPos, wSize):
        if wPos:
            self.anchorX, self.anchorY = wPos
        if wSize:
            self.anchorW, self.anchorH = wSize

    def __setLink(self, link):
        self.__link = link

    def prepare(self):
        # 确保在 qt 线程中启动
        self.__tkHandler.post(
            lambda: self.__link.activate_from_thread(self.anchorX, self.anchorY, self.anchorW, self.anchorH))

    def beforeTell(self, words: str) -> str:
        return words.strip()

    def doReaction(self, waifu, words) -> str:
        """该函数将会在 io 线程 (kizuna looper) 中执行"""
        mm: Moment = waifu.currentMoment
        chara_settings = [
            {
                "role": "user",
                "content": waifu.desc,
            },
            {
                "role": "assistant",
                "content": waifu.greeting,
            },
        ]
        context = [
            {
                "role": "assistant" if h.fromWaifu else "user",
                "content": h.words,
            }
            for h in mm.hitokotos
        ]
        msg = self.qianfan.chat(
            chara_settings + context
        )
        log.Info(f"[{waifu.name}@kizuna] {msg}")
        return msg

    def onReaction(self, return_words: str):
        # live data trigger
        self.words.value = return_words
        # 处理完毕，可以继续输入
        self.__tkHandler.post(lambda: self.__link.enable())

    def doSuspend(self):
        # self.__tkHandler.post(lambda: Looper.getLooper(TkLooper.name).shutdown())
        pass

from abc import abstractmethod
from threading import Lock, Thread

from framework.handler.message import Message
from framework.handler.message_queue import MessageQueue


class Looper:
    __loopers = dict()
    __looperMapLock: Lock = Lock()

    def __init__(self, name: str, manualStart: bool = False):
        if name == "main" and not manualStart:
            raise RuntimeError("flag `manualStart` must be `True` for main looper!")
        self.__name = name

        self.mq = MessageQueue()
        with self.__looperMapLock:
            if self.__loopers.get(name, None) is not None:
                raise RuntimeError("duplicated looper name")
            self.__loopers[name] = self

        if not manualStart:
            self.__thread = Thread(None, self.loop, name, daemon=True)
            self.__thread.start()
        else:
            self.__thread = None

    def start(self, *args, **kwargs):
        self.__thread = Thread(None, self.loop, self.__name, args, kwargs, daemon=True)
        self.__thread.start()

    @abstractmethod
    def shutdown(self):
        pass

    def loop(self, *args, **kwargs):
        while True:
            msg = self.mq.getOrBlock()
            if msg.handle is not None:
                msg.handle(msg)

            msg.recycle()

    def post(self, msg: Message):
        self.mq.put(msg)

    @staticmethod
    def getLooper(name: str):
        return Looper.__loopers.get(name)

    @staticmethod
    def mainLooper():
        return Looper.getLooper("Main")

    @staticmethod
    def loopers():
        return tuple(Looper.__loopers.keys())

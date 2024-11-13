import time
from typing import Callable

from framework.handler.looper import Looper
from framework.handler.message import Message


class Handler:

    def __init__(self, looper: Looper = None):
        if looper is None:
            self.__looper = Looper.getLooper("main")
        else:
            self.__looper = looper
        self.__handle: Callable | None = None

    def post(self, obj: Message | Callable):
        self.__post(obj, 0)

    def postDelay(self, obj: Message | Callable[[Message], None], delay: float):
        self.__post(obj, delay)

    def __post(self, obj: Message | Callable[[Message], None], delay: float):
        if type(obj) == Message:
            obj.at = time.time() + delay
            obj.handle = self.__handle
            self.__looper.post(obj)
        elif callable(obj):
            msg = Message.obtain()
            msg.handle = lambda _: obj()
            msg.at = time.time() + delay
            self.__looper.post(msg)
        else:
            raise RuntimeError(f"invalid type {obj}")

    @property
    def handle(self):
        return self.__handle

    @handle.setter
    def handle(self, value: Callable | None):
        self.__handle = value

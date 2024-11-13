from logging import warning
from threading import Lock
from typing import Any, Callable


class Message:
    __availableMsgs = list()
    __lock: Lock = Lock()
    __maxCache: int = 10

    def __init__(self):
        self.what: int | None = None
        self.data: Any = None
        self.at: float = 0
        self.handle: Callable | None = None
        self.__obtained = False

    @staticmethod
    def obtain():
        with Message.__lock:
            if len(Message.__availableMsgs) <= 0:
                msg = Message()
                msg.__obtained = True
                return msg
            else:
                return Message.__availableMsgs.pop(0)

    def recycle(self):
        self.data = None
        self.handle = None
        self.at = 0
        self.what = 0

        with Message.__lock:
            if len(self.__availableMsgs) < self.__maxCache:
                if self not in self.__availableMsgs:
                    self.__availableMsgs.append(self)
                else:
                    warning("tried to recycle a message many times")

    def __str__(self):
        return f"Message(data={self.data}, handle={self.handle})"

import time
from threading import Lock, Event
from time import sleep

from framework.handler.message import Message


class MessageQueue:

    def __init__(self):
        self.__messages: list[Message] = list()
        self.__lock = Lock()
        self.__enqueued: Event = Event()

    def put(self, message: Message):
        with self.__lock:
            insert_pos = len(self.__messages)
            # 按 delay 升序插入
            for i, m in enumerate(self.__messages):
                if m.at > message.at:
                    insert_pos = i
                    break

            self.__messages.insert(insert_pos, message)
            self.__enqueued.set()

    def __len__(self):
        return len(self.__messages)

    def getOrBlock(self) -> Message:
        while True:
            with self.__lock:
                if len(self.__messages) > 0:
                    break
            self.__enqueued.wait()

        self.__enqueued.clear()
        t = time.time()
        if self.__messages[0].at > t:
            sleep(self.__messages[0].at - t)

        return self.__messages.pop(0)

    def get(self) -> Message | None:
        with self.__lock:
            if len(self.__messages) <= 0:
                return None

            t = time.time()
            if self.__messages[0].at > t:
                return None

            return self.__messages.pop(0)

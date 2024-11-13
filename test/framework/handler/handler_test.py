from threading import Thread
from time import sleep

from framework.handler.handler import Handler
from framework.handler.message import Message
from framework.handler.looper import Looper


def handle(m):
    print(f"\n===\n{m}\n===\n")


def task(i):
    if i > 5:
        msg = Message.obtain()
        msg.data = "live_data " + str(i)
        handler.postDelay(msg, 5)
    else:
        handler.post(lambda: handle(i))
    print(f"posted {i}")


if __name__ == '__main__':
    msg = Message.obtain()
    msg.recycle()
    print(msg)

    handler = Handler(Looper("wow"))

    message = Message.obtain()
    print(message)
    handler.handle = handle
    message.data = "hello"

    handler.post(message)

    msg = Message.obtain()
    msg.data = "delayed msg"
    print(msg)
    handler.postDelay(msg, 5)

    for i in range(10):
        t = Thread(None, task, "", (i,), daemon=True)
        t.start()

    sleep(10)

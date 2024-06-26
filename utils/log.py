import time
from app import settings, define


def info(msg: str):
    if settings.APP_MODE == define.AppMode.RELEASE:
        return

    print(
        time.strftime(
            f"[INFO  %Y-%m-%d %H:%M:%S] {msg}",
            time.localtime(time.time())))

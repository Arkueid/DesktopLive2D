import base64
from abc import ABC
from typing import Generator


class ChatResponse(ABC):
    KEY_SRC = "src"
    KEY_DST = "dst"
    KEY_TEXT = "text"
    KEY_AUDIO = "audio"

    __meta: dict

    def __init__(self, meta: dict):
        self.__meta = meta

    def meta(self) -> dict:
        return self.__meta

    def text(self) -> str | None:
        return self.__meta.get(self.KEY_TEXT, None)

    def audio(self) -> bytes | None:
        if self.__meta.get(self.KEY_AUDIO):
            return base64.b64decode(self.__meta[self.KEY_AUDIO])
        return None

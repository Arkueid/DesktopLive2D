from abc import abstractmethod, ABC
from typing import Any

import peewee

from chat.client.responses import ChatResponse
from chat.data.entity import Message, Character
from config import Configuration
from utils import log


class ChatClient(ABC):
    """
    大模型聊天接口类
    """
    name: str  # 名称
    messages: list[Any]  # 消息对话
    config: Configuration

    KEY_SRC: str
    KEY_CONTENT: str
    VALUE_USER: str
    VALUE_ASSISTANT: str

    def __init__(self, name: str, key_src: str, key_content: str):
        self.messages = list()
        self.name = name
        self.KEY_SRC = key_src
        self.KEY_CONTENT = key_content

    def setup(self, config: Configuration) -> None:
        self.config = config
        self.__loadConfig()
        self.config.chatId.valueChanged.connect(self.loadMessages)

    def __loadConfig(self):
        self.loadMessages(self.config.chatId.value)

    @abstractmethod
    def chat(self, text: str) -> ChatResponse:
        pass

    def getCharaSetting(self):
        charaSetting: Character | None = None
        try:
            charaSetting = Character.get_by_id(self.config.charaId.value)
        except Exception as e:
            log.info(f"failed to get chara setting: {e}, use default chara[toyama kasumi] instead.")

        ls = [
            {
                self.KEY_SRC: self.VALUE_USER,
                self.KEY_CONTENT: Character.DEFAULT_PROFILE if charaSetting is None else charaSetting.profile
            },
            {
                self.KEY_SRC: self.VALUE_ASSISTANT,
                self.KEY_CONTENT: Character.DEFAULT_GREETING if charaSetting is None else charaSetting.greeting
            }]
        return ls

    def loadMessages(self, chat_id: str):
        self.messages.clear()
        self.messages.extend([{self.KEY_SRC: i.src, self.KEY_CONTENT: i.text}
                             for i in Message.select().where(Message.chatId == chat_id)])


class ChatClientWithSQLite(ChatClient, ABC):
    pass

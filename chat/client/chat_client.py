from abc import abstractmethod, ABC

from chat.cache.database import Message
from chat.client.response import Response


class ChatClient(ABC):
    """
    大模型聊天接口类
    """
    user: str  # 用户名称
    assistant: str  # 聊天角色名称
    messages: list[any]  # 消息对话

    @abstractmethod
    def chat(self, text):
        """
        文本对话
        """
        pass


class ChatClientWithCache(ChatClient, ABC):
    """
    附带本地对话储存
    """

    def load(self):

        query = Message.select().where(Message.src in (self.user, self.assistant),
                                       Message.dst in (self.assistant, self.user))
        self.messages = [{'role': msg.src, 'content': msg.text} for msg in query]


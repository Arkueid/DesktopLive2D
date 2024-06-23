from abc import ABC, abstractmethod


class Response(ABC):
    """
    聊天回复类
    """

    @abstractmethod
    def text(self) -> str:
        """
        回复文本
        """
        pass

    @abstractmethod
    def sound(self) -> str:
        """
        回复语音
        """
        pass


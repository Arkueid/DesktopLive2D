from chat.client.chat_client import ChatClient
from chat.client.responses import ChatResponse
from config import Configuration


class ChatDelegate:
    chatClient: ChatClient

    def setup(self, config: Configuration, client: ChatClient):
        self.chatClient = client
        self.chatClient.setup(config)

    def chat(self, msg: str, callback: callable):
        response: ChatResponse = self.chatClient.chat(msg)
        callback(response.text(), response.audio())

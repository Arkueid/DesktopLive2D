from chat.client.chat_client import ChatClient
from chat.client.response import Response


class ChatDelegate:
    chatClient: ChatClient

    def setup(self, client: ChatClient):
        self.chatClient = client

    def chat(self, msg: str, callback: callable):
        response: Response = self.chatClient.chat(msg)
        callback(response.text(), response.sound())

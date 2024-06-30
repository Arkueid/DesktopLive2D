import json
import os.path
import time

import requests

from chat.client.chat_client import ChatClientWithSQLite
from chat.client.responses import ChatResponse
from chat.data.entity import Message
from utils import log


class Qianfan(ChatClientWithSQLite):
    API_KEY: str
    SECRET_KEY: str
    KEY_SRC = "role"
    KEY_CONTENT = "content"

    MODEL: str = "ERNIE Speed-AppBuilder"
    API: str = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ai_apaas"
    VALUE_USER = "user"
    VALUE_ASSISTANT = "assistant"
    access_token: str = ""
    expire_at: int = 0

    def __init__(self, apiKey: str, secretKey: str):
        super().__init__("qianfan", "role", "content")
        self.API_KEY = apiKey
        self.SECRET_KEY = secretKey

    def chat(self, text):
        Message.create(chatId=self.config.chatId.value, dst=self.VALUE_ASSISTANT, src=self.VALUE_USER, text=text)
        self.messages.append({
            "role": self.VALUE_USER,
            "content": text
        })

        try:
            res = self.__baidu_api()
        except Exception as e:
            res = str(e)

        self.messages.append({
            'role': self.VALUE_ASSISTANT,
            'content': res
        })
        Message.create(chatId=self.config.chatId.value, src=self.VALUE_ASSISTANT, dst=self.VALUE_USER, text=res)

        return ChatResponse({'text': res})

    def __baidu_api(self):
        if not self.expire_at or time.time() > self.expire_at:
            self.get_access_token()

        url = f"{self.API}?access_token={self.access_token}"
        payload = {
            "messages": self.getCharaSetting() + self.messages,
            "temperature": 0.95,
            "top_p": 0.7,
            "penalty_score": 1
        }
        headers = {
            "ContentType": "application/json"
        }
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        return res.json().get('result', str(res.json()))

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        log.info("refresh access token")
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        x = requests.post(url, params=params).json()
        self.access_token = x.get('access_token')
        self.expire_at = time.time() + x.get('expires_in')
        self.save_token()

    def loadMessages(self, chat_id: str):
        access_token_path = 'access_token.baidu.json'

        if os.path.exists(access_token_path):
            with open(access_token_path, 'r', encoding='utf-8') as f:
                x = json.loads(f.read())
                self.access_token = x.get('access_token')
                self.expire_at = x.get('expire_at')

        return super().loadMessages(chat_id)

    def save_token(self):
        with open(f'access_token.baidu.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                'access_token': self.access_token,
                'expire_at': self.expire_at
            }, ensure_ascii=False))

import json
import os.path
import time

import requests

from chat.cache.database import Message
from chat.client.chat_client import ChatClientWithCache
from chat.client.response import Response
from utils import log


class Qianfan(ChatClientWithCache):
    class Response(Response):
        _text: str

        def __init__(self, text: str):
            self._text = text

        def sound(self) -> None:
            return None

        def text(self) -> str:
            return self._text

    API_KEY: str
    SECRET_KEY: str
    MODEL: str
    API: str

    user = "user"
    assistant = "assistant"
    access_token: str = ""
    expire_at: int = 0

    def __init__(self, apiKey: str, secretKey: str, model: str):
        self.API_KEY = apiKey
        self.SECRET_KEY = secretKey
        self.MODEL = model
        self.API = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ai_apaas"
        self.messages = list()

    def chat(self, text):
        Message.create(dst=self.assistant, src=self.user, text=text)

        try:
            res = self.__baidu_api(text)
        except Exception as e:
            res = str(e)

        self.messages.append({
            'role': self.assistant,
            'content': text
        })
        Message.create(src=self.assistant, dst=self.user, text=res)
        return self.Response(res)

    def __baidu_api(self, text):
        if not self.expire_at or time.time() > self.expire_at:
            self.get_access_token()

        url = f"{self.API}?access_token={self.access_token}"
        self.messages.append({
            "role": self.user,
            "content": text
        })
        payload = {
            "messages": self.messages,
            "temperature": 0.95,
            "top_p": 0.7,
            "penalty_score": 1
        }
        headers = {
            "ContentType": "application/json"
        }
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        return res.json().get('result')

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

    def load(self):
        super().load()
        access_token_path = 'access_token.json'

        if not os.path.exists(access_token_path):
            return

        with open(access_token_path, 'r', encoding='utf-8') as f:
            x = json.loads(f.read())
            self.access_token = x.get('access_token')
            self.expire_at = x.get('expire_at')

    def save_token(self):
        with open(f'access_token.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                'access_token': self.access_token,
                'expire_at': self.expire_at
            }, ensure_ascii=False))





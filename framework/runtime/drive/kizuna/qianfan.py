import json
import os.path
import time

import requests


class Qianfan:
    KEY_SRC = "role"
    KEY_CONTENT = "content"

    MODEL: str = "ERNIE Speed-AppBuilder"
    API: str = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ai_apaas"
    VALUE_USER = "user"
    VALUE_ASSISTANT = "assistant"

    def __init__(self, apiKey: str, secretKey: str):
        self.messages = None
        self.API_KEY = apiKey
        self.SECRET_KEY = secretKey
        self.access_token = ""
        self.expire_at: int = 0
        self.loadToken()

    def chat(self, messages):

        try:
            res = self.__baidu_api(messages)
        except Exception as e:
            res = str(e)

        return res

    def __baidu_api(self, messages):
        if not self.expire_at or time.time() > self.expire_at:
            self.get_access_token()

        url = f"{self.API}?access_token={self.access_token}"
        payload = {
            "messages": messages,
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
        print("refresh access token")
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        x = requests.post(url, params=params).json()
        self.access_token = x.get('access_token')
        self.expire_at = time.time() + x.get('expires_in')
        self.save_token()

    def loadToken(self):
        access_token_path = 'access_token.baidu.json'

        if os.path.exists(access_token_path):
            with open(access_token_path, 'r', encoding='utf-8') as f:
                x = json.loads(f.read())
                self.access_token = x.get('access_token')
                self.expire_at = x.get('expire_at')

    def save_token(self):
        with open(f'access_token.baidu.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                'access_token': self.access_token,
                'expire_at': self.expire_at
            }, ensure_ascii=False))

from moocxing.plugins.sdk.AbstractPlugin import AbstractPlugin
from moocxing.robot import Config

import requests
import json
import logging

log = logging.getLogger(__name__)


class Plugin(AbstractPlugin):
    SLUG = "chat"

    def __init__(self):
        super().__init__()
        self.result = ""
        self.type = ""

    # 执行
    def handle(self, query):
        if Config.get("chat/naixing/isUse") and query != "":
            self.type = "naixing"

            url = "https://api.naixing.vip/anonymous/wordManage/answers/"

            data = {"question": "", "robotId": 0, "deviceId": ""}
            data["robotId"] = Config.get("chat/naixing/robotId")
            data["question"] = query.replace("chat", "")

            info = requests.post(url=url, json=data).json()
            data["deviceId"] = info["data"]["deviceId"]

            self.result = info['data']['answers']

        elif Config.get("chat/qianfan/isUse") and query != "":
            self.type = "qianfan"

            API_KEY = Config.get("chat/qianfan/API_KEY")
            SECRET_KEY = Config.get("chat/qianfan/SECRET_KEY")
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

            url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
            access_token = requests.request("POST", url, headers=headers).json().get("access_token")

            url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={access_token}"
            payload = json.dumps({"messages": [{"role": "user", "content": query.replace("chat", "")}]})
            response = requests.request("POST", url, headers=headers, data=payload)
            self.result = response.json()['result']

        elif Config.get("chat/chatgpt/isUse") and query != "":
            self.type = "chatgpt"

            url = "https://api.openai.com/v1/chat/completions"
            payload = json.dumps({"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": query.replace("chat", "")}]})
            headers = {
                'Authorization': f'Bearer {Config.get("chat/chatgpt/SECRET_KEY")}',
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            self.result = response.json()['choices'][0]['message']['content']

        log.info(f"{self.type} answers: {self.result}")
        self.say(self.result)

    def isValid(self, query):
        keyword = "chat"
        return keyword in query

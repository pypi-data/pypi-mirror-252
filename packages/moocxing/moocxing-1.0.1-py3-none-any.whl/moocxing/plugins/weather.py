import requests
from moocxing.plugins.sdk.AbstractPlugin import AbstractPlugin
from moocxing.robot import Config


class Plugin(AbstractPlugin):
    SLUG = "weather"

    def handle(self, query):
        city = self.nlp.getCity(query)
        if city is None:
            city = Config.get('heweather/city')

        url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={Config.get('heweather/key')}"
        city_id = requests.get(url).json()['location'][0]['id']
        url = f"https://devapi.qweather.com/v7/weather/3d?location={city_id}&key={Config.get('heweather/key')}"
        info = requests.get(url).json()
        try:
            nowInfo = info["daily"][0]

            textDay = nowInfo["textDay"]
            tempMin = nowInfo["tempMin"]
            tempMax = nowInfo["tempMax"]
            windDirDay = nowInfo["windDirDay"]
            windSpeedDay = nowInfo["windSpeedDay"]
            humidity = nowInfo["humidity"]
            vis = nowInfo["vis"]

            print(f"今天{city}的天气状况{textDay},最低温度{tempMin},最高温度{tempMax},风向{windDirDay},风速{windSpeedDay}公里/小时,湿度百分之{humidity},能见度{vis}公里")
            self.say(f"今天{city}的天气状况{textDay},最低温度{tempMin},最高温度{tempMax},风向{windDirDay},风速{windSpeedDay}公里/小时,湿度百分之{humidity},能见度{vis}公里")
        except:
            return "没有查到%s的天气" % city

    def isValid(self, query):
        return "天气" in query

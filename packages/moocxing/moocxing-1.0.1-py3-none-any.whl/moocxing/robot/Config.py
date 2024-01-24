from moocxing.robot import Constants
from moocxing.robot.utils import yamlUtils
import logging

log = logging.getLogger(__name__)

# 创建 临时文件 文件夹
yamlUtils.mkdir(Constants.PATH_TEMP)
# 创建 技能插件 文件夹
yamlUtils.mkdir(Constants.PATH_CUSTOM_PLUGIN)

DEFAULT = {
    "logger": {
        "level": 20
    },
    "media": {
        "isUse": False,
    },
    "pinyin": {
        "isUse": False,
    },
    "minecraft": {
        "isUse": False,
        "host": "localhost",
        "post": 4711,
    },
    "mqtt": {
        "isUse": False,
        "host": "mqtt.16302.com",
        "post": 1883,
    },
    "serial": {
        "isUse": False,
        "bps": 9600,
        "com": "",
    },
    "speech": {
        "isUse": False,
        "APP_ID": "25496064",
        "API_KEY": "A6fXM6nA1B8GY2txDIUCXYyu",
        "SECRET_KEY": "4qb3jX1C8ue1rhwMkp27kzmrxLTli9G8",
    },
    "nlp": {
        "isUse": False,
        "API_KEY": "A6fXM6nA1B8GY2txDIUCXYyu",
        "SECRET_KEY": "4qb3jX1C8ue1rhwMkp27kzmrxLTli9G8",
    },
    "heweather": {
        "isUse": False,
        "city": "上海",
        "key": "3bffba48276c408b9107e275a51f111e",
    },
    "netease": {
        "isUse": False,
        "baseUrl": "http://sliot.top:3000",
    },
    "chat": {
        "naixing": {
            "isUse": False,
            "robotId": 4595,
        },
        "qianfan": {
            "isUse": False,
            "API_KEY": "afwfK19AwedxCBpdaFnIqbOg",
            "SECRET_KEY": "GGyg3CRdUvkSMnmOHuDm28wGZi048hD9"
        },
        "chatgpt": {
            "isUse": False,
            "SECRET_KEY": "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"
        },
    }
}

# 创建配置文件，并写入默认配置
yamlUtils.writeYaml(Constants.PATH_CONFIG_YAML, DEFAULT)


def comments(config):
    config['logger'].yaml_add_eol_comment(
        "日志等级，等级越低越详细 / FATAL = CRITICAL = CRITICAL = 50 / ERROR = 40 / WARN = WARNING = 30 / INFO = 20 / DEBUG = 10 / NOTSET = 0", column=0)
    config['minecraft'].yaml_add_eol_comment("我的世界配置项 / isUse: 是否启用(bool) / host: 服务器地址 / post: 服务器端口", column=0)
    config['mqtt'].yaml_add_eol_comment("MQTT配置项 / isUse: 是否启用(bool) / host: 服务器地址 / post: 服务器端口", column=0)
    config['serial'].yaml_add_eol_comment("串口配置项 / isUse: 是否启用(bool) / bps: 波特率 / com: 串口号（缺省时，默认选择最后一个串口）", column=0)
    config['speech'].yaml_add_eol_comment("百度语音api / isUse: 是否启用(bool)", column=0)
    config['nlp'].yaml_add_eol_comment("百度自然语言api / isUse: 是否启用(bool)", column=0)
    config['heweather'].yaml_add_eol_comment("和风天气配置项 / isUse: 是否启用(bool) / city: 城市地名 / key: 密钥", column=0)
    config['netease'].yaml_add_eol_comment("网易云音乐配置项 / isUse: 是否启用(bool) / baseUrl: 网易云音乐API地址", column=0)
    config['chat'].yaml_add_eol_comment("知识库配置项 / isUse: 是否启用(bool) 只能启用一个 / robotId: 氖星ID", column=0)
    config['media'].yaml_add_eol_comment("媒体模块配置项(播放录音)需要手动安装Pyaudio库 / isUse: 是否启用(bool)", column=0)
    config['pinyin'].yaml_add_eol_comment("拼音转换配置项 / isUse: 是否启用(bool)", column=0)


# 添加注释
yamlUtils.addComments(Constants.PATH_CONFIG_YAML, comments)

allConfig = yamlUtils.readYaml(Constants.PATH_CONFIG_YAML)


# 获取配置
def get(items):
    global item
    config = allConfig

    for item in items.split("/"):
        if isinstance(config, dict):
            config = config.get(item)
        elif isinstance(config, list):
            if len(config) > int(item):
                config = config[int(item)]

    if config is None and item != "isUse":
        log.warning(f"--- {items} 参数不存在")
    return config

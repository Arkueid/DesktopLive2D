from app.define import AppMode, Live2DVersion
from chat.client.baidu.qianfan import Qianfan
from chat.client.chat_client import ChatClient

APP_MODE = AppMode.DEBUG

LIVE2D_VERSION = Live2DVersion.V2

if LIVE2D_VERSION == Live2DVersion.V3:
    MODEL_JSON_SUFFIX = ".model3.json"
    CONFIG_PATH = "./config.v3.json"
elif LIVE2D_VERSION == Live2DVersion.V2:
    MODEL_JSON_SUFFIX = ".model.json"
    CONFIG_PATH = "./config.v2.json"
else:
    raise Exception("Unknown live2d version: %s", LIVE2D_VERSION)

API_KEY = "uDTLTDFxtJZSTt93RlZsZupC"
SECRET_KEY = "iOL7AdZldfwJVbCQ2hVrggrnIM5fS8RW"

CHAT_CLIENT: ChatClient = Qianfan(
    API_KEY, SECRET_KEY, "ERNIE Speed-AppBuilder"
)

CHAT_CLIENT.load()


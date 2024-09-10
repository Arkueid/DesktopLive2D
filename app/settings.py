from app.define import AppMode, Live2DVersion

APP_MODE = AppMode.DEBUG

LIVE2D_VERSION = Live2DVersion.V3

API_KEY = "uDTLTDFxtJZSTt93RlZsZupC"
SECRET_KEY = "iOL7AdZldfwJVbCQ2hVrggrnIM5fS8RW"

if LIVE2D_VERSION == Live2DVersion.V3:
    MODEL_JSON_SUFFIX = ".model3.json"
    CONFIG_PATH = "./config.v3.json"
elif LIVE2D_VERSION == Live2DVersion.V2:
    MODEL_JSON_SUFFIX = ".model.json"
    CONFIG_PATH = "./config.v2.json"
else:
    raise Exception("Unknown live2d version: %s", LIVE2D_VERSION)

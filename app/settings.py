from app.define import AppMode, Live2DVersion

APP_MODE = AppMode.DEBUG

LIVE2D_VERSION = Live2DVersion.V3

if LIVE2D_VERSION == Live2DVersion.V3:
    MODEL_JSON_SUFFIX = ".model3.json"
    CONFIG_PATH = "./config.v3.json"
elif LIVE2D_VERSION == Live2DVersion.V2:
    MODEL_JSON_SUFFIX = ".model.json"
    CONFIG_PATH = "./config.v2.json"
else:
    raise Exception("Unknown live2d version: %s", LIVE2D_VERSION)

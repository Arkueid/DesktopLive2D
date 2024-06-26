from . import settings, define

if settings.LIVE2D_VERSION == define.Live2DVersion.V3:
    import live2d.v3 as live2d
elif settings.LIVE2D_VERSION == define.Live2DVersion.V2:
    import live2d.v2 as live2d
else:
    raise Exception("Unknown live2d version: %s", settings.LIVE2D_VERSION)

if settings.APP_MODE == define.AppMode.DEBUG:
    live2d.setLogEnable(True)
elif settings.APP_MODE == define.AppMode.RELEASE:
    live2d.setLogEnable(False)
else:
    raise Exception("Unknown app mode: %s", settings.APP_MODE)

settings.CHAT_CLIENT.load()

__all__ = ['live2d', 'settings', 'define']

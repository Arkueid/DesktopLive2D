from framework.runtime.app_config import Configuration
from framework.constant import Live2DVersion

if __name__ == '__main__':
    appConfig = Configuration()
    appConfig.save("runtime.json")

    appConfig.load("runtime.json")
    print(appConfig.modelInfo)
    print(appConfig.windowSize)
    print(appConfig.windowPos)

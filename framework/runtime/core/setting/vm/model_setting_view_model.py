from framework.live_data.live_data import LiveData
from framework.utils.model_json import MotionGroup, Motion


class ModelSettingViewModel:

    def __init__(self, model_info: LiveData):
        self.__currentModelInfo = model_info
        self.__modelInfoList = model_info.value.mm.modelInfoList
        self.__modelNameList = [i.name for i in self.__modelInfoList]
        self.__currentMotionGroups = LiveData(self.__currentModelInfo.value.modelJson.motion_groups())

    @property
    def modelNames(self) -> list[str]:
        return self.__modelNameList

    @property
    def currentModelName(self) -> str:
        return self.__currentModelInfo.value.name

    @property
    def currentMotionGroups(self) -> LiveData:
        return self.__currentMotionGroups

    def changeModel(self, name: str):
        self.__currentModelInfo.value = self.__modelInfoList[self.__modelNameList.index(name)]
        self.__currentMotionGroups.value = self.__currentModelInfo.value.modelJson.motion_groups()

    def startMotion(self, group, no):
        self.__currentModelInfo.value.mm.startMotion(group, no, 3)

    def newMotionGroup(self, name):
        self.__currentMotionGroups.value.add(name, MotionGroup(self.__currentModelInfo.value.version))

    def removeMotionGroup(self, name):
        self.__currentMotionGroups.value.remove(name)

    def addMotion(self, group, file, sound, text):
        keys = self.__currentModelInfo.value.modelJson.keys
        self.__currentMotionGroups.value.group(group).add(Motion(self.__currentModelInfo.value.version, {
            keys.FILE: file,
            keys.SOUND: sound,
            keys.TEXT: text
        }))

    def removeMotion(self, group, no):
        self.__currentMotionGroups.value.group(group).pop(no)

    def setMotionFile(self, group, no, file):
        self.__currentMotionGroups.value.group(group).motion(no).set_file(file)

    def setMotionSound(self, group, no, sound):
        self.__currentMotionGroups.value.group(group).motion(no).set_sound(sound)

    def setMotionText(self, group, no, text):
        self.__currentMotionGroups.value.group(group).motion(no).set_text(text)

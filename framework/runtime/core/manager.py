from threading import Lock


class Manager:
    __managers = dict()
    __lock = Lock()

    def __init__(self, name: str):
        with self.__lock:
            if self.__managers.get(name, None) is not None:
                raise RuntimeError(f"duplicated manager `{name}`")

            self.__managers[name] = self

    @staticmethod
    def getManager(name: str):
        return Manager.__managers.get(name)

from typing import Any, Callable

from framework.handler.handler import Handler


class LiveData:

    def __init__(self, value: Any):
        self.__value: Any = value
        self.__observers: list[Callable] = list()
        self.__handler = None

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v
        # TODO: make it thread safe if necessary ... well, not now
        self.__onUpdate(self.__value)

    def observeOn(self, looper):
        if self.__handler:
            del self.__handler

        self.__handler = Handler(looper)

    def __str__(self):
        return f"LiveData({self.__value})"

    def observe(self, callback: Callable, updateNow=True):
        if not callable(callback):
            raise RuntimeError(f"invalid param type {type(callback)}")

        if callback not in self.__observers:
            self.__observers.append(callback)
            if updateNow:
                self.__call(callback, self.__value)

    def unobserve(self, callback: Callable):
        if callback in self.__observers:
            self.__observers.remove(callback)

    def __call(self, f, value):
        if self.__handler:
            self.__handler.post(lambda: f(value))
        else:
            f(value)

    def __onUpdate(self, value: Any):
        for f in self.__observers:
            self.__call(f, value)


class RangeLiveData(LiveData):

    def __init__(self, liveData: LiveData, vRange):
        super().__init__(None)
        self.liveData = liveData
        self.range = vRange

    @property
    def value(self):
        return self.liveData.value

    @value.setter
    def value(self, v):
        self.liveData.value = v


class BiasRangeLiveData(RangeLiveData):

    def __init__(self, liveData: LiveData, vRange, bias):
        super().__init__(liveData, vRange)
        self.bias = bias

    @property
    def value(self):
        return self.liveData.value[self.bias]

    @value.setter
    def value(self, v):
        old = list(self.liveData.value)
        old[self.bias] = v
        self.liveData.value = tuple(old)

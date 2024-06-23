class Lockable:
    _locked: bool

    def __init__(self):
        self._locked = False

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def isLocked(self) -> bool:
        return self._locked

    @staticmethod
    def lock_decor(func):
        def wrapper(self: Lockable, *args, **kwargs):
            if self.isLocked():
                return
            return func(self, *args, **kwargs)

        return wrapper

from abc import ABC, abstractmethod


class Application(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @staticmethod
    def launch(app):
        app.initialize()
        app.start()

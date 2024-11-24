import os

from PySide6.QtGui import QIcon


class IconDesign:

    def __init__(self):
        self.resource_dir = None

    def icon(self, path):
        return QIcon(str(os.path.join(self.resource_dir.rsplit("/", maxsplit=1)[0], path)))

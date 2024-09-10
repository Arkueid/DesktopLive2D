import os
from PySide6.QtGui import QIcon


class IconDesign:
    resource_dir: str

    def icon(self, path):
        return QIcon(os.path.join(self.resource_dir.rsplit("/", maxsplit=1)[0], path))

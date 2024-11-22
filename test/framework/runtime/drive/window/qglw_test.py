import threading
import time

from PySide6.QtWidgets import QApplication

import live2d.v3 as live2d
from temp.qglw import QGLW


def task(win):
    model = live2d.LAppModel()
    model.LoadModelJson(r"D:\forDesktop\live2d-desktop\Resources\v3\nn\nn.model3.json")

    while True:
        live2d.clearBuffer()
        model.Update()
        model.Draw()
        time.sleep(1 / 60)


if __name__ == '__main__':
    live2d.init()
    app = QApplication()

    win = QGLW()

    win.show()

    threading.Thread(None, task, "ok", (win, ), daemon=True).start()

    app.exec()
    live2d.dispose()

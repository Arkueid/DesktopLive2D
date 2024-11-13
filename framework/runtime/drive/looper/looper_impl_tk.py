import tkinter as tk

from framework.runtime.drive.window.gal_dialog import GalDialog
from framework.handler.looper import Looper


class TkLooper(Looper):
    """
    引导 tkinter 启动
    """
    name = "tkinter"

    def __init__(self):
        super().__init__(self.name, True)
        self.root: tk.Tk | None = None

    def shutdown(self):
        self.root.quit()

    def handleMessage(self):
        msg = self.mq.get()
        if msg is not None:
            print(msg)
            if msg.handle:
                msg.handle(msg)

            msg.recycle()

        self.root.after(100, self.handleMessage)

    def loop(self, *args, **kwargs):
        root = tk.Tk()
        self.root = root
        root.withdraw()

        # 等待 dialog 初始化
        dialog_init_msg = self.mq.getOrBlock()
        dialog = GalDialog(root)
        dialog_init_msg.handle(dialog)
        dialog_init_msg.recycle()

        root.after(100, self.handleMessage)

        root.mainloop()

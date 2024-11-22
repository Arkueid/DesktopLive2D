import tkinter as tk

from framework.runtime.drive.window.gal_dialog_tk import TkGalDialog
from framework.handler.looper import Looper
from framework.runtime.drive.window.kizuna_link_tk import TkKizunaLink
from framework.utils import log


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
            if msg.handle:
                msg.handle(msg)

            msg.recycle()

        self.root.after(100, self.handleMessage)

    def loop(self, *args, **kwargs):
        self.root = tk.Tk()
        root = self.root
        root.withdraw()

        # 等待 kizuna 初始化
        kzn_init_msg = self.mq.getOrBlock()
        link = TkKizunaLink(root)
        link.hide()
        link.receiver = kzn_init_msg.data
        kzn_init_msg.handle(link)
        kzn_init_msg.recycle()

        log.Info("[TkLooper] kizuna link init")

        # 等待 text manager 初始化
        tm_init_msg = self.mq.getOrBlock()
        dialog = TkGalDialog(root)
        tm_init_msg.handle(dialog)
        tm_init_msg.recycle()

        log.Info("[TkLooper] dialog init")

        root.after(100, self.handleMessage)

        root.mainloop()

        log.Info("[TkLooper] shutdown")

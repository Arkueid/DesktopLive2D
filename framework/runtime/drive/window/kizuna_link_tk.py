import tkinter as tk
from tkinter import ttk


class KizunaLinkView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.hbox = tk.Frame(self, bg="white")
        self.hbox.pack(fill=tk.X, padx=5, pady=5)

        # 创建输入框
        self.lineEdit = ttk.Entry(self.hbox, width=25)
        self.lineEdit.pack(side=tk.LEFT, padx=1, pady=1, fill=tk.X, expand=True)

        # 创建发送按钮 (紧凑型)
        self.sendBtn = ttk.Button(self.hbox, text="Send", width=8, padding=(5, 2))
        self.sendBtn.pack(side=tk.LEFT, padx=2, pady=2)

        # 创建关闭按钮 (紧凑型)
        self.closeBtn = ttk.Button(self.hbox, text="Close", width=8, padding=(5, 2))
        self.closeBtn.pack(side=tk.LEFT, padx=2, pady=2)


class TkKizunaLink(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # 设置无边框、圆角和半透明背景
        self.overrideredirect(True)  # 去掉边框
        self.attributes("-topmost", True)  # 窗口置顶
        self.attributes("-alpha", 0.9)  # 半透明，0.0（全透明）到1.0（不透明）

        # 初始化视图
        self.view = KizunaLinkView(self)
        self.view.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # 拖动窗口功能
        self._offsetX = 0
        self._offsetY = 0
        self.bind("<Button-1>", self._start_move)
        self.bind("<B1-Motion>", self._do_move)
        self.bind("<Return>", self.__sendMsg)
        # 关闭按钮行为
        self.view.closeBtn.config(command=self.hide)
        self.view.sendBtn.config(command=self.__sendMsg)

        self.receiver = None

    def _start_move(self, event):
        self._offsetX = event.x
        self._offsetY = event.y

    def _do_move(self, event):
        x = self.winfo_x() + (event.x - self._offsetX)
        y = self.winfo_y() + (event.y - self._offsetY)
        self.geometry(f"+{x}+{y}")

    def activate_from_thread(self, x, y, w, h):
        # 设置弹窗的位置
        self.geometry(f"+{x + w // 2 - self.winfo_width() // 2}+{y + h + 10}")
        self.deiconify()  # 显示窗口

    def hide(self):
        self.withdraw()  # 隐藏窗口

    def enable(self):
        self.view.lineEdit.config(state=tk.NORMAL)
        self.view.sendBtn.config(state=tk.NORMAL)

        self.view.lineEdit.delete(0, tk.END)

    def disable(self):
        self.view.lineEdit.config(state=tk.DISABLED)
        self.view.sendBtn.config(state=tk.DISABLED)

    def __sendMsg(self, event=None):
        txt = self.view.lineEdit.get()
        if len(txt) > 0 and self.receiver:
            self.receiver.value = txt
            self.disable()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    kizuna_link = TkKizunaLink(root)
    kizuna_link.activate_from_thread(100, 100, 200, 100)  # 示例使用

    root.mainloop()

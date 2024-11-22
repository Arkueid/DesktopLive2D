import tkinter as tk


class TkGalDialog:
    MAX_WIDTH = 400

    def __init__(self, root, bg_color="#000000", opacity=0.8, max_width=MAX_WIDTH, font=("Arial", 14)):
        self.root = root
        self.dialog = None
        self.text_var = tk.StringVar()
        self.bg_color = bg_color
        self.opacity = opacity
        self.max_width = max_width
        self.font = font
        self.locked = False

    def __calculate_text_size(self, text):
        temp_label = tk.Label(self.root, text=text, font=self.font, wraplength=self.max_width)
        temp_label.pack()
        self.root.update_idletasks()
        height = temp_label.winfo_reqheight() + 20
        temp_label.destroy()
        return self.max_width, height

    def __show(self, text, x, y, w, h, duration):
        if self.dialog:
            self.dialog.destroy()

        # 根据文本内容调整窗口大小
        width, height = self.__calculate_text_size(text)

        self.dialog = tk.Toplevel(self.root)
        self.dialog.geometry(f"{width}x{height}")
        # 无边框
        self.dialog.overrideredirect(True)
        # 半透明
        self.dialog.wm_attributes("-alpha", self.opacity)
        # 置顶
        self.dialog.wm_attributes("-topmost", True)
        self.dialog.geometry(f"+{x + w // 2 - width // 2}+{y + h // 2}")

        canvas = tk.Canvas(self.dialog, width=width, height=height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # 背景
        canvas.create_rectangle(0, 0, width, height, fill=self.bg_color, outline=self.bg_color)

        # 显示文本在半透明背景图片之上，居中对齐
        self.text_id = canvas.create_text(width // 2, height // 2, text="", font=self.font, fill="white",
                                          width=width - 20, anchor="center", justify='center')
        self.current_text = text
        self.text_index = 0
        self.duration = duration

        # 双击关闭事件
        self.dialog.bind("<Double-Button-1>", lambda e: self.__stop())

        # 逐字显示文本
        self.dialog.after(100, self.__update_text)

    def __update_text(self):
        if self.text_index < len(self.current_text):
            self.text_index += 1
            text_to_display = self.current_text[:self.text_index]
            canvas = self.dialog.children['!canvas']
            canvas.itemconfig(self.text_id, text=text_to_display)
            self.dialog.after(100, self.__update_text)
        else:
            # 播放结束后延迟关闭
            self.dialog.after(self.duration * 1000, self.__stop)
            self.locked = False

    def __stop(self):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

    def trigger_from_thread(self, text, x, y, w, h, duration=2, lock=False):
        if self.locked:
            return
        self.locked = lock
        self.root.after(0, lambda: self.__show(text, x, y, w, h, duration))

    def move_from_thread(self, x, y, w, h):
        self.root.after(0, lambda: self.__doMove(x, y, w, h))

    def __doMove(self, x, y, w, h):
        if self.dialog:
            self.dialog.geometry(f"+{x + w // 2 - self.max_width // 2}+{y + h // 2}")

    def isVisible(self):
        return self.dialog is not None and self.dialog.winfo_exists()

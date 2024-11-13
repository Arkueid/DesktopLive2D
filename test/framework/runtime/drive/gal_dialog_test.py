import threading
import time
import tkinter as tk

from framework.runtime.drive.window.gal_dialog import GalDialog


def thread_function(dialog):
    time.sleep(2)
    dialog.trigger_from_thread("这是来自线程的第一条消息！窗口宽度固定，高度随文本内容调整", 200, 200)

    time.sleep(7)
    dialog.trigger_from_thread("这是第二条消息，自动关闭后再次触发！测试窗口重新显示并调整大小以适应不同长度的文本内容。",
                               500, 500)
    time.sleep(2)
    dialog.move_from_thread(800, 500)


def main():
    root = tk.Tk()
    root.withdraw()

    # 初始化对话框，传入背景颜色和透明度
    dialog = GalDialog(root, bg_color="black")

    # 启动线程模拟外部事件触发
    threading.Thread(target=thread_function, args=(dialog,), daemon=True).start()

    root.mainloop()


if __name__ == "__main__":
    main()
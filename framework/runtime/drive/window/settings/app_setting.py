import tkinter as tk
from tkinter import ttk


class AppSettingView:
    def __init__(self, notebook, viewModel):
        self.viewModel = viewModel

        # 创建一个新 Tab
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="App Settings")

        # 创建控件容器
        self.frame = ttk.Frame(self.tab)
        self.frame.pack(fill=tk.Y, expand=True, padx=10, pady=10)

        # 添加控件
        self.add_labeled_entry("Window Width", viewModel.getWindowWidth, viewModel.setWindowWidth, (0, 65535), 0)
        self.add_labeled_entry("Window Height", viewModel.getWindowHeight, viewModel.setWindowHeight, (0, 65535), 1)
        self.add_labeled_entry("Draw X", viewModel.getDrawX, viewModel.setDrawX, (-2.0, 2.0), 2)
        self.add_labeled_entry("Draw Y", viewModel.getDrawY, viewModel.setDrawY, (-2.0, 2.0), 3)
        self.add_labeled_entry("Scale", viewModel.getScale, viewModel.setScale, (0.01, 65535), 4)
        self.add_labeled_entry("FPS", viewModel.getFps, viewModel.setFps, (30, 120), 5)
        self.add_labeled_entry("Motion Interval", viewModel.getMotionInterval, viewModel.setMotionInterval, (-1, 65535),
                               6)
        self.add_labeled_entry("Lip Sync N", viewModel.getLipSyncN, viewModel.setLipSyncN, (0, 65535), 7)
        self.add_labeled_entry("Volume", viewModel.getVolume, viewModel.setVolume, (0, 100), 8)

        ttk.Button(self.frame, text="Apply").grid(row=9, column=0, columnspan=2, pady=10)

    def add_labeled_entry(self, label_text, getter, setter, value_range, row):
        """创建一个标签 + 输入框的控件组合"""
        ttk.Label(self.frame, text=label_text).grid(row=row, column=0, pady=5)

        entry_var = tk.StringVar()
        entry_var.set(str(getter()))

        def validate_input(new_value):
            try:
                value = float(new_value) if '.' in new_value else int(new_value)
                if value_range[0] <= value <= value_range[1]:
                    setter(value)
                    return True
                else:
                    return False
            except ValueError:
                return False

        def on_invalid_input():
            entry_var.set(str(getter()))

        validate_cmd = self.frame.register(validate_input)
        invalid_cmd = self.frame.register(on_invalid_input)

        entry = ttk.Entry(
            self.frame,
            textvariable=entry_var,
            validate="focusout",
            validatecommand=(validate_cmd, "%P"),
            invalidcommand=invalid_cmd,
            width=15,
        )
        entry.grid(row=row, column=1, sticky=tk.W, padx=5)



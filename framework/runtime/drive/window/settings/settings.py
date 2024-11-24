from framework.runtime.core.setting.vm.app_setting_view_model import AppSettingViewModel
from framework.runtime.core.setting.vm.model_setting_view_model import ModelSettingViewModel
from framework.runtime.core.setting.vm.waifu_setting_view_model import WaifuSettingViewModel
from framework.runtime.drive.window.settings.app_setting import AppSettingView
from tkinter import ttk
import tkinter as tk

from framework.runtime.drive.window.settings.model_setting import ModelSettingView
from framework.runtime.drive.window.settings.waifu_setting import WaifuSettingView


class Settings:

    def __init__(self, root, config):
        self.p = None
        self.root = root
        self.notebook = None
        self.aViewModel = AppSettingViewModel(config)
        self.mViewModel = ModelSettingViewModel(config.modelInfo)
        self.wViewModel = WaifuSettingViewModel(config.waifu)

    def show(self):
        if self.p:
            self.p.destroy()

        self.p = tk.Toplevel(self.root)
        self.p.title("Settings")
        # 退出时，将self.root 置为None，避免重复销毁
        self.p.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

        notebook = ttk.Notebook(self.p)
        self.notebook = notebook
        self.notebook.pack(fill=tk.BOTH, expand=True)
        AppSettingView(notebook, self.aViewModel)
        ModelSettingView(notebook, self.mViewModel)
        WaifuSettingView(notebook, self.wViewModel)

    def destroy(self):
        self.p.destroy()
        self.p = None

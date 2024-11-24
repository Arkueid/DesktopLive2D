import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from framework.runtime.core.setting.vm.waifu_setting_view_model import WaifuSettingViewModel


class WaifuSettingView:

    def __init__(self, notebook, view_model: WaifuSettingViewModel):
        self.view_model = view_model

        # 创建一个新的Tab
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="Waifu Settings")

        # 创建 UI 组件
        self.create_waifu_selector()
        self.create_moment_area()

        # 初始化
        self.update_waifus()

    def create_waifu_selector(self):
        """创建 Waifu 选择区域"""
        frame = ttk.Frame(self.tab)
        frame.pack(fill=tk.X, padx=5, pady=5)

        # Waifu 选择下拉框
        ttk.Label(frame, text="Select Waifu:").pack(anchor=tk.W, padx=5, pady=5)
        self.waifu_selector = ttk.Combobox(frame, state="readonly")
        self.waifu_selector.pack(fill=tk.X, padx=5, pady=5)
        self.waifu_selector.bind("<<ComboboxSelected>>", self.on_waifu_selected)
        ttk.Button(frame, text="New Waifu", command=self.new_waifu).pack(padx=5, pady=5)

        # waifu detail：name, desc (entry), greeting
        ttk.Label(frame, text="Name:").pack(anchor=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.pack(fill=tk.X, padx=5, pady=5)
        self.desc_entry = ttk.Entry(frame, width=30)
        self.desc_entry.pack(fill=tk.X, padx=5, pady=5)
        self.greeting_entry = ttk.Entry(frame, width=30)
        self.greeting_entry.pack(fill=tk.X, padx=5, pady=5)
        self.name_entry.bind("<Return>", self.on_name_changed)
        self.desc_entry.bind("<Return>", self.on_desc_changed)
        self.greeting_entry.bind("<Return>", self.on_greeting_changed)
        self.name_entry.bind("<FocusOut>", self.on_name_changed)
        self.desc_entry.bind("<FocusOut>", self.on_desc_changed)
        self.greeting_entry.bind("<FocusOut>", self.on_greeting_changed)

    def on_name_changed(self, event):
        self.view_model.currentWaifu.value.name = self.name_entry.get()

    def on_desc_changed(self, event):
        self.view_model.currentWaifu.value.desc = self.desc_entry.get()

    def on_greeting_changed(self, event):
        self.view_model.currentWaifu.value.greeting = self.greeting_entry.get()

    def create_moment_area(self):
        """创建 Moment 查看和选择区域"""
        frame = ttk.Frame(self.tab)
        frame.pack(fill=tk.X, padx=5, pady=5)

        # Moment 选择下拉框
        ttk.Label(frame, text="Select Moment:").pack(anchor=tk.W, padx=5, pady=5)
        self.moment_selector = ttk.Combobox(frame, state="readonly")
        self.moment_selector.pack(fill=tk.X, padx=5, pady=5)
        self.moment_selector.bind("<<ComboboxSelected>>", self.on_moment_selected)


        # Hitokoto 显示区域
        self.hitokoto_text = tk.Text(frame, wrap=tk.WORD, height=15)
        self.hitokoto_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 配置文本样式
        self.hitokoto_text.tag_configure("waifu", foreground="blue", font=("Arial", 10, "bold"))
        self.hitokoto_text.tag_configure("user", foreground="green", font=("Arial", 10, "bold"))
        self.hitokoto_text.config(state=tk.DISABLED)

        ttk.Button(frame, text="New Moment", command=self.new_moment).pack(padx=5, pady=5)

    def new_moment(self):
        self.view_model.newMoment()
        self.update_waifus()

    def new_waifu(self):
        name: str = simpledialog.askstring("New Waifu", "Enter Waifu Name:")
        if not name:
            return
        if name in self.view_model.currentWaifu.value.waifus():
            messagebox.showerror("Error", "Waifu already exists!")
        else:
            self.view_model.newWaifu(name, "", "")
            self.update_waifus()

    def update_waifus(self):
        """更新 Waifu 下拉框内容"""
        waifu_names = self.view_model.getWaifuNames()
        self.waifu_selector["values"] = waifu_names
        if waifu_names:
            self.waifu_selector.current(0)  # 默认选择第一个 Waifu
            self.on_waifu_selected(None)  # 默认显示该 Waifu 的 Moments


    def update_moments(self):
        """更新 Moment 下拉框内容"""
        self.moment_selector["values"] = []
        current_waifu = self.view_model.currentWaifu.value
        if current_waifu:
            moments = current_waifu.mids
            self.moment_selector["values"] = moments
            if moments:
                self.moment_selector.current(0)  # 默认选择第一个 Moment
                self.update_hitokotos(moments[0])  # 显示对应的 Hitokoto

    def update_hitokotos(self, moment):
        """根据选中的 Moment 更新 Hitokoto 显示"""
        self.hitokoto_text.config(state=tk.NORMAL)
        self.hitokoto_text.delete(1.0, tk.END)

        current_waifu = self.view_model.currentWaifu.value
        if current_waifu:
            moment_obj = current_waifu.moments[moment]
            for hitokoto in moment_obj.hitokotos:
                tag = "waifu" if hitokoto.fromWaifu else "user"
                self.hitokoto_text.insert(tk.END, f"{hitokoto.who} ({hitokoto.when}):\n", tag)
                self.hitokoto_text.insert(tk.END, f"{hitokoto.words}\n\n", tag)

        self.hitokoto_text.config(state=tk.DISABLED)

    def on_waifu_selected(self, event):
        """当选择 Waifu 时，更新对应 Moments 和 Hitokotos"""
        selected_waifu = self.waifu_selector.get()
        if selected_waifu:
            self.view_model.selectWaifu(selected_waifu)
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_waifu)
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, self.view_model.currentWaifu.value.desc)
            self.greeting_entry.delete(0, tk.END)
            self.greeting_entry.insert(0, self.view_model.currentWaifu.value.greeting)
            self.update_moments()

    def on_moment_selected(self, event):
        """当选择 Moment 时，更新 Hitokoto 显示"""
        selected_moment = self.moment_selector.get()
        if selected_moment:
            self.view_model.selectMoment(selected_moment)
            self.update_hitokotos(selected_moment)

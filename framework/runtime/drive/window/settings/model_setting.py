from tkinter import ttk, Menu, simpledialog, messagebox
import tkinter as tk

from framework.runtime.core.setting.vm.model_setting_view_model import ModelSettingViewModel


class ModelSettingView:
    def __init__(self, notebook, viewModel: ModelSettingViewModel):
        self.viewModel = viewModel
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="Model Settings")

        # 主区域：左侧树型结构 + 右侧详情
        self.main_frame = ttk.Frame(self.tab)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # 左侧树型结构
        self.tree = ttk.Treeview(self.main_frame, show="tree")
        self.tree.pack(side="left", expand=True, fill="both", padx=(0, 10))

        # 添加滚动条
        tree_scroll = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="left", fill="y")

        # 右键菜单
        self.tree_menu = Menu(self.tree, tearoff=0)
        self.tree_menu.add_command(label="Add Group", command=self.add_motion_group)
        self.tree_menu.add_command(label="Remove Group", command=self.remove_motion_group)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label="Add Motion", command=self.add_motion)
        self.tree_menu.add_command(label="Remove Motion", command=self.remove_motion)
        self.tree_menu.add_command(label="Start Motion", command=self.start_motion)

        self.tree.bind("<Button-3>", self.show_tree_menu)

        self.tree.bind("<ButtonRelease-1>", self.on_show_detail)

        # 右侧详情区
        self.detail_frame = ttk.LabelFrame(self.main_frame, text="Detail", padding=10)
        self.detail_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(self.detail_frame, text="Current Model").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.current_model = ttk.Combobox(self.detail_frame,
                                          values=self.viewModel.modelNames, width=25)
        self.current_model.set(self.viewModel.currentModelName)
        self.current_model.bind("<<ComboboxSelected>>", self.on_current_model_changed)
        self.current_model.grid(row=0, column=1, padx=5, pady=5)
        self.current_model.state(["readonly"])

        ttk.Label(self.detail_frame, text="File:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.file_entry = ttk.Entry(self.detail_frame, width=30)
        self.file_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.detail_frame, text="Sound:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.sound_entry = ttk.Entry(self.detail_frame, width=30)
        self.sound_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.detail_frame, text="Text:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.text_entry = ttk.Entry(self.detail_frame, width=30)
        self.text_entry.grid(row=3, column=1, padx=5, pady=5)

        # 修改按钮
        self.modify_button = ttk.Button(self.detail_frame, text="Apply", command=self.save_motion_detail)
        self.modify_button.grid(row=4, column=0, columnspan=2, pady=10)

        # 初始化数据
        self.load_motion_groups()

    def load_motion_groups(self):
        """加载动作组和动作到树型结构"""
        self.tree.delete(*self.tree.get_children())  # 清空树
        for group_name, group in self.viewModel.currentMotionGroups.value:
            group_id = self.tree.insert("", "end", text=group_name, open=True)
            for i, motion in enumerate(group):
                self.tree.insert(group_id, "end", text=f"{group_name}_{i}", values=(group_name, i))

    def on_current_model_changed(self, event):
        self.viewModel.changeModel(self.current_model.get())
        self.load_motion_groups()

    def start_motion(self):
        selected_item = self.tree.selection()
        group_name, motion_index = self.tree.item(selected_item[0], "values")
        self.viewModel.startMotion(group_name, int(motion_index))

    def on_show_detail(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.file_entry.delete(0, "end")
            self.sound_entry.delete(0, "end")
            self.text_entry.delete(0, "end")
            if len(values) == 2:
                group_name, motion_index = values
                motion = self.viewModel.currentMotionGroups.value.group(group_name).motion(int(motion_index))
                self.file_entry.insert(0, motion.file())
                self.sound_entry.insert(0, motion.sound())
                self.text_entry.insert(0, motion.text())

    def show_tree_menu(self, event):
        """显示右键菜单"""
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.tree.selection_set(selected_item)
            if len(values) == 2:
                self.tree_menu.entryconfig("Add Group", state=tk.DISABLED)
                self.tree_menu.entryconfig("Remove Group", state=tk.DISABLED)
                self.tree_menu.entryconfig("Add Motion", state=tk.NORMAL)
                self.tree_menu.entryconfig("Remove Motion", state=tk.NORMAL)
                self.tree_menu.entryconfig("Start Motion", state=tk.NORMAL)
                self.tree_menu.post(event.x_root, event.y_root)
            else:
                self.tree_menu.entryconfig("Add Group", state=tk.NORMAL)
                self.tree_menu.entryconfig("Remove Group", state=tk.NORMAL)
                self.tree_menu.entryconfig("Add Motion", state=tk.DISABLED)
                self.tree_menu.entryconfig("Remove Motion", state=tk.DISABLED)
                self.tree_menu.entryconfig("Start Motion", state=tk.DISABLED)
                self.tree_menu.post(event.x_root, event.y_root)

    def add_motion_group(self):
        """添加动作组"""
        group_name = simpledialog.askstring("输入动作组名称", "动作组名称")
        if group_name:
            self.viewModel.newMotionGroup(group_name)
            self.load_motion_groups()

    def remove_motion_group(self):
        """删除动作组"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        group_name = self.tree.item(selected_item[0], "text")
        if messagebox.askyesno("删除动作组", f"确定删除动作组 {group_name} 吗？"):
            self.viewModel.removeMotionGroup(group_name)
            self.load_motion_groups()

    def add_motion(self):
        """添加动作"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        group_name = self.tree.item(selected_item[0], "text")
        if not group_name:  # 必须选择动作组
            messagebox.showerror("错误", "请先选择动作组")
            return
        self.viewModel.addMotion(group_name, "", "", "")
        self.load_motion_groups()

    def remove_motion(self):
        """删除动作"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        parent = self.tree.parent(selected_item[0])
        if not parent:  # 必须选择动作
            messagebox.showerror("错误", "请先选择动作")
            return
        group_name = self.tree.item(parent, "text")
        motion_index = self.tree.index(selected_item[0])
        if messagebox.askyesno("删除动作", f"确定删除动作组 {group_name} 的动作 {motion_index + 1} 吗？"):
            self.viewModel.removeMotion(group_name, motion_index)
            self.load_motion_groups()

    def save_motion_detail(self):
        """保存详情区内容到 ViewModel"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        parent = self.tree.parent(selected_item[0])
        if not parent:  # 必须选择动作
            messagebox.showerror("错误", "请先选择动作")
            return
        group_name = self.tree.item(parent, "text")
        motion_index = self.tree.index(selected_item[0])

        # 获取详情信息
        file = self.file_entry.get()
        sound = self.sound_entry.get()
        text = self.text_entry.get()

        # 更新 ViewModel
        self.viewModel.setMotionFile(group_name, motion_index, file)
        self.viewModel.setMotionSound(group_name, motion_index, sound)
        self.viewModel.setMotionText(group_name, motion_index, text)

        messagebox.showinfo("成功", "动作详情已修改")

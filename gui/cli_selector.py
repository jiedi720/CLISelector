"""CLI选择器组件模块"""
import tkinter as tk
from .config import COLORS


class CLISelectorWidget:
    """CLI选择器组件"""

    def __init__(self, parent, group_name, commands, on_select_callback=None, on_double_click_callback=None):
        """
        初始化CLI选择器组件

        Args:
            parent: 父容器
            group_name: 组名称
            commands: 命令字典
            on_select_callback: 选择回调函数
            on_double_click_callback: 双击回调函数
        """
        self.group_name = group_name
        self.commands = commands
        self.on_select_callback = on_select_callback
        self.on_double_click_callback = on_double_click_callback
        self.other_listboxes = []

        # 创建组框架
        self.frame = tk.Frame(
            parent,
            bg=COLORS['card_bg'],
            padx=15,
            pady=15
        )

        # 创建UI
        self.create_widgets()

    def create_widgets(self):
        """创建组件"""
        # 组标题
        group_label = tk.Label(
            self.frame,
            text=self.group_name,
            font=("Segoe UI", 14, "bold"),
            bg=COLORS['card_bg'],
            fg=COLORS['accent']
        )
        group_label.pack(pady=(0, 10))

        # 列表框
        self.listbox = tk.Listbox(
            self.frame,
            font=("Segoe UI", 11),
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            selectbackground=COLORS['accent'],
            selectforeground=COLORS['bg'],
            selectmode=tk.SINGLE,
            borderwidth=0,
            highlightthickness=0,
            relief=tk.FLAT,
            height=8,
            exportselection=False,
            activestyle='none',
            selectborderwidth=0
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # 填充CLI选项
        for cli_name in self.commands:
            self.listbox.insert(tk.END, cli_name)

        # 默认选中第一个（只对AI CLI选中）
        if self.group_name == "AI CLI":
            self.listbox.select_set(0)

        # 绑定事件
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Double-Button-1>', self.on_double_click)

    def on_select(self, event):
        """选择事件处理"""
        if self.on_select_callback:
            self.on_select_callback(self.listbox)

    def on_double_click(self, event):
        """双击事件处理"""
        if self.on_double_click_callback:
            self.on_double_click_callback()

    def set_other_listboxes(self, other_listboxes):
        """设置其他列表框引用"""
        self.other_listboxes = other_listboxes

    def get_selected(self):
        """获取选中的CLI名称"""
        selection = self.listbox.curselection()
        if selection:
            return self.listbox.get(selection[0])
        return None

    def clear_selection(self):
        """清除选中"""
        self.listbox.selection_clear(0, tk.END)

    def pack(self, **kwargs):
        """包装pack方法"""
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        """包装grid方法"""
        self.frame.grid(**kwargs)
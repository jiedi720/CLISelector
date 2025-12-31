"""路径栏组件模块"""
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os


class PathBar:
    """路径栏组件"""

    def __init__(self, parent, colors):
        """
        初始化路径栏组件

        Args:
            parent: 父容器
            colors: 颜色配置
        """
        self.colors = colors
        self.frame = tk.Frame(parent, bg=colors['bg'])

        # 创建UI
        self.create_widgets()

    def create_widgets(self):
        """创建组件"""
        # 标签
        path_label = tk.Label(
            self.frame,
            text="工作目录:",
            font=("Segoe UI", 10),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        path_label.pack(side=tk.LEFT, padx=(0, 10))

        # 路径输入框
        self.path_entry = tk.Entry(
            self.frame,
            font=("Segoe UI", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['accent']
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.path_entry.insert(0, os.getcwd())

        # 启用拖放
        self.path_entry.drop_target_register(DND_FILES)
        self.path_entry.dnd_bind('<<Drop>>', self.on_drop)

        # 浏览按钮
        browse_button = tk.Button(
            self.frame,
            text="📁 浏览",
            command=self.browse_directory,
            font=("Segoe UI", 9),
            bg=self.colors['card_bg'],
            fg=self.colors['accent'],
            activebackground=self.colors['border'],
            activeforeground=self.colors['accent'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5,
            borderwidth=0
        )
        browse_button.pack(side=tk.LEFT)

    def on_drop(self, event):
        """处理拖放事件"""
        data = event.data
        # 移除花括号和引号
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]
        # 移除可能的引号
        data = data.strip('"').strip("'")

        if os.path.isdir(data):
            self.set_path(data)
        elif os.path.isfile(data):
            # 如果是文件，使用其所在目录
            self.set_path(os.path.dirname(data))

    def browse_directory(self):
        """打开目录选择对话框"""
        directory = filedialog.askdirectory(
            title="选择工作目录",
            initialdir=self.path_entry.get()
        )

        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def get_path(self):
        """获取当前路径"""
        return self.path_entry.get()

    def set_path(self, path):
        """设置路径"""
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def pack(self, **kwargs):
        """包装pack方法"""
        self.frame.pack(**kwargs)
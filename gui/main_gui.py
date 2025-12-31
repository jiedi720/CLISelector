"""主GUI模块"""
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from .config import COLORS, CLI_GROUPS, WINDOW_CONFIG
from .cli_selector import CLISelectorWidget
from .path_bar import PathBar
from .cli_launcher import CLILauncher


class MainWindow:
    """主窗口类"""

    def __init__(self, root):
        """
        初始化主窗口

        Args:
            root: Tk根窗口
        """
        self.root = root
        self.root.title(WINDOW_CONFIG['title'])

        # 先隐藏窗口，避免闪烁
        self.root.withdraw()

        # 设置窗口背景
        self.root.configure(bg=COLORS['bg'])

        # 扁平化的命令映射
        self.cli_commands = {}
        for group, commands in CLI_GROUPS.items():
            self.cli_commands.update(commands)

        # 创建CLI启动器
        self.launcher = CLILauncher(self.cli_commands)

        # 存储CLI选择器组件
        self.cli_selectors = []

        # 创建所有组件
        self.create_widgets()

        # 设置窗口大小和居中位置
        self.root.geometry(WINDOW_CONFIG['geometry'])
        self.center_window()

        # 显示窗口
        self.root.deiconify()

    def center_window(self):
        """居中窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """创建所有组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="CLI 选择器",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=(30, 20))

        # 路径栏
        self.path_bar = PathBar(self.root, COLORS)
        self.path_bar.pack(pady=(0, 10), padx=30, fill=tk.X)

        # 主框架
        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)

        # 创建CLI选择器
        self.create_cli_selectors(main_frame)

        # 状态栏
        self.status_label = tk.Label(
            self.root,
            text="准备就绪",
            font=("Segoe UI", 9),
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=30, pady=(0, 15))

        # 启用整个窗口的拖放
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def create_cli_selectors(self, parent):
        """创建CLI选择器"""
        column = 0
        for group_name, commands in CLI_GROUPS.items():
            selector = CLISelectorWidget(
                parent,
                group_name,
                commands,
                on_select_callback=self.on_listbox_select,
                on_double_click_callback=self.launch_cli
            )
            selector.grid(row=0, column=column, padx=10, sticky="nsew", rowspan=2)
            self.cli_selectors.append(selector)

            # 配置网格权重
            parent.grid_columnconfigure(column, weight=1)
            parent.grid_rowconfigure(0, weight=1)

            column += 1

        # 设置其他列表框引用
        all_listboxes = [s.listbox for s in self.cli_selectors]
        for selector in self.cli_selectors:
            other_listboxes = [lb for lb in all_listboxes if lb != selector.listbox]
            selector.set_other_listboxes(other_listboxes)

    def on_listbox_select(self, current_listbox):
        """当选择一个列表框时，清除其他列表框的选中状态"""
        for selector in self.cli_selectors:
            if selector.listbox != current_listbox:
                selector.clear_selection()

    def launch_cli(self):
        """从当前选中的列表框启动CLI"""
        # 检查哪个列表框有选中项
        selected_cli = None
        for selector in self.cli_selectors:
            cli = selector.get_selected()
            if cli:
                selected_cli = cli
                break

        if not selected_cli:
            messagebox.showwarning("提示", "请先选择一个CLI！")
            return

        # 获取工作目录
        working_dir = self.path_bar.get_path()

        # 启动CLI
        self.launcher.launch(
            selected_cli,
            working_dir,
            status_callback=self.update_status
        )

    def update_status(self, message, color_type):
        """更新状态栏"""
        color = COLORS.get(color_type, COLORS['fg'])
        self.status_label.config(text=message, fg=color)

    def on_drop(self, event):
        """处理拖放事件"""
        import os
        data = event.data
        # 移除花括号和引号
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]
        # 移除可能的引号
        data = data.strip('"').strip("'")

        if os.path.isdir(data):
            self.path_bar.set_path(data)
        elif os.path.isfile(data):
            # 如果是文件，使用其所在目录
            self.path_bar.set_path(os.path.dirname(data))


class CLISelector(MainWindow):
    """CLI选择器主类（向后兼容）"""
    pass
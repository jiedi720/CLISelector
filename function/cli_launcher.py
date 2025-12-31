"""CLI启动器模块"""
import subprocess
import sys
import os
from tkinter import messagebox
from .proxy import get_proxy_env


class CLILauncher:
    """CLI启动器"""

    def __init__(self, cli_commands):
        """
        初始化CLI启动器

        Args:
            cli_commands: CLI命令字典
        """
        self.cli_commands = cli_commands

    def launch(self, cli_name, working_dir, status_callback=None):
        """
        启动指定的CLI

        Args:
            cli_name: CLI名称
            working_dir: 工作目录
            status_callback: 状态回调函数

        Returns:
            bool: 启动是否成功
        """
        if cli_name not in self.cli_commands:
            messagebox.showwarning("提示", "无效的CLI选择！")
            return False

        command = self.cli_commands[cli_name]

        try:
            if status_callback:
                status_callback(f"正在启动 {cli_name}...", 'warning')

            # 检查工作目录
            if not os.path.isdir(working_dir):
                messagebox.showwarning("提示", f"目录不存在: {working_dir}")
                return False

            # 获取带代理的环境变量
            env = get_proxy_env()

            # 在新窗口中启动CLI，并设置工作目录
            if sys.platform == "win32":
                # 构建居中窗口的 PowerShell 命令
                cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in command)
                center_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Win32 -Namespace Native -MemberDefinition @"
[DllImport("user32.dll")]
public static extern IntPtr GetForegroundWindow();
[DllImport("user32.dll")]
public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
"@
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$hwnd = [Native.Win32]::GetForegroundWindow()
$windowWidth = 960
$windowHeight = 800
$x = ($screen.Width / 2) - ($windowWidth / 2)
$y = ($screen.Height / 2) - ($windowHeight / 2)
$SWP_NOZORDER = 0x0004
[Native.Win32]::ShowWindow($hwnd, 0) | Out-Null
$host.UI.RawUI.WindowTitle = "{cli_name}"
$host.UI.RawUI.ForegroundColor = "White"
$host.UI.RawUI.BackgroundColor = "Black"
$host.UI.RawUI.BufferSize = New-Object System.Management.Automation.Host.Size (120, 3000)
$host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size (120, 50)
[Native.Win32]::SetWindowPos($hwnd, 0, $x, $y, $windowWidth, $windowHeight, $SWP_NOZORDER) | Out-Null
[Native.Win32]::ShowWindow($hwnd, 5) | Out-Null
{cmd_str}
'''
                subprocess.Popen(
                    ["powershell", "-NoExit", "-Command", center_script],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    env=env,
                    cwd=working_dir
                )
            else:
                subprocess.Popen(command, env=env, cwd=working_dir)

            if status_callback:
                status_callback(f"{cli_name} 已启动 (代理已设置)", 'success')

            return True

        except Exception as e:
            messagebox.showerror("错误", f"启动 {cli_name} 失败:\n{str(e)}")
            if status_callback:
                status_callback("启动失败", 'error')
            return False
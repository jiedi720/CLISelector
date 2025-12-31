"""GUI配置模块"""

# CLI命令列表 - 按组分类
CLI_GROUPS = {
    "AI CLI": {
        "iFlow": ["powershell", "-NoExit", "-Command", "iflow"],
        "Qwen": ["powershell", "-NoExit", "-Command", "qwen"],
        "Gemini": ["powershell", "-NoExit", "-Command", "gemini"]
    },
    "System CLI": {
        "WSL": ["wsl"],
        "PowerShell": ["powershell", "-NoExit"],
        "CMD": ["cmd", "/k"],
        "Python Shell": ["python", "-i"]
    }
}

# 主题颜色配置
COLORS = {
    'bg': '#1e1e2e',
    'fg': '#cdd6f4',
    'accent': '#89b4fa',
    'accent_hover': '#b4befe',
    'card_bg': '#313244',
    'border': '#45475a',
    'success': '#a6e3a1',
    'warning': '#f9e2af',
    'error': '#f38ba8'
}

# 窗口配置
WINDOW_CONFIG = {
    'title': 'CLI 选择器',
    'geometry': '700x450',
    'minsize': (550, 400)
}
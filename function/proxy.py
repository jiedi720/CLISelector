"""代理配置模块"""
import os


PROXY_CONFIG = {
    'url': 'http://127.0.0.1:3128'
}


def get_proxy_env():
    """
    获取代理环境变量

    Returns:
        dict: 包含代理设置的环境变量字典
    """
    env = os.environ.copy()
    env['https_proxy'] = PROXY_CONFIG['url']
    env['http_proxy'] = PROXY_CONFIG['url']
    return env


def get_proxy_url():
    """
    获取代理URL

    Returns:
        str: 代理URL
    """
    return PROXY_CONFIG['url']
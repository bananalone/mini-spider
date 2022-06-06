from os import name
from typing import Mapping
import yaml

def load_config(config_path: str) -> dict:
    '''
    加载配置文件
    参数：
    config_path：字符串，yaml配置文件路径
    返回：
    字典，yaml配置文件
    '''
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config
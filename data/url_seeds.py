import yaml

def load_url_seeds(url_seeds_path: str) -> list:
    '''
    加载URL种子
    参数：
    url_seeds_path: 字符串，种子yaml文件路径
    返回：
    种子列表
    '''
    with open(url_seeds_path) as f:
        seeds = yaml.load(f, Loader=yaml.FullLoader)
    
    return seeds
import re

PREFIX = r'https://'

def parse_urls(page: str, pattern: re.Pattern) -> list:
    """
    解析网页中的url
    """
    urls = pattern.findall(page)
    urls = [PREFIX + url for url in urls]
    return urls
    
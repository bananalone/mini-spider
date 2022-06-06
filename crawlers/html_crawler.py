import re
import os
import time
import threading

import requests

from data.url_table import UrlTable
from data.page_file import save_page
from parse.url_parse import parse_urls
from log import Logger

SUFFIX = r'.html'
INTERVAL = 0.1

class HtmlCrawler:
    def __init__(self, url_table: UrlTable, config: dict, logger: Logger, name: str ) -> None:
        self.url_table = url_table
        '''
        max_threads: 5
        log_path: log.txt

        crawlers:
        HtmlCrawler:
            pattern: www.runoob.com/go/[^\s]*.html
            save_root: html_results
            max_deepth: 5
        '''
        self.name = name
        self.log_path = config["log_path"]
        self._config = config['crawlers']['HtmlCrawler']
        self.pattern = re.compile(self._config['pattern'])
        self.save_root = self._config['save_root']
        self.max_deepth = self._config['max_deepth']
        self.logger = logger

    def _parse(self, url: str):
        try:
            response = requests.get(url)
        except Exception as ex:
            msg = str(ex)
            self.logger.log(msg)
            return None
        page = response.text
        urls = parse_urls(page, self.pattern)
        return page, urls

    def _save(self, page: str, url: str):
        name = url.replace('/', '_').replace(':', '_')
        save_path = os.path.join(self.save_root, name + SUFFIX)
        save_page(page, save_path)

    def _add_urls(self, urls, deepth):
        for url in urls:
            self.url_table.add(url, deepth)

    def _run(self):
        ret = self.url_table.get()
        if ret is None:
            return
        url, deepth = ret
        if deepth < self.max_deepth:
            parse = self._parse(url)
            if parse is None:
                return
            page, urls = parse
            self._save(page, url)
            self._add_urls(urls, deepth+1)
            msg = "{} || {} deepth:{} is_empty:{}".format(self.name, url, deepth+1, self.url_table.is_empty())
            self.logger.log(msg)
    
    def run(self):
        while not self.url_table.is_empty():
            time.sleep(INTERVAL)
            self.url_table.lock.acquire()
            self._run()
            self.url_table.lock.release()

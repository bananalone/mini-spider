import threading
import argparse
import time

from crawlers.html_crawler import HtmlCrawler
from data.config_load import load_config
from data.url_seeds import load_url_seeds
from data.url_table import UrlTable
from log import Logger

DEFAULT_CONFIG_PATH = r"configs/config.yaml"
DEFAULT_URL_SEEDS_PATH = r"configs/url_seeds.yaml"

class MiniSpider:
    def __init__(self, url_seeds_path: str, config_path: str) -> None:
        seeds = load_url_seeds(url_seeds_path)
        self.config = load_config(config_path)
        self.max_threads = self.config["max_threads"]
        self.logger = Logger(self.config["log_path"])
        self.url_table = UrlTable()
        for seed in seeds:
            self.url_table.add(seed, 0)
        self.crawlers = []

    def _run(self, crawler_id):
        crawler_name = "{}@crawler".format(crawler_id)
        crawler = HtmlCrawler(self.url_table, self.config, self.logger, crawler_name)
        crawler.run()

    def start(self):
        for crawler_id in range(self.max_threads):
            crawler = threading.Thread(target=self._run, args=[crawler_id])
            self.crawlers.append(crawler)
            crawler.setDaemon(True)
            crawler.start()

    def join(self):
        for crawler in self.crawlers:
            crawler.join()
    

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--config_path', type=str, default=DEFAULT_CONFIG_PATH)
    parse.add_argument('--url_seeds_path', type=str, default=DEFAULT_URL_SEEDS_PATH)
    args = parse.parse_args()

    spider = MiniSpider(args.url_seeds_path, args.config_path)
    spider.start()
    spider.join()

if __name__ == "__main__":
    main()
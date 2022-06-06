import threading

class UrlTable:
    """
    爬虫共用的一张线程安全并去重的url表
    """
    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.queue = [] # 先进先出，确保是广度优先遍历
        self.all_urls_set = set() # 当前所有url，用于去重
    
    def add(self, url: str, deepth: int) -> None:
        self.lock.acquire()
        if url not in self.all_urls_set:
            self.all_urls_set.add(url)
            self.queue.append([url, deepth])
        self.lock.release()

    def get(self):
        """
        获取URL及其当前深度，如果获取不了就返回空
        """
        ret = None
        self.lock.acquire()
        if not self.is_empty():
            url, deepth = self.queue.pop(0)
            ret = url, deepth
        self.lock.release()
        return ret

    def is_empty(self):
        self.lock.acquire()
        ret = False
        if len(self.queue) == 0:
            ret = True
        self.lock.release()
        return ret
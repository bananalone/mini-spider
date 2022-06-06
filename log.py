import time
import threading

class Logger:
    def __init__(self, log_path) -> None:
        self.log_path = log_path
        self.lock = threading.Lock()

    def log(self, msg: str):
        self.lock.acquire()
        log = "===== " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' =====\n' + msg
        print(log)
        with open(self.log_path, 'a') as f:
            f.write(log + '\n')
        self.lock.release()
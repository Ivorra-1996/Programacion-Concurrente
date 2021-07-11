

import threading


class MonitorContador():
    lock = threading.Lock()

    def incrementar(self):
        self.lock.acquire()
        try:
            i +=1
        finally:
            self.lock.release()

    def getValor(self):
        self.lock.acquire()
        try:
            return i
        finally:
            self.lock.release()


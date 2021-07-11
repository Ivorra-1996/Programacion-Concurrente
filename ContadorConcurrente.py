import threading


class MonitorContador():
    lock = threading.Lock()
    i = 0

    def incrementar(self):
        self.lock.acquire()
        try:
            self.i += 1
        finally:
            self.lock.release()

    def getValor(self):
        self.lock.acquire()
        try:
            return self.i
        finally:
            self.lock.release()

class HiloContador(threading.Thread):
    def __init__(self,contadorMon):
        super().__init__()
        self.contador = contadorMon

    def run(self):
        for i  in range(0,1000000):
            self.contador.incrementar()

def main():
    countMon = MonitorContador()
    hilos : threading.Thread = []

    for posicion in range(5):
        r = HiloContador(countMon)
        t = threading.Thread(target= r.run())
        hilos.append(t)
        t.start()
        print('Arranca hilo', posicion)

    for posicion in range(0,5):
        hilos[posicion].join()

    print("Valor final = ", countMon.getValor())


if __name__ == "__main__":
    main()
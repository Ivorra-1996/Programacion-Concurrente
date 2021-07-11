import threading

# Modificar el monitor del ejemplo 1 (contador) de modo que solo dos hilos puedan incrementar el contador a la vez, 
# debiendo los demás hilos esperar a que uno de estos termine para tomar su lugar.

class MonitorContador():
    lock = threading.RLock()
    i = 0
    lista = []
    esperar = threading.Condition(lock)

    
    # Usamos funciones que simulan ser semaforos.
    def darPermiso(self):
        self.lock.acquire()
        try:
            while( len(self.lista) == 2):
                self.esperar.wait()
            self.lista.append(threading.current_thread())
        finally:
            self.lock.release()

    def quitarPermiso(self):
        self.lock.acquire()
        try:
            if(threading.current_thread() in self.lista):
                self.lista.remove(threading.current_thread())
                self.esperar.notify_all()
        finally:
            self.lock.release()


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
        self.contador.darPermiso()
        for i  in range(0,1000000):
            self.contador.incrementar()
        self.contador.quitarPermiso()

def main():
    countMon = MonitorContador()
    hilos : threading.Thread = []

    for posicion in range(5):
        r = HiloContador(countMon)
        t = threading.Thread(target= r.run())
        hilos.append(t)
        t.start()
        print('Arranca hilo', posicion+1)

    for posicion in range(0,5):
        hilos[posicion].join()

    print("Valor final = ", countMon.getValor())


if __name__ == "__main__":
    main()
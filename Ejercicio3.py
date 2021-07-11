import threading
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Modificar el el ejercicio anterior de modo que solo dos hilos incrementen el contador y los demas deberán esperar a que ambos hilos terminen para tomar sus lugares.

class MonitorContador():
    lock = threading.RLock()
    i = 0
    lista = []
    esperar = threading.Condition(lock)

    
    # Usamos funciones que simulan ser semaforos.
    def darPermiso(self):
        self.lock.acquire()
        try:
            while( len(self.lista) > 1):
                self.esperar.wait()
            logging.info(f'entro {threading.current_thread().name}')
            self.lista.append(threading.current_thread())
            logging.info(f'{len(self.lista)} agrego' )
        finally:
            self.lock.release()

    def quitarPermiso(self):
        self.lock.acquire()
        try:
            if(threading.current_thread() in self.lista):
                logging.info(f'entro {threading.current_thread().name}')
                self.lista.remove(threading.current_thread())
                logging.info(f'{len(self.lista)}')
                if(len(self.lista) == 0):
                    logging.info(f'{len(self.lista)}')
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
        hilos.append(r)
        r.start()
        print('Arranca hilo', posicion+1)

    for posicion in range(0,5):
        hilos[posicion].join()

    print("Valor final = ", countMon.getValor())


if __name__ == "__main__":
    main()
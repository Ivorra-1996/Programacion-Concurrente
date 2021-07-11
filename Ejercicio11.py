import threading
import logging
import time
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Supongamos que un centro de computadores tiene dos impresoras, A y B, que son parecidas pero no idénticas. 
# Tres clases de procesos usan las impresoras: los que usan la impresora A, los que usan la impresora B y los que usan ambas impresoras. 
# Desarrollar el código que cada clase de proceso ejecuta para acceder y liberar una impresora. 
# Construir un monitor que asigne las impresoras y que permita usarlas con el máximo rendimiento.

class Monitor():
    lockA = threading.Lock()
    lockB = threading.Lock()

    def impresoraA(self):
        self.lockA.acquire()
        try:
            logging.info(f'{threading.current_thread().getName()} esta usando la impresora A')
            logging.info(f'Imprimiendo....')
            logging.info(f'......')
            logging.info(f'......')
            time.sleep(5)
        finally:
            logging.info(f'{threading.current_thread().getName()} libero la impresora A')
            time.sleep(5)
            self.lockA.release()


    def impresoraB(self):
        self.lockB.acquire()
        try:
            logging.info(f'{threading.current_thread().getName()} esta usando la impresora B')
            logging.info(f'Imprimiendo....')
            logging.info(f'......')
            logging.info(f'......')
            time.sleep(5)
        finally:
            logging.info(f'{threading.current_thread().getName()} libero la impresora B')
            time.sleep(5)
            self.lockB.release()


    def asignarImpresora(self,tipoDeImpresora):
        if(tipoDeImpresora == "A"):
            self.impresoraA()
        elif(tipoDeImpresora == "B"):
            self.impresoraB()

class ProcesoA(threading.Thread):
    def __init__(self,contadorMon):
        self.contador = contadorMon
        self.impresora = "A"
        super().__init__()
        

    def run(self):
        while(True):
            self.contador.asignarImpresora(self.impresora)


class ProcesoB(threading.Thread):
    def __init__(self,contadorMon):
        self.contador = contadorMon
        self.impresora = "B"
        super().__init__()
        

    def run(self):
        while(True):
            self.contador.asignarImpresora(self.impresora)

class ProcesoAB(threading.Thread):
    def __init__(self,contadorMon):
        self.contador = contadorMon
        self.impresora = ""
        super().__init__()
        

    def run(self):
        while(True):
            opcion = random.randint(1,2)
            if(opcion == 1):
                self.impresora = "A"
            elif(opcion == 2):
                self.impresora = "B"
            self.contador.asignarImpresora(self.impresora)

def main():
    countMon = Monitor()
    hilos : threading.Thread = []

    for posicion in range(0,5):
        a = ProcesoA(countMon)
        b = ProcesoB(countMon)
        ab = ProcesoAB(countMon)
        hilos.append(a)
        hilos.append(b)
        hilos.append(ab)
        a.start()
        b.start()
        ab.start()
        logging.info(f'Arranca hilo{threading.current_thread().getName()} en la posicion {posicion+1}')

   # for posicion in range(0,3):
    #    hilos[posicion].join()


if __name__ == "__main__":
    main()

import threading
import logging
import time
import random
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Una cuenta de ahorros es compartida entre distintas personas (procesos). Cada persona puede sacar y depositar dinero en la cuenta. 
# El saldo actual de la cuenta es la suma de los depósitos menos la suma de las extracciones. El saldo nunca pude ser negativo. 
# Construir un monitor que resuelva este problema con las operaciones depositar y extraer.


class Monitor():
    lock = threading.RLock()
    saldo = 0
    #esperar = threading.Condition(lock)

    def depositar(self):
        self.lock.acquire()
        deposito = random.randint(100,1000)
        try:
            logging.info(f'se deposito :{deposito}')
            self.saldo += deposito
            logging.info(f'el saldo actual es :{self.saldo}')
        finally:
            time.sleep(5)
            self.lock.release()


    def extraer(self):
        self.lock.acquire()
        print("Entro a la funcion Extraer")
        extracion = random.randint(100,1000)
        try:
            if(self.saldo > 0 and self.saldo >= extracion):
                self.saldo -= extracion
                logging.info(f'se extrajo :{extracion}')
                logging.info(f'el salgo actual es :{self.saldo}')
                time.sleep(5)
        finally:
            self.lock.release()

class HiloPersona(threading.Thread):
    def __init__(self,contadorMon):
        super().__init__()
        self.contador = contadorMon

    def run(self):
        while(True):
            opcion = random.randint(0,3)
            if opcion == 1 :
                self.contador.depositar()
            if opcion == 2 :
                self.contador.extraer()
                
def main():
    countMon = Monitor()
    hilos : threading.Thread = []

    for posicion in range(0,3):
        d = HiloPersona(countMon)
        hilos.append(d)
        d.start()
        logging.info(f'Arranca hilo{threading.current_thread().getName()} en la posicion {posicion+1}')

    for posicion in range(0,3):
        hilos[posicion].join()


if __name__ == "__main__":
    main()


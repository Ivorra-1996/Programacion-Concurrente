import threading
import logging
import time
import random
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Modificar la solución anterior suponiendo que las extracciones son resueltas por orden de llegada. 
# Es decir si hay 200 y alguien quiere sacar 300 y luego llega alguien que quiere sacar 200, 
# este último tendrá que esperar hasta que el que pidió 300 consiga esa cantidad.


class Monitor():
    lock = threading.RLock()
    saldo = 0
    extracionesPendientes = []
    esperar = threading.Condition(lock)
    cantidad = 0

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
        logging.info(f'El Hilo {threading.current_thread().getName()} entro a la funcion Extraer')
        try:
            if(len(self.extracionesPendientes) == self.cantidad-1 ): # 0 == 1 / 1 == 1
                logging.info(f'Despierta a los hilos')
                self.esperar.notify_all()
            extracion = random.randint(100,1000)
            if(not threading.current_thread() in self.extracionesPendientes ):
                self.extracionesPendientes.append(threading.current_thread())
                logging.info(f'duerme el hilo')
                self.esperar.wait()
                for hilo in self.extracionesPendientes:
                    print(hilo)
            if(self.extracionesPendientes[0] == threading.current_thread()):
                if(self.saldo > 0 and self.saldo >= extracion):
                    self.saldo -= extracion
                    self.extracionesPendientes.remove(threading.current_thread())
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
            opcion = random.randint(1,2)
            if opcion == 1 :
                self.contador.depositar()
            if opcion == 2 :
                self.contador.extraer()
                
def main():
    countMon = Monitor()
    hilos : threading.Thread = []
    cantidadDeHilos = 0

    for posicion in range(0,2):
        cantidadDeHilos += 1 
        d = HiloPersona(countMon)
        hilos.append(d)
        d.start()
        logging.info(f'Arranca hilo{threading.current_thread().getName()} en la posicion {posicion+1}')
    countMon.cantidad = cantidadDeHilos

    for posicion in range(0,3):
        hilos[posicion].join()


if __name__ == "__main__":
    main()


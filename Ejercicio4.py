import threading
import logging
import time
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Diseñar un monitor con un único procedimiento llamado entrada, que provoque que los dos primeros procesos que llamen al procedimiento sean suspendidos y 
# el tercero los despierte y así cíclicamente.

class Monitor():
    lock = threading.RLock()
    contador = 0
    esperar = threading.Condition(lock)

    def entrada(self):
        logging.info(f'{threading.current_thread().name} entro')
        time.sleep(1)
        self.lock.acquire()
        self.contador +=1
        logging.info(f'valor de contador :{self.contador}')
        try:
            if(self.contador < 3):
                logging.info(f'{threading.current_thread().name} se durmio')
                self.esperar.wait()
            elif(self.contador == 3):
                self.contador = 0
                self.esperar.notify_all()
                logging.info(f'{threading.current_thread().name} desperto a los 2 hilos dormidos')
        finally:
            self.lock.release()
        time.sleep(1)
        logging.info(f'{threading.current_thread().name} salio')
        

     

class HiloContador(threading.Thread):
    def __init__(self,contadorMon):
        super().__init__()
        self.contador = contadorMon

    def run(self):
        for i  in range(0,3):
            self.contador.entrada()


def main():
    countMon = Monitor()
    hilos : threading.Thread = []

    for posicion in range(0,3):
        r = HiloContador(countMon)
        hilos.append(r)
        r.start()
        print('Arranca hilo', posicion+1)

    for posicion in range(0,3):
        hilos[posicion].join()


if __name__ == "__main__":
    main()
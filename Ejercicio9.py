import threading
import logging
import time
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Coches que vienen del Norte y del Sur llegan a un puente de una sola vía. Los coches en el mismo sentido pueden cruzar el puente a la vez, 
# pero los coches en sentidos opuestos no. Desarrollar una solución a este problema modelando los coches como hilos y usar un monitor para la sincronización.



class Monitor():
    lock = threading.RLock()
    #esperar = threading.Condition(lock)
    conches  = []

    def puente(self):
        self.lock.acquire()
        opcion = random.randint(1,2)
        direccionDelPuente = logging.NullHandler
        try:
            if(opcion == 1):
                direccionDelPuente = "Norte"
            elif(opcion == 2):
                direccionDelPuente = "Sur"
            if(not threading.current_thread() in self.conches):
                self.conches.append(threading.current_thread())
            for hilo in self.conches:
                logging.info(f'Coches apunto de cruzar el puente {hilo}')
            print(direccionDelPuente)
            for hilo in self.conches:
                print(hilo.getDireccion())
                if(hilo.getDireccion() == direccionDelPuente):
                    self.conches.remove(hilo)

        finally:
            for hilo in self.conches:
                logging.info(f'hilos restantes en la lista{hilo}')
            time.sleep(5)
            self.lock.release()
            
class CocheLadoSur(threading.Thread):
    def __init__(self,contadorMon):
        self.contador = contadorMon
        self.direccion = "Sur"
        super().__init__()
        

    def getDireccion(self):
        return self.direccion

    def run(self):
        while(True):
            self.contador.puente()

class CocheLadoNorte(threading.Thread):
    def __init__(self,contadorMon):
        self.contador = contadorMon
        self.direccion = "Norte"
        super().__init__()
        

    def getDireccion(self):
        return self.direccion

    def run(self):
        while(True):
            self.contador.puente()

def main():
    countMon = Monitor()
    hilos : threading.Thread = []

    for posicion in range(0,5):
        s = CocheLadoSur(countMon)
        n = CocheLadoNorte(countMon)
        hilos.append(s)
        hilos.append(n)
        s.start()
        n.start()
        logging.info(f'Arranca hilo{threading.current_thread().getName()} en la posicion {posicion+1}')

    for posicion in range(0,3):
        hilos[posicion].join()


if __name__ == "__main__":
    main()


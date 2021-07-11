import threading
import logging
import time
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Modificar la solución anterior para asegurar equitatividad. 
# Por ejemplo, permitir que como mucho C coches pasen en una dirección si hay coches esperando en la otra dirección


class Monitor():
    lock1 = threading.RLock()
    lock2 = threading.RLock()
    esperar = threading.Condition(lock1)
    conches  = []
    cantidadDeHilos = 0

    count  = 0

    def direccionDelPuente(self):
        opcion = random.randint(1,2)
        direccionDelPuente = ""
        if(opcion == 1):
            direccionDelPuente = "Norte"
        elif(opcion == 2):
            direccionDelPuente = "Sur"
        return direccionDelPuente

    def puente(self):
        self.lock1.acquire()
        try:
            
            if(not threading.current_thread() in self.conches):
                self.conches.append(threading.current_thread())
            for hilo in self.conches:
                logging.info(f'Coches apunto de cruzar el puente {hilo}')
            print(self.direccionDelPuente())

            cochesPermitidos = random.randint(1,10)
            for i in range(cochesPermitidos):
                if(i < len(self.conches)):
                    print( self.conches[i].getDireccion())
                    if self.conches[i].getDireccion() == self.direccionDelPuente():
                        self.conches.remove(self.conches[i])
                    else:
                        self.lock2.acquire()
                        try:
                            self.count += 1
                        finally:
                            self.lock2.release()
                        print("cantidad de hilos dormidos", (self.count))
                        #print("tamaño de la lista",len(self.conches),"y cantidad de hilos",self.cantidadDeHilos-1)
                        if(self.count == 10):
                            self.count = 0
                            self.esperar.notify_all()
                        self.esperar.wait()
        finally:
            for hilo in self.conches:
                logging.info(f'hilos restantes en la lista : { hilo.getDireccion()}')
            time.sleep(5)
            self.lock1.release()
            
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
    cantidad = 0

    for posicion in range(0,5):
        cantidad +=1
        s = CocheLadoSur(countMon)
        n = CocheLadoNorte(countMon)
        hilos.append(s)
        hilos.append(n)
        s.start()
        n.start()
        logging.info(f'Arranca hilo{threading.current_thread().getName()} en la posicion {posicion+1}')
    countMon.cantidadDeHilos = cantidad
    print(countMon.cantidadDeHilos)

   # for posicion in range(0,3):
    #    hilos[posicion].join()


if __name__ == "__main__":
    main()
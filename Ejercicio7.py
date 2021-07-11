import threading
import logging
import time
import random
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Implementar utilizando un monitor una relación de productor/consumidor entre tres procesos: generador, visualizador e impresor:

# El proceso generador generará caracteres en forma aleatoria (simula un usuario utilizando el teclado de un terminal) y 
# almacena esos caracteres en un buffer cíclico cuyo tamaño se corresponde con una línea en pantalla.

# El proceso visualizador recogerá los caracteres producidos por el generador y los introducirá en otro recurso de almacenamiento simulando una memoria 
# de pantalla con un tamaño preestablecido de varias líneas. Nota: la memoria de imagen puede ser un array bi-dimensional de n arrays 
# con el mismo tamaño que el buffer cíclico (linea).

# El proceso impresor enviará a la impresora (simulada por la pantalla) el contendio de la memoria de pantalla.

# Para resolver el problema además de las condiciones típicas del esquema productor/consumidor, se deben tener en cuenta las siguientes restricciones:

# 1- Cada vez que se llena la memoria de pantalla, para volver a utilizarla el proceso visualizador debe esperar a que el proceso impresor haya realizado la copia.

# 2- Una vez que se visualizaron todos los caracteres generados, el procesos impresor realizará la copia de la última pantalla aunque esta no este completa (llena).ç

# 3- Se puede suponer que la terminación de los proceos ocurrirá cuando se detecte un caracter especial.

class Monitor():
    lock = threading.RLock()
    saldo = 0
    caracteres = []
    esperar = threading.Condition(lock)


    def consumidor(self):
        pass

    def productor(self):
        pass


class Generador(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass


class Visualizador(threading.Thread):
    def __ini__(self):
        super().__init__()

    def run(self):
        pass


class Impresor(threading.Thread):
    def __init__(self,contadorMon):
        super().__init__()
        self.contador = contadorMon

    def run(self):
        pass

                
def main():
    countMon = Monitor()
    hilos : threading.Thread = []

    for posicion in range(0,5):
        #d = HiloPersona(countMon)
        #hilos.append(d)
      #  d.start()
        logging.info(f'Arranca hilo{threading.current_thread().getName()} en la posicion {posicion+1}')

    for posicion in range(0,3):
        hilos[posicion].join()


if __name__ == "__main__":
    main()

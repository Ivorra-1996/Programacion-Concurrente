

class HiloContador():
    def __init__(self,contadorMon):
        self.contador = contadorMon

    def run(self):
        for i  in range(0,1000000):
            self.contador.incrementar()

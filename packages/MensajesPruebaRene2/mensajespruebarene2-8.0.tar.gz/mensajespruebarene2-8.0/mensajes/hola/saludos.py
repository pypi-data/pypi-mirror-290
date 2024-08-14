import numpy as np

def saludar():
    print("buenas, te saludo desde saludos.saludar()")

def prueba ():
    print('Esto es una NUEVA prueba de la nueva version 8.0 ;)')

def generar_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__ (self):
        print("Ahora te saludo desde Saludo.__init__()")


if __name__ == '__main__':
    print(generar_array(5))
   
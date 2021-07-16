from random import randint as sorteio
from threading import Thread as Corrente

class SimFixos:
    def __init__(self):
        self.area = int(input("Qual a área do seu mapa?\n _ "))
        self.alimento = int(input("Qual a quantidade inicial de alimento?\n _ "))
        self.mapa = (self.area, self.area)


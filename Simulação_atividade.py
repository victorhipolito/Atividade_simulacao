from random import randint as sorteio
from threading import Thread as Corrente

class SimFixos:
    def __init__(self):
        while True:
            self.area = int(input("Qual o tamanho do seu mapa?\n(Valor x Valor)\n _ "))
            self.alimento = int(input("Qual a quantidade inicial de alimento?\n _ "))
            self.pos_alimento = list()
            if self.alimento > self.area**2:
                print("Valor de alimento inválido.")
                continue
            else:
                break

    def gerar_alimento(self):
        for _ in range(0,self.alimento):
            check = True
            while check:
                pos = [sorteio(1,self.area),sorteio(1,self.area)]
                if len(self.pos_alimento) > 1:
                    rep = False
                    for alimento in self.pos_alimento:
                        if alimento == pos:
                            rep = True
                    if not rep:
                        self.pos_alimento.append(pos)
                        check = False
                else:
                    self.pos_alimento.append(pos)
                    check = False

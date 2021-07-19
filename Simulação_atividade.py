# Existem duas raças, vermelha e verde.
# A única forma de se alimentar é através de uma unidade de comida.
# Para sobreviver a raça verde precisa comer uma unidade de comida e para reproduzir, duas.
# Para a raça vermelha sobreviver, ela precisa comer uma unidade de comida, e para reproduzir, uma e meia.
# Se duas pessoas da mesma espécie pegarem a mesma comida, elas dividem a comida no meio.
# Se duas pessoas de espécies diferentes tentarem comer o mesmo alimento, alguma delas é escolhida aleatoriamente.
# A cada dois dias, alguém da raça vermelha morre, a cada 3 dias alguém da raça verde morre.
# A cada dia q passa todos os sobreviventes ganham uma geração.
# Quantos de cada+ raça morreram, quantos foram gerados e a porcentagem de um sobre o outro.

from random import randint as sorteio
from threading import Thread as Corrente
from time import sleep

class SimFixos:
    def __init__(self):
        while True:
            self.area = int(input("Qual o tamanho do seu mapa?\n(Valor x Valor)\n _ "))
            self.alimento = int(input("Qual a quantidade inicial de alimento?\n _ "))
            self.gen_alimento = int(input("A geração posterior de alimento será de quantas em quantas rodadas?\n _ "))
            self.pos_alimento = list()
            if self.alimento > self.area**2:
                print("Valor de alimento inválido.")
                continue
            else:
                break
        self.rodada = 0

    def gerar_alimento(self):
        # Gerar comida inicialmente
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
        # Gerar comida em x rodadas
        if self.rodada % self.gen_alimento == 0:
            while True:
                pos = [sorteio(1, self.area), sorteio(1, self.area)]
                rep = False
                for alimento in self.pos_alimento:
                    if alimento == pos:
                        rep = True
                if not rep:
                    self.pos_alimento.append(pos)
                    break

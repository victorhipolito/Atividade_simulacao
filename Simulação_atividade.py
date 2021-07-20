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
from random import choice as escolha
from threading import Thread as Corrente
from time import sleep
from func_xtra import modulo, dis_vet

class SimGerar:
    def __init__(self):
        while True:
            self.area = int(input("Qual o tamanho do seu mapa?\n(Valor x Valor)\n _ "))
            self.num_verdes = int(input("Qual a quantidade inicial de seres da espécie verde?\n _ "))
            self.num_vermelhos = int(input("Qual a quantidade inicial de seres da espécie vermelha?\n _ "))
            self.alimento = int(input("Qual a quantidade inicial de alimento?\n _ "))
            self.gen_alimento = int(input("A geração posterior de alimento será de quantas em quantas rodadas?\n _ "))

            if self.alimento + self.num_vermelhos + self.num_verdes > self.area**2:
                print("Valores inválidos.")
                continue
            else:
                break
        self.pos_alimento = list()
        self.verdes = list()
        self.vermelhos = list()
        self.pos_tudo = list()
        self.rodada = 1
        self.gerar_alimento()
        self.gerar_especies()

    def gerar_pos(self, item, tipo):
        check = True
        while check:
            pos = [sorteio(1, self.area), sorteio(1, self.area)]
            if len(self.pos_tudo) >= 1:
                rep = False
                for unit in self.pos_tudo:
                    if unit[1] == pos:
                        rep = True
                if not rep:
                    if item != self.pos_alimento:
                        item.append([pos])
                    else:
                        item.append(pos)
                    self.pos_tudo.append([tipo,pos])
                    check = False
            else:
                if item != self.pos_alimento:
                    item.append([pos])
                else:
                    item.append(pos)
                self.pos_tudo.append([tipo,pos])
                check = False

    def gerar_alimento(self):
        # Gerar comida inicialmente
        if self.pos_alimento == list():
            for _ in range(0,self.alimento):
                self.gerar_pos(self.pos_alimento, "Alimento")
        # Gerar comida em x rodadas
        if self.rodada % self.gen_alimento == 0:
            self.gerar_pos(self.pos_alimento, "Alimento")

    # O verde vai ter 5 rodadas de vida, e o vermelho 10
    def gerar_especies(self):
        for _ in range(0,self.num_verdes):
            self.gerar_pos(self.verdes, "Verde")
            self.verdes[len(self.verdes) - 1].append(5)
            print(self.verdes)
        for _ in range(0,self.num_vermelhos):
            self.gerar_pos(self.vermelhos, "Vermelho")
            self.vermelhos[len(self.vermelhos) - 1].append(10)


class SimComportamento(SimGerar):
    def __init__(self):
        super().__init__()

    def comp_escolherComida(self, especie):
        comida_perto = list()
        for ser in especie:
            print(ser)
            dis_menor = None
            for alimento in self.pos_alimento:
                if alimento == self.pos_alimento[0]:
                    dis_menor = alimento
                    ser.append(dis_menor)
                else:
                    if dis_vet(ser[0],alimento) < dis_vet(ser[0], dis_menor):
                        dis_menor = alimento
                        ser[2] = dis_menor
                    elif dis_vet(ser[0],alimento) == dis_vet(ser[0], dis_menor):
                        dis_menor = escolha([alimento, dis_menor])
                        ser[2] = dis_menor
            comida_perto.append(ser)
        return comida_perto


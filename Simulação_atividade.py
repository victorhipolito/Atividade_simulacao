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
            self.num_rodadas = int(input("Qual o número de rodadas que você quer ver?\n _ "))

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
            self.verdes[len(self.verdes) - 1].append(0.0)
        for _ in range(0,self.num_vermelhos):
            self.gerar_pos(self.vermelhos, "Vermelho")
            self.vermelhos[len(self.vermelhos) - 1].append(10)
            self.vermelhos[len(self.vermelhos) - 1].append(0.0)


class SimComportamento(SimGerar):
    def __init__(self):
        super().__init__()
        while self.num_rodadas != self.rodada:
            self.comp_movimento(self.verdes)
            self.comp_movimento(self.vermelhos)
            self.comp_reproduzir(self.verdes,1.0,"Verde")
            self.comp_reproduzir(self.vermelhos,2.0,"Vermelho")
            self.comp_tempodeVida()

    def comp_escolherComida(self, especie):
        comida_perto = list()
        for ser in especie:
            dis_menor = None
            for alimento in self.pos_alimento:
                if alimento == self.pos_alimento[0]:
                    dis_menor = alimento
                    ser.append(dis_menor)
                else:
                    if dis_vet(ser[0],alimento) < dis_vet(ser[0], dis_menor):
                        dis_menor = alimento
                        ser[3] = dis_menor
                    elif dis_vet(ser[0],alimento) == dis_vet(ser[0], dis_menor):
                        dis_menor = escolha([alimento, dis_menor])
                        ser[3] = dis_menor
            comida_perto.append(ser)
        return comida_perto

    def comp_movimento(self,especie):
        for org in self.comp_escolherComida(especie):
            getdis = [org[3][0]-org[0][0],org[3][1]-org[0][1]]
            if dis_vet(org[0],org[3]) == 1:
                self.comp_comer(org)

            elif getdis[0] < -1 or getdis[0] > 1:
                mov = getdis[0] // modulo(getdis[0])
                novapos = especie[especie.index([org[0], org[1], org[2]])][0][0] + mov
                sobrepos = False
                for animal in self.pos_tudo:
                    if animal[1] == [novapos,especie[especie.index([org[0],org[1],org[2]])][0][1]] and animal[0] != "Alimento":
                        sobrepos = True
                if not sobrepos:
                    especie[especie.index([org[0],org[1],org[2]])][0][0] = novapos
                    if especie == self.verdes:
                        self.pos_tudo[self.pos_tudo.index(["Verde",[org[0]]])][1][0] = novapos
                    else:
                        self.pos_tudo[self.pos_tudo.index(["Vermelho",[org[0]]])][1][0] = novapos

            elif getdis[1] < -1 or getdis[1] > 1 and getdis[0] == 1:
                mov = getdis[1] // modulo(getdis[1])
                novapos = especie[especie.index([org[0],org[1],org[2]])][0][1] + mov
                sobrepos = False
                for animal in self.pos_tudo:
                    if animal[1] == [especie[especie.index([org[0],org[1],org[2]])][0][0],novapos] and animal[0] != "Alimento":
                        sobrepos = True
                if not sobrepos:
                    especie[especie.index([org[0],org[1],org[2]])][0][1] = novapos
                    if especie == self.verdes:
                        self.pos_tudo[self.pos_tudo.index(["Verde",[org[0]]])][1][1] = novapos
                    else:
                        self.pos_tudo[self.pos_tudo.index(["Vermelho",[org[0]]])][1][1] = novapos

    def comp_comer(self, ser):
        oser = None
        for bicho in self.pos_tudo:
            if bicho[1] == ser[0]:
                oser = bicho
        for compare in self.comp_escolherComida(self.verdes):
            if dis_vet(compare[3], compare[0]) == 1 and compare[0] != oser[1]:
                if oser[0] == "Verdes":
                    self.verdes[self.verdes.index([compare[0],compare[1],compare[2]])][2] += 0.5
                    self.verdes[self.verdes.index([ser[0],ser[1],ser[2]])][2] += 0.5
                    self.pos_alimento.remove([self.pos_alimento.index(ser[3])])
                    self.pos_tudo.remove(["Alimento", self.pos_tudo.index(["Alimento", ser[3]])])
                else:
                    if sorteio(1,2) == 1:
                        self.verdes[self.verdes.index([compare[0], compare[1], compare[2]])][2] += 1.0
                        self.pos_alimento.remove([self.pos_alimento.index(ser[3])])
                        self.pos_tudo.remove(["Alimento", self.pos_tudo.index(["Alimento", ser[3]])])
                    else:
                        self.vermelhos[self.vermelhos.index([ser[0], ser[1], ser[2]])][2] += 1.0
                        self.pos_alimento.remove([self.pos_alimento.index(ser[3])])
                        self.pos_tudo.remove(["Alimento", self.pos_tudo.index(["Alimento", ser[3]])])
                break
        for compare in self.comp_escolherComida(self.vermelhos):
            if dis_vet(compare[0], compare[3]) == 1 and compare[0] != oser[1]:
                if oser[0] == "Vermelhos":
                    self.vermelhos[self.vermelhos.index([compare[0],compare[1],compare[2]])][2] += 0.5
                    self.vermelhos[self.vermelhos.index([ser[0],ser[1],ser[2]])][2] += 0.5
                    self.pos_alimento.remove([self.pos_alimento.index(ser[3])])
                    self.pos_tudo.remove(["Alimento", self.pos_tudo.index(["Alimento", ser[3]])])
                else:
                    if sorteio(1,2) == 1:
                        self.verdes[self.verdes.index([ser[0], ser[1], ser[2]])][2] += 1.0
                        self.pos_alimento.remove([self.pos_alimento.index(ser[3])])
                        self.pos_tudo.remove(["Alimento", self.pos_tudo.index(["Alimento", ser[3]])])
                    else:
                        self.vermelhos[self.vermelhos.index([compare[0], compare[1], compare[2]])][2] += 1.0
                        self.pos_alimento.remove([self.pos_alimento.index(ser[3])])
                        self.pos_tudo.remove(["Alimento", self.pos_tudo.index(["Alimento", ser[3]])])
                break

    def comp_reproduzir(self, bicho, comida, tipo):
        for ser in bicho:
            pert_ser = [[ser[0][0]-1,ser[0][1]],[ser[0][0],ser[0][1]-1],[ser[0][0]+1,ser[0][1]],[ser[0][0],ser[0][1]+1]]
            if ser[2] >= comida:
                bicho[bicho.index(ser)][2] = 0.0
                sobrepos = False
                ladoobs = list()
                for coisa in self.pos_tudo:
                    for lado in pert_ser:
                        if coisa[1] == lado:
                            ladoobs.append(lado)
                for lado in pert_ser:
                    for pos in lado:
                        if not 0 < pos < 11:
                            ladoobs.append(lado)
                for rep in ladoobs:
                    pert_ser.remove(rep)
                if pert_ser != []:
                    pos_def = escolha(pert_ser)
                    self.pos_tudo.append([tipo,pos_def])
                    bicho.append([pos_def,int(comida*5),0.0])

    def comp_tempodeVida(self):
        self.rodada += 1
        for verminho in self.vermelhos:
            self.vermelhos[self.vermelhos.index(verminho)][1] -= 1
        for verdinho in self.verdes:
            self.verdes[self.verdes.index(verdinho)][1] -= 1
        mortos_vermelhos = list()
        mortos_verdes = list()
        for verminho in self.vermelhos:
            if self.vermelhos[self.vermelhos.index(verminho)][1] <= 0:
                mortos_vermelhos.append(verminho)
        for verdinho in self.verdes:
            if self.verdes[self.verdes.index(verdinho)][1] <= 0:
                mortos_verdes.append(verdinho)
        for f in mortos_vermelhos:
            self.vermelhos.remove(f)
            self.pos_tudo.remove(["Vermelho",f[0]])
        for f in mortos_verdes:
            self.verdes.remove(f)
            self.pos_tudo.remove(["Verde",f[0]])


SimComportamento()

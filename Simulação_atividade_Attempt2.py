# Existem duas raças, vermelha e verde
# A única forma de se alimentar é através de uma unidade de comida
# Para sobreviver a raça verde precisa comer uma unidade de comida e para reproduzir, duas
# Para a raça vermelha sobreviver, ela precisa comer uma unidade de comida, e para reproduzir, uma e meia
# Se duas pessoas da mesma espécie pegarem a mesma comida, elas dividem a comida no meio
# Se duas pessoas de espécies diferentes tentarem comer o mesmo alimento, alguma delas é escolhida aleatoriamente
# A cada dois dias, alguém da raça vermelha morre, a cada 3 dias alguém da raça verde morre
# A cada dia q passa todos os sobreviventes ganham uma geração
# Quantos de cada raça morreram, quantos foram gerados e a porcentagem de um sobre o outro

from random import randint as sorteio
from random import choice as escolha
from threading import Thread as Corrente
from func_xtra import modulo, dis_vet, maior


# Essa classe será responsável por gerar os termos, desde o mapa até os alimentos e seres.
class Geracao:
    def __init__(self):
        # Area do mapa.
        self.area = int(input("Qual será a área do seu mapa?\n(Valor X Valor)\n _ "))
        # While que checa se a quantidade de comida, de verdes e vermelhos é menor que a área do mapa.
        while True:
            self.qt_comida = int(input("Quantas comidas serão geradas no mapa?\n _ "))
            self.qt_verdes = int(input("Quantos verdes serão gerados no mapa?\n _ "))
            self.qt_vermelhos = int(input("Quantos vermelhos serão gerados no mapa?\n _ "))
            if self.qt_vermelhos + self.qt_verdes + self.qt_comida <= self.area**2:
                break
            else:
                print("Você colocou valores que excedem o limite do mapa, tente novamente")
        self.taxa_alimentos = int(input("De quantas em quantas rodadas um alimento novo será gerado?\n _ "))
        self.lim_rodadas = int(input("Até que rodada você quer ver a simulação?\n _ "))
        # Variável de rodada e array de todos os termos do mapa juntos, uma apenas de alimentos e outra apenas de seres.
        self.rodada = 1
        self.tudo = list()
        self.seres = list()
        self.alimento = list()
        self.estatisticas = [["Alimentos", 0], ["Verdes", 0], ["Vermelhos", 0], ["Mortos verdes", 0], ["Mortos vermelhos", 0]]
        # Geração de tudo com base nas variáveis de input.
        self.gerar_posicao(self.seres, tipo="Ser", qt=self.qt_verdes, vida=3, ser="Verde", infos=[0.0, 2.0, 3])
        self.gerar_posicao(self.seres, tipo="Ser", qt=self.qt_vermelhos, vida=2, ser="Vermelho", infos=[0.0, 1.5, 2])
        self.gerar_posicao(self.alimento, qt=self.qt_comida)

    # Função que gera posições, com apenas um parâmetro obrigatório, que é a array onde vão ser adicionados os termos.
    # De padrão, essa função funciona para alimentos mas é possível gerar seres com a mesma.
    def gerar_posicao(self, array, tipo="Alimento", qt=1, vida=None, ser=None, infos=None):
        # If para geração de alimentos.
        if tipo == "Alimento":
            self.estatisticas[0][1] += qt
            for _ in range(0, qt):
                check = True
                while check:
                    pos = [sorteio(1, self.area), sorteio(1, self.area)]
                    if len(self.tudo) >= 1:
                        rep = False
                        for unit in self.tudo:
                            if unit[1] == pos:
                                rep = True
                        if not rep:
                            self.tudo.append(pos)
                            array.append(pos)
                            check = False
                    else:
                        self.tudo.append(pos)
                        array.append(pos)
                        check = False

        # If para geração de seres.
        elif tipo == "Ser":
            if ser == "Verde":
                self.estatisticas[1][1] += qt
            else:
                self.estatisticas[2][1] += qt
            for _ in range(0, qt):
                check = True
                while check:
                    pos = [sorteio(1, self.area), sorteio(1, self.area)]
                    if len(self.tudo) >= 1:
                        rep = False
                        for unit in self.tudo:
                            if unit[1] == pos:
                                rep = True
                        if not rep:
                            self.tudo.append(pos)
                            array.append([ser, vida, infos, pos])
                            check = False
                    else:
                        self.tudo.append(pos)
                        array.append([ser, vida, infos, pos])
                        check = False

    # Função que usa a taxa de geração de alimentos como base para gerar em um intervalo definido de rodadas.
    def geracao_rodadas(self):
        if self.rodada % self.taxa_alimentos == 0:
            self.gerar_posicao(self.alimento)


class Acao(Geracao):
    def __init__(self):
        super().__init__()
        while self.rodada <= self.lim_rodadas:
            self.movimento()
            comer = Corrente(target=self.comer())
            comer.start()
            rep = Corrente(target=self.reproducao())
            rep.start()
            comer.join()
            rep.join()
            self.vida()
            self.geracao_rodadas()
        numf = [0, 0]
        print("As estatisticas finais foram: ")
        for ser in self.seres:
            if ser[0] == "Verde":
                numf[0] += 1
            else:
                numf[1] += 1
        if 0 in numf:
            if numf[0] + numf[1] < 1:
                print(f"Nenhuma das espécies sobreviveu.")
            else:
                if maior(numf) == 0:
                    print(f"A espécie Verde foi a única que sobreviveu.")
                else:
                    print(f"A espécie Vermelha foi a única que sobreviveu.")
        else:
            if maior(numf) == 0:
                print(f"O Verde foi aproximadamente {int((numf[1]*numf[0])/100)}% maior do que o Vermelho no final.")
            else:
                print(f"O Vermelho foi aproximadamente {int((numf[1]*numf[0])/100)}% maior do que o Verde no final.")

        print("+="*30 + f"\nVerdes no final: {numf[0]}\nVermelhos no final: {numf[1]}")
        for est in self.estatisticas:
            print("+="*30 + f"\n{est[0]}: {est[1]}")

    def procurar_alimento(self):
        comida_perto = list()
        for index, ser in enumerate(self.seres):
            if len(self.alimento) != 0:
                dis_menor = self.alimento[0]
                for comida in self.alimento:
                    if dis_vet(ser[3], comida) < dis_vet(dis_menor, ser[3]):
                        dis_menor = comida
                    elif dis_vet(ser[3], comida) == dis_vet(dis_menor, ser[3]):
                        dis_menor = escolha([comida, dis_menor])
                comida_perto.append((index, dis_menor))
        return comida_perto

    def movimento(self):
        for index, alimento in self.procurar_alimento():
            getdis = [self.seres[index][3][0]-alimento[0],self.seres[index][3][1]-alimento[1]]
            if modulo(getdis[0])+modulo(getdis[1]) > 1:
                ind = maior(getdis)
                novapos = self.seres[index][3].copy()
                try:
                    novapos[ind] -= getdis[ind] // modulo(getdis[ind])
                except ZeroDivisionError:
                    novapos[ind] -= getdis[ind]
                sobreposicao = False
                for ser in self.seres:
                    if ser[3] == novapos:
                        sobreposicao = True
                if not sobreposicao:
                    self.tudo[self.tudo.index(self.seres[index][3])] = novapos
                    self.seres[index][3] = novapos

    def comer(self):
        for index, alimento in self.procurar_alimento():
            if dis_vet(alimento, self.seres[index][3]) <= 1 and alimento in self.alimento:
                competiu = False
                for ser in self.seres:
                    if dis_vet(ser[3], alimento) <= 1 and ser != self.seres[index]:
                        competiu = True
                        if ser[0] == self.seres[index][0]:
                            self.seres[index][2][0] += 0.5
                            self.seres[index][1] += 1
                            self.seres[self.seres.index(ser)][2][0] += 0.5
                        else:
                            resul = escolha([self.seres.index(ser), index])
                            self.seres[resul][2][0] += 1.0
                            self.seres[resul][1] += 1
                        break
                if not competiu:
                    self.seres[index][2][0] += 1.0
                    self.seres[index][1] += 1
                self.alimento.remove(alimento)
                self.tudo.remove(alimento)

    def reproducao(self):
        for ser in self.seres:
            if ser[2][0] >= ser[2][1]:
                max = 0
                while max < 4:
                    pos = [sorteio(0,1), escolha([-1,1])]
                    newborn = ser[3].copy()
                    newborn[pos[0]] += pos[1]
                    if newborn in self.tudo:
                        max += 1
                        continue
                    else:
                        self.tudo.append(newborn)
                        definitivo = ser.copy()
                        definitivo = [definitivo[0],definitivo[2][2],[0.0,definitivo[2][1],definitivo[2][2]],newborn.copy()]
                        self.seres.append(definitivo)
                        self.seres[self.seres.index(ser)][2][0] -= self.seres[self.seres.index(ser)][2][1]
                        for ind, est in enumerate(self.estatisticas):
                            if definitivo[0] + "s" == est[0]:
                                self.estatisticas[ind][1] += 1
                        break

    def vida(self):
        self.rodada += 1
        condenados = list()
        numf = [0, 0]
        for index, ser in enumerate(self.seres):
            self.seres[index][1] -= 1
            if ser[1] <= 0:
                condenados.append(ser)
                if ser[0] == "Verde":
                    numf[0] += 1
                else:
                    numf[1] += 1
        if len(condenados) >= 1:
            for f in condenados:
                self.seres.remove(f)
                self.tudo.remove(f[3])
        self.estatisticas[3][1] += numf[0]
        self.estatisticas[4][1] += numf[1]


Acao()
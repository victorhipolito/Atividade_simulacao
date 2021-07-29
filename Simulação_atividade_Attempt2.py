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
from time import sleep
from func_xtra import modulo, dis_vet

# Essa classe será responsável por gerar os termos, desde o mapa até os alimentos e seres.
class Geracao:
    def __init__(self):
        # Area do mapa
        self.area = int(input("Qual será a área do seu mapa?\n(Valor X Valor)\n _ "))
        # While que checa se a quantidade de comida, de verdes e vermelhos é menor que a área do mapa
        while True:
            self.qt_comida = int(input("Quantas comidas serão geradas no mapa?\n _ "))
            self.qt_verdes = int(input("Quantos verdes serão gerados no mapa?\n _ "))
            self.qt_vermelhos = int(input("Quantos vermelhos serão gerados no mapa?\n _ "))
            if self.qt_vermelhos + self.qt_verdes + self.qt_comida < self.area:
                break
            else:
                print("Você colocou valores que excedem o limite do mapa, tente novamente")
        self.taxa_alimentos = int(input("De quantas em quantas rodadas um alimento novo será gerado?\n _ "))
        # Variável de rodada e arrays de todos os termos do mapa juntos, uma apenas de alimentos e outra apenas de seres.
        self.rodada = 1
        self.tudo = list()
        self.seres = list()
        self.alimento = list()


    def gerar_posicao(self, array, tipo="Alimento", qt=1, vida=None, ser=None):
        if tipo == "Alimento":
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
                            self.tudo.append([tipo, pos])
                            array.append([pos])
                            check = False
                    else:
                        self.tudo.append([tipo, pos])
                        array.append([pos])
                        check = False

        elif tipo == "Ser":
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
                            self.tudo.append([ser, pos])
                            array.append([ser, vida, 0.0, pos])
                            check = False
                    else:
                        self.tudo.append([ser, pos])
                        array.append([ser, vida, 0.0, pos])
                        check = False

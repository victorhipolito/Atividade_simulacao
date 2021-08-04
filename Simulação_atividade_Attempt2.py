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
        # A array self.tudo guarda apenas a posição de todos os seres e alimentos no mapa.
        self.tudo = list()
        # A array self.seres guarda uma série de informações:
        # O tipo da espécie, a vida atual, a posição e uma outra array interna que guarda a
        # quantidade de comida que o ser já consumiu, a quantidade que ele precisa pra reproduzir e a vida máxima dele.
        self.seres = list()
        # A array self.alimento guarda apenas a posição dos alimentos no mapa.
        self.alimento = list()
        # Array que armazena as estatísticas que aparecerão no final da simulação.
        self.estatisticas = [["Alimentos", 0], ["Verdes", 0], ["Vermelhos", 0],
                             ["Mortos verdes", 0], ["Mortos vermelhos", 0]]
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


# Classe que Determina a ação dos seres, sendo essas: encontrar comida, comer, andar, reproduzir e morrer.
# A classe também inclui as estatísticas finais e usa herança para usar o que existe da classe Geração.
class Acao(Geracao):
    def __init__(self):
        # Definindo herança de Geracao()
        super().__init__()
        # Rodando as funções na ordem.
        # Primeiramente, a função comer() e reproducao() estão em Thread.
        # Entretanto, a função movimento é a única que não espera o fim da Thread para funcionar.
        # As funções "vida" e "geração_rodadas" não podem funcionar junto da Thread pois
        # elas têm influência direta ou com o número da rodada, ou com o funcionamento da mesma.
        while self.rodada <= self.lim_rodadas:
            comer = Corrente(target=self.comer())
            comer.start()
            rep = Corrente(target=self.reproducao())
            rep.start()
            self.movimento()
            comer.join()
            rep.join()
            self.vida()
            self.geracao_rodadas()
        # Essa última seção do __init__ é direcionada apenas para a apresentação das estatísticas da simulação.
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

    # A função de procurar alimento acha o alimento mais próximo e relaciona com a index do ser.
    def procurar_alimento(self):
        comida_perto = list()
        for index, ser in enumerate(self.seres):
            # Se houverem comidas no mapa, ele checa comida por comida para ver qual a mais perto do ser.
            if len(self.alimento) != 0:
                dis_menor = self.alimento[0]
                for comida in self.alimento:
                    if dis_vet(ser[3], comida) < dis_vet(dis_menor, ser[3]):
                        dis_menor = comida
                    elif dis_vet(ser[3], comida) == dis_vet(dis_menor, ser[3]):
                        dis_menor = escolha([comida, dis_menor])
                # Para cada index, o programa coloca uma tupla com ela e a comida mais perto do ser equivalente,
                # para no final retornar essa relação no comida_perto.
                comida_perto.append((index, dis_menor))
        return comida_perto

    # A função movimento usa como base o que foi retornado na função procurar_alimento para se movimentar.
    def movimento(self):
        for index, alimento in self.procurar_alimento():
            # A variável getdis pega a distância separada de x e y do ser em relação a comida.
            getdis = [self.seres[index][3][0]-alimento[0], self.seres[index][3][1]-alimento[1]]
            # Se o ser estiver a mais de 1 de distância da comida,
            # ele calcula uma nova posição, movendo 1 no vetor em que ele está mais longe.
            if modulo(getdis[0])+modulo(getdis[1]) > 1:
                ind = maior(getdis)
                novapos = self.seres[index][3].copy()
                # O try evita que haja uma divisão por 0 quando o ser está do lado da comida.
                try:
                    novapos[ind] -= getdis[ind] // modulo(getdis[ind])
                except ZeroDivisionError:
                    novapos[ind] -= getdis[ind]
                # Esta parte evita que haja sobreposição de seres no mapa
                sobreposicao = False
                for ser in self.seres:
                    if ser[3] == novapos:
                        sobreposicao = True
                # Por ultimo, essa parte define a nova posição dos seres no self.tudo e self.seres.
                if not sobreposicao:
                    self.tudo[self.tudo.index(self.seres[index][3])] = novapos
                    self.seres[index][3] = novapos

    # A função comer checa se o ser está a pelo menos 1 de distância da comida para comê-la.
    def comer(self):
        for index, alimento in self.procurar_alimento():
            if dis_vet(alimento, self.seres[index][3]) <= 1 and alimento in self.alimento:
                competiu = False
                # O for checa se houve competição para o alimento, ou seja, se houveram mais de 1 ser perto da comida.
                for ser in self.seres:
                    if dis_vet(ser[3], alimento) <= 1 and ser != self.seres[index]:
                        competiu = True
                        # Se os seres são da mesma espécie, eles dividem a comida.
                        if ser[0] == self.seres[index][0]:
                            self.seres[index][2][0] += 0.5
                            self.seres[index][1] += 1
                            self.seres[self.seres.index(ser)][2][0] += 0.5
                            self.seres[self.seres.index(ser)][1] += 1
                        else:
                            # Se os seres são de especies diferentes, o ganhador do alimento é sorteado.
                            resul = escolha([self.seres.index(ser), index])
                            self.seres[resul][2][0] += 1.0
                            self.seres[resul][1] += 1
                        break
                if not competiu:
                    # Se não houve competição, o ser come só e come bem.
                    self.seres[index][2][0] += 1.0
                    self.seres[index][1] += 1
                # Por fim, o programa remove o alimento.
                self.alimento.remove(alimento)
                self.tudo.remove(alimento)

    # A função reprodução checa se o ser tem o valor mínimo necessário de comida consumida para reproduzir.
    def reproducao(self):
        # O programa checa ser por ser para saber se algum apresenta a quantidade mínima para reproduzir.
        for ser in self.seres:
            if ser[2][0] >= ser[2][1]:
                # O maxpos é uma delimitação para impedir que o programa rode em loop para sempre;
                # se não houver espaço para reproduzir, o ser espera até a próxima rodada.
                maxpos = 0
                while maxpos < 4:
                    # A escolha da posição de nascimento define onde que o ser vai nascer,
                    # sendo obrigatoriamente na tangente do ser que reproduziu
                    pos = [sorteio(0, 1), escolha([-1, 1])]
                    newborn = ser[3].copy()
                    newborn[pos[0]] += pos[1]
                    if newborn in self.tudo:
                        maxpos += 1
                        continue
                    else:
                        # Caso não haja outro ser no local de nascimento,
                        # o programa adiciona a nova posição no self.tudo e herda as informações do
                        # ser que reproduziu para o ser que 'nasceu'.
                        self.tudo.append(newborn)
                        definitivo = ser.copy()
                        definitivo = [definitivo[0], definitivo[2][2],
                                      [0.0, definitivo[2][1], definitivo[2][2]], newborn.copy()]
                        self.seres.append(definitivo)
                        # Por último, o programa retira a comida necessária pra reprodução do ser que reproduziu.
                        self.seres[self.seres.index(ser)][2][0] -= self.seres[self.seres.index(ser)][2][1]
                        # Esse for é apenas para adicionar o ser novo nas estatísticas.
                        for ind, est in enumerate(self.estatisticas):
                            # noinspection PyTypeChecker
                            if definitivo[0] + "s" == est[0]:
                                self.estatisticas[ind][1] += 1
                        break

    # A função vida vai somando rodadas durante a simulação, além de checar quais seres morreram e removê-los da lista.
    def vida(self):
        self.rodada += 1
        condenados = list()
        numf = [0, 0]
        # O for armazena quais seres morreram e vão adicionando na array 'condenados'.
        for index, ser in enumerate(self.seres):
            self.seres[index][1] -= 1
            if ser[1] <= 0:
                condenados.append(ser)
                # Essa parte é dedicada a contar as estatísticas dos mortos verdes e vermelhos, adicionando em 'numf'.
                if ser[0] == "Verde":
                    numf[0] += 1
                else:
                    numf[1] += 1
        # Após armazenar os mortos em condenados,
        # ele remove todos presentes no self.tudo e no self.seres.
        if len(condenados) >= 1:
            for f in condenados:
                self.seres.remove(f)
                self.tudo.remove(f[3])
            condenados.clear()
        # Adicionando os mortos nas estatísticas.
        self.estatisticas[3][1] += numf[0]
        self.estatisticas[4][1] += numf[1]


Acao()

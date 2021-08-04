from random import choice


# A modulo checa se o número é negativo, se for, ele transforma em positivo
def modulo(a):
    if a < 0:
        a *= -1
    return a


# A dis_vet checa a distância entre 2 vetores a partir da modulo.
def dis_vet(a, b):
    return modulo(a[0]-b[0])+modulo(a[1]-b[1])


# A maior pega uma array e indica a index do maior termo da array.
# Se existirem 2 termos maiores, o programa faz um sorteio entre eles.
def maior(a):
    final = 0
    for num, _ in enumerate(a):
        if _ > a[final]:
            final = num
        elif _ == a[final]:
            final = choice([final, num])
    return final

from random import choice
def modulo(a):
    if a < 0:
        a *= -1
    return a

def dis_vet(a,b):
    return modulo(a[0]-b[0])+modulo(a[1]-b[1])

def maior(a=list()):
    final = 0
    for num, _ in enumerate(a):
        if _ > a[final]:
            final = num
        elif _ == a[final]:
            final = choice([final, num])
    return final

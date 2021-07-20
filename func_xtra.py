def modulo(a):
    if a < 0:
        a *= -1
    return a

def dis_vet(a,b):
    return modulo(a[0]-b[0])+modulo(a[1]-b[1])
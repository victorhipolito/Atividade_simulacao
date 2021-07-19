def modulo(a):
    if a < 0:
        a *= -1
    return a

def dis_vet(a,b):
    return (modulo(a[0])-modulo(b[0]))+(modulo(a[1])-modulo(b[1]))
"""🥞 Soluciones — Pila (stack)"""


def apilar(pila, x):
    pila.append(x)
    return pila


def desapilar(pila):
    if not pila:
        return None
    return pila.pop()


def tope(pila):
    return pila[-1] if pila else None


def balanceado(texto):
    pila = []
    for c in texto:
        if c == "(":
            pila.append(c)
        elif c == ")":
            if not pila:
                return False
            pila.pop()
    return len(pila) == 0

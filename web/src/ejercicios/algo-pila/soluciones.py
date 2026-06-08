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


def esta_vacia(pila):
    return len(pila) == 0


def tamano(pila):
    return len(pila)


def tope_seguro(pila):
    if not pila:
        return None
    return pila[-1]


def apilar_varios(pila, elementos):
    for e in elementos:
        pila.append(e)
    return pila


def vaciar(pila):
    out = []
    while pila:
        out.append(pila.pop())
    return out


def invertir(lista):
    pila = []
    for e in lista:
        pila.append(e)
    out = []
    while pila:
        out.append(pila.pop())
    return out


def balanceado_todo(texto):
    pares = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in texto:
        if c in "([{":
            pila.append(c)
        elif c in ")]}":
            if not pila or pila.pop() != pares[c]:
                return False
    return len(pila) == 0


def profundidad_maxima(texto):
    prof = maxp = 0
    for c in texto:
        if c == "(":
            prof += 1
            if prof > maxp:
                maxp = prof
        elif c == ")":
            prof -= 1
    return maxp


def evaluar_postfija(tokens):
    pila = []
    for t in tokens:
        if t in ("+", "-", "*"):
            b = pila.pop()
            a = pila.pop()
            if t == "+":
                pila.append(a + b)
            elif t == "-":
                pila.append(a - b)
            else:
                pila.append(a * b)
        else:
            pila.append(int(t))
    return pila[-1]


def decimal_a_binario(n):
    if n == 0:
        return "0"
    pila = []
    while n > 0:
        pila.append(str(n % 2))
        n //= 2
    out = ""
    while pila:
        out += pila.pop()
    return out


def quitar_adyacentes(texto):
    pila = []
    for c in texto:
        if pila and pila[-1] == c:
            pila.pop()
        else:
            pila.append(c)
    return "".join(pila)


def es_palindromo_pila(texto):
    pila = list(texto)
    for c in texto:
        if c != pila.pop():
            return False
    return True


def simular_pila(operaciones):
    pila = []
    for op in operaciones:
        if op == "pop":
            if pila:
                pila.pop()
        else:
            pila.append(int(op.split()[1]))
    return pila


def invertir_texto(texto):
    pila = list(texto)
    out = ""
    while pila:
        out += pila.pop()
    return out


def pares_completos(texto):
    abiertos = 0
    pares = 0
    for c in texto:
        if c == "(":
            abiertos += 1
        elif c == ")" and abiertos > 0:
            abiertos -= 1
            pares += 1
    return pares


def sin_cerrar(texto):
    abiertos = 0
    for c in texto:
        if c == "(":
            abiertos += 1
        elif c == ")" and abiertos > 0:
            abiertos -= 1
    return abiertos

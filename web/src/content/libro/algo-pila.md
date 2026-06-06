---
title: "Algoritmos: Pila (stack)"
order: 1202
---

> 🎯 **Meta:** dominar la **pila** (LIFO), la estructura detrás del "deshacer", los paréntesis y la recursión.

---

Una **pila** es como una pila de platos: ponés arriba, sacás de arriba. **LIFO**: *last in, first out* — el último que entra es el primero que sale.

## Operaciones

Con una lista de Python, una pila es directa:

```python
pila = []
pila.append("a")    # push: poner arriba
pila.append("b")
tope = pila[-1]     # ver el de arriba  → "b"
ultimo = pila.pop() # pop: sacar el de arriba  → "b"
```

Tres operaciones: **push** (apilar), **pop** (desapilar), **peek** (ver el tope sin sacarlo).

## ¿Para qué sirve?

La pila aparece por todos lados:

- El botón **deshacer** (cada acción se apila; deshacer = pop).
- La **recursión** (Python usa una pila de llamadas internamente).
- Validar **paréntesis balanceados**:

```python
def balanceado(texto):
    pila = []
    for c in texto:
        if c == "(":
            pila.append(c)
        elif c == ")":
            if not pila:        # cierra sin abrir → mal
                return False
            pila.pop()          # casa un cierre con su apertura
    return len(pila) == 0       # no quedó nada abierto
```

> 💡 Si un problema dice "lo último primero" o "deshacer hacia atrás", pensá en una pila.

## ✅ Comprobá lo que aprendiste

```quiz
P: Una pila (stack) es…
+ LIFO: el último que entra es el primero que sale
- FIFO: el primero que entra sale primero
- una lista siempre ordenada
> Como una pila de platos: ponés y sacás de arriba.
```

```quiz
P: ¿Para cuál de estos sirve naturalmente una pila?
+ deshacer acciones / validar paréntesis
- atender una fila de turnos
- ordenar de menor a mayor
> "Lo último primero" → pila. Los turnos son cola (FIFO).
```

🥞 El **Líder Iono** te espera para apilar a lo grande.

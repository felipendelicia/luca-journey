---
title: "Algoritmos: Diccionarios y sets"
order: 1206
---

> 🎯 **Meta:** usar **diccionarios** y **sets** para contar, deduplicar y comparar a velocidad relámpago.

---

Buscar en una lista es lento (mirás uno por uno). Buscar en un **diccionario** o un **set** es casi instantáneo: usan una **tabla hash** que va directo al dato. Son la herramienta secreta de los programas rápidos.

## Contar frecuencias

El patrón más útil de todos:

```python
def frecuencias(items):
    f = {}
    for x in items:
        f[x] = f.get(x, 0) + 1   # .get(x, 0): cuánto llevaba, o 0
    return f

print(frecuencias(["a", "b", "a", "a"]))   # {"a": 3, "b": 1}
```

## Deduplicar con `set`

Un **set** es una colección sin repetidos y con búsqueda instantánea (`x in conjunto` es O(1)):

```python
def sin_duplicados(items):
    vistos = set()
    out = []
    for x in items:
        if x not in vistos:      # O(1), no recorre nada
            vistos.add(x)
            out.append(x)
    return out
```

## Comparar colecciones

Los sets tienen operaciones de conjuntos:

```python
a, b = {1, 2, 3}, {2, 3, 4}
print(a & b)   # {2, 3}   intersección (en ambos)
print(a | b)   # {1,2,3,4} unión (en alguno)
print(a - b)   # {1}      diferencia (en a, no en b)
```

> 💡 Si tu código hace `if x in lista` dentro de un bucle y va lento, cambiá la lista por un **set**. Suele ser la optimización más grande con el menor esfuerzo.

## ✅ Comprobá lo que aprendiste

```quiz
P: Preguntar `x in conjunto` (un `set`) es…
+ casi instantáneo (O(1))
- lento, como recorrer una lista (O(n))
- imposible
> Los sets usan una tabla hash: van directo al dato.
```

```quiz
P: Para contar cuántas veces aparece cada elemento, conviene…
+ un diccionario: `f[x] = f.get(x, 0) + 1`
- una lista
- un set
> El dict guarda elemento → cantidad.
```

🗂️ La **Líder Tulip** te espera para contar patrones.

---
title: "Algoritmos: Búsqueda lineal y binaria"
order: 1200
---

> 🎯 **Meta:** buscar datos de dos formas y entender por qué una es **muchísimo** más rápida.

---

Buscar es la operación más común de todas. Hay dos formas clásicas, y la diferencia entre ellas es enorme cuando los datos crecen.

## Búsqueda lineal

Mirás uno por uno hasta encontrarlo. Simple y funciona en cualquier lista (ordenada o no):

```python
def busqueda_lineal(lista, x):
    for i, v in enumerate(lista):
        if v == x:
            return i
    return -1   # no está
```

Si la lista tiene un millón de elementos, en el peor caso hacés un millón de comparaciones. Eso es **O(n)**: el tiempo crece igual que el tamaño.

## Búsqueda binaria

Si la lista está **ordenada**, podés ser mucho más vivo: mirás el del medio y descartás la mitad que no sirve. Repetís hasta encontrarlo:

```python
def busqueda_binaria(ordenada, x):
    lo, hi = 0, len(ordenada) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ordenada[mid] == x:
            return mid
        if ordenada[mid] < x:
            lo = mid + 1     # descartá la mitad izquierda
        else:
            hi = mid - 1     # descartá la mitad derecha
    return -1
```

Cada paso parte el problema al medio: un millón de elementos se resuelve en ~20 pasos. Eso es **O(log n)** — abismalmente más rápido.

> ⚠️ La binaria SOLO funciona si la lista está ordenada. Por eso el próximo capítulo es ordenar.

## ✅ Comprobá lo que aprendiste

```quiz
P: La búsqueda binaria requiere que la lista esté…
+ ordenada
- vacía
- sin repetidos
> Parte el rango al medio descartando mitades; por eso necesita orden.
```

```quiz
P: Buscar en un millón de elementos: lineal vs binaria…
+ binaria ~20 pasos; lineal hasta un millón
- las dos tardan igual
- la lineal es más rápida
> O(log n) (binaria) es muchísimo mejor que O(n) (lineal).
```

🔎 La **Líder Katy** te espera para construir buscadores.

---
title: "Algoritmos: Ordenar listas"
order: 1201
---

> 🎯 **Meta:** entender **cómo** se ordena una lista implementando los métodos clásicos a mano.

---

Python tiene `sorted()`, y en la vida real lo vas a usar siempre. Pero implementar el orden vos mismo te enseña a pensar como un programador: comparar, intercambiar, repetir.

## Ordenamiento burbuja

Comparás pares vecinos y los intercambiás si están al revés. En cada pasada, el más grande "burbujea" hasta el final:

```python
def burbuja(lista):
    a = list(lista)              # copia, no tocar el original
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]   # intercambio pythonico
    return a
```

## Ordenamiento por selección

Buscás el mínimo y lo ponés adelante; repetís con el resto:

```python
def seleccion(lista):
    a = list(lista)
    for i in range(len(a)):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a
```

Los dos son **O(n²)**: con listas grandes se vuelven lentos. Los algoritmos reales (Timsort, el de Python) son **O(n log n)** — mucho mejores. Pero burbuja y selección son perfectos para entender la mecánica.

> 💡 El truco `a, b = b, a` intercambia dos variables sin una tercera. Es marca registrada de Python.

🔢 El **Líder Brassius** te espera para ordenar su obra.

---
title: "NumPy: Arrays"
order: 200
---

> 🎯 **Meta:** dar el primer paso en el **análisis de datos**. Vas a conocer **NumPy**, la librería que maneja **montones de números a la vez**, rapidísimo.

Bienvenido a **Johto**, la región del **análisis de datos**. 📊 Acá aprendés a trabajar con
**muchos** datos: stats de cientos de Pokémon, tablas, gráficos. La primera herramienta es **NumPy**.

## 🎮 Analogía: el array es la ficha de stats del equipo

Una lista de Python guarda cosas, pero para hacer **cálculos** con muchos números es lenta.
Un **array de NumPy** es como la **planilla de stats** de tu equipo: todos los números juntos,
y podés operar sobre **todos a la vez** (eso se llama *vectorización*).

```python
import numpy as np

niveles = np.array([25, 90, 12, 70])
print(niveles)
print("tipo:", type(niveles))
```

> 💡 Por convención, NumPy siempre se importa como `np`. Lo vas a ver en todos lados.

## ✨ Crear arrays

```python
import numpy as np

a = np.array([1, 2, 3])        # desde una lista
ceros = np.zeros(5)            # array de 5 ceros
unos = np.ones(3)             # array de 3 unos
rango = np.arange(1, 6)       # del 1 al 5 (el 6 NO entra)
print(a)
print(ceros)
print(rango)
```

## ⚡ Vectorización: matemática sobre TODO el array

Lo mágico: operás con el array entero, **sin escribir un `for`**.

```python
import numpy as np

ataques = np.array([10, 20, 30])
print(ataques * 2)        # duplica cada valor -> [20 40 60]
print(ataques + 5)        # suma 5 a cada uno  -> [15 25 35]

defensa = np.array([3, 8, 1])
print(ataques - defensa)  # elemento a elemento -> [ 7 12 29]
```

> ⚡ Comparalo con Python puro: ahí necesitarías un `for` y una lista nueva. NumPy lo hace de una, y mucho más rápido.

## 🔪 Indexing y slicing

Igual que en las listas: accedés por posición y cortás con `:`.

```python
import numpy as np

equipo = np.array([25, 90, 12, 70, 5])
print(equipo[0])     # primero -> 25
print(equipo[-1])    # último  -> 5
print(equipo[:3])    # primeros tres -> [25 90 12]
print(equipo[1:4])   # del 1 al 3     -> [90 12 70]
```

## 🎭 Máscaras booleanas: filtrar por condición

Una **máscara** es un array de `True/False`. La usás para **quedarte con lo que cumple una condición**.

```python
import numpy as np

niveles = np.array([25, 90, 12, 70, 5])
print(niveles > 30)          # [False  True False  True False]
print(niveles[niveles > 30]) # solo los que cumplen -> [90 70]
```

## 📐 Forma (shape) y matrices 2D

Un array puede ser 2D (una **tabla** de números): filas y columnas.

```python
import numpy as np

stats = np.array([[35, 55, 40],
                  [78, 84, 78]])
print(stats.shape)    # (2, 3) -> 2 filas, 3 columnas
print(stats.flatten())  # aplanar a 1D -> [35 55 40 78 84 78]
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `np.array([...])` | crear un array desde una lista |
| `np.zeros(n)` / `np.ones(n)` | array de ceros / unos |
| `np.arange(a, b)` | rango de a hasta b-1 |
| `arr * 2`, `a + b` | operaciones vectorizadas |
| `arr[i]`, `arr[a:b]` | indexing y slicing |
| `arr[arr > x]` | filtrar con máscara booleana |
| `arr.shape`, `arr.flatten()` | forma y aplanar |

## ➡️ ¿Y ahora qué?

Ahora **practicá**: andá a los [ejercicios de este tema](/ejercicios/numpy-arrays) y resolvelos. Se corrigen al instante en tu navegador. 💪

> ⚡ *"Un buen Entrenador conoce las stats de su equipo. Un buen analista, las de miles."*

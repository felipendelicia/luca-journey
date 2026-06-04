---
title: "NumPy: Cálculo numérico"
order: 210
---

> 🎯 **Meta:** sacarle **conclusiones** a un array: promedios, máximos, contar cuántos cumplen algo. Es el corazón del análisis.

Ya sabés crear arrays. Ahora vamos a **resumirlos**: ¿cuál es el Pokémon más fuerte? ¿el promedio de niveles? ¿cuántos superan el nivel 50?

## 📊 Agregaciones: de muchos números a uno

Una **agregación** toma todo el array y devuelve **un solo número**.

```python
import numpy as np

niveles = np.array([25, 90, 12, 70, 50])
print("suma:", niveles.sum())
print("promedio:", niveles.mean())
print("máximo:", niveles.max())
print("mínimo:", niveles.min())
print("desvío:", niveles.std())
```

> 💡 `mean` (media/promedio), `std` (desvío estándar) y `max/min` son las estrellas del análisis: te dan una "foto" rápida de los datos.

## 🧭 El eje (axis) en matrices 2D

En una tabla 2D podés agregar **por columna** (`axis=0`) o **por fila** (`axis=1`).

```python
import numpy as np

# filas = Pokémon, columnas = [ataque, defensa, velocidad]
stats = np.array([[55, 40, 90],
                  [84, 78, 100]])

print(stats.sum(axis=0))   # total por columna -> [139 118 190]
print(stats.sum(axis=1))   # total por fila    -> [185 262]
print(stats.mean(axis=0))  # promedio por columna
```

> 💡 Truco para no marearte: `axis=0` "aplasta hacia abajo" (resume las filas → te queda una por columna). `axis=1` "aplasta hacia el costado".

## 🎭 Contar y filtrar con condiciones

Combinás máscaras con agregaciones para **contar** o **medir**.

```python
import numpy as np

niveles = np.array([25, 90, 12, 70, 50])
print((niveles > 40).sum())          # cuántos superan 40 -> 3
print(niveles[niveles > 40].mean())  # promedio de los que superan 40
```

> 💡 `(niveles > 40)` da `[False True False True True]`. Sumar booleanos cuenta los `True` (porque `True` vale 1).

## 🔀 np.where: elegir según una condición

`np.where(condición, si_cumple, si_no)` arma un array nuevo decidiendo valor por valor.

```python
import numpy as np

hp = np.array([100, -5, 30, -20, 80])
sano = np.where(hp < 0, 0, hp)   # los negativos pasan a 0
print(sano)   # [100   0  30   0  80]
```

## 📏 Normalizar: llevar todo a la misma escala

Una técnica clásica: escalar los valores al rango **0 a 1** para poder compararlos.

```python
import numpy as np

niveles = np.array([10, 50, 100])
norm = (niveles - niveles.min()) / (niveles.max() - niveles.min())
print(norm)   # [0.  0.444  1. ]
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `arr.sum()/mean()/max()/min()/std()` | resumir todo el array en un número |
| `arr.sum(axis=0/1)` | resumir por columna / por fila |
| `(arr > x).sum()` | contar cuántos cumplen |
| `np.where(cond, a, b)` | elegir valor según condición |
| `(x - min) / (max - min)` | normalizar a 0..1 |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/numpy-calculo). 💪

> ⚡ *"Los números cuentan historias. Aprendé a escucharlos."*

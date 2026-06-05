---
title: "ML: preparar los datos"
order: 710
---

> 🎯 **Meta:** preparar los datos antes de entrenar: separar **features** de **etiquetas**, dividir en **entrenamiento y prueba**, y **escalar**. Sin esto, el modelo aprende mal.

Un modelo es tan bueno como sus datos. Antes de `fit`, casi siempre hay que **preparar** los datos. Es el paso menos glamoroso y el más importante.

## ✂️ Features (X) y etiquetas (y)

Los datos suelen venir en una tabla donde las primeras columnas son las **features** y la última es la **etiqueta** (lo que querés predecir).

```python
import numpy as np

# [ataque, defensa, tipo]
datos = np.array([
    [90, 40, 0],
    [85, 45, 0],
    [40, 90, 1],
])

X = datos[:, :-1]   # todas las columnas menos la última -> features
y = datos[:, -1]    # la última columna -> etiqueta
print("X =", X.tolist())
print("y =", y.tolist())
```

## 🪓 Train / test: no te engañes a vos mismo

Si evaluás el modelo con los **mismos** datos con que lo entrenaste, te miente (se los sabe de memoria). Por eso se separan: una parte para **entrenar** y otra, que el modelo **nunca vio**, para **probar**.

```python
import numpy as np
from sklearn.model_selection import train_test_split

X = np.arange(20).reshape(10, 2)
y = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("entrenamiento:", len(X_train), "filas")
print("prueba:", len(X_test), "filas")
```

> 💡 `test_size=0.3` aparta el 30% para probar. `random_state=42` fija el "azar" para que el reparto sea siempre el mismo (reproducible).

```quiz
P: ¿Por qué se divide el dataset en train y test antes de entrenar?
- Para usar menos memoria al entrenar
+ Para evaluar el modelo con datos que nunca vio y medir su desempeño real
- Porque `fit` no acepta todos los datos a la vez
> Si evaluás con los mismos datos de entrenamiento, el modelo parece mejor de lo que es (se los "sabe de memoria"). El **test set** mide cómo se porta con datos nuevos.
```

## 📏 Escalar: misma medida para todos

Si una feature va de 0 a 1000 y otra de 0 a 1, la grande "pisa" a la chica. **Escalar** las pone en la misma medida (media 0, desvío 1).

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[0.0, 100.0], [10.0, 200.0], [20.0, 300.0]])
X_escalado = StandardScaler().fit_transform(X)
print(X_escalado.round(2))
```

```quiz
P: ¿Para qué sirve `StandardScaler().fit_transform(X)`?
- Para convertir los datos a formato JSON antes de entrenar
- Para rellenar los valores faltantes con cero
+ Para poner todas las features en la misma escala (media 0, desvío 1)
> Si una feature va de 0 a 1000 y otra de 0 a 1, la grande domina al modelo. Escalar las pone en la misma medida para que todas tengan igual peso.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `X = datos[:, :-1]` | features (entradas) |
| `y = datos[:, -1]` | etiqueta (a predecir) |
| `train_test_split(...)` | separar entrenamiento / prueba |
| `random_state` | hacer el reparto reproducible |
| `StandardScaler().fit_transform(X)` | escalar a la misma medida |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-datos). 💪

> ⚡ *"Datos prolijos, modelo honesto. Datos sucios, IA que alucina."*

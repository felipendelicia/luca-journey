---
title: "ML: regresión"
order: 740
---

> 🎯 **Meta:** predecir un **número** (no una categoría). Vas a estimar valores continuos con **regresión lineal**.

Clasificar responde "¿qué tipo es?". La **regresión** responde "¿**cuánto**?": el precio de una casa, la temperatura de mañana, el **CP** de un Pokémon. La respuesta es un **número**.

## 📈 Regresión lineal

Busca la **recta** (o plano) que mejor pasa por los datos, para estimar valores nuevos.

```python
from sklearn.linear_model import LinearRegression

# nivel -> CP (relación aproximada: CP sube con el nivel)
X = [[10], [20], [30], [40]]
y = [100, 200, 300, 400]

modelo = LinearRegression()
modelo.fit(X, y)

print(modelo.predict([[25]]))   # [250.] -> estima el CP a nivel 25
print(modelo.predict([[50]]))   # [500.]
```

> 💡 A diferencia del clasificador, acá `predict` devuelve un **número con decimales**, no una categoría.

## 🔢 La fórmula que aprendió

El modelo aprende una **pendiente** y una **ordenada** (`y = pendiente·x + ordenada`):

```python
from sklearn.linear_model import LinearRegression

X = [[1], [2], [3], [4]]
y = [3, 5, 7, 9]      # y = 2*x + 1

modelo = LinearRegression().fit(X, y)
print("pendiente:", round(modelo.coef_[0], 2))      # 2.0
print("ordenada:", round(modelo.intercept_, 2))     # 1.0
print("predice x=10:", modelo.predict([[10]])[0])   # 21.0
```

## 🧬 Con varias features

Igual que la clasificación, podés usar **muchas** columnas de entrada:

```python
from sklearn.linear_model import LinearRegression

# [ataque, defensa] -> poder de combate
X = [[50, 50], [80, 40], [40, 80], [90, 90]]
y = [100, 120, 120, 180]

modelo = LinearRegression().fit(X, y)
print(modelo.predict([[70, 70]]).round(1))
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| regresión | predecir un número (continuo) |
| `LinearRegression()` | el modelo de la recta |
| `.fit(X, y)` / `.predict(...)` | entrenar / estimar |
| `.coef_` / `.intercept_` | la fórmula aprendida |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-regresion). 💪

> ⚡ *"Clasificar dice 'qué'. Regresión dice 'cuánto'. Con las dos, predecís casi todo."*

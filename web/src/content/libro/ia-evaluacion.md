---
title: "ML: evaluar modelos"
order: 730
---

> 🎯 **Meta:** medir si tu modelo es **bueno**. Vas a calcular su **exactitud** sobre datos que nunca vio. Un modelo sin evaluar es una promesa sin pruebas.

Entrenar un modelo es fácil. Lo difícil es saber si **anda bien**. Para eso se mide la **exactitud (accuracy)**: el porcentaje de aciertos sobre datos de **prueba**.

## ✅ Accuracy: proporción de aciertos

```python
from sklearn.metrics import accuracy_score

y_real    = [0, 1, 1, 0, 1]
y_predicho = [0, 1, 0, 0, 1]   # se equivocó en el 3ro

print(accuracy_score(y_real, y_predicho))   # 0.8 -> 4 de 5
```

## 🪓 Entrenar y evaluar bien

La regla de oro: entrenás con una parte y **evaluás con otra** (que el modelo no vio). Así sabés cómo se va a portar con datos nuevos de verdad.

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# dos grupos bien separados
X = np.array([[90, 40], [88, 42], [86, 44], [40, 90], [42, 88], [44, 86]])
y = np.array([0, 0, 0, 1, 1, 1])

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
modelo = KNeighborsClassifier(n_neighbors=1).fit(X_tr, y_tr)

predicciones = modelo.predict(X_te)
print("exactitud:", accuracy_score(y_te, predicciones))
```

## ⚡ Atajo: .score()

Casi todos los modelos tienen `.score(X_test, y_test)`, que entrena... no: **calcula la exactitud** directamente.

```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

X = np.array([[90, 40], [40, 90]])
y = np.array([0, 1])
modelo = KNeighborsClassifier(n_neighbors=1).fit(X, y)

print(modelo.score(X, y))   # 1.0
```

> ⚠️ Si tu modelo da **100% en entrenamiento pero mal en prueba**, está **sobreajustado** (overfitting): se memorizó los datos en vez de aprender el patrón. Por eso SIEMPRE se evalúa con datos separados.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `accuracy_score(real, pred)` | proporción de aciertos |
| entrenar con train, evaluar con test | medición honesta |
| `modelo.score(X_test, y_test)` | exactitud en un paso |
| overfitting | memorizar en vez de aprender |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-evaluacion). 💪

> ⚡ *"Un modelo sin evaluar es como un Pokémon sin combatir: no sabés si sirve."*

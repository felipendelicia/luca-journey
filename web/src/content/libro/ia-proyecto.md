---
title: "Proyecto: clasificador Pokédex"
order: 770
---

> 🎯 **Meta:** juntar **todo Unova** en un proyecto de IA real: a partir de las stats de un Pokémon, un modelo aprende a **predecir su tipo**. Pipeline completo, de punta a punta.

Llegaste al final de Unova. 🦾 Ahora armás un **clasificador** que, dadas las stats de un Pokémon, predice si es de Fuego o de Agua. Vas a recorrer los 4 pasos de todo proyecto de Machine Learning.

## 🗺️ Los 4 pasos del ML

1. **Preparar** los datos (features `X` y etiquetas `y`).
2. **Dividir** en entrenamiento y prueba.
3. **Entrenar** un modelo.
4. **Evaluar** y **usar** para predecir.

## 🤖 El proyecto completo

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1) DATOS: [ataque, defensa, tipo]  (0 = Fuego, 1 = Agua)
datos = np.array([
    [90, 40, 0], [88, 42, 0], [86, 44, 0], [92, 38, 0],
    [40, 90, 1], [42, 88, 1], [44, 86, 1], [38, 92, 1],
])
X = datos[:, :-1]
y = datos[:, -1]

# 2) DIVIDIR
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)

# 3) ENTRENAR
modelo = KNeighborsClassifier(n_neighbors=3).fit(X_tr, y_tr)

# 4) EVALUAR
print("exactitud:", accuracy_score(y_te, modelo.predict(X_te)))

# 5) USAR: predecir un Pokémon nuevo
stats = [87, 43]   # mucho ataque, poca defensa
tipo = modelo.predict([stats])[0]
print("Predicción:", "Fuego" if tipo == 0 else "Agua")
```

## 🧠 Lo que aprendiste en Unova

1. **ML** = aprender de ejemplos (`fit` / `predict`).
2. **Preparar datos** — features/etiquetas, train/test, escalar.
3. **Clasificación** — predecir categorías (KNN).
4. **Evaluación** — accuracy, evitar overfitting.
5. **Regresión** — predecir números (recta).
6. **Árboles** — modelos que se entienden + importancia de features.
7. **Clustering** — agrupar sin etiquetas (KMeans).

Con esto entendés la base de la IA moderna. Las redes neuronales y los modelos gigantes (como los que generan texto) son **la misma idea, a lo grande**: aprender de un montón de ejemplos. 🚀

## ➡️ ¿Y ahora qué?

Cerrá Unova con los [ejercicios de este tema](/ejercicios/ia-proyecto). Al completarlos ganás la medalla **Leyenda** y sos **Campeón de Unova**. 🦾🏆

> ⚡ *"Le diste ejemplos y aprendió a decidir solo. Eso, mi amigo, es Inteligencia Artificial."*

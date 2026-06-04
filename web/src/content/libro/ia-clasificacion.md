---
title: "ML: clasificación"
order: 720
---

> 🎯 **Meta:** entrenar un modelo que prediga **categorías** — el ejemplo clásico de IA. Vas a clasificar el **tipo** de un Pokémon a partir de sus stats.

**Clasificar** = predecir a qué **grupo** pertenece algo: ¿es spam o no? ¿perro o gato? ¿Fuego o Agua? La respuesta es una **categoría** (no un número).

## 🧲 KNN: clasificar por parecido

El `KNeighborsClassifier` mira los **k vecinos más cercanos** y hace que **voten**. Con `k=3`, mira los 3 más parecidos y elige la categoría que más se repite.

```python
from sklearn.neighbors import KNeighborsClassifier

# [ataque, defensa] -> 0 = Fuego, 1 = Agua
X = [[90, 40], [85, 45], [88, 42], [40, 90], [45, 85], [42, 88]]
y = [0, 0, 0, 1, 1, 1]

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X, y)

print(modelo.predict([[89, 41]]))   # [0] -> Fuego
print(modelo.predict([[41, 89]]))   # [1] -> Agua
```

> 💡 `k=3` suele andar mejor que `k=1`: al votar entre varios vecinos, un dato raro no arruina la predicción.

## 🔮 Predecir muchos de una

```python
from sklearn.neighbors import KNeighborsClassifier

X = [[90, 40], [85, 45], [88, 42], [40, 90], [45, 85], [42, 88]]
y = ["Fuego", "Fuego", "Fuego", "Agua", "Agua", "Agua"]

modelo = KNeighborsClassifier(n_neighbors=3).fit(X, y)

nuevos = [[95, 35], [38, 92], [80, 50]]
print(modelo.predict(nuevos))   # ['Fuego' 'Agua' 'Fuego']
```

> 💡 Las etiquetas pueden ser textos (`"Fuego"`) o números (`0`). El modelo no se da cuenta de la diferencia: aprende del patrón de las features.

## 🎯 ¿Y qué tan seguro está?

Muchos modelos te dan la **probabilidad** de cada categoría con `predict_proba`:

```python
from sklearn.neighbors import KNeighborsClassifier
X = [[90, 40], [85, 45], [88, 42], [40, 90], [45, 85], [42, 88]]
y = [0, 0, 0, 1, 1, 1]
modelo = KNeighborsClassifier(n_neighbors=3).fit(X, y)

print(modelo.predict_proba([[60, 60]]))   # [[prob_Fuego, prob_Agua]]
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| clasificar | predecir una categoría |
| `KNeighborsClassifier(n_neighbors=k)` | clasificador por k vecinos |
| `.predict([fila])` | predecir una |
| `.predict(filas)` | predecir muchas |
| `.predict_proba(...)` | probabilidad de cada categoría |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-clasificacion). 💪

> ⚡ *"Mostrale ejemplos y aprende a etiquetar el mundo. Eso hace un clasificador."*

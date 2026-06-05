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

```quiz
P: En `KNeighborsClassifier(n_neighbors=3)`, ¿qué significa `n_neighbors=3`?
- El modelo necesita mínimo 3 datos para entrenarse
+ Mira los 3 ejemplos más parecidos y hace que voten
- Divide los datos en 3 grupos iguales
> Con `k=3` el modelo busca los 3 vecinos más cercanos y elige la categoría que más se repite entre ellos. Más vecinos = decisión más estable.
```

## 🎯 ¿Y qué tan seguro está?

Muchos modelos te dan la **probabilidad** de cada categoría con `predict_proba`:

```python
from sklearn.neighbors import KNeighborsClassifier
X = [[90, 40], [85, 45], [88, 42], [40, 90], [45, 85], [42, 88]]
y = [0, 0, 0, 1, 1, 1]
modelo = KNeighborsClassifier(n_neighbors=3).fit(X, y)

print(modelo.predict_proba([[60, 60]]))   # [[prob_Fuego, prob_Agua]]
```

```quiz
P: ¿Qué devuelve `modelo.predict_proba([[60, 60]])`?
- El nombre de la categoría predicha
- Un número entre 0 y 1 que indica el nivel de confianza total
+ Un arreglo con la probabilidad de cada categoría posible
> `predict_proba` da la **probabilidad** de cada clase. Por ejemplo `[[0.67, 0.33]]` significa 67% Fuego y 33% Agua. `predict` solo da la más probable.
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

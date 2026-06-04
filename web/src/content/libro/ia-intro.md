---
title: "ML: tu primer modelo"
order: 700
---

> 🎯 **Meta:** entrar a **Unova**, la región de la **Inteligencia Artificial**. Vas a entrenar tu primer modelo de **Machine Learning** y verlo **predecir** solo.

Bienvenido a **Unova**. 🤖 La IA está en todos lados: recomendaciones, reconocimiento de voz, autos que se manejan solos. La base de casi todo eso es el **Machine Learning (ML)**: en vez de programar las reglas, le mostrás **ejemplos** al modelo y **aprende** las reglas solo.

## 🎮 Analogía: entrenar un Pokémon

No le explicás a tu Pokémon *cómo* pelear con una fórmula: lo **entrenás con experiencia** y aprende. El ML es igual: le das **datos** y **respuestas correctas**, y el modelo aprende a responder por su cuenta.

| Concepto | Qué es |
|----------|--------|
| **X** (features) | los datos de entrada (ej: ataque y defensa) |
| **y** (etiquetas) | la respuesta correcta (ej: el tipo) |
| **`.fit(X, y)`** | entrenar con ejemplos |
| **`.predict(...)`** | usar el modelo para predecir algo nuevo |

## 🧠 Tu primer modelo (KNN)

Usamos un clasificador de **vecinos cercanos**: para predecir, mira a los ejemplos más **parecidos** y copia su respuesta. Tocá **▶ ejecutar** (la primera vez tarda: descarga scikit-learn).

```python
from sklearn.neighbors import KNeighborsClassifier

# datos: [ataque, defensa]  ->  tipo: 0 = Fuego, 1 = Agua
X = [[90, 40], [85, 45], [40, 90], [45, 85]]
y = [0, 0, 1, 1]

modelo = KNeighborsClassifier(n_neighbors=1)
modelo.fit(X, y)            # 🏋️ entrenamos

# ¿qué tipo es un Pokémon con ataque 88 y defensa 42?
print(modelo.predict([[88, 42]]))   # [0] -> ¡Fuego!
print(modelo.predict([[42, 88]]))   # [1] -> ¡Agua!
```

> 💡 `n_neighbors=1` significa "mirá el vecino MÁS cercano". El modelo nunca vio `[88, 42]`, pero lo parecido a sus ejemplos de Fuego, así que predice Fuego. **Eso es aprender de los datos.**

## 🔄 El ciclo del ML

```python
from sklearn.neighbors import KNeighborsClassifier

# 1) datos de ejemplo
X = [[10, 1], [9, 2], [1, 10], [2, 9]]
y = ["rápido", "rápido", "lento", "lento"]

# 2) elegir y entrenar un modelo
modelo = KNeighborsClassifier(n_neighbors=1).fit(X, y)

# 3) predecir algo nuevo
print(modelo.predict([[8, 3]]))   # ['rápido']
```

Siempre los mismos 3 pasos: **datos → entrenar (`fit`) → predecir (`predict`)**.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| Machine Learning | aprender reglas a partir de ejemplos |
| `X` / `y` | datos de entrada / respuestas |
| `modelo.fit(X, y)` | entrenar |
| `modelo.predict([fila])` | predecir |
| `KNeighborsClassifier` | clasifica mirando a los más parecidos |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-intro). 💪

> ⚡ *"No le programaste las reglas: se las enseñaste. Bienvenido a la IA."*

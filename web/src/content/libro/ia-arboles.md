---
title: "ML: árboles de decisión"
order: 750
---

> 🎯 **Meta:** usar un modelo que **se entiende**: el árbol de decisión aprende reglas tipo "si... entonces..." y te dice qué dato fue más importante.

El KNN funciona pero es una "caja negra". Un **árbol de decisión** es distinto: aprende una serie de **preguntas** (como un cuestionario) y podés **leer** cómo decide.

## 🌳 Cómo decide un árbol

```
            ¿ataque > 60?
            /          \
          sí            no
          │              │
        Fuego          Agua
```

```python
from sklearn.tree import DecisionTreeClassifier

# [ataque, defensa] -> 0 = Fuego, 1 = Agua
X = [[90, 40], [80, 50], [40, 90], [50, 80]]
y = [0, 0, 1, 1]

modelo = DecisionTreeClassifier(random_state=0)
modelo.fit(X, y)

print(modelo.predict([[85, 45]]))   # [0] -> Fuego
print(modelo.predict([[45, 85]]))   # [1] -> Agua
```

> 💡 `random_state=0` fija el azar interno del árbol para que el resultado sea siempre el mismo.

## 🔍 ¿Qué feature importa más?

Lo mejor del árbol: te dice **cuánto pesó cada feature** en sus decisiones. Útil para entender tus datos.

```python
from sklearn.tree import DecisionTreeClassifier

# la decisión depende SOLO del ataque (la defensa es siempre 50)
X = [[10, 50], [20, 50], [80, 50], [90, 50]]
y = [0, 0, 1, 1]

modelo = DecisionTreeClassifier(random_state=0).fit(X, y)
print("importancia de cada feature:", modelo.feature_importances_)
# [1. 0.] -> el ataque importó todo, la defensa nada
```

> 💡 Las importancias suman 1. Si una feature da `0`, no aportó nada para decidir; podrías hasta sacarla.

## 🌲 Ventajas y cuidado

- ✅ Se **entiende** (podés explicar cada decisión).
- ✅ No necesita escalar los datos.
- ⚠️ Si lo dejás crecer sin límite, **memoriza** (overfitting). Se controla con `max_depth`.

```python
from sklearn.tree import DecisionTreeClassifier
modelo = DecisionTreeClassifier(max_depth=2, random_state=0)   # árbol cortito
print(modelo)
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `DecisionTreeClassifier(random_state=0)` | árbol de decisión |
| `.feature_importances_` | cuánto pesó cada feature |
| `max_depth` | limitar el tamaño (evitar overfitting) |
| ventaja | es interpretable (se entiende) |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-arboles). 💪

> ⚡ *"El árbol no solo predice: te explica por qué. Eso vale oro."*

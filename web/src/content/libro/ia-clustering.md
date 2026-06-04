---
title: "ML: clustering"
order: 760
---

> 🎯 **Meta:** descubrir grupos en los datos **sin** tener las respuestas. Es el aprendizaje **no supervisado**: el modelo agrupa solo lo que se parece.

Hasta ahora siempre tuvimos `y` (las respuestas). Pero a veces **no las tenés** y querés que la IA **descubra** la estructura sola. Por ejemplo: agrupar Pokémon parecidos sin decirle de qué tipo son. Eso es **clustering**.

## 🧩 KMeans: armar k grupos

`KMeans` divide los datos en **k grupos** poniendo juntos los que están cerca.

```python
import numpy as np
from sklearn.cluster import KMeans

# stats de 6 Pokémon: dos "familias" bien separadas
X = np.array([[1, 1], [2, 1], [1, 2], [10, 10], [11, 10], [10, 11]])

modelo = KMeans(n_clusters=2, random_state=0, n_init=10)
modelo.fit(X)

print("grupo de cada uno:", modelo.labels_)   # ej: [0 0 0 1 1 1]
```

> 💡 Los números de grupo (0, 1) son **arbitrarios**: lo que importa es que los parecidos quedaron **juntos**. `random_state=0` y `n_init=10` lo hacen reproducible.

## 🔮 ¿A qué grupo va uno nuevo?

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1, 1], [2, 1], [10, 10], [11, 10]])
modelo = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X)

# un Pokémon nuevo cercano a la primera familia
print(modelo.predict([[1.5, 1.5]]))   # el grupo de los primeros
```

## 🎯 Supervisado vs no supervisado

| | Supervisado | No supervisado |
|---|---|---|
| **Tenés `y`** | sí (las respuestas) | no |
| **Hace** | predecir una etiqueta | descubrir grupos |
| **Ejemplos** | clasificación, regresión | clustering (KMeans) |

> 💡 El clustering sirve para **explorar**: segmentar clientes, agrupar noticias parecidas, detectar familias de Pokémon... todo sin etiquetas previas.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| no supervisado | aprender sin respuestas (`y`) |
| `KMeans(n_clusters=k)` | armar k grupos |
| `.labels_` | a qué grupo quedó cada dato |
| `.predict([fila])` | grupo de un dato nuevo |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/ia-clustering). 💪

> ⚡ *"Sin respuestas, sin problema: la IA encuentra el orden escondido en los datos."*

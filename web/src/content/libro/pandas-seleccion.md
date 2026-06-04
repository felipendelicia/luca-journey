---
title: "pandas: Selección y filtrado"
order: 230
---

> 🎯 **Meta:** elegir exactamente las filas y columnas que te interesan. Filtrar es el 80% del trabajo de un analista.

Ya tenés tu Pokédex como DataFrame. Ahora vas a **hacerle preguntas**: ¿quiénes superan el nivel 50? ¿cuáles son de tipo Fuego? ¿quién es el más fuerte?

## 🎯 Elegir filas por posición: iloc

`.iloc` usa **posiciones** (como los índices de una lista: 0, 1, 2...).

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur"],
    "nivel":  [25, 90, 12],
})
print(pokedex.iloc[0])     # primera fila
print(pokedex.iloc[1]["nombre"])   # nombre de la 2da fila -> Charizard
```

## 🎭 Filtrar con condiciones (boolean indexing)

Lo más poderoso: le pasás una **condición** entre corchetes y te quedan solo las filas que cumplen.

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"],
    "nivel":  [25, 90, 12, 70],
    "tipo":   ["Eléctrico", "Fuego", "Planta", "Normal"],
})
print(pokedex[pokedex["nivel"] >= 50])          # los de nivel 50+
print(pokedex[pokedex["tipo"] == "Fuego"])      # los de tipo Fuego
```

> 💡 `pokedex["nivel"] >= 50` da una Series de True/False (una máscara, como en NumPy). pandas usa esa máscara para filtrar filas.

## 🔗 Varias condiciones a la vez

Combinás con `&` (y) / `|` (o). **Ojo:** cada condición va entre paréntesis.

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Snorlax"],
    "nivel":  [25, 90, 70],
    "tipo":   ["Eléctrico", "Fuego", "Normal"],
})
fuertes_no_fuego = pokedex[(pokedex["nivel"] > 30) & (pokedex["tipo"] != "Fuego")]
print(fuertes_no_fuego)
```

## ↕️ Ordenar

```python
import pandas as pd
pokedex = pd.DataFrame({"nombre": ["Pikachu", "Charizard", "Bulbasaur"], "nivel": [25, 90, 12]})
print(pokedex.sort_values("nivel", ascending=False))   # del más fuerte al más débil
```

## 🏆 El más fuerte: idxmax

```python
import pandas as pd
pokedex = pd.DataFrame({"nombre": ["Pikachu", "Charizard", "Bulbasaur"], "nivel": [25, 90, 12]})
pos = pokedex["nivel"].idxmax()                  # posición del nivel máximo
print("El más fuerte es:", pokedex.loc[pos, "nombre"])   # -> Charizard
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `df.iloc[i]` | fila por posición |
| `df[df["col"] > x]` | filtrar filas por condición |
| `(c1) & (c2)`, `(c1) \| (c2)` | combinar condiciones |
| `df.sort_values("col", ascending=False)` | ordenar |
| `df["col"].idxmax()` | posición del valor máximo |
| `df.loc[pos, "col"]` | un valor por etiqueta de fila/columna |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/pandas-seleccion). 💪

> ⚡ *"Saber preguntar es más valioso que saber todas las respuestas."*

---
title: "pandas: Agrupar y combinar"
order: 250
---

> 🎯 **Meta:** sacar **resúmenes por grupo** (ej: nivel promedio por tipo) y **combinar** dos tablas. Acá pandas se vuelve mágico.

Tenés una Pokédex enorme. No querés mirar fila por fila: querés **resúmenes**. ¿Cuántos hay de cada tipo? ¿Qué tipo tiene el nivel promedio más alto? Para eso está **`groupby`**.

## 🔢 Contar categorías: value_counts

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Raichu", "Charizard", "Bulbasaur", "Ivysaur"],
    "tipo":   ["Eléctrico", "Eléctrico", "Fuego", "Planta", "Planta"],
})
print(pokedex["tipo"].value_counts())   # cuántos de cada tipo
```

## 🧮 groupby: resumir por grupo

`groupby("tipo")` arma grupos por tipo; después elegís una columna y una operación.

```python
import pandas as pd
pokedex = pd.DataFrame({
    "tipo":  ["Eléctrico", "Eléctrico", "Fuego", "Planta", "Planta"],
    "nivel": [25, 40, 90, 12, 30],
    "hp":    [35, 60, 78, 45, 60],
})
print(pokedex.groupby("tipo")["nivel"].mean())   # nivel promedio por tipo
print(pokedex.groupby("tipo")["hp"].sum())       # hp total por tipo
print(pokedex.groupby("tipo")["nivel"].max())    # nivel máximo por tipo
```

> 💡 El patrón mental: **agrupá por** (`groupby`), **mirá esta columna** (`["nivel"]`), **calculá esto** (`.mean()`). Cambiá las 3 piezas según tu pregunta.

## 🏆 El tipo más común

```python
import pandas as pd
pokedex = pd.DataFrame({"tipo": ["Fuego", "Agua", "Agua", "Planta"]})
print(pokedex["tipo"].value_counts().idxmax())   # -> Agua
```

## 🔗 Combinar dos tablas: merge

Tenés una tabla de Pokémon y otra de **debilidades por tipo**. Las unís por la columna en común (`tipo`).

```python
import pandas as pd

pokemon = pd.DataFrame({"nombre": ["Charizard", "Blastoise"], "tipo": ["Fuego", "Agua"]})
debilidades = pd.DataFrame({"tipo": ["Fuego", "Agua"], "debil_a": ["Agua", "Planta"]})

print(pd.merge(pokemon, debilidades, on="tipo"))
```

> 💡 `merge` es como cruzar dos Pokédex que comparten una columna. Es la base de juntar datos de distintas fuentes.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `df["col"].value_counts()` | contar cuántos de cada categoría |
| `df.groupby("col")["otra"].mean()` | promedio por grupo |
| `.sum()`, `.max()`, `.min()`, `.count()` | otras operaciones por grupo |
| `df["col"].value_counts().idxmax()` | la categoría más común |
| `pd.merge(a, b, on="col")` | combinar dos tablas por una columna |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/pandas-groupby). 💪

> ⚡ *"Mil Pokémon, una pregunta, una respuesta. Eso es groupby."*

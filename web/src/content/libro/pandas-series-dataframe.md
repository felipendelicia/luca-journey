---
title: "pandas: Series y DataFrame"
order: 220
---

> 🎯 **Meta:** conocer **pandas**, la librería estrella para trabajar con **tablas de datos** (como una Pokédex en Excel, pero con superpoderes).

NumPy maneja números. **pandas** maneja **tablas**: filas y columnas con nombres, tipos distintos, datos faltantes. Es la herramienta nº1 del análisis de datos.

## 🎮 Analogía: el DataFrame es tu Pokédex

- Una **Series** es una **columna** con etiquetas (como la lista de niveles de tu equipo).
- Un **DataFrame** es la **tabla completa**: muchas columnas, una fila por Pokémon. Es tu Pokédex.

```python
import pandas as pd

niveles = pd.Series([25, 90, 12], index=["Pikachu", "Charizard", "Bulbasaur"])
print(niveles)
print("El nivel de Charizard:", niveles["Charizard"])
```

> 💡 pandas se importa como `pd`, siempre. Y por dentro usa NumPy: una Series es un array con etiquetas.

```quiz
P: ¿Qué diferencia hay entre una `Series` y un `DataFrame` en pandas?
- Una Series tiene etiquetas; un DataFrame no.
+ Una Series es una columna; un DataFrame es una tabla con muchas columnas.
- Son lo mismo, solo cambia el nombre.
> Una `Series` es una sola columna con etiquetas. Un `DataFrame` agrupa muchas Series en una tabla completa (como una Pokédex).
```

## 🗂️ Crear un DataFrame

Lo más común: desde un **diccionario** donde cada clave es una columna.

```python
import pandas as pd

pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"],
    "nivel":  [25, 90, 12, 70],
    "tipo":   ["Eléctrico", "Fuego", "Planta", "Normal"],
})
print(pokedex)
```

## 👀 Mirar la tabla por arriba

Antes de analizar, siempre **mirás** los datos: las primeras filas, info, estadísticas.

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"],
    "nivel":  [25, 90, 12, 70],
})
print(pokedex.head(2))     # las primeras 2 filas
print("filas, columnas:", pokedex.shape)
print(pokedex.describe())  # min, max, promedio, etc. de las columnas numéricas
```

> 💡 `.head()`, `.info()` y `.describe()` son lo primero que corre todo analista al abrir un dataset nuevo.

## 🏛️ Columnas

Accedés a una columna con corchetes y su nombre. Te devuelve una Series.

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard"],
    "nivel":  [25, 90],
})
print(pokedex["nivel"])            # la columna
print(pokedex["nivel"].mean())     # promedio de la columna
print(list(pokedex.columns))       # nombres de columnas
```

```quiz
P: ¿Qué devuelve `pokedex.shape` si el DataFrame tiene 4 Pokémon y 3 columnas?
- `(3, 4)`
- `12`
+ `(4, 3)`
> `.shape` devuelve `(filas, columnas)`. Primero las filas, después las columnas.
```

## ➕ Agregar una columna

```python
import pandas as pd
pokedex = pd.DataFrame({"nombre": ["Pikachu", "Charizard"], "nivel": [25, 90]})
pokedex["hp"] = [35, 78]      # columna nueva
print(pokedex)
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `pd.Series(datos, index=...)` | una columna con etiquetas |
| `pd.DataFrame({...})` | una tabla (desde un dict de columnas) |
| `df.head(n)` | primeras n filas |
| `df.shape` | (filas, columnas) |
| `df.describe()` | estadísticas de las columnas numéricas |
| `df["col"]` | una columna (Series) |
| `df["nueva"] = [...]` | agregar columna |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/pandas-series-dataframe). 💪

> ⚡ *"Una buena Pokédex ordena el mundo. Un buen DataFrame, los datos."*

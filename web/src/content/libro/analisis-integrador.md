---
title: "Análisis integrador"
order: 270
---

> 🎯 **Meta:** juntar TODO Johto en un mini-análisis real de punta a punta: cargar, limpiar, resumir, graficar y **concluir**. Así trabaja un analista de datos.

Llegaste al final de Johto. 🐉 Ahora ponés todo junto. Un análisis de datos siempre sigue los mismos pasos. Vamos a hacerlos con una Pokédex.

## 1️⃣ Cargar los datos

```python
import pandas as pd

pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Ivysaur", "Snorlax", "Eevee"],
    "tipo":   ["Eléctrico", "Fuego", "Planta", "Planta", "Normal", "Normal"],
    "nivel":  [25, 90, 12, 30, 70, None],
    "hp":     [35, 78, 45, 60, 160, 55],
})
print(pokedex)
```

## 2️⃣ Mirar y limpiar

Siempre: ¿cuántas filas? ¿faltan datos? Limpiamos lo que esté roto.

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Snorlax", "Eevee"],
    "tipo":   ["Eléctrico", "Fuego", "Normal", "Normal"],
    "nivel":  [25, 90, 70, None],
})
print("faltan:", pokedex.isna().sum().sum())
limpia = pokedex.dropna().reset_index(drop=True)
print(limpia)
```

```quiz
P: ¿Qué hace `pokedex.dropna().reset_index(drop=True)` en el paso de limpieza?
- Rellena los valores faltantes con 0 y reinicia el índice.
- Solo reinicia el índice sin tocar los NaN.
+ Elimina las filas con valores faltantes y renumera el índice desde 0.
> `dropna()` saca las filas con NaN. `reset_index(drop=True)` renumera las filas desde 0 (sin guardar el índice viejo como columna).
```

## 3️⃣ Resumir: las preguntas clave

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Ivysaur", "Snorlax"],
    "tipo":   ["Eléctrico", "Fuego", "Planta", "Planta", "Normal"],
    "nivel":  [25, 90, 12, 30, 70],
})
print("cantidad:", len(pokedex))
print("nivel promedio:", pokedex["nivel"].mean())
print("tipo más común:", pokedex["tipo"].value_counts().idxmax())
print("promedio por tipo:")
print(pokedex.groupby("tipo")["nivel"].mean())
```

```quiz
P: ¿En qué orden van los pasos del flujo de análisis de datos?
- Limpiar → Cargar → Resumir → Explorar → Graficar
- Graficar → Resumir → Limpiar → Cargar → Explorar
+ Cargar → Explorar → Limpiar → Resumir → Graficar
> El orden es siempre: primero cargás los datos, los explorás (`head`, `describe`), los limpiás (NaN, duplicados), los resumís (`groupby`, `mean`) y finalmente graficás.
```

## 4️⃣ Graficar la conclusión

```python
import pandas as pd
import matplotlib.pyplot as plt

pokedex = pd.DataFrame({
    "tipo":  ["Eléctrico", "Fuego", "Planta", "Planta", "Normal"],
    "nivel": [25, 90, 12, 30, 70],
})
promedio = pokedex.groupby("tipo")["nivel"].mean()

fig, ax = plt.subplots()
promedio.plot(kind="bar", ax=ax)
ax.set_title("Nivel promedio por tipo")
ax.set_ylabel("Nivel")
plt.show()
```

## 5️⃣ El campeón de un tipo

```python
import pandas as pd
pokedex = pd.DataFrame({
    "nombre": ["Bulbasaur", "Ivysaur", "Venusaur"],
    "tipo":   ["Planta", "Planta", "Planta"],
    "nivel":  [12, 30, 80],
})
planta = pokedex[pokedex["tipo"] == "Planta"]
campeon = planta.loc[planta["nivel"].idxmax(), "nombre"]
print("Campeón Planta:", campeon)
```

## 🗺️ El flujo del análisis (memorizalo)

1. **Cargar** los datos (`pd.DataFrame`, `read_csv`).
2. **Explorar** (`head`, `info`, `describe`, `isna`).
3. **Limpiar** (`dropna`, `fillna`, `drop_duplicates`).
4. **Resumir** (`groupby`, `value_counts`, `mean`).
5. **Graficar** (matplotlib) y **concluir**.

Ese ciclo es el mismo para 5 Pokémon o para 5 millones de filas de datos reales. 🚀

## ➡️ ¿Y ahora qué?

Cerrá Johto con los [ejercicios de este tema](/ejercicios/analisis-integrador). Cuando los completes, tenés la medalla **Subida** y sos **Campeón de Johto**. 🐉🏆

> ⚡ *"Cargar, limpiar, resumir, graficar, concluir. Ese es el camino del analista."*

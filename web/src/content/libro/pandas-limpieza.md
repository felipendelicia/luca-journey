---
title: "pandas: Limpieza de datos"
order: 240
---

> 🎯 **Meta:** arreglar datos sucios. En la vida real **ningún dataset viene perfecto**: faltan valores, hay duplicados, tipos mal. Limpiar es el paso que nadie ve pero todos necesitan.

Los datos reales son un desastre: un Pokémon sin nivel cargado, filas repetidas, números guardados como texto. Antes de analizar, hay que **limpiar**.

## 🕳️ Datos faltantes (NaN)

Un valor que falta aparece como **`NaN`** (*Not a Number*). pandas tiene herramientas para detectarlos y tratarlos.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "nombre": ["Pikachu", "Charizard", "Bulbasaur"],
    "nivel":  [25, np.nan, 12],
})
print(df.isna())            # True donde falta
print("faltan:", df.isna().sum().sum())   # cuántos NaN en total
```

### Rellenar o eliminar

```python
import pandas as pd
import numpy as np
df = pd.DataFrame({"nombre": ["A", "B", "C"], "nivel": [25, np.nan, 12]})

print(df.fillna(0))    # rellena los NaN con 0
print(df.dropna())     # elimina las filas que tengan algún NaN
```

> ⚠️ `fillna` y `dropna` **devuelven una copia**; no cambian el original salvo que se lo asignes (`df = df.dropna()`).

## 🔢 Tipos de datos

A veces un número viene como texto. Lo convertís con `.astype()`.

```python
import pandas as pd
s = pd.Series(["25", "90", "12"])
print(s.astype(int) + 5)   # ahora sí podés sumar -> 30 95 17
```

## 👯 Duplicados

```python
import pandas as pd
df = pd.DataFrame({"nombre": ["Pikachu", "Pikachu", "Eevee"]})
print(df.drop_duplicates())   # saca filas repetidas
```

## ✏️ Renombrar columnas

```python
import pandas as pd
df = pd.DataFrame({"hp": [35, 78]})
print(df.rename(columns={"hp": "vida"}))
```

## 🔤 Texto y transformaciones

`.str` te da métodos de string para toda la columna; `.apply()` aplica una función a cada valor.

```python
import pandas as pd
nombres = pd.Series(["pikachu", "charizard"])
print(nombres.str.upper())          # PIKACHU CHARIZARD
print(nombres.str.len())            # largo de cada nombre

niveles = pd.Series([25, 90, 12])
print(niveles.apply(lambda x: x * 2))   # función propia a cada valor
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `df.isna()` / `.isna().sum()` | encontrar y contar faltantes |
| `df.fillna(v)` | rellenar NaN |
| `df.dropna()` | eliminar filas con NaN |
| `s.astype(int)` | cambiar el tipo |
| `df.drop_duplicates()` | sacar filas repetidas |
| `df.rename(columns={...})` | renombrar columnas |
| `s.str.upper()`, `s.apply(f)` | transformar texto / aplicar función |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/pandas-limpieza). 💪

> ⚡ *"Datos limpios, conclusiones confiables. Datos sucios, mentiras prolijas."*

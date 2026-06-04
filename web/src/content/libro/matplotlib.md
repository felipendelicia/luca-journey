---
title: "matplotlib: Gráficos"
order: 260
---

> 🎯 **Meta:** **ver** los datos. Un gráfico cuenta en un segundo lo que una tabla esconde en mil filas. Vas a graficar con **matplotlib**.

Los números están buenos, pero un **gráfico** convence. matplotlib es la librería clásica para dibujar: barras, líneas, dispersión, histogramas.

> 💡 Tocá **▶ ejecutar** en los ejemplos: el gráfico aparece abajo, dibujado de verdad en tu navegador. 🎨

## 📊 Gráfico de barras

Lo más común: comparar valores entre categorías (ej: nivel de cada Pokémon).

```python
import matplotlib.pyplot as plt

nombres = ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"]
niveles = [25, 90, 12, 70]

fig, ax = plt.subplots()
ax.bar(nombres, niveles)
ax.set_title("Nivel de mi equipo")
ax.set_ylabel("Nivel")
plt.show()
```

> 💡 El patrón es siempre el mismo: `fig, ax = plt.subplots()` crea el lienzo, después dibujás sobre `ax`, y `plt.show()` lo muestra.

## 📈 Gráfico de línea

Ideal para ver una evolución (ej: cómo sube el nivel con la experiencia).

```python
import matplotlib.pyplot as plt

exp = [0, 100, 250, 500, 800]
nivel = [1, 5, 12, 22, 35]

fig, ax = plt.subplots()
ax.plot(exp, nivel, marker="o")
ax.set_title("Nivel según experiencia")
ax.set_xlabel("EXP")
ax.set_ylabel("Nivel")
plt.show()
```

## ⚬ Dispersión (scatter)

Para ver la **relación** entre dos variables (ej: ataque vs defensa).

```python
import matplotlib.pyplot as plt

ataque  = [55, 84, 49, 110]
defensa = [40, 78, 49, 65]

fig, ax = plt.subplots()
ax.scatter(ataque, defensa)
ax.set_xlabel("Ataque")
ax.set_ylabel("Defensa")
plt.show()
```

## 📊 Histograma

Muestra cómo se **reparten** los valores (ej: ¿hay muchos Pokémon de nivel bajo?).

```python
import matplotlib.pyplot as plt

niveles = [5, 12, 15, 18, 22, 25, 28, 30, 70, 90]

fig, ax = plt.subplots()
ax.hist(niveles, bins=5)
ax.set_title("Distribución de niveles")
plt.show()
```

## 🤝 pandas + matplotlib

Lo mejor: pandas grafica directo. `df.plot(...)` usa matplotlib por dentro.

```python
import pandas as pd
import matplotlib.pyplot as plt

pokedex = pd.DataFrame({"nombre": ["Pikachu", "Charizard", "Snorlax"], "nivel": [25, 90, 70]})
pokedex.plot(x="nombre", y="nivel", kind="bar", legend=False)
plt.title("Niveles")
plt.show()
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `fig, ax = plt.subplots()` | crear el lienzo |
| `ax.bar(x, y)` | gráfico de barras |
| `ax.plot(x, y)` | línea |
| `ax.scatter(x, y)` | dispersión |
| `ax.hist(datos)` | histograma |
| `ax.set_title/xlabel/ylabel(...)` | títulos y etiquetas |
| `plt.show()` | mostrar el gráfico |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/matplotlib). 💪

> ⚡ *"Una imagen vale más que mil filas de un DataFrame."*

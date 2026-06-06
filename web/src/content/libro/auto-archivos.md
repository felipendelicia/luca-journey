---
title: "Automatización: Archivos y rutas"
order: 1001
---

> 🎯 **Meta:** crear, leer y mover archivos desde Python con **`pathlib`**, la base de toda automatización que toca el disco.

---

Automatizar casi siempre significa **trabajar con archivos**: leer un CSV, guardar un reporte, mover fotos a carpetas. Python trae `pathlib`, que trata una ruta como un objeto inteligente en vez de un texto frágil lleno de barras.

## `Path`: una ruta con superpoderes

```python
from pathlib import Path

p = Path("datos/pokedex/kanto.csv")
print(p.name)     # "kanto.csv"   → nombre del archivo
print(p.stem)     # "kanto"       → sin extensión
print(p.suffix)   # ".csv"        → la extensión
print(p.parent)   # "datos/pokedex" → la carpeta que lo contiene
```

Para **armar** rutas, usás `/` (sí, el operador división) y `pathlib` pone las barras por vos, funcione en Windows, Mac o Linux:

```python
carpeta = Path("reportes")
archivo = carpeta / "marzo.txt"     # "reportes/marzo.txt"
nuevo = archivo.with_suffix(".csv") # "reportes/marzo.csv"
```

## Leer y escribir en una línea

Lo más práctico de `pathlib`: escribís y leés texto sin abrir/cerrar nada a mano.

```python
Path("nota.txt").write_text("¡Atrapá a todos!")
contenido = Path("nota.txt").read_text()
print(contenido)   # ¡Atrapá a todos!
```

> 💡 La forma "clásica" es `with open("nota.txt") as f: ...`. Sigue siendo válida y la vas a ver mucho; `write_text`/`read_text` son el atajo para archivos chicos.

## ¿Existe? ¿Es carpeta?

```python
p = Path("datos")
print(p.exists())     # ¿existe?
print(p.is_dir())     # ¿es carpeta?
p.mkdir(exist_ok=True)  # crear carpeta (sin error si ya está)
```

Con esto manejás archivos sueltos. En los ejercicios vas a descomponer rutas y guardar/leer texto.

## ✅ Comprobá lo que aprendiste

```quiz
P: `Path("datos/a/c.txt").name` devuelve…
- "datos/a/c"
+ "c.txt"
- ".txt"
> `.name` es el nombre final del archivo; `.suffix` sería `".txt"`.
```

```quiz
P: ¿Cómo unís una carpeta y un archivo con pathlib?
+ `Path("carpeta") / "archivo.txt"`
- `Path("carpeta") + "archivo.txt"`
- `Path.unir("carpeta", "archivo.txt")`
> Se usa el operador `/` y pathlib pone las barras correctas en cualquier sistema.
```

📁 La **Capitana Lana** te espera para ordenar su carpeta de descargas.

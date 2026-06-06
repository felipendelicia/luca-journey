---
title: "Automatización: Procesar carpetas en lote"
order: 1002
---

> 🎯 **Meta:** hacerle lo mismo a **muchos archivos de una vez** — el superpoder que ahorra horas de trabajo manual.

---

La magia de automatizar aparece cuando dejás de tocar archivos uno por uno. ¿Renombrar 200 fotos? ¿Sumar 50 CSV? Un bucle lo hace en segundos.

## Listar una carpeta

`Path.glob(patrón)` te da los archivos que coinciden con un patrón. El comodín `*` significa "cualquier cosa":

```python
from pathlib import Path

for archivo in Path("descargas").glob("*.png"):
    print(archivo.name)        # todas las imágenes .png
```

¿Querés mirar también dentro de las subcarpetas? Usá `**`:

```python
for archivo in Path("proyecto").glob("**/*.py"):
    print(archivo)             # todos los .py, en cualquier subcarpeta
```

## El patrón "procesar en lote"

Casi toda automatización sigue la misma forma: **recorrer → filtrar → hacer algo**.

```python
archivos = ["IMG_1.png", "IMG_2.png", "notas.txt"]

# filtrar: solo las imágenes
imagenes = [a for a in archivos if a.endswith(".png")]

# transformar: renombrarlas
nuevos = [a.replace("IMG", "foto") for a in imagenes]
print(nuevos)   # ["foto_1.png", "foto_2.png"]
```

## Resumir el lote

Mientras recorrés, vas juntando datos: contar por tipo, sumar tamaños, encontrar el más grande.

```python
archivos = [("a.txt", 10), ("b.txt", 99), ("c.txt", 5)]
total = sum(tam for _, tam in archivos)         # 114
grande = max(archivos, key=lambda par: par[1])  # ("b.txt", 99)
print(total, grande[0])
```

En los ejercicios vas a clasificar y resumir un listado de carpeta. 🔁 El **Capitán Kiawe** quiere ver tu velocidad procesando en lote.

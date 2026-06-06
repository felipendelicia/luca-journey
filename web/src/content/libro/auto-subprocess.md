---
title: "Automatización: Ejecutar programas"
order: 1003
---

> 🎯 **Meta:** que tu script **llame a otros programas** (git, ffmpeg, otro `.py`) y entienda su resultado.

---

Una automatización potente no reinventa todo: **usa programas que ya existen**. Desde Python los lanzás con el módulo **`subprocess`**.

## `subprocess.run`

Le pasás el comando como una **lista**: `[programa, argumento, argumento, ...]`.

```python
import subprocess

resultado = subprocess.run(
    ["echo", "hola"],
    capture_output=True,   # capturá la salida en vez de imprimirla
    text=True,             # salida como texto (no bytes)
)
print(resultado.returncode)   # 0 = salió bien
print(resultado.stdout)       # "hola\n"
```

Tres datos clave del resultado:

- `returncode`: **0** significa éxito; cualquier otro número, que algo falló.
- `stdout`: lo que el programa imprimió.
- `stderr`: los mensajes de error.

> ⚠️ Pasá el comando como **lista** (`["git", "status"]`), no como un solo texto `"git status"`. La lista evita problemas con espacios y es más segura.

> 🌐 **Ojo:** `subprocess` lanza procesos del sistema operativo, así que **no corre acá en el navegador**. En tu compu funciona perfecto. En los ejercicios practicás las dos mitades que sí podemos probar: **armar** el comando (la lista) y **procesar** su salida (el texto).

## Entender la salida

La salida viene como texto con varias líneas. Procesarla es puro Python:

```python
salida = "rama main\n\n  2 cambios  \n"
lineas = [l.strip() for l in salida.splitlines() if l.strip()]
print(lineas)         # ["rama main", "2 cambios"]
print(len(lineas))    # 2
```

## ✅ Comprobá lo que aprendiste

```quiz
P: En subprocess, un `returncode` de 0 significa…
+ que el programa salió bien
- que falló
- que no se ejecutó
> 0 = éxito; cualquier otro número indica un error.
```

```quiz
P: ¿Cómo conviene pasar el comando a `subprocess.run`?
+ como lista: `["git", "status"]`
- como texto: `"git status"`
- como diccionario
> La lista evita problemas con espacios y es más segura.
```

🖥️ La **Capitana Mallow** te espera para armar comandos y leer resultados.

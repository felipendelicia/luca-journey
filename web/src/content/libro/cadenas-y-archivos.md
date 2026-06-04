---
title: "Python: Cadenas y Archivos"
order: 70
---

> 🎯 **Meta:** trabajar con texto en profundidad y hacer que tus datos **sobrevivan** cuando cerrás el programa (guardándolos en archivos).

---

## 🎮 Analogía: la Pokédex que recuerda

Hasta ahora, cuando cerrabas tu programa, todo se borraba: tu equipo, tus capturas, todo. Era una Pokédex con amnesia. 😵

Acá le damos **memoria permanente**: vas a guardar datos en **archivos** del disco. Apagás la compu, volvés mañana, y tu Pokédex se acuerda de todo. 💾

---

## 🔤 Métodos de strings (cadenas de texto)

Un string tiene un montón de **métodos** (acciones) para transformarlo. No modifican el original: **devuelven uno nuevo**.

```python
nombre = "  Pikachu  "

print(nombre.upper())        # "  PIKACHU  "   (mayúsculas)
print(nombre.lower())        # "  pikachu  "   (minúsculas)
print(nombre.strip())        # "Pikachu"       (saca espacios de los bordes)
print(nombre.replace("a", "@"))  # reemplaza
print("pikachu".capitalize())    # "Pikachu"   (primera en mayúscula)
print("Pikachu".startswith("Pika"))  # True
print("Pikachu".endswith("chu"))     # True
print("Pikachu".find("ka"))          # 2  (posición donde aparece)
print(len("Pikachu"))                # 7  (longitud)
```

### split y join: separar y unir

```python
# split: parte un texto en una lista, usando un separador.
linea = "Pikachu,Electrico,25"
partes = linea.split(",")
print(partes)    # ['Pikachu', 'Electrico', '25']

# join: une una lista en un texto, con un separador.
datos = ["Charizard", "Fuego", "50"]
linea = ",".join(datos)
print(linea)     # "Charizard,Fuego,50"
```

> 💡 `split` y `join` son **clave** para trabajar con archivos CSV (lo vemos abajo).

---

## ✂️ Slicing: rebanar strings

El **slicing** saca una "rebanada" de un string usando `[inicio:fin]`. El `fin` NO se incluye.

```python
texto = "Pikachu"
#        0123456     (índices)

print(texto[0])      # "P"        (un carácter)
print(texto[0:4])    # "Pika"     (del 0 al 3)
print(texto[4:])     # "chu"      (del 4 hasta el final)
print(texto[:4])     # "Pika"     (del principio al 3)
print(texto[-3:])    # "chu"      (los últimos 3)
print(texto[::-1])   # "uhcakiP"  (al revés)
```

---

## 📂 Abrir archivos con open()

`open()` abre un archivo. Le pasás el nombre y el **modo**:

| Modo | Significa |
|------|-----------|
| `"r"` | leer (*read*) — el archivo debe existir |
| `"w"` | escribir (*write*) — crea o REEMPLAZA todo |
| `"a"` | agregar (*append*) — escribe al final |

```python
# Escribir (¡pisa lo que había!)
archivo = open("equipo.txt", "w")
archivo.write("Pikachu\n")     # \n = salto de línea
archivo.write("Charizard\n")
archivo.close()                # ¡siempre hay que cerrar!
```

---

## ✅ with: la forma correcta de abrir archivos

El problema de `open()` solo es que hay que acordarse de `close()`. La forma recomendada es usar **`with`**, que cierra el archivo solo, aunque haya un error.

```python
# Escribir
with open("equipo.txt", "w") as archivo:
    archivo.write("Pikachu\n")
    archivo.write("Charizard\n")
# Al salir del 'with', el archivo se cierra automáticamente. 🎉

# Leer todo de una
with open("equipo.txt", "r") as archivo:
    contenido = archivo.read()
    print(contenido)

# Leer línea por línea (lo más común)
with open("equipo.txt", "r") as archivo:
    for linea in archivo:
        print(linea.strip())   # strip saca el \n del final
```

> 💡 Usá **siempre** `with`. Es más corto, más seguro, y es lo que vas a ver en todos lados.

---

## 📊 CSV: datos en filas y columnas

Un **CSV** (*Comma-Separated Values*) es un archivo de texto donde cada línea es una fila y los datos van separados por comas. Es como una mini planilla de Excel.

```
nombre,tipo,nivel
Pikachu,Electrico,25
Charizard,Fuego,50
```

Lo podés manejar con `split` y `join`, o con el módulo `csv` de la librería estándar:

```python
import csv

# Escribir un CSV
with open("pokedex.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(["nombre", "tipo", "nivel"])   # encabezado
    escritor.writerow(["Pikachu", "Electrico", 25])
    escritor.writerow(["Charizard", "Fuego", 50])

# Leer un CSV
with open("pokedex.csv", "r", encoding="utf-8") as f:
    lector = csv.reader(f)
    for fila in lector:
        print(fila)    # cada fila es una lista: ['Pikachu', 'Electrico', '25']
```

> 💡 `newline=""` y `encoding="utf-8"` son detalles que evitan problemas. Copialos siempre que uses CSV.

---

## ⚠️ Manejo de excepciones: try / except

Un **error** (excepción) puede romper tu programa: abrir un archivo que no existe, convertir "abc" a número, etc. Con `try`/`except` lo **atrapás** y seguís adelante.

```python
try:
    # Código que PODRÍA fallar.
    numero = int(input("Nivel: "))
    print(f"El nivel es {numero}")
except ValueError:
    # Esto corre SOLO si hubo un ValueError.
    print("Eso no es un número válido")
```

Atrapar errores al abrir archivos:

```python
try:
    with open("noexiste.txt", "r") as f:
        contenido = f.read()
except FileNotFoundError:
    print("El archivo no existe, creando uno nuevo...")
    contenido = ""
```

Errores comunes que vas a atrapar:
- `ValueError` → conversión inválida (`int("abc")`).
- `FileNotFoundError` → archivo que no existe.
- `KeyError` → clave que no está en un diccionario.
- `ZeroDivisionError` → división por cero.

> 💡 Atrapá **errores específicos** (como `ValueError`), no un `except:` pelado. Así sabés qué estás manejando.

---

## 📝 Resumen

```python
# Métodos de string
"  Hola  ".strip().upper()      # "HOLA"
"a,b,c".split(",")              # ['a', 'b', 'c']
",".join(["a", "b"])           # "a,b"

# Slicing
"Pikachu"[0:4]                  # "Pika"

# Archivos con with
with open("datos.txt", "w") as f:
    f.write("hola\n")

with open("datos.txt", "r") as f:
    for linea in f:
        print(linea.strip())

# CSV con la librería estándar
import csv
# csv.writer / csv.reader

# Manejo de errores
try:
    n = int("abc")
except ValueError:
    print("no es número")
```

| Concepto | Para qué sirve |
|----------|----------------|
| métodos de string | Transformar texto |
| `split` / `join` | Separar / unir texto |
| slicing `[i:j]` | Rebanar texto |
| `with open()` | Abrir archivos seguro |
| módulo `csv` | Datos en filas/columnas |
| `try`/`except` | Atrapar errores |

---

## ➡️ ¿Y ahora qué?

Ahora **practicá**: andá a los [ejercicios de este tema](/ejercicios/cadenas-y-archivos) y resolvelos. Se corrigen al instante con tests reales en tu navegador. 💪

> ⚡ *"Los datos que no guardás, se los lleva el viento. Una buena Pokédex nunca olvida."*

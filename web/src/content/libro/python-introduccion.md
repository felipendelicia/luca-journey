---
title: "Python: Introducción"
order: 30
---

> 🎯 **Meta:** escribir tus primeros programas en Python. Vas a aprender a guardar datos en variables, mostrar cosas en pantalla y pedirle información al usuario.

---

## 🧬 ¿Qué es Python?

**Python** es un lenguaje de programación. Un "lenguaje" es la forma en que le das **órdenes a la computadora**. Python es famoso porque se lee casi como inglés, es fácil de aprender y se usa para TODO: webs, videojuegos, inteligencia artificial, análisis de datos...

### 🎮 Analogía Pokémon

Pensá en Python como el **idioma de los Entrenadores**. Vos escribís instrucciones (el código) y la computadora las obedece como un Pokémon bien entrenado obedece a su dueño. Cuanto mejor escribas las órdenes, mejor pelea tu equipo.

---

## 🚀 ¿Cómo se corre Python?

Hay dos formas principales:

### 1. El REPL (modo interactivo)
Escribís `python3` en la terminal y se abre un intérprete donde probás cosas al instante:

```python
>>> 2 + 2
4
>>> print("Hola")
Hola
```

El `>>>` es el prompt de Python. Es ideal para **experimentar**. Para salir, escribís `exit()`.

### 2. Archivos `.py`
Escribís tu programa en un archivo, por ejemplo `programa.py`, y lo corrés:

```bash
python3 programa.py
```

Así hacés programas de verdad que podés guardar y reusar.

---

## 🖨️ print(): mostrar cosas en pantalla

`print()` muestra texto o valores en la pantalla. Es lo primero que hace todo programador.

```python
print("¡Hola, mundo Pokémon!")
print("Elegí a Pikachu como inicial")
```

Podés imprimir varias cosas separándolas con comas:

```python
print("Mi Pokémon es", "Charizard")   # Mi Pokémon es Charizard
```

---

## 📦 Variables: cajas con nombre

Una **variable** guarda un dato con un nombre, para usarlo después. Es como una **Pokéball**: adentro guardás algo y le ponés una etiqueta.

```python
nombre = "Pikachu"      # guardamos el texto "Pikachu" en la variable nombre
nivel = 25              # guardamos el número 25 en la variable nivel
print(nombre)           # Pikachu
print(nivel)            # 25
```

Regla: el nombre va a la izquierda del `=`, el valor a la derecha. **No** lleva espacios raros ni empieza con números.

```python
pokemon_inicial = "Charmander"   # ✅ bien (guiones bajos para separar palabras)
3pokemon = "no"                  # ❌ mal (no puede empezar con número)
```

---

## 🏷️ Tipos de datos

Cada dato tiene un **tipo**. Los cuatro básicos:

| Tipo | Qué es | Ejemplo Pokémon |
|------|--------|-----------------|
| `int` | Número entero | nivel = `25`, hp = `100` |
| `float` | Número con decimales | peso = `6.0`, altura = `0.4` |
| `str` | Texto (*string*) | nombre = `"Pikachu"` |
| `bool` | Verdadero o falso | es_legendario = `True` |

```python
nivel = 25            # int
peso = 6.0            # float
nombre = "Pikachu"    # str (siempre entre comillas)
es_legendario = False # bool (True o False, con mayúscula)
```

Para ver el tipo de algo, usás `type()`:

```python
print(type(nivel))    # <class 'int'>
print(type(nombre))   # <class 'str'>
```

```quiz
P: ¿De qué tipo es el valor `6.0`?
- int
+ float
- str
> Tiene decimales (el `.0`), así que es un **float**. Un `int` sería `6`, sin la coma.
```

---

```quiz
P: ¿Qué hace `input()` cuando el usuario escribe el número `42`?
- Devuelve el entero 42
- Devuelve el float 42.0
+ Devuelve el texto "42"
> `input()` SIEMPRE devuelve un `str`, sin importar qué escriba el usuario. Para tener el número, hay que convertirlo con `int()`.
```

---

## ⌨️ input(): pedirle datos al usuario

`input()` **pausa** el programa y espera a que el usuario escriba algo y apriete Enter. Lo que escribe se guarda como texto.

```python
nombre = input("¿Cómo se llama tu Pokémon? ")
print("¡Hola,", nombre + "!")
```

> ⚠️ **MUY IMPORTANTE:** `input()` SIEMPRE devuelve **texto (str)**, aunque el usuario escriba un número. Si querés un número, hay que convertirlo (lo vemos ahora).

---

## 🔄 Conversión de tipos

Para convertir entre tipos, usás funciones con el nombre del tipo:

```python
nivel_texto = input("¿Nivel de tu Pokémon? ")   # esto es str, ej "25"
nivel = int(nivel_texto)                          # ahora es int: 25
print(nivel + 5)                                  # 30 (suma de números)
```

Funciones de conversión:
- `int("25")` → `25` (texto a entero)
- `float("6.5")` → `6.5` (texto a decimal)
- `str(25)` → `"25"` (número a texto)

```python
# Forma compacta, muy común:
edad = int(input("¿Tu edad? "))    # pide y convierte en una sola línea
```

---

## 💬 Comentarios

Un **comentario** es texto que Python ignora. Sirve para explicar tu código. Empieza con `#`.

```python
# Esto es un comentario, Python no lo ejecuta.
nombre = "Pikachu"   # también podés comentar al final de una línea
```

Comentar bien tu código es de buen programador. Tu yo del futuro te lo va a agradecer.

---

## ✨ f-strings: la forma copada de armar texto

Un **f-string** te deja meter variables dentro de un texto poniendo una `f` antes de las comillas y las variables entre `{llaves}`.

```python
nombre = "Pikachu"
nivel = 25

# Forma vieja (funciona pero es incómoda):
print("Mi " + nombre + " es nivel " + str(nivel))

# Forma copada con f-string:
print(f"Mi {nombre} es nivel {nivel}")   # Mi Pikachu es nivel 25
```

Los f-strings son **la forma recomendada**. Fijate que no hace falta convertir el número con `str()`: el f-string lo hace solo. 🎉

```python
hp = 100
ataque = 55
print(f"{nombre} tiene {hp} HP y {ataque} de ataque")
```

---

## 📝 Resumen

```python
# Variables: caja con nombre
nombre = "Pikachu"

# Tipos: int, float, str, bool
nivel = 25          # int
peso = 6.0          # float
texto = "hola"      # str
activo = True       # bool

# print: mostrar en pantalla
print("Hola")

# input: pedir datos (devuelve SIEMPRE texto)
edad = input("Edad: ")

# Conversión de tipos
numero = int("25")
texto = str(25)

# f-string: armar texto con variables
print(f"{nombre} es nivel {nivel}")
```

| Concepto | Para qué sirve |
|----------|----------------|
| `print()` | Mostrar cosas |
| variable | Guardar un dato |
| `int/float/str/bool` | Los tipos de datos |
| `input()` | Pedir datos al usuario |
| `int()`, `str()` | Convertir tipos |
| `#` | Comentar |
| `f"..."` | Armar texto con variables |

---

## ➡️ ¿Y ahora qué?

Ahora **practicá**: andá a los [ejercicios de este tema](/ejercicios/python-introduccion) y resolvelos. Se corrigen al instante con tests reales en tu navegador. 💪

> ⚡ *"El viaje de mil Pokémon empieza con un solo `print()`."*

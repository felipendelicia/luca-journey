# 🐍 Semana 05 — Python: Funciones

> 🎯 **Meta de la semana:** aprender a empaquetar código en **funciones** para reusarlo, organizarlo y no repetirte. Es uno de los conceptos más importantes de toda la programación.

---

## 🎮 Analogía: los ataques aprendidos

Un Pokémon aprende un ataque **una vez** y lo puede usar **mil veces**. No tiene que reaprender "Impactrueno" en cada batalla: lo sabe, le pone un nombre, y lo invoca cuando quiere.

Una **función** es eso: un bloque de código que escribís **una vez**, le ponés un **nombre**, y lo **llamás** (lo usás) todas las veces que quieras. ⚡

---

## 🛠️ Definir una función con def

```python
def saludar():
    print("¡Hola, Entrenador!")
```

Desglose:
- `def` → palabra clave para **def**inir una función.
- `saludar` → el nombre que le ponés.
- `()` → los paréntesis (después vemos qué va adentro).
- `:` → dos puntos, obligatorios.
- El cuerpo va **indentado** (4 espacios), igual que en los `if`.

**Definir** una función no la ejecuta. Para ejecutarla, la **llamás** por su nombre:

```python
saludar()    # ¡Hola, Entrenador!
saludar()    # ¡Hola, Entrenador!  (la usamos de nuevo, gratis)
```

---

## 📥 Parámetros: darle datos a la función

Un **parámetro** es un dato que la función recibe para trabajar. Va dentro de los paréntesis.

```python
def saludar(nombre):
    print(f"¡Hola, {nombre}!")

saludar("Ash")      # ¡Hola, Ash!
saludar("Misty")    # ¡Hola, Misty!
```

Podés tener varios parámetros, separados por comas:

```python
def presentar(nombre, tipo):
    print(f"{nombre} es de tipo {tipo}")

presentar("Pikachu", "Eléctrico")
```

> 💡 "Parámetro" es el nombre en la definición (`nombre`). "Argumento" es el valor que pasás al llamar (`"Ash"`). Mucha gente usa los términos como sinónimos, no te preocupes por eso.

---

## 📤 return: devolver un resultado

`return` hace que la función **devuelva** un valor para usarlo después. Es la diferencia entre una función que solo "muestra" y una que "calcula y entrega".

```python
def calcular_dano(ataque, defensa):
    return ataque - defensa

# Guardamos lo que devuelve en una variable.
resultado = calcular_dano(50, 20)
print(resultado)    # 30

# O lo usamos directamente.
print(calcular_dano(80, 30))   # 50
```

> ⚠️ Cuando Python ejecuta un `return`, **sale** de la función inmediatamente. El código que esté después del `return` no se ejecuta.

### print vs return — la confusión clásica

```python
def con_print(x):
    print(x * 2)        # MUESTRA en pantalla, pero no devuelve nada

def con_return(x):
    return x * 2        # DEVUELVE el valor para seguir usándolo

a = con_print(5)        # imprime 10, pero a queda en None
b = con_return(5)       # no imprime nada, pero b vale 10
print(b + 1)            # 11  (porque b es un número de verdad)
```

Regla práctica: si querés **usar** el resultado después, usá `return`.

---

## 🎚️ Valores por defecto

Podés darle a un parámetro un valor por defecto, que se usa si no pasás nada:

```python
def atacar(nombre, dano=10):       # dano vale 10 si no se especifica
    print(f"{nombre} hizo {dano} de daño")

atacar("Pikachu")          # Pikachu hizo 10 de daño  (usa el default)
atacar("Charizard", 35)    # Charizard hizo 35 de daño (lo pisamos)
```

---

## 🌐 Scope: dónde vive cada variable

El **scope** (alcance) es la zona donde una variable existe. Una variable creada **adentro** de una función **solo existe ahí adentro**. Es como un Pokémon dentro de su Pokéball: afuera no se lo ve.

```python
def entrenar():
    secreto = "técnica oculta"    # variable LOCAL: solo vive acá adentro
    print(secreto)

entrenar()
# print(secreto)   # ❌ ERROR: 'secreto' no existe afuera de la función
```

Las variables creadas afuera son **globales** y se pueden leer adentro:

```python
entrenador = "Ash"        # variable global

def saludar():
    print(f"Hola {entrenador}")   # puede leer la global

saludar()    # Hola Ash
```

---

## ⚡ Funciones lambda: funciones express

Una **lambda** es una función chiquita de una sola línea, sin nombre. Útil para cosas simples.

```python
# Función normal:
def doble(x):
    return x * 2

# La misma como lambda:
doble = lambda x: x * 2

print(doble(5))    # 10
```

La estructura es: `lambda parámetros: expresión`. El resultado de la expresión es lo que devuelve.

```python
sumar = lambda a, b: a + b
print(sumar(3, 4))    # 7
```

> 💡 Las lambda se usan mucho para ordenar o filtrar (lo vas a ver en la semana 6). Por ahora, alcanza con saber qué son.

---

## 📖 Docstrings: documentar tu función

Un **docstring** es un texto (entre `"""triple comillas"""`) justo abajo del `def`, que explica qué hace la función.

```python
def calcular_dano(ataque, defensa):
    """Calcula el daño restando la defensa al ataque."""
    return ataque - defensa
```

Sirve para que vos (y otros) entiendan la función sin leer todo el código. Es de buena programadora documentar así.

---

## 🔁 Recursión: una función que se llama a sí misma

**Recursión** es cuando una función se llama a sí misma para resolver un problema más chico. Suena raro, pero es potente.

El ejemplo clásico es el **factorial** (5! = 5×4×3×2×1):

```python
def factorial(n):
    # Caso base: el punto donde la recursión FRENA.
    if n <= 1:
        return 1
    # Caso recursivo: la función se llama a sí misma con un número más chico.
    return n * factorial(n - 1)

print(factorial(5))    # 120
```

> ⚠️ Toda recursión necesita un **caso base** (una condición que la frene). Sin él, se llama infinitamente y revienta. Es como las muñecas rusas: en algún momento llegás a la más chiquita.

---

## 📝 Resumen de la semana

```python
# Definir
def atacar(nombre, dano=10):
    """Muestra un ataque (docstring)."""
    return f"{nombre} hizo {dano} de daño"

# Llamar
mensaje = atacar("Pikachu", 25)

# return devuelve un valor; print solo muestra
# Valores por defecto: dano=10
# Scope: las variables locales no existen afuera
# Lambda: función express
doble = lambda x: x * 2
# Recursión: función que se llama a sí misma (necesita caso base)
```

| Concepto | Para qué sirve |
|----------|----------------|
| `def` | Definir una función |
| parámetros | Pasarle datos |
| `return` | Devolver un resultado |
| valor por defecto | Parámetro opcional |
| scope | Dónde vive una variable |
| `lambda` | Función chica de una línea |
| docstring | Documentar qué hace |
| recursión | Función que se llama a sí misma |

---

## ➡️ ¿Y ahora qué?

1. Resolvé `ejercicios.py` (varios te piden refactorizar código repetido en funciones).
2. Corré los tests: `pytest semana-05-python-funciones/`
3. Jugá la **calculadora de estadísticas Pokémon**:
   ```bash
   python interactivo.py
   ```

> ⚡ *"Una buena función es como un buen ataque: la aprendés una vez y te sirve toda la vida."*

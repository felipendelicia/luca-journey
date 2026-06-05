---
title: "Python: Control de Flujo"
order: 40
---

> 🎯 **Meta:** que tu programa **tome decisiones** y **repita** cosas. Hasta ahora tu código corría en línea recta. Ahora va a poder elegir caminos y dar vueltas.

---

## 🎮 Analogía: decisiones en batalla

En una batalla Pokémon, vos tomás decisiones todo el tiempo: *"SI el rival es de tipo Agua, USO un ataque Eléctrico"*. Y repetís acciones: *"MIENTRAS el rival tenga HP, sigo atacando"*.

Eso es exactamente el **control de flujo**: decirle al programa **cuándo** hacer algo (decisiones) y **cuántas veces** hacerlo (repeticiones).

---

## 🔀 if: tomar decisiones

`if` ejecuta un bloque de código **solo si** una condición es verdadera.

```python
nivel = 30

if nivel >= 25:
    print("¡Tu Pokémon puede evolucionar!")
```

> ⚠️ **La indentación importa.** El código "adentro" del `if` va con **4 espacios** de sangría. Python usa esa sangría para saber qué está adentro y qué afuera. No es decorativo: es obligatorio.

---

```quiz
P: ¿Qué es lo que hace que el código adentro de un `if` se ejecute?
- Que la línea empiece con cuatro espacios
+ Que la condición sea verdadera (`True`)
- Que la variable no sea `None`
> La indentación le dice a Python qué código está "adentro", pero ese código solo se ejecuta si la condición del `if` es `True`.
```

---

## 🔢 Operadores de comparación

Sirven para construir condiciones. Devuelven `True` o `False`:

| Operador | Significa | Ejemplo | Resultado |
|----------|-----------|---------|-----------|
| `==` | igual a | `nivel == 25` | True si nivel es 25 |
| `!=` | distinto de | `tipo != "Agua"` | True si no es Agua |
| `>` | mayor que | `hp > 0` | True si hp es positivo |
| `<` | menor que | `nivel < 100` | |
| `>=` | mayor o igual | `nivel >= 25` | |
| `<=` | menor o igual | `hp <= 0` | |

> ⚠️ **Ojo:** `=` asigna (guarda en una variable), `==` compara. ¡No los confundas!

```python
nivel = 25      # asignación: guardo 25 en nivel
nivel == 25     # comparación: ¿nivel es igual a 25? → True
```

---

## 🪜 elif y else: más caminos

`else` es el "si no". `elif` ("else if") agrega más condiciones a chequear.

```python
hp = 40

if hp > 70:
    print("Tu Pokémon está sano 💚")
elif hp > 30:
    print("Tu Pokémon está cansado 💛")
elif hp > 0:
    print("¡Tu Pokémon está grave! ❤️")
else:
    print("Tu Pokémon se debilitó 💀")
```

Python revisa las condiciones **de arriba hacia abajo** y entra en la **primera** que sea verdadera. Las demás las ignora.

---

## 🧠 Operadores lógicos: and, or, not

Combinan varias condiciones:

- `and` → verdadero si **ambas** son verdaderas.
- `or` → verdadero si **al menos una** es verdadera.
- `not` → invierte (verdadero ↔ falso).

```python
nivel = 30
tipo = "Fuego"

# Evoluciona SI tiene nivel suficiente Y es de fuego.
if nivel >= 25 and tipo == "Fuego":
    print("¡Charmander evoluciona a Charmeleon!")

# Es fuerte SI es legendario O tiene nivel 100.
if es_legendario or nivel == 100:
    print("¡Pokémon poderoso!")

# Puede pelear SI NO está debilitado.
if not debilitado:
    print("¡A la batalla!")
```

---

## 🔁 while: repetir mientras...

`while` repite un bloque **mientras** una condición sea verdadera. Es el bucle de "seguí hasta que...".

```python
hp_rival = 100

while hp_rival > 0:
    print(f"Atacás. HP del rival: {hp_rival}")
    hp_rival = hp_rival - 20   # bajamos el HP en cada vuelta

print("¡Ganaste la batalla! 🏆")
```

> ⚠️ **¡Cuidado con los bucles infinitos!** Si la condición nunca se vuelve falsa, el programa nunca termina. Asegurate de que algo cambie adentro del `while` (acá, el HP baja).

---

## 🔂 for: repetir una cantidad de veces

`for` recorre una secuencia de valores, uno por uno. Es el bucle de "para cada...".

```python
# Recorre una lista de Pokémon (las listas las vemos a fondo más adelante).
equipo = ["Pikachu", "Charizard", "Snorlax"]

for pokemon in equipo:
    print(f"Tengo a {pokemon}")
```

### range(): generar números

`range()` genera una secuencia de números, ideal para repetir N veces.

```python
# Repite 5 veces (del 0 al 4).
for i in range(5):
    print(f"Lanzamiento de Pokéball número {i + 1}")

# range(inicio, fin): del 1 al 10 (el 'fin' NO se incluye).
for nivel in range(1, 11):
    print(f"Nivel {nivel}")

# range(inicio, fin, paso): de 0 a 100 de 10 en 10.
for hp in range(0, 101, 10):
    print(hp)
```

> 💡 Recordá: `range(5)` da `0, 1, 2, 3, 4` (empieza en 0, termina **antes** del 5).

---

```quiz
P: ¿Qué imprime `range(3)` si lo recorrés con `for i in range(3): print(i)`?
- 1, 2, 3
- 0, 1, 2, 3
+ 0, 1, 2
> `range(3)` genera los números del 0 al 2 (tres números). El límite final NO se incluye.
```

---

## ⏭️ break y continue

Controlan el bucle desde adentro:

- `break` → **corta** el bucle por completo.
- `continue` → **saltea** el resto de esta vuelta y pasa a la siguiente.

```python
# break: dejamos de buscar al encontrar a Mewtwo.
for pokemon in equipo:
    if pokemon == "Mewtwo":
        print("¡Encontramos a Mewtwo!")
        break          # salimos del for inmediatamente

# continue: salteamos a los Pokémon debilitados.
for pokemon in equipo:
    if pokemon == "debilitado":
        continue       # saltamos a la próxima vuelta
    print(f"{pokemon} entra a la batalla")
```

---

## 📝 Resumen

```python
# if / elif / else: decisiones
if hp > 50:
    print("sano")
elif hp > 0:
    print("herido")
else:
    print("debilitado")

# Comparadores: ==, !=, >, <, >=, <=
# Lógicos: and, or, not
if nivel >= 25 and tipo == "Fuego":
    print("evoluciona")

# while: repetir mientras una condición sea verdadera
while hp > 0:
    hp -= 20

# for + range: repetir N veces
for i in range(5):
    print(i)

# break corta el bucle; continue saltea una vuelta
```

| Concepto | Para qué sirve |
|----------|----------------|
| `if/elif/else` | Elegir qué código correr |
| `==, !=, >, <` | Comparar valores |
| `and, or, not` | Combinar condiciones |
| `while` | Repetir mientras algo sea cierto |
| `for` + `range()` | Repetir una cantidad de veces |
| `break` | Cortar el bucle |
| `continue` | Saltar a la próxima vuelta |

---

## ➡️ ¿Y ahora qué?

Ahora **practicá**: andá a los [ejercicios de este tema](/ejercicios/control-de-flujo) y resolvelos. Se corrigen al instante con tests reales en tu navegador. 💪

> ⚡ *"En la batalla y en el código, las buenas decisiones ganan combates."*

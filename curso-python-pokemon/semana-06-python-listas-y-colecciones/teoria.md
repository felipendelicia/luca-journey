# 🐍 Semana 06 — Python: Listas y Colecciones

> 🎯 **Meta de la semana:** guardar **muchos** datos juntos. Hasta ahora cada variable guardaba UNA cosa. Ahora vas a manejar equipos enteros, Pokédex completas y mucho más.

---

## 🎮 Analogía: tu equipo Pokémon

Un Entrenador no lleva un solo Pokémon: lleva un **equipo** (hasta 6). Una **lista** es justamente eso: una colección ordenada de cosas guardadas bajo un solo nombre. ⚾⚾⚾

---

## 📋 Listas: colección ordenada y modificable

Una **lista** se escribe entre corchetes `[]`, con los elementos separados por comas.

```python
equipo = ["Pikachu", "Charizard", "Snorlax"]
niveles = [25, 50, 40]
mezcla = ["Pikachu", 25, True]   # puede tener tipos distintos
vacia = []                        # una lista vacía
```

### Acceder por índice

Cada elemento tiene una **posición (índice)**. ¡Empieza en 0!

```python
equipo = ["Pikachu", "Charizard", "Snorlax"]
print(equipo[0])    # Pikachu  (el primero)
print(equipo[1])    # Charizard
print(equipo[-1])   # Snorlax  (el último, contando desde atrás)
```

### Modificar

```python
equipo[0] = "Raichu"     # cambiamos el primero (Pikachu evolucionó)
print(equipo)            # ['Raichu', 'Charizard', 'Snorlax']
```

---

## 🔧 Métodos de listas (las acciones de tu equipo)

```python
equipo = ["Pikachu", "Charizard"]

equipo.append("Snorlax")     # agrega al final → ['Pikachu','Charizard','Snorlax']
equipo.insert(0, "Mewtwo")   # inserta en una posición
equipo.remove("Charizard")   # borra por valor
ultimo = equipo.pop()        # saca y devuelve el último
print(len(equipo))           # cantidad de elementos
print("Pikachu" in equipo)   # ¿está? → True o False
equipo.sort()                # ordena la lista
equipo.reverse()             # la da vuelta
```

| Método | Qué hace |
|--------|----------|
| `.append(x)` | Agrega x al final |
| `.insert(i, x)` | Inserta x en la posición i |
| `.remove(x)` | Borra la primera aparición de x |
| `.pop()` | Saca y devuelve el último |
| `len(lista)` | Cantidad de elementos |
| `x in lista` | ¿x está en la lista? |
| `.sort()` | Ordena |
| `.reverse()` | Invierte el orden |

---

## 📌 Tuplas: colección que NO se modifica

Una **tupla** es como una lista, pero **inmutable** (no se puede cambiar). Se escribe con paréntesis `()`. Sirve para datos fijos.

```python
coordenada = (10, 20)         # una posición que no debería cambiar
tipos_pikachu = ("Electrico",)  # tupla de un solo elemento (ojo a la coma)

print(coordenada[0])    # 10
# coordenada[0] = 5     # ❌ ERROR: una tupla no se puede modificar
```

> 💡 Usá tupla cuando los datos NO deberían cambiar (como las coordenadas de un punto). Usá lista cuando sí (como tu equipo, que cambia).

---

## 🎯 Sets: colección SIN duplicados

Un **set** (conjunto) guarda elementos **únicos**, sin orden y sin repetidos. Se escribe con llaves `{}`.

```python
tipos_vistos = {"Fuego", "Agua", "Fuego", "Planta"}
print(tipos_vistos)    # {'Fuego', 'Agua', 'Planta'}  (el Fuego repetido desaparece)

tipos_vistos.add("Electrico")    # agregar
print("Agua" in tipos_vistos)    # True
```

Útil para sacar duplicados de una lista:

```python
capturados = ["Pikachu", "Pidgey", "Pikachu", "Rattata"]
unicos = set(capturados)
print(len(unicos))    # 3 (sin contar el Pikachu repetido)
```

---

## 🗂️ Diccionarios: pares clave → valor

Un **diccionario** guarda pares de **clave: valor**. Es como una Pokédex de verdad: buscás por nombre y obtenés los datos. Se escribe con llaves `{}`.

```python
pikachu = {
    "nombre": "Pikachu",
    "tipo": "Electrico",
    "nivel": 25,
    "hp": 100,
}

print(pikachu["nombre"])    # Pikachu  (accedés por la clave)
print(pikachu["nivel"])     # 25
```

### Modificar y agregar

```python
pikachu["nivel"] = 26           # cambiar un valor
pikachu["ataque"] = 55          # agregar una clave nueva
print(pikachu.get("defensa", 0))  # .get() devuelve un default si la clave no está
```

### Recorrer un diccionario

```python
for clave in pikachu:
    print(clave, "->", pikachu[clave])

# O directamente clave y valor con .items()
for clave, valor in pikachu.items():
    print(f"{clave}: {valor}")
```

| Operación | Cómo |
|-----------|------|
| Acceder | `dic["clave"]` |
| Acceso seguro | `dic.get("clave", default)` |
| Agregar/cambiar | `dic["clave"] = valor` |
| Borrar | `del dic["clave"]` |
| ¿Existe la clave? | `"clave" in dic` |
| Recorrer | `for k, v in dic.items():` |

---

## ✨ Comprensiones de listas: crear listas en una línea

Una **comprensión** arma una lista nueva a partir de otra, en una sola línea. Es elegante y muy "pythónico".

```python
niveles = [25, 50, 40, 15]

# Forma larga:
dobles = []
for n in niveles:
    dobles.append(n * 2)

# Comprensión (la misma cosa, en una línea):
dobles = [n * 2 for n in niveles]
print(dobles)    # [50, 100, 80, 30]

# Con condición (filtrar):
altos = [n for n in niveles if n >= 40]
print(altos)     # [50, 40]
```

Estructura: `[expresión for elemento in coleccion if condición]`.

---

## 🔁 enumerate y zip

### enumerate: índice + valor a la vez

```python
equipo = ["Pikachu", "Charizard", "Snorlax"]

for indice, pokemon in enumerate(equipo):
    print(f"{indice + 1}. {pokemon}")
# 1. Pikachu
# 2. Charizard
# 3. Snorlax
```

### zip: recorrer dos listas en paralelo

```python
nombres = ["Pikachu", "Charizard"]
niveles = [25, 50]

for nombre, nivel in zip(nombres, niveles):
    print(f"{nombre} es nivel {nivel}")
# Pikachu es nivel 25
# Charizard es nivel 50
```

---

## 📝 Resumen de la semana

```python
# Lista: ordenada y modificable
equipo = ["Pikachu", "Charizard"]
equipo.append("Snorlax")

# Tupla: inmutable
punto = (10, 20)

# Set: sin duplicados
tipos = {"Fuego", "Agua"}

# Diccionario: clave -> valor
pikachu = {"nombre": "Pikachu", "nivel": 25}

# Comprensión: lista en una línea
dobles = [n * 2 for n in [1, 2, 3]]

# enumerate y zip
for i, p in enumerate(equipo): ...
for n, l in zip(nombres, niveles): ...
```

| Colección | Símbolo | Característica |
|-----------|---------|---------------|
| Lista | `[]` | Ordenada, modificable |
| Tupla | `()` | Ordenada, inmutable |
| Set | `{}` | Única, sin orden |
| Diccionario | `{clave: valor}` | Pares clave-valor |

---

## ➡️ ¿Y ahora qué?

1. Resolvé `ejercicios.py` (énfasis en manipular datos).
2. Corré los tests: `pytest semana-06-python-listas-y-colecciones/`
3. Jugá el **gestor de equipo Pokémon**:
   ```bash
   python interactivo.py
   ```

> ⚡ *"Un buen Entrenador conoce a cada miembro de su equipo. Un buen programador conoce sus estructuras de datos."*

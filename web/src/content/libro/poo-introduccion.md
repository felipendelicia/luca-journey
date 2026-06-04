---
title: "Python: POO Introducción"
order: 80
---

> 🎯 **Meta de la semana:** aprender **Programación Orientada a Objetos (POO)**. Vas a crear tus propios "moldes" para fabricar Pokémon, cada uno con sus datos y sus acciones.

---

## 🎮 Analogía: el molde y los Pokémon

Imaginá la **especie "Pikachu"** como un **molde**: define que todo Pikachu tiene un nombre, un nivel, HP, y que puede usar Impactrueno. Pero TU Pikachu y el Pikachu de Ash son **individuos distintos**: mismo molde, datos diferentes.

En POO:
- El **molde** se llama **clase** (la especie, el plano).
- Cada **individuo** fabricado con ese molde se llama **objeto** o **instancia** (tu Pikachu concreto).

---

## 🏗️ Definir una clase

Una **clase** se define con la palabra `class`. Por convención, su nombre empieza con **mayúscula**.

```python
class Pokemon:
    pass    # por ahora vacía
```

Para **crear un objeto** (instancia) de esa clase, la llamás como si fuera una función:

```python
mi_pokemon = Pokemon()    # fabricamos un Pokémon con el molde
```

---

## 🧬 __init__: el constructor

El método `__init__` es el **constructor**: se ejecuta automáticamente cuando creás un objeto. Sirve para darle sus datos iniciales.

```python
class Pokemon:
    def __init__(self, nombre, tipo, nivel):
        # 'self' es el objeto que se está creando.
        # Guardamos los datos DENTRO del objeto con self.
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel

# Al crear el objeto, pasamos los datos que pide __init__.
pikachu = Pokemon("Pikachu", "Electrico", 25)
print(pikachu.nombre)    # Pikachu
print(pikachu.nivel)     # 25
```

### ¿Qué es `self`?

`self` es el **propio objeto**. Es la forma en que el objeto se refiere a sí mismo. Cuando hacés `self.nombre = nombre`, estás diciendo *"guardá este nombre adentro mío"*.

> 💡 `self` siempre es el **primer parámetro** de los métodos, pero **no lo pasás** al llamarlos: Python lo hace solo. Es automático.

---

## 📊 Atributos: los datos del objeto

Los **atributos** son las variables que viven dentro de un objeto (`self.nombre`, `self.nivel`...). Son sus "stats".

```python
pikachu = Pokemon("Pikachu", "Electrico", 25)

print(pikachu.nivel)      # leer un atributo: 25
pikachu.nivel = 26        # modificar un atributo
print(pikachu.nivel)      # 26
```

Cada objeto tiene **sus propios** atributos, independientes de los demás:

```python
pikachu = Pokemon("Pikachu", "Electrico", 25)
charizard = Pokemon("Charizard", "Fuego", 50)

print(pikachu.nivel)      # 25
print(charizard.nivel)    # 50  (son distintos)
```

---

## ⚡ Métodos: las acciones del objeto

Un **método** es una función definida dentro de la clase. Son las "acciones" o "ataques" que el objeto puede hacer. Siempre reciben `self` primero.

```python
class Pokemon:
    def __init__(self, nombre, tipo, nivel):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp = 100

    def atacar(self):
        # Un método puede usar los atributos del objeto con self.
        return f"{self.nombre} ataca con un golpe de tipo {self.tipo}!"

    def subir_nivel(self):
        # Un método puede modificar los atributos del objeto.
        self.nivel = self.nivel + 1

pikachu = Pokemon("Pikachu", "Electrico", 25)
print(pikachu.atacar())     # Pikachu ataca con un golpe de tipo Electrico!
pikachu.subir_nivel()
print(pikachu.nivel)        # 26
```

> 💡 Fijate: llamás los métodos con `objeto.metodo()`. No pasás `self`, Python lo manda solo.

---

## 🖨️ __str__: cómo se muestra el objeto

Por defecto, si hacés `print(pikachu)`, Python muestra algo feo como `<__main__.Pokemon object at 0x7f...>`. El método especial `__str__` define un texto lindo.

```python
class Pokemon:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

    def __str__(self):
        # Lo que devuelva esto es lo que ve el usuario con print().
        return f"{self.nombre} (Nivel {self.nivel})"

pikachu = Pokemon("Pikachu", 25)
print(pikachu)    # Pikachu (Nivel 25)  ← ¡mucho mejor!
```

---

## 🔍 __repr__: la versión para programadores

`__repr__` es parecido a `__str__`, pero es la representación "técnica", la que ves en el REPL o cuando un objeto está dentro de una lista. La idea es que sea precisa y útil para debuggear.

```python
class Pokemon:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

    def __repr__(self):
        return f"Pokemon(nombre='{self.nombre}', nivel={self.nivel})"

pikachu = Pokemon("Pikachu", 25)
print(repr(pikachu))    # Pokemon(nombre='Pikachu', nivel=25)
equipo = [pikachu]
print(equipo)           # [Pokemon(nombre='Pikachu', nivel=25)]
```

> 💡 Regla práctica: `__str__` para el usuario (lindo), `__repr__` para vos (preciso). Si solo vas a definir uno, definí `__repr__`.

---

## 🔒 Encapsulamiento básico

**Encapsular** es proteger los datos internos de un objeto. En Python, por convención, un atributo "privado" (que no debería tocarse desde afuera) se nombra con un **guión bajo** adelante.

```python
class Pokemon:
    def __init__(self, nombre):
        self.nombre = nombre
        self._hp = 100         # _hp: "esto es interno, no lo toques directo"

    def recibir_dano(self, cantidad):
        # La forma CORRECTA de cambiar el HP es a través de un método,
        # que puede validar (que no baje de 0, por ejemplo).
        self._hp = self._hp - cantidad
        if self._hp < 0:
            self._hp = 0

    def hp_actual(self):
        return self._hp
```

El guión bajo no lo "bloquea" de verdad (Python confía en vos), pero es una señal clara: *"accedé a esto solo a través de los métodos"*. En la semana 9 lo profundizamos con `@property`.

---

## 📝 Resumen de la semana

```python
class Pokemon:                          # clase = molde
    def __init__(self, nombre, nivel):  # constructor
        self.nombre = nombre            # atributos (datos del objeto)
        self.nivel = nivel
        self._hp = 100                  # _hp: atributo "interno"

    def atacar(self):                   # método (acción)
        return f"{self.nombre} ataca!"

    def __str__(self):                  # texto lindo para print()
        return f"{self.nombre} (Nv {self.nivel})"

    def __repr__(self):                 # texto técnico para debug
        return f"Pokemon({self.nombre!r}, {self.nivel})"

pikachu = Pokemon("Pikachu", 25)        # instancia (objeto)
print(pikachu.atacar())
print(pikachu)
```

| Concepto | Qué es |
|----------|--------|
| `class` | El molde / plano |
| objeto / instancia | Un individuo hecho con el molde |
| `__init__` | El constructor (datos iniciales) |
| `self` | El propio objeto |
| atributo | Un dato del objeto (`self.x`) |
| método | Una acción del objeto |
| `__str__` | Texto lindo para el usuario |
| `__repr__` | Texto técnico para debug |
| `_atributo` | Convención de "interno/privado" |

---

## ➡️ ¿Y ahora qué?

1. Resolvé `ejercicios.py` (vas de una clase básica a una con métodos de batalla).
2. Corré los tests: `pytest semana-08-python-poo-introduccion/`
3. Jugá el **creador de Pokémon personalizado**:
   ```bash
   python interactivo.py
   ```

> ⚡ *"Una clase es un molde. Con un buen molde, fabricás Pokémon ilimitados."*

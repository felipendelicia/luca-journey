# 🐍 Semana 09 — Python: POO Avanzado

> 🎯 **Meta de la semana:** llevar la POO al siguiente nivel con **herencia** y **polimorfismo**. Vas a crear familias de clases donde los Pokémon de Fuego, Agua y Planta comparten cosas pero cada uno tiene su estilo.

---

## 🎮 Analogía: las especies y los tipos

Todos los Pokémon comparten cosas básicas (nombre, HP, pueden atacar). Pero un **Charizard** (Fuego) y un **Blastoise** (Agua) atacan distinto y tienen ventajas diferentes.

La **herencia** te deja escribir lo común UNA vez (en una clase "padre") y que cada tipo lo **herede** y le agregue lo suyo. ⚡🔥💧🌿

---

## 🧬 Herencia: heredar de una clase padre

Una clase puede **heredar** de otra: recibe todos sus atributos y métodos, y puede agregar o cambiar lo que quiera.

```python
# Clase PADRE (o "base", o "superclase")
class Pokemon:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

    def atacar(self):
        return f"{self.nombre} ataca!"

# Clase HIJA: hereda de Pokemon (se pone entre paréntesis)
class PokemonFuego(Pokemon):
    def lanzallamas(self):
        return f"{self.nombre} usa Lanzallamas! 🔥"

# El hijo tiene LO SUYO y LO HEREDADO:
charizard = PokemonFuego("Charizard", 50)
print(charizard.atacar())       # heredado de Pokemon
print(charizard.lanzallamas())  # propio de PokemonFuego
```

---

## 🆙 super(): llamar al padre

Cuando el hijo define su propio `__init__`, puede llamar al del padre con `super()` para no repetir código.

```python
class Pokemon:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

class PokemonFuego(Pokemon):
    def __init__(self, nombre, nivel):
        # super() llama al __init__ del padre: setea nombre y nivel.
        super().__init__(nombre, nivel)
        # Después agregamos lo propio del tipo Fuego.
        self.tipo = "Fuego"
        self.poder_fuego = 80

charizard = PokemonFuego("Charizard", 50)
print(charizard.nombre)        # Charizard (lo seteó el padre)
print(charizard.tipo)          # Fuego (lo seteó el hijo)
```

---

## 🎭 Polimorfismo: cada uno responde a su manera

**Polimorfismo** ("muchas formas") significa que el mismo método se comporta distinto según la clase. Todos los Pokémon tienen `atacar()`, pero cada tipo lo **sobrescribe** a su manera.

```python
class Pokemon:
    def __init__(self, nombre):
        self.nombre = nombre

    def atacar(self):
        return f"{self.nombre} usa un ataque normal"

class PokemonFuego(Pokemon):
    def atacar(self):       # SOBRESCRIBE el método del padre
        return f"{self.nombre} usa Lanzallamas! 🔥"

class PokemonAgua(Pokemon):
    def atacar(self):
        return f"{self.nombre} usa Pistola Agua! 💧"

# El mismo método atacar(), distinto resultado según el tipo:
equipo = [PokemonFuego("Charizard"), PokemonAgua("Blastoise")]
for p in equipo:
    print(p.atacar())
# Charizard usa Lanzallamas! 🔥
# Blastoise usa Pistola Agua! 💧
```

> 💡 Esto es potente: podés tratar a todos como "Pokémon" y cada uno hace lo suyo. No necesitás `if tipo == "fuego"` por todos lados.

---

## 🏛️ Métodos de clase y estáticos

### Método estático (`@staticmethod`)
Una función que vive dentro de la clase pero **no usa `self`**. Es una utilidad relacionada con la clase.

```python
class Pokemon:
    @staticmethod
    def es_tipo_valido(tipo):
        return tipo in ["Fuego", "Agua", "Planta", "Electrico"]

# Se llama desde la clase, sin crear un objeto:
print(Pokemon.es_tipo_valido("Fuego"))   # True
print(Pokemon.es_tipo_valido("Pizza"))   # False
```

### Método de clase (`@classmethod`)
Recibe la **clase** (`cls`) en vez del objeto. Útil para crear objetos de formas alternativas ("constructores extra").

```python
class Pokemon:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

    @classmethod
    def recien_nacido(cls, nombre):
        # cls es la clase. Creamos un Pokémon nivel 1.
        return cls(nombre, 1)

bebe = Pokemon.recien_nacido("Pichu")
print(bebe.nivel)    # 1
```

---

## 🎚️ Propiedades con @property

`@property` te deja usar un método **como si fuera un atributo** (sin paréntesis). Sirve para calcular valores o validar. Es la forma elegante del encapsulamiento.

```python
class Pokemon:
    def __init__(self, nombre, hp):
        self.nombre = nombre
        self._hp = hp          # atributo interno

    @property
    def hp(self):
        # Se accede como pokemon.hp (sin paréntesis).
        return self._hp

    @hp.setter
    def hp(self, valor):
        # Se ejecuta al hacer pokemon.hp = algo. Validamos acá.
        if valor < 0:
            valor = 0
        self._hp = valor

pikachu = Pokemon("Pikachu", 100)
print(pikachu.hp)       # 100 (parece atributo, pero pasa por el método)
pikachu.hp = -50        # el setter lo corrige
print(pikachu.hp)       # 0 (¡no quedó negativo!)
```

---

## 🔲 Clases abstractas con abc

Una **clase abstracta** es un molde que **no se puede instanciar directamente**: obliga a las clases hijas a implementar ciertos métodos. Se usa el módulo `abc`.

```python
from abc import ABC, abstractmethod

class Pokemon(ABC):              # ABC = Abstract Base Class
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def atacar(self):
        # No tiene cuerpo: cada hijo DEBE implementarlo.
        pass

# No se puede hacer Pokemon("X"): es abstracta.
# pokemon = Pokemon("X")   # ❌ ERROR

class PokemonFuego(Pokemon):
    def atacar(self):            # obligatorio implementarlo
        return f"{self.nombre} usa Lanzallamas!"

charizard = PokemonFuego("Charizard")   # ✅ funciona
print(charizard.atacar())
```

> 💡 Las clases abstractas sirven para definir un "contrato": *"todo Pokémon DEBE saber atacar"*. Si un hijo se olvida de implementar `atacar()`, Python no lo deja crear el objeto.

---

## 📝 Resumen de la semana

```python
from abc import ABC, abstractmethod

class Pokemon(ABC):                       # clase abstracta
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self._hp = 100

    @property                             # atributo calculado/validado
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, valor):
        self._hp = max(0, valor)

    @staticmethod                         # utilidad sin self
    def es_tipo_valido(tipo):
        return tipo in ["Fuego", "Agua"]

    @abstractmethod                       # cada hijo DEBE implementarlo
    def atacar(self):
        pass

class PokemonFuego(Pokemon):              # herencia
    def __init__(self, nombre, nivel):
        super().__init__(nombre, nivel)   # llama al padre
        self.tipo = "Fuego"

    def atacar(self):                     # polimorfismo (sobrescribe)
        return f"{self.nombre} usa Lanzallamas!"
```

| Concepto | Qué es |
|----------|--------|
| herencia | Una clase hija recibe lo del padre |
| `super()` | Llama métodos del padre |
| polimorfismo | El mismo método, distinto según la clase |
| `@staticmethod` | Función en la clase sin `self` |
| `@classmethod` | Recibe la clase (`cls`) |
| `@property` | Método usado como atributo |
| `abc` / `@abstractmethod` | Clase abstracta (contrato obligatorio) |

---

## ➡️ ¿Y ahora qué?

1. Resolvé `ejercicios.py`.
2. Corré los tests: `pytest semana-09-python-poo-avanzado/`
3. Jugá el **sistema de tipos Pokémon** (batallas con ventajas):
   ```bash
   python interactivo.py
   ```

> ⚡ *"Un buen sistema de clases es como una buena familia Pokémon: comparten raíces, pero cada uno brilla a su manera."*

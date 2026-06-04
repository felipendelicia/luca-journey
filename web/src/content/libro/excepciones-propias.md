---
title: "Excepciones personalizadas"
order: 920
---

> 🎯 **Meta:** crear tus **propios** tipos de error heredando de `Exception`. Le ponen nombre claro a los problemas de tu programa.

Python trae muchos errores (`ValueError`, `KeyError`...), pero a veces ninguno describe bien **tu** problema. Para eso creás los tuyos: una clase que **hereda de `Exception`**.

## 🏷️ Una excepción con nombre propio

```python
class EquipoLlenoError(Exception):
    pass

def agregar(equipo, pokemon):
    if len(equipo) >= 6:
        raise EquipoLlenoError("el equipo ya tiene 6 Pokémon")
    equipo.append(pokemon)
    return equipo

equipo = ["Pikachu", "Eevee", "Snorlax", "Gengar", "Lapras", "Onix"]
try:
    agregar(equipo, "Mew")
except EquipoLlenoError as e:
    print("No se pudo:", e)
```

> 💡 Con `pass` alcanza para una excepción simple: hereda todo de `Exception`. El nombre (`EquipoLlenoError`) ya cuenta la historia.

## 🎒 Por qué conviene

Quien usa tu código puede atrapar **justo** tu error, sin confundirlo con otros:

```python
class PokemonNoEncontrado(Exception):
    pass

def buscar(equipo, nombre):
    if nombre in equipo:
        return nombre
    raise PokemonNoEncontrado(nombre)

try:
    buscar(["Pikachu"], "Mew")
except PokemonNoEncontrado as e:
    print("Falta:", e)   # Falta: Mew
```

## 🧰 Excepciones con datos extra

Podés hacer que tu error **guarde información** con un `__init__`:

```python
class EntrenadorError(Exception):
    def __init__(self, mensaje, codigo):
        super().__init__(mensaje)   # el mensaje normal
        self.codigo = codigo        # un dato extra

try:
    raise EntrenadorError("acceso denegado", 403)
except EntrenadorError as e:
    print(e)          # acceso denegado
    print(e.codigo)   # 403
```

> 💡 `super().__init__(mensaje)` hace que `str(e)` muestre el mensaje, como cualquier error. `self.codigo` agrega tu dato propio.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `class MiError(Exception): pass` | crear un error propio |
| `raise MiError("...")` | lanzarlo |
| `except MiError as e:` | atrapar justo el tuyo |
| `__init__` con `super()` | guardar datos extra en el error |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/excepciones-propias). 💪

> ⚡ *"Un error con nombre propio se arregla diez veces más rápido."*

---
title: "Errores: try / except"
order: 900
---

> 🎯 **Meta:** entrar a **Kalos**, la región de la **calidad de código**. Acá tu programa deja de explotar ante el primer error: los vas a **atrapar** con `try` / `except`.

Bienvenido a **Kalos**. 🧪 Hasta ahora, si algo salía mal, tu programa **crasheaba**. Pero el código real tiene que aguantar imprevistos: un archivo que no está, un número mal escrito, una división por cero. La región de **Testing y calidad** te enseña a hacer programas **robustos**.

## 💥 Qué es una excepción

Cuando Python encuentra un error en ejecución, **lanza una excepción** y, si nadie la atrapa, el programa muere. Mirá el clásico:

```python
numeros = [10, 20, 30]
print(numeros[5])   # IndexError: list index out of range 💥
```

## 🛡️ try / except: atrapar el error

`try` envuelve el código riesgoso; `except` dice qué hacer si falla. El programa **sigue vivo**.

```python
def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(dividir_seguro(10, 2))   # 5.0
print(dividir_seguro(10, 0))   # None  (no explota)
```

```quiz
P: ¿Qué hace el bloque `except` en un `try/except`?
- Evita que el error ocurra
+ Define qué hacer cuando el código del `try` lanza una excepción
- Repite el código del `try` hasta que funcione
> `except` no evita el error: lo **atrapa** después de que ocurre. Define el camino alternativo para que el programa siga vivo en vez de crashear.
```

## 🎯 Atrapar el error correcto

Cada error tiene su **tipo**. Conviene atrapar el específico (no todos a ciegas):

```python
def a_entero(texto):
    try:
        return int(texto)
    except ValueError:
        return 0

print(a_entero("42"))        # 42
print(a_entero("pikachu"))   # 0  (no es un número)
```

| Excepción | Cuándo salta |
|-----------|--------------|
| `ZeroDivisionError` | dividir por cero |
| `ValueError` | valor inválido (ej: `int("abc")`) |
| `IndexError` | posición fuera de la lista |
| `KeyError` | clave inexistente en un dict |
| `TypeError` | tipo equivocado |

## 🧹 Atrapar varios casos

```python
def valor(dic, clave):
    try:
        return dic[clave]
    except KeyError:
        return "no encontrado"

pokemon = {"nombre": "Pikachu", "nivel": 25}
print(valor(pokemon, "nivel"))   # 25
print(valor(pokemon, "tipo"))    # no encontrado
```

> 💡 Atrapá solo lo que esperás. Un `except:` pelado (sin tipo) esconde bugs reales. Mejor `except ValueError:` que tapar todo.

```quiz
P: ¿Qué excepción lanza `int("pikachu")`?
- `TypeError`
- `IndexError`
+ `ValueError`
> `ValueError` ocurre cuando el tipo está bien (es un string) pero el valor no se puede convertir. `TypeError` sería si pasaras un tipo completamente incompatible, como una lista.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| excepción | un error que Python lanza en ejecución |
| `try:` | envolver el código que puede fallar |
| `except TipoError:` | qué hacer si falla |
| atrapar el tipo justo | no esconder otros bugs |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/errores-try-except). 💪

> ⚡ *"El código amateur explota; el código pro atrapa el error y sigue."*

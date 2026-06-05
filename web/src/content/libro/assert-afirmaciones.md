---
title: "assert: afirmaciones"
order: 930
---

> 🎯 **Meta:** usar `assert` para **afirmar** que algo es verdadero. Es la herramienta base de los **tests** y de los chequeos internos.

`assert` es una afirmación: "esto **tiene** que ser verdad". Si lo es, no pasa nada. Si no, lanza `AssertionError`. Es la pieza con la que están hechos los tests.

## ✅ assert en acción

```python
assert 2 + 2 == 4          # verdadero -> sigue de largo, sin ruido
print("primera afirmación OK")

assert 2 + 2 == 5          # falso -> 💥 AssertionError
print("esto no se imprime")
```

## 💬 assert con mensaje

Agregá un mensaje después de la coma para saber **qué** falló:

```python
def verificar_positivo(n):
    assert n > 0, "n debe ser positivo"
    return n

print(verificar_positivo(5))    # 5
print(verificar_positivo(-2))   # 💥 AssertionError: n debe ser positivo
```

```quiz
P: ¿Qué pasa si ejecutás `assert 5 > 10, "el cinco no es mayor que diez"`?
- No pasa nada: `assert` solo muestra advertencias
- Lanza un `ValueError` con el mensaje
+ Lanza un `AssertionError` con el mensaje "el cinco no es mayor que diez"
> Cuando la condición de `assert` es **falsa**, Python lanza `AssertionError`. El texto después de la coma es el mensaje que aparece para saber qué falló.
```

## 🧪 assert como chequeo de supuestos

Sirve para validar supuestos en medio de un cálculo:

```python
def promedio(numeros):
    assert len(numeros) > 0, "lista vacía"
    return sum(numeros) / len(numeros)

print(promedio([10, 20, 30]))   # 20.0
# promedio([])  ->  AssertionError: lista vacía
```

## ⚖️ assert vs raise

| | `assert` | `raise` |
|---|---|---|
| **Para** | tests y chequeos internos | validar entradas de usuario |
| **Lanza** | `AssertionError` | el error que elijas |
| **Ojo** | se puede desactivar (modo optimizado) | siempre activo |

> 💡 Regla práctica: **`raise`** para validar datos que vienen de afuera; **`assert`** para verificar cosas que *deberían* ser ciertas si tu código está bien (y en los **tests**, que es lo que viene ahora).

```quiz
P: ¿Cuándo es mejor usar `raise` en vez de `assert`?
- Cuando querés que el error tenga un mensaje
+ Cuando validás datos que vienen de afuera del programa (usuario, archivo, API)
- Cuando estás escribiendo tests
> `assert` puede desactivarse con el modo optimizado de Python. `raise` siempre actúa. Para validar entradas del usuario o datos externos, usá `raise`; para checks internos y tests, `assert`.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `assert condición` | afirmar que algo es verdad |
| `assert cond, "msg"` | con mensaje si falla |
| `AssertionError` | lo que lanza cuando es falso |
| base de los tests | un test es una pila de asserts |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/assert-afirmaciones). 💪

> ⚡ *"`assert` es decirle al código: 'demostrame que no me estás mintiendo'."*

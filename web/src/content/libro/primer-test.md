---
title: "Tu primer test"
order: 940
---

> 🎯 **Meta:** escribir **tests**: código que prueba otro código automáticamente. Es lo que hace que un programa siga andando aunque lo cambies mil veces.

Un **test** es una función que verifica que otra función haga lo correcto. En vez de probar a mano cada vez, lo escribís **una vez** y lo corrés siempre. Así, si algún día rompés algo, te enterás al toque.

## 🧪 Un test es una pila de asserts

```python
def doble(x):
    return x * 2

def probar_doble():
    assert doble(3) == 6
    assert doble(0) == 0
    assert doble(-2) == -4
    print("✅ doble pasó todos los chequeos")

probar_doble()
```

Si `doble` está bien, el test pasa calladito. Si la rompés (`return x + 2`), un `assert` falla y te avisa **exactamente** dónde.

## 🎛️ Probar la función que te pasen

Un test puede recibir la función a probar como **parámetro**. Así el mismo test sirve para cualquier implementación:

```python
def probar_es_par(es_par):
    assert es_par(2) is True
    assert es_par(3) is False
    assert es_par(0) is True

# le pasamos una implementación correcta
probar_es_par(lambda x: x % 2 == 0)
print("pasó ✅")
```

> 💡 Si le pasás una versión **rota** (`lambda x: True`), el test lanza `AssertionError`: **detectó el bug**. Eso es exactamente lo que querés.

## 🤖 pytest: el corredor de tests

En el mundo real no llamás los tests a mano: usás **pytest**, que busca todas las funciones que empiezan con `test_` y las corre solas. (¡Es lo que usa esta plataforma para corregirte!)

```python
# archivo test_pokemon.py
def test_doble():
    assert doble(3) == 6

# en la terminal:  pytest
# pytest encuentra test_doble, lo corre y te dice si pasó o falló
```

> 💡 Cada botón **Corregir** de los ejercicios corre `pytest` en tu navegador. Ahora ya sabés qué hay abajo del capó. 🔧

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| test | función que verifica otra con asserts |
| recibir la función por parámetro | testear cualquier implementación |
| test que falla | encontró un bug (¡es bueno!) |
| `pytest` | corre todos los `test_*` automáticamente |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/primer-test). 💪

> ⚡ *"Sin tests, cada cambio es una apuesta. Con tests, es un paso firme."*

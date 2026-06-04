---
title: "Casos límite y errores"
order: 950
---

> 🎯 **Meta:** escribir tests que de verdad **cazan bugs**: probar los **casos límite** (lo vacío, el cero, el negativo) y verificar que tu código **lance** el error correcto.

Un test que solo prueba "lo fácil" da una falsa sensación de seguridad. Los bugs se esconden en los **casos límite**: la lista vacía, el cero, el número negativo, el texto sin nada. Un buen test va justo a buscarlos.

## 🧨 Dónde viven los bugs

```python
def probar_largo(largo):
    assert largo("hola") == 4    # caso normal
    assert largo("") == 0        # ⚠️ caso LÍMITE: texto vacío
    assert largo("a") == 1       # caso mínimo

probar_largo(len)
print("pasó ✅")
```

> 💡 El caso `""` (vacío) es el que más bugs descubre. Siempre incluilo. Lo mismo con listas vacías, el `0` y los negativos.

## 🎯 Tabla de casos límite típicos

| Tipo de dato | Casos límite a probar |
|--------------|----------------------|
| texto | vacío `""`, un solo carácter |
| número | `0`, negativos, muy grande |
| lista | vacía `[]`, un solo elemento |
| división | dividir por `0` |

## 💥 Testear que SÍ lance un error

A veces lo correcto es que la función **falle**. ¿Cómo lo probás? Esperás el error con `try`/`except`: si **no** salta, el test debe fallar.

```python
def probar_dividir(dividir):
    assert dividir(10, 2) == 5
    try:
        dividir(5, 0)
    except ZeroDivisionError:
        return                      # ✅ bien: lanzó el error esperado
    raise AssertionError("dividir(5, 0) debería lanzar ZeroDivisionError")

probar_dividir(lambda a, b: a / b)
print("pasó ✅")
```

> 💡 En `pytest` esto se escribe más cortito con `with pytest.raises(ZeroDivisionError):`, pero la idea es la misma: **verificar que el error ocurra**.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| casos límite | vacío, cero, negativo, un solo elemento |
| el caso vacío | el que más bugs esconde |
| `try/except` en el test | verificar que el error SÍ ocurra |
| `pytest.raises(...)` | la forma corta de lo mismo |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/casos-limite). 💪

> ⚡ *"Cualquiera prueba que funciona; un buen test prueba que no se rompe."*

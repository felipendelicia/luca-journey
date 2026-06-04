---
title: "Proyecto: módulo testeado"
order: 970
---

> 🎯 **Meta:** cerrar **Kalos** juntando todo: funciones **robustas** (que validan y manejan errores) **con sus tests**. Así se escribe código de calidad de verdad.

Llegaste al final de Kalos. 🧪 Un módulo profesional tiene dos caras: el **código robusto** (valida, maneja errores) y los **tests** que lo respaldan. Acá los combinás.

## 🛡️ Código robusto + su test

```python
def raiz_cuadrada(n):
    if n < 0:
        raise ValueError("no hay raíz cuadrada de un número negativo")
    return n ** 0.5


def probar_raiz(raiz):
    assert raiz(9) == 3        # caso normal
    assert raiz(0) == 0        # caso límite
    try:
        raiz(-1)               # debe lanzar
    except ValueError:
        return
    raise AssertionError("raiz(-1) debería lanzar ValueError")


probar_raiz(raiz_cuadrada)
print("✅ módulo robusto y testeado")
```

## 🔧 Otra pieza: manejar el error sin explotar

```python
def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def probar_dividir_seguro(dividir):
    assert dividir(6, 2) == 3
    assert dividir(1, 0) is None   # el caso del cero, manejado

probar_dividir_seguro(dividir_seguro)
print("✅ pasó")
```

## 🗺️ Lo que aprendiste en Kalos

1. **try / except** — atrapar errores sin crashear.
2. **raise** — lanzar errores claros al validar.
3. **Excepciones propias** — errores con nombre y datos.
4. **assert** — afirmar lo que debe ser cierto.
5. **Escribir tests** — probar el código automáticamente.
6. **Casos límite** — cazar los bugs donde se esconden.
7. **TDD** — el test primero, el código después.

Con esto escribís código que **no se rompe en silencio** y que podés cambiar con confianza. Es lo que separa a quien "hace que ande una vez" de quien construye software serio. 🏆

## ➡️ ¿Y ahora qué?

Cerrá Kalos con los [ejercicios de este tema](/ejercicios/proyecto-testing). Al completarlos ganás la medalla **Iceberg** y sos **Campeón de Kalos**. 🏔️🏆

> ⚡ *"Código sin tests es un castillo de naipes. Con tests, es de ladrillo."*

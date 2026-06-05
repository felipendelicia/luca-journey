---
title: "Lanzar errores: raise"
order: 910
---

> 🎯 **Meta:** que tu propio código **avise** cuando algo está mal, lanzando errores con `raise`. Validar entradas es la primera defensa contra los bugs.

Atrapar errores es la mitad. La otra mitad: **lanzarlos vos**. Si una función recibe datos imposibles (una edad negativa, un nivel de 9000), lo mejor es **cortar de una** con un error claro, en vez de seguir con datos basura.

## 🚨 raise: lanzar un error

```python
def validar_edad(edad):
    if edad < 0:
        raise ValueError("la edad no puede ser negativa")
    return edad

print(validar_edad(25))    # 25
print(validar_edad(-3))    # 💥 ValueError: la edad no puede ser negativa
```

> 💡 `raise` corta la función al instante y avisa a quien la llamó. El mensaje entre comillas ayuda a entender qué pasó.

## 🛂 Validar entradas

Validar al principio de la función ("guard clause") mantiene el resto del código limpio y seguro:

```python
def validar_nivel(nivel):
    if nivel < 1 or nivel > 100:
        raise ValueError("el nivel debe estar entre 1 y 100")
    return nivel

print(validar_nivel(50))    # 50
```

```quiz
P: ¿Para qué se usa `raise` en una función?
- Para mostrar un mensaje de advertencia sin detener el programa
+ Para lanzar un error y cortar la ejecución cuando los datos son inválidos
- Para reintentar la operación que falló
> `raise` lanza una excepción **intencionalmente**. Cortás de inmediato y le avisás a quien llamó la función qué salió mal, con un mensaje claro.
```

## 🧬 Elegir el tipo de error

Usá el error que mejor describe el problema:

```python
def solo_texto(x):
    if not isinstance(x, str):
        raise TypeError("se esperaba un string")
    return x.upper()

print(solo_texto("pikachu"))   # PIKACHU
print(solo_texto(123))         # 💥 TypeError: se esperaba un string
```

| Lanzá... | Cuando... |
|----------|-----------|
| `ValueError` | el tipo está bien pero el valor no (edad −3) |
| `TypeError` | el tipo está mal (esperabas texto, llegó número) |

## 🔄 raise + try/except: el equipo completo

Una función **lanza**, otra **atrapa**:

```python
def dividir(a, b):
    if b == 0:
        raise ValueError("no se puede dividir por cero")
    return a / b

try:
    dividir(10, 0)
except ValueError as e:
    print("Error controlado:", e)
```

> 💡 `except ValueError as e` guarda el error en `e` para leer su mensaje. Así informás sin crashear.

```quiz
P: Si recibís un número entero donde esperabas un string, ¿qué error deberías lanzar?
+ `TypeError`
- `ValueError`
- `IndexError`
> `TypeError` es para cuando el **tipo** está mal (esperabas texto, llegó un número). `ValueError` es cuando el tipo está bien pero el valor no tiene sentido (ej: edad negativa).
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `raise ValueError("...")` | lanzar un error con mensaje |
| validar al inicio | cortar antes de usar datos malos |
| `ValueError` / `TypeError` | valor inválido / tipo inválido |
| `except ... as e` | leer el mensaje del error |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/raise-validar). 💪

> ⚡ *"Mejor un error claro hoy que un bug misterioso mañana."*

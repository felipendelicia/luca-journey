---
title: "TDD: el test primero"
order: 960
---

> 🎯 **Meta:** dar vuelta el orden: escribir el **test antes** que el código. Es **TDD** (Test-Driven Development), la forma de programar de muchos equipos pro.

Hasta ahora escribías la función y después el test. **TDD** lo invierte: primero escribís el **test** de lo que querés, lo ves **fallar** (rojo), y recién ahí escribís el código justo para que **pase** (verde).

## 🔴🟢 El ciclo Rojo → Verde → Refactor

1. **🔴 Rojo:** escribís un test de algo que todavía no existe. Falla (obvio).
2. **🟢 Verde:** escribís el código **mínimo** para que el test pase.
3. **🔵 Refactor:** mejorás el código, tranquilo, porque el test te cubre.

```python
# 1) 🔴 ROJO: primero el test (es_palindromo todavía no existe)
def test_es_palindromo():
    assert es_palindromo("oso") is True
    assert es_palindromo("gato") is False
    assert es_palindromo("ana") is True

# 2) 🟢 VERDE: ahora el código mínimo para que pase
def es_palindromo(texto):
    return texto == texto[::-1]

test_es_palindromo()
print("✅ verde")
```

```quiz
P: En TDD, ¿qué significa la fase "Rojo"?
- El test pasó y el código está listo
+ El test falla porque el código que prueba todavía no existe
- El test tiene un error de sintaxis
> En el ciclo Rojo → Verde → Refactor, el **rojo** es intencional: escribís el test antes que el código, así que falla. Es la señal de que hay algo por hacer.
```

## 🧭 Por qué TDD funciona

- **Pensás primero qué querés** (el test te obliga a definir el comportamiento).
- **No escribís código de más**: solo lo necesario para pasar.
- **Refactorizás sin miedo**: si rompés algo, el test te avisa al instante.

```python
# el test define el contrato: factorial(0)==1, factorial(5)==120
def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

def factorial(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

test_factorial()
print("✅ verde")
```

> 💡 En estos ejercicios el test ya está escrito por nosotros: tu trabajo es escribir el código que lo ponga en **verde**. Eso es vivir el lado lindo de TDD. 🟢

```quiz
P: ¿Cuánto código debería escribir en la fase "Verde" del TDD?
- Todo el código posible para cubrir casos futuros
+ El mínimo necesario para que el test pase, nada más
- Primero el test, después refactorizás antes de que pase
> La idea es escribir lo **mínimo** para pasar el test. Nada de más. Si necesitás más casos, primero escribís otro test (rojo) y después lo implementás (verde).
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| TDD | escribir el test antes que el código |
| 🔴 Rojo | el test falla (todavía no hay código) |
| 🟢 Verde | código mínimo para que pase |
| 🔵 Refactor | mejorar con la red de los tests |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/tdd). 💪

> ⚡ *"Primero decís qué querés (el test); después lo construís. Diseño, no adivinanza."*

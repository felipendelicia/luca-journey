---
title: "Algoritmos: Recursión"
order: 1204
---

> 🎯 **Meta:** resolver problemas que se **repiten en versión más chica** con funciones que se llaman a sí mismas.

---

Una función **recursiva** se llama a sí misma con un problema más pequeño, hasta llegar a un **caso base** que la frena. Sin caso base, se llama para siempre y revienta (`RecursionError`).

## Las dos partes

Toda recursión tiene:

1. **Caso base**: el más simple, que se resuelve sin recursión.
2. **Caso recursivo**: la función se llama con una entrada más chica.

```python
def factorial(n):
    if n == 0:           # caso base: 0! = 1
        return 1
    return n * factorial(n - 1)   # caso recursivo

print(factorial(5))   # 5 * 4 * 3 * 2 * 1 = 120
```

## Pensar en recursivo

El truco es **confiar**: asumí que la función ya funciona para el caso más chico, y armá el grande con eso.

```python
def suma_lista(nums):
    if not nums:                 # base: lista vacía suma 0
        return 0
    return nums[0] + suma_lista(nums[1:])   # primero + suma del resto
```

Fibonacci es el ejemplo clásico (cada número es la suma de los dos anteriores):

```python
def fib(n):
    if n < 2:        # base: fib(0)=0, fib(1)=1
        return n
    return fib(n - 1) + fib(n - 2)
```

> ⚠️ Toda recursión se puede escribir con bucles, y viceversa. La recursión brilla cuando el problema **es** recursivo: árboles, fractales, dividir y conquistar.

## ✅ Comprobá lo que aprendiste

```quiz
P: Una función recursiva SIN caso base…
+ se llama para siempre y revienta (RecursionError)
- devuelve 0
- es más rápida
> El caso base es lo que la frena.
```

```quiz
P: `factorial(0)` debe devolver…
+ 1
- 0
- error
> Es el caso base: 0! = 1.
```

🔁 El **Líder Larry** te espera: lo simple, recursivo.

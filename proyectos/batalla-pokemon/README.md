# ⚔️ Simulador de Batalla Pokémon

> Un simulador de batalla **por turnos** completo, con tipos, movimientos, **PP**, **estados alterados** (paralizado, dormido, envenenado) y **dos modos de juego**: contra la CPU o contra otro jugador en la misma terminal.

---

## ✨ Características

- 🔥💧🌿 **Sistema de tipos** con ventajas y desventajas (súper efectivo / poco efectivo).
- 🎯 **Movimientos con PP**: cada ataque tiene usos limitados.
- 😵 **Estados alterados**:
  - ⚡ **Paralizado**: a veces no podés moverte.
  - 💤 **Dormido**: no atacás hasta despertarte.
  - 🤢 **Envenenado**: perdés HP al final de cada turno.
- 🤖 **Modo vs CPU**: la compu elige sus movimientos sola.
- 👥 **Modo vs Jugador**: dos personas, misma terminal, por turnos.
- 📋 5 Pokémon jugables: Pikachu, Charizard, Blastoise, Venusaur y Snorlax.

---

## ▶️ Uso

```bash
python batalla.py
```

Elegís el modo, después tu Pokémon, y a pelear. En cada turno elegís un movimiento
mirando su tipo, poder y PP restantes.

No necesita librerías externas: solo la librería estándar de Python.

---

## 🗂️ Estructura

```
batalla-pokemon/
├── batalla.py                  # lanzador
├── batalla_pokemon/
│   ├── tipos.py                # tabla de efectividad
│   ├── modelos.py              # clases Movimiento y Pokemon
│   ├── estados.py              # paralizado / dormido / envenenado
│   ├── batalla.py              # lógica de la batalla
│   ├── datos.py                # roster de Pokémon
│   └── juego.py                # interfaz de consola (2 modos)
└── tests/
    └── test_batalla.py
```

---

## 🧪 Tests

```bash
pytest
```

Los tests son **deterministas**: el azar (paralización, proc de estados, elección
de la CPU) se inyecta como parámetro, así los resultados son siempre los mismos y
se pueden verificar.

---

## 🎮 Cómo funciona el daño

```
daño = poder_del_movimiento × efectividad_de_tipo
```

Donde la efectividad es **2.0** (súper efectivo), **0.5** (poco efectivo) o **1.0** (normal).

> ⚡ *"En una batalla Pokémon, conocer los tipos es la mitad de la victoria."*

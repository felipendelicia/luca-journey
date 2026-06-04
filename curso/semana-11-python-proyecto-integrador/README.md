# 📒 Agenda del Entrenador — Proyecto Integrador (Semana 11)

> Tu primera aplicación **completa y modular**. Una agenda de consola para llevar el registro de tu vida como Entrenador Pokémon: a quién capturaste, tu equipo activo, tus batallas y tus estadísticas. Todo guardado en JSON. 🎒

---

## ✨ ¿Qué hace?

- 📝 **Registrar Pokémon capturados** (nombre, tipo, nivel, fecha de captura).
- 🎯 **Equipo activo** de hasta 6 Pokémon.
- ⚔️ **Historial de batallas** con resultado (ganó/perdió), contra quién y con qué Pokémon.
- 💾 **Persistencia en JSON**: cerrás el programa y tus datos siguen ahí.
- 📊 **Estadísticas**: total capturados, porcentaje de victorias, Pokémon más usado.
- 🧭 **Menú navegable** por consola.

---

## 🗂️ Estructura del proyecto

```
semana-11-python-proyecto-integrador/
├── main.py                 # lanzador: arranca la app
├── agenda/                 # el paquete con toda la lógica (modular)
│   ├── __init__.py
│   ├── pokemon.py          # clase Pokemon
│   ├── equipo.py           # clase Equipo (máx 6)
│   ├── batallas.py         # Batalla e Historial
│   ├── estadisticas.py     # cálculos (victorias, más usado, etc.)
│   ├── storage.py          # guardar/cargar JSON
│   ├── ui.py               # textos y formato de consola
│   └── app.py              # la clase App que orquesta todo
├── tests/                  # un archivo de tests por módulo
│   ├── test_pokemon.py
│   ├── test_equipo.py
│   ├── test_batallas.py
│   ├── test_estadisticas.py
│   ├── test_storage.py
│   └── test_main.py
└── conftest.py             # hace importable el paquete en los tests
```

> 💡 **¿Por qué tantos archivos?** Porque dividir un programa en módulos chiquitos
> lo hace más fácil de entender, testear y mantener. Así trabajan los proyectos reales.

---

## ▶️ Cómo usar

Desde esta carpeta:

```bash
python main.py
```

(En algunos sistemas el comando es `python3`.)

No necesita librerías externas: usa solo la librería estándar de Python.

El menú te guía: registrás capturas, armás tu equipo, anotás batallas y mirás tus
estadísticas. Acordate de elegir **"Guardar"** (o salir con la opción 8, que guarda
automáticamente) para que tus datos queden en `agenda_datos.json`.

---

## 🧪 Cómo correr los tests

Desde esta carpeta:

```bash
pytest
```

O desde la raíz del curso:

```bash
pytest semana-11-python-proyecto-integrador/
```

Hay un archivo de tests por cada módulo, más un test de integración que verifica
el ciclo completo de guardar y cargar.

---

## 🎓 Conceptos que aplica

Este proyecto junta TODO lo que aprendiste:

| De la semana | Concepto usado acá |
|--------------|--------------------|
| 03-05 | variables, funciones, control de flujo |
| 06 | listas y diccionarios |
| 07 | manejo de archivos y excepciones |
| 08-09 | clases, objetos, métodos |
| 10 | módulos propios, `json` |

> ⚡ *"Un proyecto completo no es magia: son muchas piezas chiquitas, bien organizadas, trabajando juntas."*

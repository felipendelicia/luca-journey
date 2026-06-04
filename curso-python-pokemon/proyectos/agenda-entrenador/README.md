# 📒 Agenda del Entrenador (versión pulida)

> La versión mejorada del proyecto de la semana 11. Una app de consola **modular** para llevar todo tu progreso como Entrenador: capturas, equipo, batallas y estadísticas, con persistencia en JSON.

---

## ✨ Novedades respecto a la semana 11

- 🔎 **Buscar** un Pokémon capturado por nombre.
- 📊 **Capturados ordenados por nivel** automáticamente.
- 🏷️ Estadística extra: **tipo favorito** (el tipo que más capturaste).
- 🧱 Código aún más limpio y testeado.

---

## ✨ Funciones

- 📝 Registrar Pokémon capturados (nombre, tipo, nivel, fecha).
- 🎯 Equipo activo de hasta 6.
- ⚔️ Historial de batallas (ganó/perdió, rival, Pokémon usado).
- 📊 Estadísticas: total, % victorias, Pokémon más usado, tipo favorito.
- 💾 Persistencia en JSON.

---

## ▶️ Uso

```bash
python main.py
```

No necesita librerías externas (solo la librería estándar).

---

## 🗂️ Estructura

```
agenda-entrenador/
├── main.py                     # lanzador
├── agenda_entrenador/
│   ├── pokemon.py
│   ├── equipo.py
│   ├── batallas.py
│   ├── estadisticas.py
│   ├── storage.py
│   ├── ui.py
│   └── app.py
└── tests/
    └── test_agenda.py
```

---

## 🧪 Tests

```bash
pytest
```

> ⚡ *"Llevar registro de tu viaje es lo que separa a un buen Entrenador de un Maestro."*

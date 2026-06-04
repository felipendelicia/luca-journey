# 🔴⚪ Pokédex CLI

> Una Pokédex que vive en tu **terminal**. Consulta datos reales de la [PokéAPI](https://pokeapi.co), te muestra stats con barritas y un **sprite en ASCII**, y te deja guardar tus Pokémon **favoritos** localmente.

```
       \   /
      __\_/__
     ( o   o )
      \  ^  /
       \___/
      zZ  zZ
```

---

## ✨ Características

- 🔎 Buscá cualquier Pokémon por nombre.
- 📊 Ves sus stats base con barras visuales.
- 🎨 Cada tipo tiene su sprite en ASCII art.
- ⭐ Guardá favoritos en un archivo JSON local.
- 📴 Funciona sin romperse aunque no tengas internet (te avisa).

---

## 🚀 Instalación

```bash
pip install requests
```

(O activá el venv del curso, que ya la tiene.)

---

## ▶️ Uso

```bash
python pokedex.py
```

Dentro del programa:

| Comando | Qué hace |
|---------|----------|
| `pikachu` | Busca y muestra a Pikachu |
| `fav pikachu` | Agrega a Pikachu a favoritos |
| `quitar pikachu` | Lo saca de favoritos |
| `favoritos` | Lista tus favoritos |
| `salir` | Cierra la Pokédex |

---

## 🗂️ Estructura

```
pokedex-cli/
├── pokedex.py              # lanzador
├── pokedex_cli/
│   ├── pokeapi.py          # cliente de la PokéAPI
│   ├── ascii_art.py        # sprites en ASCII por tipo
│   ├── favoritos.py        # guardado local en JSON
│   ├── ui.py               # formato de la ficha
│   └── cli.py              # bucle interactivo
└── tests/
    └── test_pokedex_cli.py
```

---

## 🧪 Tests

```bash
pytest
```

Los tests **no usan internet** (la PokéAPI se simula) y verifican el parseo,
los favoritos, los sprites y el formato.

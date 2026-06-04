# 🌐 Pokédex Web (versión pulida)

> La versión mejorada del proyecto de la semana 12. Una Pokédex web con **Flask**, ahora con **persistencia en SQLite**, **buscador** y **edición** de Pokémon.

---

## ✨ Novedades respecto a la semana 12

- 🗄️ **Persistencia en SQLite** (en vez de JSON) — más cerca de una app real.
- 🔎 **Buscador** por nombre o tipo en la página principal.
- ✏️ **Editar** un Pokémon ya guardado.

---

## ✨ Funciones

- 🏠 Lista de Pokémon (con buscador).
- ➕ Formulario para agregar (con autocompletado desde la PokéAPI).
- 🔎 Página de detalle.
- ✏️ Editar y 🗑️ eliminar.
- 🎨 HTML + CSS propio.

---

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

(SQLite ya viene incluido con Python, no hay que instalar nada extra.)

---

## ▶️ Uso

```bash
python run.py
```

Abrí el navegador en **http://127.0.0.1:5000**. La base de datos `pokedex.db` se
crea sola la primera vez.

> 💡 El autocompletado necesita internet. Sin conexión, cargás los datos a mano.

---

## 🗂️ Estructura

```
pokedex-web/
├── run.py                      # lanzador
├── requirements.txt
├── conftest.py
├── pokedex_app/
│   ├── __init__.py             # create_app() y rutas
│   ├── db.py                   # persistencia en SQLite
│   ├── pokeapi.py              # integración con la PokéAPI
│   ├── templates/              # HTML (Jinja2)
│   └── static/style.css        # estilos
└── tests/
    └── test_app.py
```

---

## 🧪 Tests

```bash
pytest
```

Usan el **cliente de test de Flask** y una base SQLite **temporal** (no tocan tu
base real ni internet). Si no tenés Flask, se saltean.

> ⚡ *"De una idea a una web con base de datos. Sos oficialmente desarrollador/a."* 🏆

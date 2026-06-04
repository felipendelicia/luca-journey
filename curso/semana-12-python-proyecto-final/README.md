# 🌐 Pokédex Web con Flask — Proyecto Final (Semana 12)

> ¡Tu primera **aplicación web**! Una Pokédex que corre en el navegador, hecha con **Flask**. Podés ver tus Pokémon, agregar nuevos (autocompletando desde la PokéAPI), ver el detalle de cada uno y liberarlos. 🔴⚪

---

## ✨ ¿Qué hace?

- 🏠 **Página principal** con la lista de Pokémon guardados (en tarjetas con colores por tipo).
- ➕ **Formulario** para agregar un Pokémon nuevo.
- 🌐 **Autocompletado desde la PokéAPI**: escribís el nombre, tocás un botón y trae los datos reales.
- 🔎 **Página de detalle** de cada Pokémon.
- 🗑️ **Liberar** (eliminar) un Pokémon.
- 💾 **Persistencia en JSON** (`pokedex_datos.json`).
- 🎨 **HTML + CSS propio** (sin frameworks de CSS).

---

## 🗂️ Estructura

```
semana-12-python-proyecto-final/
├── run.py                      # lanza la app
├── requirements.txt
├── conftest.py                 # hace importable el paquete en los tests
├── pokedex_web/                # el paquete de la app
│   ├── __init__.py             # create_app() y las rutas (vistas)
│   ├── storage.py              # persistencia en JSON
│   ├── pokeapi.py              # integración con la PokéAPI
│   ├── templates/              # HTML (Jinja2)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── agregar.html
│   │   ├── detalle.html
│   │   └── 404.html
│   └── static/
│       └── style.css           # estilos
└── tests/
    ├── test_app.py             # tests con el cliente de Flask
    └── test_storage.py
```

---

## 🚀 Instalación

Desde esta carpeta:

```bash
# 1. (Recomendado) Activá el entorno virtual del curso
source ../venv/bin/activate      # si usaste el setup.sh de la raíz

# 2. Instalá las dependencias
pip install -r requirements.txt
```

---

## ▶️ Cómo correr la app

```bash
python run.py
```

Después abrí tu navegador en:

```
http://127.0.0.1:5000
```

Para frenar el servidor, apretá **Ctrl+C** en la terminal.

> 💡 El autocompletado desde la PokéAPI necesita **internet**. Si no tenés conexión,
> igual podés cargar los Pokémon a mano: la app funciona perfecto sin internet.

---

## 🧪 Cómo correr los tests

```bash
pytest
```

O desde la raíz del curso:

```bash
pytest semana-12-python-proyecto-final/
```

Los tests usan el **cliente de test de Flask** (no hace falta levantar el servidor)
y **no usan internet** (la PokéAPI se simula). Si no tenés Flask instalado, los
tests se saltean en vez de fallar.

---

## 🎓 Conceptos nuevos de Flask

| Concepto | Qué es |
|----------|--------|
| `create_app()` | Una "fábrica" que arma la aplicación |
| ruta / vista (`@app.route`) | Conecta una URL con una función |
| `render_template` | Genera HTML a partir de una plantilla |
| plantillas Jinja2 | HTML con `{{ variables }}` y `{% lógica %}` |
| `request.form` | Los datos que envía un formulario |
| `redirect` / `url_for` | Mandar al usuario a otra página |
| test client | Probar la web sin abrir el navegador |

> ⚡ *"De `print('Hola mundo')` a tu propia web. Mirá lo lejos que llegaste, Entrenador."* 🏆

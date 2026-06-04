"""
pokedex_app — Pokédex Web (versión pulida con Flask + SQLite).

Mejoras respecto a la semana 12:
  - Persistencia en SQLite (en vez de JSON).
  - Buscador en la página principal.
  - Edición de un Pokémon ya guardado.
"""

import os

from flask import (
    Flask, render_template, request, redirect, url_for, jsonify, abort
)

from . import db, pokeapi

RUTA_DB_DEFECTO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "pokedex.db"
)


def create_app(db_path=None):
    """Fábrica de la app. db_path permite usar una base temporal en los tests."""
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or RUTA_DB_DEFECTO

    # Creamos la tabla si no existe.
    db.init_db(app.config["DB_PATH"])

    @app.route("/")
    def index():
        # Soportamos un parámetro de búsqueda ?q=...
        query = request.args.get("q", "").strip()
        if query:
            pokemons = db.buscar(app.config["DB_PATH"], query)
        else:
            pokemons = db.listar(app.config["DB_PATH"])
        return render_template("index.html", pokemons=pokemons, query=query)

    @app.route("/agregar", methods=["GET", "POST"])
    def agregar():
        if request.method == "POST":
            datos = _datos_form()
            if not datos["nombre"]:
                return render_template("form.html", error="El nombre es obligatorio.",
                                       pokemon=datos, accion="Agregar")
            db.agregar(app.config["DB_PATH"], datos)
            return redirect(url_for("index"))
        return render_template("form.html", error=None, pokemon={}, accion="Agregar")

    @app.route("/pokemon/<int:pokemon_id>")
    def detalle(pokemon_id):
        pokemon = db.obtener(app.config["DB_PATH"], pokemon_id)
        if pokemon is None:
            abort(404)
        return render_template("detalle.html", pokemon=pokemon)

    @app.route("/pokemon/<int:pokemon_id>/editar", methods=["GET", "POST"])
    def editar(pokemon_id):
        pokemon = db.obtener(app.config["DB_PATH"], pokemon_id)
        if pokemon is None:
            abort(404)
        if request.method == "POST":
            datos = _datos_form()
            if not datos["nombre"]:
                return render_template("form.html", error="El nombre es obligatorio.",
                                       pokemon=pokemon, accion="Editar")
            db.actualizar(app.config["DB_PATH"], pokemon_id, datos)
            return redirect(url_for("detalle", pokemon_id=pokemon_id))
        return render_template("form.html", error=None, pokemon=pokemon, accion="Editar")

    @app.route("/pokemon/<int:pokemon_id>/eliminar", methods=["POST"])
    def eliminar(pokemon_id):
        db.eliminar(app.config["DB_PATH"], pokemon_id)
        return redirect(url_for("index"))

    @app.route("/api/buscar/<nombre>")
    def api_buscar(nombre):
        datos = pokeapi.consultar(nombre)
        if datos is None:
            return jsonify({"error": "No encontrado o sin conexión"}), 404
        return jsonify(datos)

    @app.errorhandler(404)
    def no_encontrado(error):
        return render_template("404.html"), 404

    return app


def _datos_form():
    """Extrae y limpia los datos del formulario de agregar/editar."""
    nivel = request.form.get("nivel", "1").strip() or "1"
    return {
        "nombre": request.form.get("nombre", "").strip(),
        "tipo": request.form.get("tipo", "").strip(),
        "nivel": int(nivel) if nivel.isdigit() else 1,
        "altura": request.form.get("altura", "").strip(),
        "peso": request.form.get("peso", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
    }

"""
pokedex_web — Aplicación web Flask (Pokédex). Semana 12.

Una web simple para guardar Pokémon, verlos en una lista, ver el detalle de cada
uno, y autocompletar datos desde la PokéAPI. Persistencia en JSON.

Uso típico:
    from pokedex_web import create_app
    app = create_app()
    app.run(debug=True)
"""

import os

from flask import (
    Flask, render_template, request, redirect, url_for, jsonify, abort
)

from . import storage, pokeapi

# Archivo JSON por defecto (al lado del paquete).
RUTA_DATOS_DEFECTO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "pokedex_datos.json"
)


def create_app(ruta_datos=None):
    """
    Fábrica de la aplicación Flask. Recibir la ruta de datos como parámetro
    permite que los tests usen un archivo temporal.
    """
    app = Flask(__name__)
    # Guardamos la ruta de datos en la config de la app.
    app.config["RUTA_DATOS"] = ruta_datos or RUTA_DATOS_DEFECTO

    # ------------------------------------------------------------------
    #  Página principal: lista de Pokémon.
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        pokemons = storage.cargar(app.config["RUTA_DATOS"])
        return render_template("index.html", pokemons=pokemons)

    # ------------------------------------------------------------------
    #  Agregar un Pokémon (formulario).
    # ------------------------------------------------------------------
    @app.route("/agregar", methods=["GET", "POST"])
    def agregar():
        if request.method == "POST":
            datos = {
                "nombre": request.form.get("nombre", "").strip(),
                "tipo": request.form.get("tipo", "").strip(),
                "nivel": request.form.get("nivel", "1").strip() or "1",
                "altura": request.form.get("altura", "").strip(),
                "peso": request.form.get("peso", "").strip(),
                "descripcion": request.form.get("descripcion", "").strip(),
            }
            # No agregamos si no hay nombre.
            if datos["nombre"]:
                storage.agregar(app.config["RUTA_DATOS"], datos)
                return redirect(url_for("index"))
            # Si falta el nombre, volvemos a mostrar el form con un aviso.
            return render_template("agregar.html", error="El nombre es obligatorio.")
        return render_template("agregar.html", error=None)

    # ------------------------------------------------------------------
    #  Detalle de un Pokémon.
    # ------------------------------------------------------------------
    @app.route("/pokemon/<int:pokemon_id>")
    def detalle(pokemon_id):
        pokemon = storage.buscar_por_id(app.config["RUTA_DATOS"], pokemon_id)
        if pokemon is None:
            abort(404)
        return render_template("detalle.html", pokemon=pokemon)

    # ------------------------------------------------------------------
    #  Eliminar un Pokémon.
    # ------------------------------------------------------------------
    @app.route("/pokemon/<int:pokemon_id>/eliminar", methods=["POST"])
    def eliminar(pokemon_id):
        storage.eliminar(app.config["RUTA_DATOS"], pokemon_id)
        return redirect(url_for("index"))

    # ------------------------------------------------------------------
    #  API interna: autocompletar desde la PokéAPI.
    #  El formulario la consulta con JavaScript (fetch).
    # ------------------------------------------------------------------
    @app.route("/api/buscar/<nombre>")
    def api_buscar(nombre):
        datos = pokeapi.consultar(nombre)
        if datos is None:
            return jsonify({"error": "No encontrado o sin conexión"}), 404
        return jsonify(datos)

    # Página 404 amigable.
    @app.errorhandler(404)
    def no_encontrado(error):
        return render_template("404.html"), 404

    return app

#!/usr/bin/env python3
"""
run.py — Lanzador de la Pokédex Web (Semana 12)

Cómo usar:
    pip install -r requirements.txt
    python run.py

Después abrí el navegador en http://127.0.0.1:5000
"""

from pokedex_web import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True recarga la app al guardar cambios y muestra errores detallados.
    app.run(debug=True)

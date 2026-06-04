#!/usr/bin/env python3
"""
run.py — Lanzador de la Pokédex Web (versión pulida).

Uso:
    pip install -r requirements.txt
    python run.py

Después abrí http://127.0.0.1:5000
"""

from pokedex_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

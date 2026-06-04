#!/usr/bin/env python3
"""
main.py — Lanzador de la Agenda del Entrenador (Semana 11)

Cómo usar:
    python main.py

Toda la lógica vive en el paquete 'agenda'. Este archivo solo arranca la app.
Los datos se guardan en 'agenda_datos.json' (en esta misma carpeta).
"""

from agenda.app import App


def main():
    App().run()


if __name__ == "__main__":
    main()

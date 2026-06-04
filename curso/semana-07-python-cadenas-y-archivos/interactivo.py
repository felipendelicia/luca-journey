#!/usr/bin/env python3
"""
💾 Pokédex con Persistencia — Semana 07

Registrá Pokémon (nombre, tipo, nivel), guardalos en un archivo CSV, y la
próxima vez que abras el programa, ¡siguen ahí! Esa es la magia de la persistencia.

Cómo jugar:
    python interactivo.py

Las funciones de guardado/carga reciben la ruta como parámetro, así son testeables.
El archivo por defecto es 'mi_pokedex.csv' en esta misma carpeta.
"""

import csv
import os

# Ruta del archivo donde se guarda la Pokédex (al lado de este script).
ARCHIVO_POR_DEFECTO = os.path.join(os.path.dirname(__file__), "mi_pokedex.csv")


def guardar_pokedex(ruta, pokedex):
    """
    Guarda la lista de Pokémon (cada uno un dict con nombre/tipo/nivel) en CSV.
    """
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        # Primera fila: el encabezado.
        escritor.writerow(["nombre", "tipo", "nivel"])
        # Una fila por Pokémon.
        for p in pokedex:
            escritor.writerow([p["nombre"], p["tipo"], p["nivel"]])


def cargar_pokedex(ruta):
    """
    Carga la Pokédex desde un CSV. Si el archivo no existe, devuelve [].
    """
    pokedex = []
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as f:
            lector = csv.reader(f)
            # next() saltea la fila del encabezado.
            encabezado = next(lector, None)
            for fila in lector:
                # Ignoramos filas vacías o mal formadas.
                if len(fila) < 3:
                    continue
                nombre, tipo, nivel = fila[0], fila[1], fila[2]
                pokedex.append({
                    "nombre": nombre,
                    "tipo": tipo,
                    # Convertimos el nivel a int de forma segura.
                    "nivel": int(nivel) if nivel.isdigit() else 0,
                })
    except FileNotFoundError:
        # No hay archivo todavía: Pokédex vacía.
        return []
    return pokedex


def agregar_a_pokedex(pokedex, nombre, tipo, nivel):
    """Agrega un Pokémon a la lista (en memoria) y la devuelve."""
    pokedex.append({"nombre": nombre, "tipo": tipo, "nivel": nivel})
    return pokedex


def jugar():
    print("=" * 50)
    print("💾  POKÉDEX CON PERSISTENCIA — Semana 07")
    print("=" * 50)

    # Al arrancar, cargamos lo que haya guardado de antes.
    pokedex = cargar_pokedex(ARCHIVO_POR_DEFECTO)
    print(f"📂 Pokédex cargada: {len(pokedex)} Pokémon registrados.")

    while True:
        print("\n¿Qué querés hacer?")
        print("   1) Registrar un Pokémon")
        print("   2) Ver la Pokédex")
        print("   3) Guardar y salir")
        print("   4) Salir sin guardar")

        try:
            opcion = input("Opción > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau! 👋")
            return

        if opcion == "1":
            nombre = input("   Nombre: ").strip()
            tipo = input("   Tipo: ").strip()
            nivel_txt = input("   Nivel: ").strip()
            nivel = int(nivel_txt) if nivel_txt.isdigit() else 1
            agregar_a_pokedex(pokedex, nombre, tipo, nivel)
            print(f"   ✅ {nombre} registrado (todavía sin guardar en disco).")

        elif opcion == "2":
            if not pokedex:
                print("   (Pokédex vacía)")
            else:
                print("\n   --- TU POKÉDEX ---")
                for i, p in enumerate(pokedex, start=1):
                    print(f"   {i}. {p['nombre']} ({p['tipo']}) - Nivel {p['nivel']}")

        elif opcion == "3":
            guardar_pokedex(ARCHIVO_POR_DEFECTO, pokedex)
            print(f"   💾 Guardado en {ARCHIVO_POR_DEFECTO}. ¡Hasta la próxima!")
            return

        elif opcion == "4":
            print("   Saliste sin guardar los cambios nuevos. 👋")
            return

        else:
            print("   ⚠️ Opción no válida.")


if __name__ == "__main__":
    jugar()

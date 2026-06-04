#!/usr/bin/env python3
"""
🎴 Registro de Entrenador — Semana 03

Te pide tus datos (nombre, edad, ciudad, Pokémon inicial) y genera tu
TARJETA DE ENTRENADOR en ASCII art.

Cómo jugar:
    python interactivo.py

La generación de la tarjeta vive en 'generar_tarjeta()', una función pura
(sin input()) para que los tests puedan verificarla.
"""


def generar_tarjeta(nombre, edad, ciudad, inicial):
    """
    Devuelve la tarjeta de Entrenador como un string de ASCII art.
    Recibe todos los datos como parámetros (no usa input()), así es testeable.
    """
    # Recortamos cada dato para que entre en el ancho de la tarjeta (18 caracteres).
    ancho = 18

    def encajar(texto):
        """Recorta o rellena un texto para que ocupe exactamente 'ancho' chars."""
        texto = str(texto)
        if len(texto) > ancho:
            return texto[: ancho - 1] + "…"
        # ljust rellena con espacios a la derecha hasta llegar al ancho.
        return texto.ljust(ancho)

    # Construimos la tarjeta línea por línea con f-strings.
    tarjeta = f"""
╔══════════════════════════════╗
║   🔴⚪ TARJETA DE ENTRENADOR  ║
╠══════════════════════════════╣
║                              ║
║  Nombre : {encajar(nombre)} ║
║  Edad   : {encajar(edad)} ║
║  Ciudad : {encajar(ciudad)} ║
║  Inicial: {encajar(inicial)} ║
║                              ║
║      ¡A ATRAPARLOS TODOS!    ║
╚══════════════════════════════╝
"""
    return tarjeta


def jugar():
    print("=" * 40)
    print("🎴  REGISTRO DE ENTRENADOR — Semana 03")
    print("=" * 40)
    print("Completá tus datos para generar tu tarjeta.\n")

    try:
        nombre = input("¿Cómo te llamás, Entrenador? ")
        edad = input("¿Qué edad tenés? ")
        ciudad = input("¿De qué ciudad sos? ")
        inicial = input("¿Cuál es tu Pokémon inicial favorito? ")
    except (EOFError, KeyboardInterrupt):
        print("\n¡Hasta la próxima! 👋")
        return

    tarjeta = generar_tarjeta(nombre, edad, ciudad, inicial)
    print(tarjeta)
    print("¡Bienvenido a tu aventura, " + (nombre or "Entrenador") + "! ⚡")


if __name__ == "__main__":
    jugar()

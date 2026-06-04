#!/usr/bin/env python3
"""
🛠️ Constructor de Scripts Bash — Semana 02

Te guía, línea por línea, a escribir tu PRIMER script bash de verdad. El script
que vas a construir se llama 'registrar.sh' y sirve para automatizar el registro
de los Pokémon que vas capturando.

En cada paso te decimos qué línea escribir. Vos la tipeás, y el programa verifica
si está bien. Al final, podés guardar el script resultante en un archivo real.

Cómo jugar:
    python interactivo.py

La lógica de validación está en funciones puras (sin input()) para que los tests
puedan probarla sin teclado.
"""

import re


# ======================================================================
#  Helpers de validación.
# ======================================================================
def _normalizar(linea):
    """Saca espacios de más para comparar de forma flexible."""
    return " ".join(linea.strip().split())


# Cada paso del constructor tiene:
#   - "instruccion": qué tiene que lograr el usuario.
#   - "ejemplo":     una línea válida de ejemplo (se usa para armar el script).
#   - "validar":     función(linea) -> (bool, mensaje_de_feedback)
def _validar_shebang(linea):
    linea = _normalizar(linea)
    # Aceptamos las dos formas comunes del shebang.
    if re.match(r"^#!\s*(/usr/bin/env\s+bash|/bin/bash)$", linea):
        return True, "✅ ¡Perfecto! El shebang le dice al sistema que use bash."
    return False, (
        "❌ El shebang va en la primera línea y empieza con '#!'. "
        "Probá con: #!/usr/bin/env bash"
    )


def _validar_comentario(linea):
    linea = linea.strip()
    if linea.startswith("#") and not linea.startswith("#!") and len(linea) > 1:
        return True, "✅ ¡Bien! Los comentarios (que empiezan con #) documentan el script."
    return False, (
        "❌ Un comentario empieza con '#' (pero no con '#!'). "
        "Escribí algo como: # Registra un Pokemon capturado"
    )


def _validar_variable(linea):
    linea = _normalizar(linea)
    # Forma: POKEMON="algo"  (sin espacios alrededor del =)
    if re.match(r'^POKEMON="[^"]+"$', linea):
        return True, '✅ ¡Genial! Guardaste el nombre en la variable POKEMON.'
    if " = " in linea or re.search(r"=\s", linea) or re.search(r"\s=", linea):
        return False, (
            "❌ ¡Ojo! En bash NO van espacios alrededor del '='. "
            'Tiene que ser: POKEMON="Pikachu"'
        )
    return False, (
        '❌ Creá la variable así (con comillas y sin espacios): POKEMON="Pikachu"'
    )


def _validar_echo_archivo(linea):
    linea = _normalizar(linea)
    # Forma: echo "$POKEMON" >> capturados.txt  (usa la variable y agrega al archivo)
    usa_variable = "$POKEMON" in linea
    agrega = ">>" in linea
    if linea.startswith("echo") and usa_variable and agrega and "capturados.txt" in linea:
        return True, "✅ ¡Excelente! Guardás el Pokémon en capturados.txt sin pisar lo anterior."
    if ">" in linea and ">>" not in linea:
        return False, (
            "❌ Usaste '>' que REEMPLAZA el archivo. Para AGREGAR sin borrar, usá '>>'."
        )
    return False, (
        '❌ Escribí algo como: echo "$POKEMON" >> capturados.txt '
        "(usá la variable con $ y agregá con >>)"
    )


def _validar_echo_confirmacion(linea):
    linea = _normalizar(linea)
    if linea.startswith("echo") and "$POKEMON" in linea:
        return True, "✅ ¡Listo! Le confirmás al usuario que el Pokémon fue registrado."
    return False, (
        '❌ Mostrá un mensaje de confirmación usando la variable, por ejemplo: '
        'echo "$POKEMON registrado!"'
    )


PASOS = [
    {
        "instruccion": "Escribí el SHEBANG: la primera línea que indica que esto es un script bash.",
        "ejemplo": "#!/usr/bin/env bash",
        "validar": _validar_shebang,
    },
    {
        "instruccion": "Escribí un COMENTARIO que explique qué hace el script (empieza con #).",
        "ejemplo": "# Registra un Pokemon capturado en capturados.txt",
        "validar": _validar_comentario,
    },
    {
        "instruccion": 'Creá una VARIABLE llamada POKEMON con un nombre. Recordá: sin espacios en el =.',
        "ejemplo": 'POKEMON="Pikachu"',
        "validar": _validar_variable,
    },
    {
        "instruccion": "Escribí un ECHO que AGREGUE el valor de POKEMON al archivo capturados.txt (usá >>).",
        "ejemplo": 'echo "$POKEMON" >> capturados.txt',
        "validar": _validar_echo_archivo,
    },
    {
        "instruccion": "Escribí un ECHO de confirmación que muestre el nombre del Pokémon registrado.",
        "ejemplo": 'echo "$POKEMON registrado con exito!"',
        "validar": _validar_echo_confirmacion,
    },
]


def construir_script(lineas):
    """Dada la lista de líneas válidas, arma el texto final del script."""
    return "\n".join(lineas) + "\n"


# ======================================================================
#  La interacción.
# ======================================================================
def jugar():
    print("=" * 60)
    print("🛠️  CONSTRUCTOR DE SCRIPTS BASH — Semana 02")
    print("=" * 60)
    print("Vamos a escribir, paso a paso, tu primer script bash:")
    print("'registrar.sh', que registra los Pokémon que capturás.\n")
    print("Escribí cada línea cuando te la pidamos. Si te trabás, escribí 'pista'.\n")

    lineas_ok = []

    for numero, paso in enumerate(PASOS, start=1):
        print(f"\n📍 Paso {numero}/{len(PASOS)}: {paso['instruccion']}")
        while True:
            try:
                linea = input("   tu línea > ")
            except (EOFError, KeyboardInterrupt):
                print("\n¡Chau, Entrenador! 👋")
                return

            if linea.strip() == "pista":
                print(f"   💡 Ejemplo: {paso['ejemplo']}")
                continue

            ok, mensaje = paso["validar"](linea)
            print("   " + mensaje)
            if ok:
                # Guardamos la línea EXACTA que escribió el usuario.
                lineas_ok.append(linea.rstrip())
                break

    script_final = construir_script(lineas_ok)

    print("\n" + "=" * 60)
    print("🎉 ¡SCRIPT COMPLETO! Así quedó tu registrar.sh:")
    print("=" * 60)
    print(script_final)

    try:
        guardar = input("¿Querés guardarlo en 'registrar.sh'? (s/n): ")
    except (EOFError, KeyboardInterrupt):
        return
    if guardar.strip().lower().startswith("s"):
        with open("registrar.sh", "w", encoding="utf-8") as f:
            f.write(script_final)
        print("✅ Guardado en registrar.sh")
        print("   Para usarlo de verdad:")
        print("     chmod +x registrar.sh")
        print("     ./registrar.sh")
    else:
        print("👍 No lo guardamos. ¡Igual aprendiste a escribirlo!")


if __name__ == "__main__":
    jugar()

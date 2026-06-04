#!/usr/bin/env python3
"""
generar_manual.py — Genera 'manual.pdf' a partir de 'manual_fuente.md'.

El manual se escribe y mantiene en 'manual_fuente.md' (Markdown). Este script lo
convierte a HTML (con índice automático) y después a PDF usando LibreOffice.

Uso:
    python generar_manual.py

Requisitos: el módulo de Python 'markdown' y 'libreoffice'/'soffice' instalados.
(Ambos suelen venir en Linux; si falta markdown: pip install markdown)

IMPORTANTE: cuando cambie el proyecto, actualizá 'manual_fuente.md' y volvé a
correr este script para regenerar el PDF. (Ver CLAUDE.md.)
"""

import os
import shutil
import subprocess
import sys
import tempfile

import markdown

RAIZ = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.join(RAIZ, "manual_fuente.md")
SALIDA_PDF = os.path.join(RAIZ, "manual.pdf")

# Estilos del manual. LibreOffice (importador HTML) soporta un subconjunto de
# CSS, así que mantenemos los estilos simples y robustos.
CSS = """
body { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 11pt;
       color: #1a1a1a; line-height: 1.5; }
h1 { color: #b71c0c; font-size: 22pt; border-bottom: 3px solid #e3350d;
     padding-bottom: 4px; page-break-before: always; }
h1.portada { page-break-before: avoid; border: none; font-size: 30pt;
             text-align: center; margin-top: 60px; }
h2 { color: #3b4cca; font-size: 16pt; margin-top: 18px; }
h3 { color: #444; font-size: 13pt; }
code { font-family: 'Liberation Mono', monospace; background: #f2f2f2;
       padding: 1px 3px; font-size: 10pt; }
pre { background: #f2f2f2; border-left: 4px solid #3b4cca; padding: 8px;
      font-family: 'Liberation Mono', monospace; font-size: 9.5pt; }
table { border-collapse: collapse; }
th, td { border: 1px solid #ccc; padding: 4px 8px; font-size: 10pt; }
th { background: #ffcb05; }
blockquote { border-left: 4px solid #ffcb05; margin-left: 0; padding-left: 12px;
             color: #555; }
.toc { background: #f7f7f7; border: 1px solid #ddd; padding: 10px 20px; }
.toc ul { list-style: none; }
a { color: #3b4cca; text-decoration: none; }
"""


def construir_html(texto_md):
    """Convierte el Markdown a un documento HTML completo y con estilos."""
    cuerpo = markdown.markdown(
        texto_md,
        extensions=["toc", "tables", "fenced_code", "sane_lists"],
    )
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Manual — Curso de Python con Pokémon</title>
<style>{CSS}</style>
</head>
<body>
{cuerpo}
</body>
</html>"""


def buscar_soffice():
    """Devuelve el comando de LibreOffice disponible, o None."""
    for cmd in ("libreoffice", "soffice"):
        if shutil.which(cmd):
            return cmd
    return None


def generar():
    if not os.path.exists(FUENTE):
        print(f"✗ No se encontró {FUENTE}")
        return 1

    with open(FUENTE, "r", encoding="utf-8") as f:
        texto_md = f.read()

    html = construir_html(texto_md)

    soffice = buscar_soffice()
    if soffice is None:
        print("✗ No se encontró LibreOffice (libreoffice/soffice).")
        print("  Instalalo, o convertí manual_fuente.md a PDF con otra herramienta.")
        return 1

    # Trabajamos en una carpeta temporal para no ensuciar el repo.
    with tempfile.TemporaryDirectory() as tmp:
        ruta_html = os.path.join(tmp, "manual.html")
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html)

        perfil = "file://" + os.path.join(tmp, "lo_profile")
        comando = [
            soffice, "--headless", "--convert-to", "pdf",
            "--outdir", RAIZ, f"-env:UserInstallation={perfil}", ruta_html,
        ]
        print("➤ Convirtiendo a PDF con LibreOffice...")
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode != 0:
            print("✗ Error al convertir:")
            print(resultado.stdout + resultado.stderr)
            return 1

    if os.path.exists(SALIDA_PDF):
        print(f"✓ Manual generado: {SALIDA_PDF}")
        return 0
    print("✗ No se generó el PDF (revisá la salida de arriba).")
    return 1


if __name__ == "__main__":
    sys.exit(generar())

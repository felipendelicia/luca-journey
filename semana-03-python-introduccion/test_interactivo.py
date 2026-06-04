"""
🧪 Tests del Registro de Entrenador — Semana 03
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana03_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")


def test_tarjeta_incluye_datos():
    tarjeta = interactivo.generar_tarjeta("Ash", "10", "Paleta", "Pikachu")
    assert "Ash" in tarjeta, "La tarjeta debería incluir el nombre"
    assert "Paleta" in tarjeta, "La tarjeta debería incluir la ciudad"
    assert "Pikachu" in tarjeta, "La tarjeta debería incluir el inicial"


def test_tarjeta_es_string_con_bordes():
    tarjeta = interactivo.generar_tarjeta("Ash", "10", "Paleta", "Pikachu")
    assert isinstance(tarjeta, str), "La tarjeta debería ser un string"
    assert "╔" in tarjeta and "╝" in tarjeta, "La tarjeta debería tener bordes ASCII"


def test_tarjeta_recorta_nombres_largos():
    # Un nombre larguísimo no debería romper el formato (se recorta).
    largo = "EsteNombreEsRidiculamenteLargoParaUnaTarjeta"
    tarjeta = interactivo.generar_tarjeta(largo, "10", "Paleta", "Pikachu")
    # Las filas de datos (las que tienen ":") deben tener todas el mismo ancho,
    # aunque el nombre original fuera larguísimo.
    filas_datos = [l for l in tarjeta.split("\n") if ":" in l and l.startswith("║")]
    anchos = {len(l) for l in filas_datos}
    assert len(anchos) == 1, (
        f"Las filas de datos deberían tener el mismo ancho, "
        f"pero se encontraron anchos distintos: {anchos}"
    )
    # Y el nombre larguísimo debería aparecer recortado con '…'.
    assert "…" in tarjeta, "Un nombre demasiado largo debería recortarse con '…'"

"""Tests del módulo agenda.storage."""

from agenda import storage


def test_guardar_y_cargar(tmp_path):
    ruta = str(tmp_path / "datos.json")
    estado = {
        "capturados": [{"nombre": "Pikachu", "tipo": "Electrico", "nivel": 25, "fecha_captura": "2024-01-01"}],
        "equipo": ["Pikachu"],
        "batallas": [{"rival": "Brock", "resultado": "gano", "pokemon_usado": "Pikachu", "fecha": "2024-01-02"}],
    }
    storage.guardar(estado, ruta)
    cargado = storage.cargar(ruta)
    assert cargado == estado


def test_cargar_inexistente_devuelve_vacio(tmp_path):
    ruta = str(tmp_path / "no_existe.json")
    estado = storage.cargar(ruta)
    assert estado == {"capturados": [], "equipo": [], "batallas": []}


def test_cargar_json_corrupto(tmp_path):
    ruta = tmp_path / "corrupto.json"
    ruta.write_text("esto no es json {{{")
    estado = storage.cargar(str(ruta))
    # No debería romper: devuelve estado vacío.
    assert estado["capturados"] == []


def test_cargar_completa_claves_faltantes(tmp_path):
    ruta = tmp_path / "parcial.json"
    ruta.write_text('{"capturados": []}')
    estado = storage.cargar(str(ruta))
    assert "equipo" in estado
    assert "batallas" in estado

"""Tests de la Agenda del Entrenador (versión pulida)."""

from agenda_entrenador.pokemon import Pokemon
from agenda_entrenador.equipo import Equipo
from agenda_entrenador.batallas import Batalla, Historial, GANO, PERDIO
from agenda_entrenador import estadisticas, storage
from agenda_entrenador.app import App


# ----- Pokemon -----
def test_pokemon_to_from_dict():
    p = Pokemon("Pikachu", "Electrico", 25, "2024-01-01")
    assert Pokemon.from_dict(p.to_dict()) == p


# ----- Equipo -----
def test_equipo_maximo():
    e = Equipo()
    for i in range(6):
        e.agregar(Pokemon(f"P{i}", "Normal", 10))
    ok, _ = e.agregar(Pokemon("Extra", "Normal", 10))
    assert ok is False


def test_equipo_quitar_inexistente():
    e = Equipo()
    ok, _ = e.quitar("Nadie")
    assert ok is False


# ----- Batallas -----
def test_historial_conteos():
    h = Historial()
    h.registrar(Batalla("A", GANO, "Pikachu"))
    h.registrar(Batalla("B", PERDIO, "Onix"))
    assert h.total() == 2
    assert h.victorias() == 1


# ----- Estadísticas -----
def test_porcentaje_victorias():
    h = Historial()
    h.registrar(Batalla("A", GANO, "Pikachu"))
    h.registrar(Batalla("B", PERDIO, "Pikachu"))
    assert estadisticas.porcentaje_victorias(h) == 50


def test_tipo_favorito():
    capturados = [
        Pokemon("Pikachu", "Electrico", 25),
        Pokemon("Raichu", "Electrico", 40),
        Pokemon("Onix", "Roca", 30),
    ]
    assert estadisticas.tipo_favorito(capturados) == "Electrico"


def test_tipo_favorito_vacio():
    assert estadisticas.tipo_favorito([]) is None


def test_capturados_ordenados():
    capturados = [
        Pokemon("Pikachu", "Electrico", 25),
        Pokemon("Charizard", "Fuego", 50),
        Pokemon("Onix", "Roca", 30),
    ]
    ordenados = estadisticas.capturados_ordenados(capturados)
    assert [p.nombre for p in ordenados] == ["Charizard", "Onix", "Pikachu"]


# ----- Storage -----
def test_storage_ciclo(tmp_path):
    ruta = str(tmp_path / "d.json")
    estado = {"capturados": [], "equipo": [], "batallas": []}
    storage.guardar(estado, ruta)
    assert storage.cargar(ruta) == estado


def test_storage_inexistente(tmp_path):
    assert storage.cargar(str(tmp_path / "no.json")) == {
        "capturados": [], "equipo": [], "batallas": []
    }


# ----- App (integración) -----
def test_app_persistencia(tmp_path):
    ruta = str(tmp_path / "d.json")
    app = App(ruta=ruta)
    app.registrar_captura("Pikachu", "Electrico", 25)
    app.registrar_captura("Charizard", "Fuego", 50)
    app.equipo.agregar(app.capturados[0])
    app.registrar_batalla("Brock", True, "Pikachu")
    app.guardar()

    app2 = App(ruta=ruta)
    assert len(app2.capturados) == 2
    assert app2.equipo.nombres() == ["Pikachu"]
    assert app2.historial.victorias() == 1


def test_app_no_duplica_captura(tmp_path):
    app = App(ruta=str(tmp_path / "d.json"))
    app.registrar_captura("Pikachu", "Electrico", 25)
    msg = app.registrar_captura("Pikachu", "Electrico", 30)
    assert "ya estaba" in msg
    assert len(app.capturados) == 1

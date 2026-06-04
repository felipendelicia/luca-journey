"""
Tests de la Pokédex Web con el cliente de test de Flask.

Si Flask no está instalado, estos tests se SALTEAN (no fallan).
Ningún test usa internet: la PokéAPI se simula con monkeypatch.
"""

import pytest

# Si no hay Flask, salteamos todo el módulo de forma elegante.
pytest.importorskip("flask")

from pokedex_web import create_app, storage, pokeapi


@pytest.fixture
def cliente(tmp_path):
    """Crea una app de test con un archivo de datos temporal y su test client."""
    ruta = str(tmp_path / "datos.json")
    app = create_app(ruta_datos=ruta)
    app.config["TESTING"] = True
    with app.test_client() as c:
        # Guardamos la ruta para que los tests puedan inspeccionar el JSON.
        c.ruta_datos = ruta
        yield c


# ----------------------------------------------------------------------
#  Página principal
# ----------------------------------------------------------------------
def test_index_vacio(cliente):
    resp = cliente.get("/")
    assert resp.status_code == 200
    # Con la Pokédex vacía, debería invitar a agregar el primero.
    assert "Todavía no guardaste" in resp.get_data(as_text=True)


def test_index_muestra_pokemon(cliente):
    storage.agregar(cliente.ruta_datos, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    resp = cliente.get("/")
    texto = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Pikachu" in texto


# ----------------------------------------------------------------------
#  Agregar
# ----------------------------------------------------------------------
def test_agregar_get(cliente):
    resp = cliente.get("/agregar")
    assert resp.status_code == 200
    assert "Agregar un Pokémon" in resp.get_data(as_text=True)


def test_agregar_post_guarda_y_redirige(cliente):
    resp = cliente.post("/agregar", data={
        "nombre": "Charizard",
        "tipo": "fire",
        "nivel": "50",
    })
    # Tras agregar, redirige (302) al inicio.
    assert resp.status_code == 302
    pokemons = storage.cargar(cliente.ruta_datos)
    assert len(pokemons) == 1
    assert pokemons[0]["nombre"] == "Charizard"


def test_agregar_sin_nombre_muestra_error(cliente):
    resp = cliente.post("/agregar", data={"nombre": "", "tipo": "fire", "nivel": "5"})
    assert resp.status_code == 200
    assert "obligatorio" in resp.get_data(as_text=True)
    # No debería haber guardado nada.
    assert storage.cargar(cliente.ruta_datos) == []


# ----------------------------------------------------------------------
#  Detalle
# ----------------------------------------------------------------------
def test_detalle_existente(cliente):
    p = storage.agregar(cliente.ruta_datos, {"nombre": "Onix", "tipo": "rock", "nivel": 30})
    resp = cliente.get(f"/pokemon/{p['id']}")
    assert resp.status_code == 200
    assert "Onix" in resp.get_data(as_text=True)


def test_detalle_inexistente_404(cliente):
    resp = cliente.get("/pokemon/999")
    assert resp.status_code == 404
    assert "escapó" in resp.get_data(as_text=True)


# ----------------------------------------------------------------------
#  Eliminar
# ----------------------------------------------------------------------
def test_eliminar(cliente):
    p = storage.agregar(cliente.ruta_datos, {"nombre": "Rattata", "tipo": "normal", "nivel": 5})
    resp = cliente.post(f"/pokemon/{p['id']}/eliminar")
    assert resp.status_code == 302
    assert storage.cargar(cliente.ruta_datos) == []


# ----------------------------------------------------------------------
#  API de autocompletado (PokéAPI simulada)
# ----------------------------------------------------------------------
def test_api_buscar_ok(cliente, monkeypatch):
    # Simulamos la respuesta de la PokéAPI sin tocar internet.
    def falso_consultar(nombre):
        return {"nombre": "Pikachu", "tipo": "electric", "altura": 0.4, "peso": 6.0,
                "descripcion": "Pokémon de tipo electric."}
    monkeypatch.setattr(pokeapi, "consultar", falso_consultar)

    resp = cliente.get("/api/buscar/pikachu")
    assert resp.status_code == 200
    datos = resp.get_json()
    assert datos["nombre"] == "Pikachu"
    assert datos["tipo"] == "electric"


def test_api_buscar_no_encontrado(cliente, monkeypatch):
    monkeypatch.setattr(pokeapi, "consultar", lambda nombre: None)
    resp = cliente.get("/api/buscar/inventado")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

"""
Tests de la Pokédex Web pulida (Flask + SQLite, sin internet).

Si Flask no está instalado, se saltean.
"""

import pytest

pytest.importorskip("flask")

from pokedex_app import create_app, db, pokeapi


@pytest.fixture
def app(tmp_path):
    ruta_db = str(tmp_path / "test.db")
    aplicacion = create_app(db_path=ruta_db)
    aplicacion.config["TESTING"] = True
    aplicacion.config["RUTA_DB_TEST"] = ruta_db
    return aplicacion


@pytest.fixture
def cliente(app):
    with app.test_client() as c:
        c.ruta_db = app.config["RUTA_DB_TEST"]
        yield c


# ----------------------------------------------------------------------
#  db (SQLite)
# ----------------------------------------------------------------------
def test_db_agregar_y_listar(tmp_path):
    ruta = str(tmp_path / "d.db")
    db.init_db(ruta)
    db.agregar(ruta, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    lista = db.listar(ruta)
    assert len(lista) == 1
    assert lista[0]["nombre"] == "Pikachu"


def test_db_obtener_y_eliminar(tmp_path):
    ruta = str(tmp_path / "d.db")
    db.init_db(ruta)
    nuevo_id = db.agregar(ruta, {"nombre": "Onix", "tipo": "rock", "nivel": 30})
    assert db.obtener(ruta, nuevo_id)["nombre"] == "Onix"
    assert db.eliminar(ruta, nuevo_id) is True
    assert db.obtener(ruta, nuevo_id) is None


def test_db_actualizar(tmp_path):
    ruta = str(tmp_path / "d.db")
    db.init_db(ruta)
    nuevo_id = db.agregar(ruta, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    db.actualizar(ruta, nuevo_id, {"nombre": "Raichu", "tipo": "electric", "nivel": 40})
    actualizado = db.obtener(ruta, nuevo_id)
    assert actualizado["nombre"] == "Raichu"
    assert actualizado["nivel"] == 40


def test_db_buscar(tmp_path):
    ruta = str(tmp_path / "d.db")
    db.init_db(ruta)
    db.agregar(ruta, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    db.agregar(ruta, {"nombre": "Charizard", "tipo": "fire", "nivel": 50})
    assert len(db.buscar(ruta, "pika")) == 1
    assert len(db.buscar(ruta, "fire")) == 1
    assert len(db.buscar(ruta, "zzz")) == 0


# ----------------------------------------------------------------------
#  Rutas
# ----------------------------------------------------------------------
def test_index_vacio(cliente):
    resp = cliente.get("/")
    assert resp.status_code == 200
    assert "Todavía no guardaste" in resp.get_data(as_text=True)


def test_agregar_y_aparece_en_index(cliente):
    cliente.post("/agregar", data={"nombre": "Pikachu", "tipo": "electric", "nivel": "25"})
    resp = cliente.get("/")
    assert "Pikachu" in resp.get_data(as_text=True)


def test_agregar_sin_nombre(cliente):
    resp = cliente.post("/agregar", data={"nombre": "", "tipo": "fire", "nivel": "5"})
    assert resp.status_code == 200
    assert "obligatorio" in resp.get_data(as_text=True)
    assert db.listar(cliente.ruta_db) == []


def test_detalle_404(cliente):
    resp = cliente.get("/pokemon/999")
    assert resp.status_code == 404


def test_editar(cliente):
    nuevo_id = db.agregar(cliente.ruta_db, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    resp = cliente.post(f"/pokemon/{nuevo_id}/editar",
                        data={"nombre": "Raichu", "tipo": "electric", "nivel": "40"})
    assert resp.status_code == 302
    assert db.obtener(cliente.ruta_db, nuevo_id)["nombre"] == "Raichu"


def test_eliminar(cliente):
    nuevo_id = db.agregar(cliente.ruta_db, {"nombre": "Rattata", "tipo": "normal", "nivel": 5})
    resp = cliente.post(f"/pokemon/{nuevo_id}/eliminar")
    assert resp.status_code == 302
    assert db.listar(cliente.ruta_db) == []


def test_buscar_en_index(cliente):
    db.agregar(cliente.ruta_db, {"nombre": "Pikachu", "tipo": "electric", "nivel": 25})
    db.agregar(cliente.ruta_db, {"nombre": "Charizard", "tipo": "fire", "nivel": 50})
    resp = cliente.get("/?q=pika")
    texto = resp.get_data(as_text=True)
    assert "Pikachu" in texto
    assert "Charizard" not in texto


# ----------------------------------------------------------------------
#  API (PokéAPI simulada)
# ----------------------------------------------------------------------
def test_api_buscar_ok(cliente, monkeypatch):
    monkeypatch.setattr(pokeapi, "consultar",
                        lambda n: {"nombre": "Pikachu", "tipo": "electric",
                                   "altura": 0.4, "peso": 6.0, "descripcion": "x"})
    resp = cliente.get("/api/buscar/pikachu")
    assert resp.status_code == 200
    assert resp.get_json()["nombre"] == "Pikachu"


def test_api_buscar_404(cliente, monkeypatch):
    monkeypatch.setattr(pokeapi, "consultar", lambda n: None)
    resp = cliente.get("/api/buscar/xxx")
    assert resp.status_code == 404

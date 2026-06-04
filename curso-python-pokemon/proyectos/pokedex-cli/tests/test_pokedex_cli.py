"""Tests de la Pokédex CLI (sin internet)."""

from pokedex_cli import pokeapi, favoritos, ui, ascii_art, cli


DATOS_FALSOS = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": [{"type": {"name": "electric"}}],
    "stats": [
        {"stat": {"name": "hp"}, "base_stat": 35},
        {"stat": {"name": "speed"}, "base_stat": 90},
    ],
}


# ----------------------------------------------------------------------
#  pokeapi
# ----------------------------------------------------------------------
def test_parsear():
    info = pokeapi.parsear(DATOS_FALSOS)
    assert info["nombre"] == "pikachu"
    assert info["tipo_principal"] == "electric"
    assert info["altura_m"] == 0.4
    assert info["stats"]["speed"] == 90


def test_parsear_sin_tipos():
    info = pokeapi.parsear({"name": "x"})
    assert info["tipo_principal"] == "normal"


# ----------------------------------------------------------------------
#  favoritos
# ----------------------------------------------------------------------
def test_favoritos_agregar(tmp_path):
    ruta = str(tmp_path / "fav.json")
    ok, msg = favoritos.agregar(ruta, "Pikachu")
    assert ok is True
    assert favoritos.cargar(ruta) == ["pikachu"]


def test_favoritos_no_duplica(tmp_path):
    ruta = str(tmp_path / "fav.json")
    favoritos.agregar(ruta, "pikachu")
    ok, msg = favoritos.agregar(ruta, "pikachu")
    assert ok is False


def test_favoritos_quitar(tmp_path):
    ruta = str(tmp_path / "fav.json")
    favoritos.agregar(ruta, "pikachu")
    ok, msg = favoritos.quitar(ruta, "pikachu")
    assert ok is True
    assert favoritos.cargar(ruta) == []


def test_es_favorito(tmp_path):
    ruta = str(tmp_path / "fav.json")
    favoritos.agregar(ruta, "pikachu")
    assert favoritos.es_favorito(ruta, "Pikachu") is True
    assert favoritos.es_favorito(ruta, "onix") is False


# ----------------------------------------------------------------------
#  ascii_art
# ----------------------------------------------------------------------
def test_sprite_conocido():
    assert isinstance(ascii_art.sprite("fire"), str)
    assert len(ascii_art.sprite("fire").strip()) > 0


def test_sprite_desconocido_usa_generico():
    assert ascii_art.sprite("inventado") == ascii_art.GENERICO


# ----------------------------------------------------------------------
#  ui
# ----------------------------------------------------------------------
def test_ficha_incluye_datos():
    info = pokeapi.parsear(DATOS_FALSOS)
    texto = ui.ficha(info)
    assert "PIKACHU" in texto
    assert "electric" in texto


def test_ficha_favorito_tiene_estrella():
    info = pokeapi.parsear(DATOS_FALSOS)
    texto = ui.ficha(info, favorito=True)
    assert "⭐" in texto


# ----------------------------------------------------------------------
#  cli.mostrar_pokemon (con la red simulada)
# ----------------------------------------------------------------------
def test_mostrar_pokemon_ok(tmp_path, monkeypatch):
    monkeypatch.setattr(pokeapi, "consultar", lambda nombre: pokeapi.parsear(DATOS_FALSOS))
    ruta = str(tmp_path / "fav.json")
    texto = cli.mostrar_pokemon("pikachu", ruta_favoritos=ruta)
    assert "PIKACHU" in texto


def test_mostrar_pokemon_no_encontrado(tmp_path, monkeypatch):
    monkeypatch.setattr(pokeapi, "consultar", lambda nombre: None)
    texto = cli.mostrar_pokemon("inventado", ruta_favoritos=str(tmp_path / "fav.json"))
    assert "No encontré" in texto

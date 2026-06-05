import ejercicios


def test_subclase_fuego():
    p = ejercicios.PokemonFuego("Vulpix", 12, 400)
    assert p.nombre == "Vulpix"
    assert p.tipo == "fuego"
    assert p.nivel == 12
    assert p.temperatura == 400
    # hereda de Pokemon
    assert isinstance(p, ejercicios.Pokemon)


def test_metodo_especial():
    assert str(ejercicios.PokemonFuego("Vulpix", 12, 400)) == "Vulpix (Nv.12) — 🔥 400°C"
    assert str(ejercicios.PokemonFuego("Arcanine", 35, 800)) == "Arcanine (Nv.35) — 🔥 800°C"


def test_metodo_evolucionar():
    p = ejercicios.PokemonFuego("Vulpix", 12, 400)
    p.evolucionar("Ninetales")
    assert p.nombre == "Ninetales"
    assert p.nivel == 22
    assert p.temperatura == 600


def test_equipo_fuego():
    datos = [
        {"nombre": "Vulpix",    "nivel": 12, "temperatura": 400},
        {"nombre": "Growlithe", "nivel": 18, "temperatura": 550},
        {"nombre": "Magmar",    "nivel": 27, "temperatura": 720},
    ]
    pokis = ejercicios.equipo_fuego(datos)
    assert len(pokis) == 3
    assert pokis[0].nombre == "Vulpix"
    assert all(isinstance(p, ejercicios.PokemonFuego) for p in pokis)
    caliente = ejercicios.mas_caliente(pokis)
    assert caliente.nombre == "Magmar"
    assert caliente.temperatura == 720

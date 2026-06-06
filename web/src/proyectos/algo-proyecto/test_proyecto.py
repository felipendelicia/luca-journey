import ejercicios


def test_por_tipo():
    assert ejercicios.por_tipo([{"nombre": "Squirtle", "tipo": "agua"}, {"nombre": "Psyduck", "tipo": "agua"}]) == {"agua": ["Squirtle", "Psyduck"]}


def test_ordenar():
    assert ejercicios.ordenar([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}]) == [{"nombre": "b", "nivel": 20}, {"nombre": "a", "nivel": 5}]


def test_mas_fuerte():
    assert ejercicios.mas_fuerte([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}]) == "b"
    assert ejercicios.mas_fuerte([]) == ""


def test_reporte():
    assert ejercicios.reporte([{"nombre": "Pikachu", "nivel": 30}, {"nombre": "Onix", "nivel": 10}]) == "2 Pokémon, el más fuerte es Pikachu."

import ejercicios


def test_cargar():
    assert ejercicios.cargar(["Pikachu,electrico,30", "Onix,roca,12"]) == [
        {"nombre": "Pikachu", "tipo": "electrico", "nivel": 30},
        {"nombre": "Onix", "tipo": "roca", "nivel": 12},
    ]


def test_promedio():
    assert ejercicios.promedio_nivel([{"nivel": 10}, {"nivel": 20}, {"nivel": 30}]) == 20
    assert ejercicios.promedio_nivel([]) == 0


def test_mejor():
    assert ejercicios.mejor([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 40}]) == "b"
    assert ejercicios.mejor([]) == ""


def test_reporte():
    assert ejercicios.reporte([{"nombre": "Pikachu", "nivel": 30}, {"nombre": "Onix", "nivel": 10}]) == "2 Pokémon, nivel promedio 20, mejor: Pikachu."

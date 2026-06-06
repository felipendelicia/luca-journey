import ejercicios


def test_espacios():
    assert ejercicios.limpiar_espacios("  Hola   \n  mundo ") == "Hola mundo"


def test_titulo():
    assert ejercicios.extraer_titulo("<h1>Pikachu</h1><p>...</p>") == "Pikachu"
    assert ejercicios.extraer_titulo("<p>nada</p>") == ""


def test_items():
    assert ejercicios.extraer_items("<ul><li>Rayo</li><li>Placaje</li></ul>") == ["Rayo", "Placaje"]


def test_ficha():
    assert ejercicios.ficha("<h1>Pikachu</h1><ul><li>Rayo</li><li>Placaje</li></ul>") == {"nombre": "Pikachu", "movimientos": ["Rayo", "Placaje"]}

# CURSO_MODULO=ejercicios → el módulo 'ejercicios' es el código ACUMULADO del alumno.
# Importamos el MÓDULO (no los nombres sueltos): así carga aunque todavía falten las
# funciones de pasos posteriores; cada test referencia lo que necesita por atributo.
import ejercicios


def test_buscar():
    assert ejercicios.buscar("Pikachu") == {"tipo": "eléctrico", "nivel": 10}
    assert ejercicios.buscar("CHARIZARD") == {"tipo": "fuego", "nivel": 36}
    assert ejercicios.buscar("nada") is None


def test_mostrar():
    assert ejercicios.mostrar({"tipo": "fuego", "nivel": 36}) == "Tipo: fuego · Nivel: 36"
    assert ejercicios.mostrar(None) == "No encontrado."


def test_responder():
    assert ejercicios.responder("charizard") == "Tipo: fuego · Nivel: 36"
    assert ejercicios.responder("xxx") == "No encontrado."


def test_pokedex():
    assert ejercicios.pokedex(["pikachu", "xxx"]) == ["Tipo: eléctrico · Nivel: 10", "No encontrado."]

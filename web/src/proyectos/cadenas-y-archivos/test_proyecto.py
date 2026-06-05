import ejercicios


def test_cifrar():
    assert ejercicios.cifrar("Pikachu") == "P1k4chv"
    assert ejercicios.cifrar("Arcanine") == "4rc4n1n3"
    assert ejercicios.cifrar("xyz") == "xyz"
    assert ejercicios.cifrar("Eevee") == "33v33"


def test_contar_palabras():
    assert ejercicios.contar_palabras("Pikachu usa Thunderbolt Pikachu gana") == {
        "pikachu": 2, "usa": 1, "thunderbolt": 1, "gana": 1
    }
    assert ejercicios.contar_palabras("Agua Fuego agua") == {"agua": 2, "fuego": 1}


def test_parsear_datos():
    assert ejercicios.parsear_datos("Venomoth|veneno|43") == {
        "nombre": "Venomoth", "tipo": "veneno", "nivel": 43
    }
    assert ejercicios.parsear_datos(" Koffing | veneno | 37 ") == {
        "nombre": "Koffing", "tipo": "veneno", "nivel": 37
    }


def test_procesar_informe():
    informe = "Venomoth|veneno|43\nKoffing|veneno|37\n\nWeezing|veneno|39"
    resultado = ejercicios.procesar_informe(informe)
    assert resultado == [
        "V3n0m0th (nivel 43)",
        "K0ff1ng (nivel 37)",
        "W33z1ng (nivel 39)",
    ]

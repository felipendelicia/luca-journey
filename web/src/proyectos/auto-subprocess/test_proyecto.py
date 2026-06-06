import ejercicios


def test_armar():
    assert ejercicios.armar("python", ["bot.py", "--v"]) == ["python", "bot.py", "--v"]
    assert ejercicios.armar("ls", []) == ["ls"]


def test_ok():
    assert ejercicios.ok(0) is True
    assert ejercicios.ok(2) is False


def test_primera():
    assert ejercicios.primera_linea("\n  Listo!  \nmás") == "Listo!"
    assert ejercicios.primera_linea("") == ""


def test_reporte():
    assert ejercicios.reporte({"returncode": 0, "stdout": "Hecho\n"}) == "OK: Hecho"
    assert ejercicios.reporte({"returncode": 2, "stdout": ""}) == "ERROR (codigo 2)"

import ejercicios


def test_crear_app():
    c = ejercicios.crear_app().test_client()
    r = c.get("/")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "¡Bienvenido, Entrenador!"


def test_ping():
    c = ejercicios.crear_app().test_client()
    r = c.get("/ping")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "pong"


def test_version():
    c = ejercicios.crear_app().test_client()
    r = c.get("/version")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "1.0"


def test_estado():
    c = ejercicios.crear_app().test_client()
    r = c.get("/estado")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "online"

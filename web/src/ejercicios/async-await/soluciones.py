"""⏳ Soluciones — await: dónde esperar"""


def necesita_await(paso):
    return paso["espera"]


def pasos_con_await(pasos):
    return [p["nombre"] for p in pasos if p["espera"]]


def agregar_await(linea):
    return linea if linea.startswith("await ") else "await " + linea


def contar_awaits(codigo):
    return codigo.count("await ")

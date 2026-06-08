"""⏳ Soluciones — await: dónde esperar"""


def necesita_await(paso):
    return paso["espera"]


def pasos_con_await(pasos):
    return [p["nombre"] for p in pasos if p["espera"]]


def agregar_await(linea):
    return linea if linea.startswith("await ") else "await " + linea


def contar_awaits(codigo):
    return codigo.count("await ")


def quitar_await(linea):
    if linea.startswith("await "):
        return linea[len("await "):]
    return linea


def tiene_await_linea(linea):
    return linea.startswith("await ")


def lineas_con_await(lineas):
    return [l for l in lineas if l.startswith("await ")]


def lineas_sin_await(lineas):
    return [l for l in lineas if not l.startswith("await ")]


def indices_con_await(lineas):
    return [i for i, l in enumerate(lineas) if l.startswith("await ")]


def cuantas_con_await(lineas):
    return sum(1 for l in lineas if l.startswith("await "))


def todas_con_await(lineas):
    return all(l.startswith("await ") for l in lineas)


def ninguna_con_await(lineas):
    return not any(l.startswith("await ") for l in lineas)


def agregar_await_a_todas(lineas):
    return [l if l.startswith("await ") else "await " + l for l in lineas]


def quitar_await_de_todas(lineas):
    return [quitar_await(l) for l in lineas]


def primer_indice_await(lineas):
    for i, l in enumerate(lineas):
        if l.startswith("await "):
            return i
    return -1


def proporcion_con_await(lineas):
    return cuantas_con_await(lineas) / len(lineas)


def normalizar_await(linea):
    cuerpo = linea
    while cuerpo.startswith("await "):
        cuerpo = cuerpo[len("await "):]
    return "await " + cuerpo


def contar_await_total(codigo):
    return codigo.count("await ")


def mas_corta_con_await(lineas):
    con = [l for l in lineas if l.startswith("await ")]
    return min(con, key=len) if con else None


def juntar_lineas(lineas):
    return "\n".join(lineas)

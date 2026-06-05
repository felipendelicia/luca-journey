# desafios-eval.py — corre el código del usuario y evalúa la función sobre los casos.
import json

def _norm(v):
    # representación canónica para comparar (independiente del orden de claves de dict)
    return json.dumps(v, sort_keys=True, default=str)

def computar_esperados(codigo, func, casos_json):
    """Para el AUTOR al publicar: corre la solución y devuelve los casos con 'esperado'.
    casos_json = [{"args":[...], "ejemplo":bool}, ...]. Devuelve JSON o {error:...}."""
    casos = json.loads(casos_json)
    g = {"__name__": "__main__"}
    try:
        exec(codigo, g)
        fn = g.get(func)
        if not callable(fn):
            return json.dumps({"error": "No se encontró la función '%s'." % func})
        out = []
        for c in casos:
            args = c.get("args", [])
            esperado = _norm(fn(*args))
            out.append({"args": args, "esperado": esperado, "ejemplo": bool(c.get("ejemplo"))})
        return json.dumps({"casos": out})
    except Exception as e:
        return json.dumps({"error": "%s: %s" % (type(e).__name__, e)})

def construir_casos(filas_json):
    """Convierte filas del constructor UI a casos JSON.
    filas_json = [{"expr": "2, 3", "ejemplo": true}, ...]
    Devuelve JSON {"casos": [{"args":[...], "ejemplo":bool}]} o {"error": "..."}."""
    filas = json.loads(filas_json)
    out = []
    for f in filas:
        expr = f.get("expr", "").strip()
        if not expr:
            continue
        try:
            args = eval("[" + expr + "]", {"__builtins__": __builtins__})
        except Exception as e:
            return json.dumps({"error": "Caso '%s': %s" % (expr, e)})
        out.append({"args": args, "ejemplo": bool(f.get("ejemplo"))})
    return json.dumps({"casos": out})

def evaluar(codigo, func, casos_json):
    """Para el SOLVER: corre su código y compara contra los 'esperado' guardados.
    Devuelve JSON {ok:bool, fallos:[{i, args, esperado, obtenido|error}]}."""
    casos = json.loads(casos_json)
    g = {"__name__": "__main__"}
    try:
        exec(codigo, g)
    except Exception as e:
        return json.dumps({"ok": False, "error": "Tu código tiene un error: %s: %s" % (type(e).__name__, e)})
    fn = g.get(func)
    if not callable(fn):
        return json.dumps({"ok": False, "error": "Definí una función llamada '%s'." % func})
    fallos = []
    for i, c in enumerate(casos):
        args = c.get("args", [])
        try:
            obtenido = _norm(fn(*args))
            if obtenido != c.get("esperado"):
                fallos.append({"i": i, "args": args if c.get("ejemplo") else None,
                               "esperado": c.get("esperado") if c.get("ejemplo") else None,
                               "obtenido": obtenido if c.get("ejemplo") else None})
        except Exception as e:
            fallos.append({"i": i, "args": args if c.get("ejemplo") else None,
                           "error": "%s: %s" % (type(e).__name__, e)})
    return json.dumps({"ok": len(fallos) == 0, "fallos": fallos})

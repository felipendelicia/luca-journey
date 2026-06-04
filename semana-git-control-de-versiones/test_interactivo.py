"""
🧪 Tests del Simulador de Git — Semana de Descanso

    pytest semana-git-control-de-versiones/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semanagit_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")
RepoVirtual = interactivo.RepoVirtual
DESAFIOS = interactivo.DESAFIOS


# ----------------------------------------------------------------------
#  init y estado
# ----------------------------------------------------------------------
def test_init():
    r = RepoVirtual()
    assert r.iniciado is False
    r.ejecutar("git init")
    assert r.iniciado is True
    assert r.current_branch == "main"


def test_status_sin_init():
    r = RepoVirtual()
    salida = r.ejecutar("git status")
    assert "no es un repositorio git" in salida


def test_status_archivo_untracked():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch equipo.txt")
    salida = r.ejecutar("git status")
    assert "equipo.txt" in salida
    assert "untracked" in salida.lower()


# ----------------------------------------------------------------------
#  crear archivos
# ----------------------------------------------------------------------
def test_touch_crea_archivo():
    r = RepoVirtual()
    r.ejecutar("touch pikachu.txt")
    assert "pikachu.txt" in r.working


def test_echo_crea_archivo_con_contenido():
    r = RepoVirtual()
    r.ejecutar('echo "Pikachu" > equipo.txt')
    assert r.working["equipo.txt"] == "Pikachu"


# ----------------------------------------------------------------------
#  add y commit
# ----------------------------------------------------------------------
def test_add_prepara_archivo():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch a.txt")
    r.ejecutar("git add a.txt")
    assert "a.txt" in r.staging


def test_add_punto_prepara_todo():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch a.txt")
    r.ejecutar("touch b.txt")
    r.ejecutar("git add .")
    assert "a.txt" in r.staging and "b.txt" in r.staging


def test_commit_crea_commit_y_limpia_staging():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch a.txt")
    r.ejecutar("git add a.txt")
    salida = r.ejecutar('git commit -m "primer commit"')
    assert len(r.commits) == 1
    assert r.commits[0]["msg"] == "primer commit"
    assert r.staging == {}, "El staging debería quedar vacío tras el commit"
    assert "primer commit" in salida


def test_commit_sin_staging_avisa():
    r = RepoVirtual()
    r.ejecutar("git init")
    salida = r.ejecutar('git commit -m "vacio"')
    assert "nada para commitear" in salida


def test_status_limpio_tras_commit():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch a.txt")
    r.ejecutar("git add a.txt")
    r.ejecutar('git commit -m "x"')
    salida = r.ejecutar("git status")
    assert "limpio" in salida


# ----------------------------------------------------------------------
#  log
# ----------------------------------------------------------------------
def test_log_muestra_commits():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch a.txt")
    r.ejecutar("git add .")
    r.ejecutar('git commit -m "mensaje uno"')
    salida = r.ejecutar("git log")
    assert "mensaje uno" in salida


def test_log_oneline():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("touch a.txt")
    r.ejecutar("git add .")
    r.ejecutar('git commit -m "msg"')
    salida = r.ejecutar("git log --oneline")
    assert "msg" in salida


# ----------------------------------------------------------------------
#  branches y switch
# ----------------------------------------------------------------------
def test_branch_crea_rama():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("git branch nueva")
    assert "nueva" in r.branch_tree


def test_switch_cambia_rama():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("git branch nueva")
    r.ejecutar("git switch nueva")
    assert r.current_branch == "nueva"


def test_switch_c_crea_y_cambia():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("git switch -c experimento")
    assert r.current_branch == "experimento"
    assert "experimento" in r.branch_tree


def test_checkout_funciona_igual_que_switch():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("git branch otra")
    r.ejecutar("git checkout otra")
    assert r.current_branch == "otra"


# ----------------------------------------------------------------------
#  Aislamiento entre ramas y merge
# ----------------------------------------------------------------------
def test_commit_en_rama_no_afecta_main():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("git switch -c rama")
    r.ejecutar("touch secreto.txt")
    r.ejecutar("git add .")
    r.ejecutar('git commit -m "secreto"')
    # En main no debería estar.
    r.ejecutar("git switch main")
    assert "secreto.txt" not in r.working
    assert "secreto.txt" not in r.branch_tree["main"]


def test_merge_trae_archivos():
    r = RepoVirtual()
    r.ejecutar("git init")
    r.ejecutar("git switch -c rama")
    r.ejecutar("touch secreto.txt")
    r.ejecutar("git add .")
    r.ejecutar('git commit -m "secreto"')
    r.ejecutar("git switch main")
    r.ejecutar("git merge rama")
    assert "secreto.txt" in r.branch_tree["main"]
    assert "secreto.txt" in r.working


# ----------------------------------------------------------------------
#  Desafíos: recorrido completo
# ----------------------------------------------------------------------
def test_hay_10_desafios():
    assert len(DESAFIOS) >= 10


def test_recorrido_completo():
    r = RepoVirtual()
    soluciones = [
        "git init",
        "touch equipo.txt",
        "git add equipo.txt",
        'git commit -m "primer commit"',
        "git status",
        "touch pokedex.txt",        # parte del desafío 6
        "git add .",                # parte del desafío 6
        'git commit -m "segundo"',  # completa desafío 6
        "git log",
        "git branch nueva-aventura",
        "git switch nueva-aventura",  # parte del desafío 9
        "touch secreto.txt",          # parte del desafío 9
        "git add .",                  # parte del desafío 9
        'git commit -m "secreto"',    # completa desafío 9
        "git switch main",            # parte del desafío 10
        "git merge nueva-aventura",   # completa desafío 10
    ]
    indice = 0
    for cmd in soluciones:
        salida = r.ejecutar(cmd)
        if indice < len(DESAFIOS) and DESAFIOS[indice]["check"](r, salida):
            indice += 1
    assert indice == len(DESAFIOS), (
        f"Se completaron {indice}/{len(DESAFIOS)} desafíos; deberían ser todos"
    )

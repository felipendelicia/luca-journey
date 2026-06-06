import ejercicios


async def af():
    return 1


async def ag():
    return 2


def sf():
    return 3


def sg():
    return 4


def test_tipo():
    assert ejercicios.tipo(af) == "async"
    assert ejercicios.tipo(sf) == "sync"


def test_separar():
    assert ejercicios.separar([af, sf]) == {"async": ["af"], "sync": ["sf"]}


def test_contar():
    assert ejercicios.contar_async([af, sf, ag]) == 2


def test_resumen():
    assert ejercicios.resumen([af, sf, sg]) == "1 async, 2 sync."

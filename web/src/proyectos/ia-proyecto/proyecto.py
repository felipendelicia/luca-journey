# Líder Drayden — Clasificador Pokédex (solución de referencia).
# El preamble (POKEDEX_DATA, POKEDEX_TIPOS, NOMBRES_TIPO) está en meta.json.

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def preparar(X, y):
    return train_test_split(X, y, test_size=0.25, random_state=0)


def entrenar_pokedex(X_train, y_train):
    return KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)


def evaluar_pokedex(modelo, X_test, y_test):
    return accuracy_score(y_test, modelo.predict(X_test))


def identificar_tipo(stats):
    modelo = entrenar_pokedex(POKEDEX_DATA, POKEDEX_TIPOS)
    tipo_id = int(modelo.predict([stats])[0])
    return NOMBRES_TIPO[tipo_id]

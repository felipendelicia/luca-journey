# Integrador de Unova — Pokédex Inteligente (solución de referencia).
# El preamble (POKEMONES, TIPOS, NOMBRES_TIPO) está en meta.json.

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def preparar_pipeline(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test


def entrenar_pipeline(X_train, y_train):
    return KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)


def evaluar_pipeline(modelo, X_test, y_test):
    y_pred = modelo.predict(X_test)
    exactitud = accuracy_score(y_test, y_pred)
    n_correctas = int(sum(y_pred == y_test))
    return exactitud, n_correctas


def predecir_tipo(stats):
    scaler = StandardScaler()
    X_train, _, y_train, _ = train_test_split(POKEMONES, TIPOS, test_size=0.25, random_state=0)
    # Re-fit scaler on all data for full-model prediction
    X_scaled = scaler.fit_transform(POKEMONES)
    modelo = KNeighborsClassifier(n_neighbors=3).fit(X_scaled, TIPOS)
    stats_scaled = scaler.transform([stats])
    tipo_id = int(modelo.predict(stats_scaled)[0])
    return NOMBRES_TIPO[tipo_id]


def pokedex_completa():
    X_train, X_test, y_train, y_test = preparar_pipeline(POKEMONES, TIPOS)
    modelo = entrenar_pipeline(X_train, y_train)
    exactitud, n_correctas = evaluar_pipeline(modelo, X_test, y_test)
    y_pred = modelo.predict(X_test)
    tipos_predichos = [NOMBRES_TIPO[int(t)] for t in y_pred]
    return {
        "exactitud_test": exactitud,
        "n_test": len(y_test),
        "tipos_predichos": tipos_predichos,
    }

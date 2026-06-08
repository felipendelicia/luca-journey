"""✅ Soluciones — ML: evaluar modelos"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def precision(y_real, y_pred):
    return accuracy_score(y_real, y_pred)


def evaluar(X, y):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
    modelo = KNeighborsClassifier(n_neighbors=1).fit(X_tr, y_tr)
    return accuracy_score(y_te, modelo.predict(X_te))


def score_modelo(modelo, X_test, y_test):
    return modelo.score(X_test, y_test)


def cantidad_correctas(y_real, y_pred):
    return int((np.array(y_real) == np.array(y_pred)).sum())


def cantidad_errores(y_real, y_pred):
    return int((np.array(y_real) != np.array(y_pred)).sum())


def tasa_error(y_real, y_pred):
    return float((np.array(y_real) != np.array(y_pred)).mean())


def verdaderos_positivos(y_real, y_pred):
    yr = np.array(y_real)
    yp = np.array(y_pred)
    return int(((yr == 1) & (yp == 1)).sum())


def falsos_positivos(y_real, y_pred):
    yr = np.array(y_real)
    yp = np.array(y_pred)
    return int(((yr == 0) & (yp == 1)).sum())


def falsos_negativos(y_real, y_pred):
    yr = np.array(y_real)
    yp = np.array(y_pred)
    return int(((yr == 1) & (yp == 0)).sum())


def verdaderos_negativos(y_real, y_pred):
    yr = np.array(y_real)
    yp = np.array(y_pred)
    return int(((yr == 0) & (yp == 0)).sum())


def precision_clase1(y_real, y_pred):
    tp = verdaderos_positivos(y_real, y_pred)
    fp = falsos_positivos(y_real, y_pred)
    return tp / (tp + fp)


def recall_clase1(y_real, y_pred):
    tp = verdaderos_positivos(y_real, y_pred)
    fn = falsos_negativos(y_real, y_pred)
    return tp / (tp + fn)


def es_perfecto(y_real, y_pred):
    return bool((np.array(y_real) == np.array(y_pred)).all())


def cantidad_test(n, frac):
    return int(n * frac)


def cantidad_train(n, frac):
    return n - int(n * frac)


def promedio(valores):
    return float(np.array(valores).mean())


def entrenar_knn(X, y, k):
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X, y)
    return m


def dividir_datos(X, y, test_frac, seed):
    return train_test_split(X, y, test_size=test_frac, random_state=seed)


def evaluar_split(X, y, seed):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=seed)
    m = KNeighborsClassifier(n_neighbors=1).fit(X_tr, y_tr)
    return accuracy_score(y_te, m.predict(X_te))


def cantidad_clases(y):
    return len(np.unique(y))

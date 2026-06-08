"""✅ Soluciones — pandas: Limpieza de datos"""
import pandas as pd


def contar_nulos(df):
    return int(df.isna().sum().sum())


def rellenar_ceros(df, col):
    nuevo = df.copy()
    nuevo[col] = nuevo[col].fillna(0)
    return nuevo


def quitar_filas_nulas(df):
    return df.dropna()


def a_entero(serie):
    return serie.astype(int)


def sin_duplicados(df):
    return df.drop_duplicates()


def renombrar(df, viejo, nuevo):
    return df.rename(columns={viejo: nuevo})


def a_mayusculas(serie):
    return serie.str.upper()


def aplicar(serie, funcion):
    return serie.apply(funcion)


def sacar_espacios(serie):
    return serie.str.strip()


def a_minusculas(serie):
    return serie.str.lower()


def reemplazar_valor(serie, viejo, nuevo):
    return serie.replace(viejo, nuevo)


def contar_unicos(serie):
    return int(serie.nunique())


def valores_unicos(serie):
    return sorted(serie.unique().tolist())


def promedio_sin_nulos(serie):
    return serie.mean()


def contar_valor(serie, v):
    return int((serie == v).sum())


def mas_frecuente(serie):
    return serie.mode()[0]


def capitalizar(serie):
    return serie.str.capitalize()


def columnas_con_nulos(df):
    return [c for c in df.columns if df[c].isnull().any()]


def normalizar_texto(serie):
    return serie.str.strip().str.lower()


def longitud_textos(serie):
    return serie.str.len().tolist()

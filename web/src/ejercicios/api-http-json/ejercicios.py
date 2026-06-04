"""
✏️ Ejercicios — APIs: HTTP y JSON

Las APIs hablan en JSON. Acá practicás convertir entre Python y JSON,
y armar respuestas, usando el módulo json.
"""
import json


# 1) Convertí un diccionario de Python a texto JSON. Usá json.dumps.
def a_json(dato):
    """Recibí un dict/list y devolvé su representación en texto JSON (str)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Convertí un texto JSON a un objeto de Python. Usá json.loads.
def de_json(texto):
    """Recibí un str JSON y devolvé el dict/list de Python."""
    # TU CÓDIGO ACÁ
    pass


# 3) Recibí el texto JSON de un Pokémon y devolvé su 'nombre'.
def extraer_nombre(texto):
    """texto es algo como '{"nombre": "Pikachu", "nivel": 25}'. Devolvé el nombre."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé True si el código de estado HTTP es de éxito (200 a 299).
def es_exito(status):
    """Para 200 o 201 devolvé True; para 404 o 500 devolvé False."""
    # TU CÓDIGO ACÁ
    pass


# 5) Armá la respuesta de la API: un dict con 'nombre' y 'nivel'.
def armar_respuesta(nombre, nivel):
    """Devolvé {"nombre": nombre, "nivel": nivel}."""
    # TU CÓDIGO ACÁ
    pass


# 6) Recibí el JSON de una LISTA de Pokémon y devolvé la lista de nombres.
def nombres(texto):
    """texto es un JSON como '[{"nombre":"Pikachu"}, {"nombre":"Eevee"}]'.
    Devolvé ['Pikachu', 'Eevee']."""
    # TU CÓDIGO ACÁ
    pass


# 7) Recibí el JSON de una lista de Pokémon (con 'nivel') y devolvé la suma de niveles.
def total_niveles(texto):
    """Sumá el 'nivel' de cada Pokémon de la lista."""
    # TU CÓDIGO ACÁ
    pass

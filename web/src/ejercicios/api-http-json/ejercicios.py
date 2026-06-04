"""✏️ Ejercicios — APIs: HTTP y JSON

Las APIs hablan en JSON. Practicás convertir entre Python y JSON y armar respuestas,
usando el módulo json. ✅ Corregir al terminar.
"""
import json


# Dict a JSON
# Convertí un diccionario (o lista) de Python a texto JSON. Pista: json.dumps.
# Ejemplo:  a_json({"nombre": "Pikachu"})  →  '{"nombre": "Pikachu"}'
def a_json(dato):
    """Devolvé el dato como texto JSON (str)."""
    # TU CÓDIGO ACÁ
    pass


# JSON a objeto
# Convertí un texto JSON a un objeto de Python. Pista: json.loads.
# Ejemplo:  de_json('{"nivel": 25}')  →  {"nivel": 25}
def de_json(texto):
    """Devolvé el dict/list de Python a partir del JSON."""
    # TU CÓDIGO ACÁ
    pass


# Extraer el nombre
# Recibís el JSON de un Pokémon y devolvés su 'nombre'.
# Ejemplo:  extraer_nombre('{"nombre": "Pikachu", "nivel": 25}')  →  "Pikachu"
def extraer_nombre(texto):
    """Devolvé el 'nombre' del Pokémon del JSON."""
    # TU CÓDIGO ACÁ
    pass


# ¿Respuesta exitosa?
# Devolvé True si el código de estado HTTP es de éxito (entre 200 y 299).
# Ejemplo:  es_exito(200)  →  True   ·   es_exito(404)  →  False
def es_exito(status):
    """Devolvé True si status está entre 200 y 299."""
    # TU CÓDIGO ACÁ
    pass


# Armar la respuesta
# Devolvé un diccionario con 'nombre' y 'nivel'.
# Ejemplo:  armar_respuesta("Pikachu", 25)  →  {"nombre": "Pikachu", "nivel": 25}
def armar_respuesta(nombre, nivel):
    """Devolvé {"nombre": nombre, "nivel": nivel}."""
    # TU CÓDIGO ACÁ
    pass


# Lista de nombres
# Recibís el JSON de una LISTA de Pokémon y devolvés solo sus nombres.
# Ejemplo:  nombres('[{"nombre":"Pikachu"}, {"nombre":"Eevee"}]')  →  ["Pikachu", "Eevee"]
def nombres(texto):
    """Devolvé la lista de nombres de los Pokémon del JSON."""
    # TU CÓDIGO ACÁ
    pass


# Sumar niveles
# Recibís el JSON de una lista de Pokémon (con 'nivel') y devolvés la suma de los niveles.
# Ejemplo:  total_niveles('[{"nivel":10}, {"nivel":20}]')  →  30
def total_niveles(texto):
    """Sumá el 'nivel' de cada Pokémon de la lista."""
    # TU CÓDIGO ACÁ
    pass

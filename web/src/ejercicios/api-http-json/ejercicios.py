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


# JSON con indentación
# Convertí el dato a JSON "lindo", con indentación de 2 espacios. Pista: json.dumps(dato, indent=2).
def con_indentacion(dato):
    """Devolvé el dato como JSON con indent=2."""
    # TU CÓDIGO ACÁ
    pass


# Claves del JSON
# Recibís un texto JSON de un objeto. Devolvé la lista de sus claves.
# Ejemplo:  claves_json('{"nombre": "Pika", "nivel": 25}')  →  ["nombre", "nivel"]
def claves_json(texto):
    """Devolvé las claves del JSON."""
    # TU CÓDIGO ACÁ
    pass


# Valor de una clave
# Devolvé el valor de `clave` en el JSON, o None si no está.
def valor_de(texto, clave):
    """Devolvé el valor de clave, o None."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de items
# Recibís un texto JSON de una LISTA. Devolvé cuántos elementos tiene.
# Ejemplo:  cantidad_items("[1, 2, 3]")  →  3
def cantidad_items(texto):
    """Devolvé cuántos items tiene el JSON."""
    # TU CÓDIGO ACÁ
    pass


# Agregar un campo
# Parseá el JSON (un objeto), agregale `clave`=`valor`, y devolvelo de nuevo como texto JSON.
# Ejemplo:  agregar_campo('{"a": 1}', "b", 2)  →  '{"a": 1, "b": 2}'
def agregar_campo(texto, clave, valor):
    """Devolvé el JSON con un campo agregado."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es JSON válido?
# Devolvé True si el texto se puede parsear como JSON, False si no.
def es_json_valido(texto):
    """Devolvé True si el texto es JSON válido."""
    # TU CÓDIGO ACÁ
    pass


# Ordenar las claves
# Convertí el dato a JSON con las claves ORDENADAS alfabéticamente. Pista: sort_keys=True.
# Ejemplo:  ordenar_claves({"b": 2, "a": 1})  →  '{"a": 1, "b": 2}'
def ordenar_claves(dato):
    """Devolvé el JSON con las claves ordenadas."""
    # TU CÓDIGO ACÁ
    pass


# Fusionar dos JSON
# Recibís dos textos JSON de objetos. Devolvé un JSON que combine ambos (si una clave está en
# los dos, gana el segundo).
# Ejemplo:  fusionar_json('{"a": 1}', '{"b": 2}')  →  '{"a": 1, "b": 2}'
def fusionar_json(a, b):
    """Devolvé un JSON con a y b combinados."""
    # TU CÓDIGO ACÁ
    pass


# Extraer un campo de cada item
# Recibís un JSON de una lista de objetos. Devolvé la lista de valores del campo `campo`.
# Ejemplo:  extraer_campo('[{"n": "a"}, {"n": "b"}]', "n")  →  ["a", "b"]
def extraer_campo(texto, campo):
    """Devolvé el valor de `campo` de cada item."""
    # TU CÓDIGO ACÁ
    pass


# ¿Código de éxito?
# Devolvé True si `status` está entre 200 y 299.
def es_codigo_exito(status):
    """Devolvé True si status es 2xx."""
    # TU CÓDIGO ACÁ
    pass


# ¿Código de error?
# Devolvé True si `status` es 400 o más.
def es_codigo_error(status):
    """Devolvé True si status es >= 400."""
    # TU CÓDIGO ACÁ
    pass


# Clase del status
# Devolvé "exito" (2xx), "redireccion" (3xx), "cliente" (4xx) o "servidor" (5xx).
# Ejemplo:  clase_status(404)  →  "cliente"
def clase_status(status):
    """Devolvé la clase del código HTTP."""
    # TU CÓDIGO ACÁ
    pass


# Contar JSON válidos
# Recibís una lista de textos. Devolvé cuántos son JSON válidos.
def contar_validos(textos):
    """Devolvé cuántos textos son JSON válido."""
    # TU CÓDIGO ACÁ
    pass

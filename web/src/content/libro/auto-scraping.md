---
title: "Automatización: Scraping (extraer datos)"
order: 1006
---

> 🎯 **Meta:** bajar una página web y **extraerle los datos** que te importan.

---

**Scraping** es automatizar la lectura de páginas web: bajás el HTML y le sacás los datos (precios, títulos, tablas). Tiene dos partes: **bajar** la página y **extraer** los datos.

## Bajar la página (con internet)

Bajar el HTML se hace con la librería **`requests`**:

```python
import requests

respuesta = requests.get("https://pokeapi.co/api/v2/pokemon/25")
print(respuesta.status_code)   # 200 = OK
datos = respuesta.json()       # si la respuesta es JSON
print(datos["name"])           # "pikachu"
```

> 🌐 **Ojo:** `requests` necesita acceso de red real, así que **no corre acá en el navegador**. En tu compu (`pip install requests`) anda perfecto. Lo que practicás en los ejercicios es la otra mitad, la que SÍ podemos probar: **extraer** datos de un HTML ya bajado.

## Extraer con expresiones regulares

Una página es texto, y las **expresiones regulares** (`re`) encuentran patrones dentro del texto.

```python
import re

html = '<a href="/kanto">Kanto</a> <a href="/johto">Johto</a>'

# todos los enlaces (lo que está dentro de href="...")
enlaces = re.findall(r'href="([^"]+)"', html)
print(enlaces)            # ["/kanto", "/johto"]

# todos los números
print(re.findall(r"\d+", "nivel 30, hp 100"))   # ["30", "100"]
```

Patrones útiles para scraping:

- `re.findall(patrón, texto)` → lista con TODO lo que coincide.
- `(...)` → un **grupo**: lo que querés capturar.
- `.*?` → "cualquier cosa, lo más corto posible" (para contenido entre etiquetas).
- `re.sub(patrón, "", texto)` → borra lo que coincide (ej. sacar etiquetas).

```python
import re
print(re.findall(r"<li>(.*?)</li>", "<li>Rayo</li><li>Placaje</li>"))  # ["Rayo", "Placaje"]
print(re.sub(r"<[^>]+>", "", "<b>Hola</b> mundo"))                      # "Hola mundo"
```

> 💡 Para HTML real y complejo se usa **BeautifulSoup**, que entiende la estructura. Pero entender `re` te da la base para extraer datos de cualquier texto.

## ✅ Comprobá lo que aprendiste

```quiz
P: La parte de "bajar" la página (con `requests`)…
+ necesita acceso a internet (no corre acá en el navegador)
- se hace solo con el módulo `re`
- no hace falta nunca
> Bajar usa `requests` con red real; lo que practicás acá es extraer datos de un HTML ya bajado.
```

```quiz
P: `re.findall(r"\d+", texto)` encuentra…
+ todos los grupos de dígitos del texto
- solo el primer número
- las letras
> `findall` devuelve todas las coincidencias; `\d+` son secuencias de dígitos.
```

🕸️ La **Capitana Mina** te espera para extraer fichas de Pokémon del HTML.

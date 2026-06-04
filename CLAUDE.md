# Instrucciones del proyecto — Curso de Python con Pokémon

Curso de programación (Linux + Python) para un adolescente principiante, en
español argentino y con temática Pokémon. Incluye un sistema de gamificación
llamado **La Liga Pokémon** (`aventura.py`).

## 📘 REGLA PRINCIPAL: mantené el manual/libro actualizado

El proyecto tiene un **libro-manual** en la raíz, en dos formatos:
`manual.html` (para el navegador, con emojis a color) y `manual.pdf`. Es a la vez
el manual del curso **y** un libro de Python para aprender el lenguaje.

- **NO se editan `manual.html` ni `manual.pdf` a mano.** Se generan.
- El **contenido** está en `manual_contenido.py` (capítulos escritos en **HTML**).
- Los **estilos y herramientas** (CSS, cajas, resaltado de código) están en `manual_lib.py`.
- Para regenerar ambos: `python generar_manual.py`
  (usa **WeasyPrint** para el PDF y **Pygments** para resaltar el código;
  si falta WeasyPrint, prueba con Chrome headless o LibreOffice).
- Dependencias de mantenimiento (no las necesita el alumno):
  `pip install weasyprint pygments`.

**Siempre que cambie el proyecto de una forma que afecte cómo se usa o qué
contiene, actualizá `manual_contenido.py` y regenerá el manual.** Por ejemplo:

- Agregar / quitar / renombrar una semana o un tema (actualizá el cap. "Mapa de temas").
- Cambiar la estructura de carpetas o los archivos de cada semana.
- Cambiar cómo se instala o se corre el curso (`setup.sh`, comandos).
- Cambiar la Liga Pokémon (`aventura.py`): EXP, medallas, logros, menús.
- Agregar / cambiar un proyecto en `proyectos/`.
- Mejorar o ampliar la parte de enseñanza de Python (capítulos 1 a 14).

El libro tiene un **índice automático** y una sección "Mapa de temas del curso":
mantené ese mapa sincronizado con las semanas reales.

Después de regenerar, **commiteá `manual_contenido.py`, `manual_lib.py`,
`manual.html` y `manual.pdf` juntos**.

## 🔁 Coherencia general

Cuando cambies contenido del curso, revisá que sigan coherentes:

- `README.md` — presentación y tabla de semanas.
- `ROADMAP.md` — mapa visual y checklist de progreso.
- `liga/datos.py` — registro de semanas y gimnasios de la Liga.
- `manual_contenido.py` → `manual.html` + `manual.pdf` — el libro-manual.

## ✅ Tests

Antes de dar por terminado un cambio, corré `pytest` desde la raíz y dejá todo
en verde. Los tests de cada semana prueban `soluciones.py` por defecto; la Liga
los corre contra `ejercicios.py` con la variable `CURSO_MODULO=ejercicios`.

## 🧱 Convenciones técnicas

- `pytest.ini` usa `--import-mode=importlib` para permitir nombres de archivo
  repetidos entre semanas (`interactivo.py`, `test_ejercicios.py`, etc.).
- Los paquetes (semanas 11-12, proyectos, `liga/`) usan **nombres únicos** para
  no chocar al importar (`agenda`, `agenda_entrenador`, `pokedex_web`,
  `pokedex_app`, `liga`, etc.). Mantené esa unicidad si agregás paquetes.
- Archivos generados (no versionar, ya están en `.gitignore`): `venv/`,
  `__pycache__/`, `progreso.json`, `*.db`. **Excepción:** `manual.pdf` SÍ se versiona.

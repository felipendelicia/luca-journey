# Instrucciones del proyecto — Curso de Python con Pokémon

Curso de programación (Linux + Python) para un adolescente principiante, en
español argentino y con temática Pokémon. Incluye un sistema de gamificación
llamado **La Liga Pokémon** (`aventura.py`).

## 📘 REGLA PRINCIPAL: mantené el manual actualizado

El proyecto tiene un **manual para novatos** en la raíz: `manual.pdf`.

- **NO se edita a mano.** El PDF se genera desde `manual_fuente.md` (Markdown).
- Para regenerarlo: `python generar_manual.py` (usa LibreOffice).

**Siempre que cambie el proyecto de una forma que afecte cómo se usa o qué
contiene, actualizá `manual_fuente.md` y regenerá `manual.pdf`.** Por ejemplo:

- Agregar / quitar / renombrar una semana o un tema.
- Cambiar la estructura de carpetas o los archivos de cada semana.
- Cambiar cómo se instala o se corre el curso (`setup.sh`, comandos).
- Cambiar la Liga Pokémon (`aventura.py`): EXP, medallas, logros, menús.
- Agregar / cambiar un proyecto en `proyectos/`.

El manual tiene un **índice de todos los temas** (sección "Mapa de temas"):
mantenelo sincronizado con las semanas reales del curso.

Después de regenerar, **commiteá `manual_fuente.md` y `manual.pdf` juntos**.

## 🔁 Coherencia general

Cuando cambies contenido del curso, revisá que sigan coherentes:

- `README.md` — presentación y tabla de semanas.
- `ROADMAP.md` — mapa visual y checklist de progreso.
- `liga/datos.py` — registro de semanas y gimnasios de la Liga.
- `manual_fuente.md` + `manual.pdf` — el manual.

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

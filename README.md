# 🔴⚪ Curso de Programación y Linux con Pokémon 🐍

[![tests](https://github.com/felipendelicia/luca-journey/actions/workflows/tests.yml/badge.svg)](https://github.com/felipendelicia/luca-journey/actions/workflows/tests.yml)
[![📖 libro online](https://img.shields.io/badge/%F0%9F%93%96_libro-online-e3350d)](https://felipendelicia.github.io/luca-journey/)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-WSL-FCC624?logo=linux&logoColor=black)
![license](https://img.shields.io/badge/license-MIT-green)

```
                ___________
           ,-~""           ""~-,
        ,-"                      "-,
      ,"                            ",
    ,"                                ",
   /                                    \
  /              ___________             \
 /            ,-"           "-,           \
,            /     _______     \           ,
|           |    ,"       ",    |          |
|___________|___|___________|___|__________|
|           |   |           |   |          |
'           |    ".       ,"    |          '
 \           \     "-_____-"    /          /
  \           "-,           ,-"           /
   \             "-,_____,-"             /
    ",                                  ,"
      ",                              ,"
        "-,                        ,-"
           "~-,__              __,-"
                ""~----------~""
```

> **¡Hola, futuro Maestro Pokémon!** 👋
> Este es tu viaje de 12 semanas para convertirte en programador. Vas a aprender **Linux** y **Python** desde cero, todo con temática Pokémon. Sin vueltas, paso a paso, atrapándolos a todos (los conceptos). ¡Arrancamos!

---

## 🎯 ¿De qué se trata?

Un curso completo, pensado para alguien que **nunca programó**. Empezás dominando la terminal de Linux (tu Pokédex del sistema) y terminás construyendo una **aplicación web con Flask**.

Cada concepto se explica con una **analogía Pokémon**, cada ejercicio usa Pokémon, y cada proyecto es algo que un Entrenador usaría de verdad.

| | |
|---|---|
| 🗣️ **Idioma** | Español (argentino, con *vos* y *che*) |
| 🎮 **Temática** | Pokémon en todo |
| 🧑‍🎓 **Nivel** | Principiante absoluto |
| ⏳ **Duración** | 12 semanas |
| 🐍 **Python** | 3.10 o superior |
| 🐧 **Sistema** | Linux o WSL (Windows Subsystem for Linux) |

---

## 📋 Requisitos

- **Python 3.10+** instalado (la semana 3 te enseña a verificarlo).
- **Linux** nativo, o **WSL** si estás en Windows (la semana 1 te explica todo).
- Ganas de aprender. Nada más. 💪

---

## 🚀 Instalación

1. **Cloná o descargá** este repositorio:
   ```bash
   git clone <url-del-repo>
   cd <carpeta-del-repo>
   ```

2. **Corré el script de setup** (crea el entorno virtual e instala todo):
   ```bash
   bash setup.sh
   ```

3. **Activá el entorno virtual** cada vez que trabajes:
   ```bash
   source venv/bin/activate
   ```

4. Cuando termines de trabajar, lo desactivás con:
   ```bash
   deactivate
   ```

> 💡 Si el `setup.sh` te tira error, no entres en pánico. Abrí el archivo, está comentado línea por línea. Las primeras dos semanas son de Linux y no necesitan Python instalado para los ejercicios de terminal.

---

## 🗺️ Las 12 semanas

| Semana | Tema | Qué vas a aprender | Proyecto interactivo |
|:------:|------|--------------------|----------------------|
| **01** | 🐧 Linux: Fundamentos | Terminal, navegación, comandos básicos, rutas, permisos | Simulador de terminal Pokémon |
| **02** | 🐧 Linux: Intermedio | nano, variables, scripts bash, pipes, grep, procesos, SSH | Constructor de scripts bash |
| **03** | 🐍 Python: Introducción | Variables, tipos, `print()`, `input()`, f-strings | Registro de Entrenador (tarjeta ASCII) |
| **04** | 🐍 Control de Flujo | `if`/`elif`/`else`, `while`, `for`, `range()`, lógica | Simulador de batalla por turnos |
| **05** | 🐍 Funciones | `def`, parámetros, `return`, scope, lambda, recursión | Calculadora de stats Pokémon |
| **06** | 🐍 Listas y Colecciones | Listas, tuplas, sets, diccionarios, comprensiones | Gestor de equipo Pokémon |
| **07** | 🐍 Cadenas y Archivos | Strings, `open()`, CSV, `try`/`except` | Pokédex con persistencia |
| **🔀** | 😌 **Descanso: Git** | `init`, `commit`, `branch`, `merge`, GitHub | Simulador de Git |
| **08** | 🐍 POO: Introducción | Clases, `__init__`, atributos, métodos, `self` | Creador de Pokémon personalizado |
| **09** | 🐍 POO: Avanzado | Herencia, polimorfismo, `@property`, clases abstractas | Sistema de tipos Pokémon |
| **10** | 🐍 Módulos y pip | `import`, módulos estándar, `pip`, `venv`, `requests` | Pokédex online (PokéAPI) |
| **11** | 🛠️ Proyecto Integrador | App de consola completa y modular | Agenda del Entrenador |
| **12** | 🌐 Proyecto Final | Web app con Flask + PokéAPI | Pokédex Web |

> 😌 La **semana de descanso de Git** está pensada para hacerse después de la semana 7, como un respiro entre tanto Python. ¡Pero podés hacerla cuando quieras!

---

## 🏆 La Liga Pokémon — ¡jugá tu progreso!

> **Esta es la mejor forma de hacer el curso.** En vez de "hacer la tarea", **subís de nivel**.

```bash
python aventura.py
```

La **Liga Pokémon** convierte todo el curso en un juego con un objetivo: **ser Campeón de Kanto**. 🥇

- 🎮 **Elegís el capítulo que querés jugar** (lanza su juego interactivo). Si tenés progreso, **continuás donde lo dejaste**; si lo completaste, lo **reintentás**.
- 🏋️ **Entrenás** una semana: la Liga corre **tus** ejercicios y te da **EXP** por cada test que pasás. Si algo falla, te dice **qué ejercicio** y una pista.
- ⚔️ **Combates de gimnasio**: con una medalla, retás al líder con un desafío integrador más difícil.
- 🎴 **Tarjeta de Entrenador** con tu nivel, EXP y rango. 🆙 **Subís de nivel**.
- 🏅 **8 medallas de gimnasio** (Roca, Cascada, Trueno...) y ✨ **logros** desbloqueables.
- 🔥 **Racha diaria**, 🗺️ **mapa de la región** y 🔀 **misión bonus de Git**.

Tu progreso se guarda solo en `progreso.json`. **Es la forma recomendada de avanzar:** abrís `aventura.py`, ves qué semana toca, hacés los ejercicios de esa carpeta, y volvés a "Entrenar" para cobrar tu EXP. 🎮

---

## 📁 ¿Qué hay en cada semana?

Cada carpeta de semana tiene (según corresponda):

- 📖 **`teoria.md`** — La explicación del tema, con analogía Pokémon, ejemplos progresivos y un resumen.
- ✏️ **`ejercicios.py`** o **`ejercicios.md`** — Los desafíos para practicar (con instrucciones claras).
- ✅ **`soluciones.py`** o **`soluciones.md`** — Las respuestas, comentadas línea por línea.
- 🧪 **`test_ejercicios.py`** — Tests con `pytest` para verificar que tus soluciones funcionan.
- 🎮 **`interactivo.py`** — Un programa jugable que aplica lo aprendido.

---

## 🧪 Cómo correr los tests

Los tests te dicen si tus ejercicios están bien resueltos. Usamos **pytest**.

**Correr TODOS los tests del curso:**
```bash
pytest
```

**Correr los tests de una semana específica:**
```bash
pytest semana-04-python-control-de-flujo/
```

**Correr un archivo de test puntual, mostrando todo el detalle:**
```bash
pytest semana-05-python-funciones/test_ejercicios.py -v
```

> 🟢 Verde = aprobado. 🔴 Rojo = revisá tu solución. Los mensajes de error están en español para ayudarte.

---

## 🎮 Cómo usar los interactivos

Los archivos `interactivo.py` son programas para jugar y aprender. Se corren así:

```bash
python semana-03-python-introduccion/interactivo.py
```

(En algunos sistemas el comando es `python3` en vez de `python`.)

---

## 🧭 ¿Por dónde empezar?

1. 📦 Corré `bash setup.sh` para preparar todo.
2. 🏆 Abrí la **Liga Pokémon** con `python aventura.py` — es tu centro de mando.
3. 📖 Andá a `semana-01-linux-fundamentos/` y abrí `teoria.md`. Leelo con calma.
4. ✏️ Hacé los ejercicios (`ejercicios.md` o `ejercicios.py`).
5. 🎮 Jugá el `interactivo.py` de la semana para reforzar.
6. 🏋️ Volvé a `python aventura.py` y elegí **Entrenar** esa semana para ganar **EXP** y medallas.
7. ➡️ Pasá a la siguiente semana. **No saltees semanas**, cada una usa lo anterior.
8. 😌 Cuando quieras relajar, hacé la **semana de descanso de Git**.
9. 🏆 Al final, construí los proyectos de la carpeta `proyectos/` y convertite en Campeón.

> **Regla de oro:** no hace falta entender todo de una. Programar es practicar. Equivocarse es parte del juego. ¡Dale para adelante, Entrenador! 🔥

---

## 📚 Más recursos

- 📘 **Leé el libro del curso online:** [Python con Pokémon](https://felipendelicia.github.io/luca-journey/) — un libro completo que enseña Linux y Python desde cero, con modo oscuro, buscador y ejercicios resueltos (también en PDF: [`manual/manual.pdf`](manual/manual.pdf)).
- 📚 **Bibliografía recomendada online:** [recursos y enlaces útiles](https://felipendelicia.github.io/luca-journey/recursos.html).
- 🗺️ Mirá el [ROADMAP.md](ROADMAP.md) para ver el mapa completo del viaje.
- 🔗 Revisá [recursos.md](recursos.md) para links de documentación, la PokéAPI y videos recomendados.

---

¡Que tengas un gran viaje! Acordate: **el mejor momento para empezar a programar fue ayer. El segundo mejor momento es ahora.** ⚡

```
        ¡A ATRAPARLOS A TODOS! 🔴⚪
```

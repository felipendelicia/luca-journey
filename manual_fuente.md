<h1 class="portada">📘 Manual del Curso<br>🔴⚪ Python con Pokémon</h1>

<p style="text-align:center; font-size:13pt; color:#555;">
Guía completa para novatos · Aprendé Linux y Python desde cero<br>
Conviértete en Campeón de Kanto programando 🏆
</p>

<p style="text-align:center; color:#888;">
Este manual se genera desde <code>manual_fuente.md</code> con <code>python generar_manual.py</code>.
</p>

---

**Índice de contenidos**

[TOC]

---

# 1. ¿Qué es este proyecto?

Este es un **curso completo de programación** pensado para alguien que **nunca programó**. Está todo en español y con temática **Pokémon**: cada concepto se explica con una analogía Pokémon, cada ejercicio usa Pokémon, y cada proyecto es algo que un Entrenador usaría.

En **12 semanas** (más una semana de descanso de Git) vas a pasar de no saber nada, a:

- Manejar la **terminal de Linux** como un experto.
- Programar en **Python** desde lo más básico hasta objetos y módulos.
- Construir **aplicaciones reales**: una agenda, una Pokédex de consola, ¡y hasta una página web!

Y lo más importante: **todo es un juego**. Hay un sistema llamado **La Liga Pokémon** que convierte el aprendizaje en una aventura con niveles, EXP y medallas (más sobre esto en la sección 3).

> 💡 **¿Para quién es este manual?** Para vos, que estás empezando. No hace falta saber NADA de antes. Vamos paso a paso.

---

# 2. Antes de empezar

## 2.1. Qué necesitás

| Necesitás | Detalle |
|-----------|---------|
| 🐍 **Python 3.10 o superior** | El lenguaje que vamos a aprender. La semana 3 te enseña a verificarlo. |
| 🐧 **Linux o WSL** | Si estás en Windows, instalá WSL (la semana 1 lo explica). En Mac, la terminal sirve igual. |
| 💪 **Ganas de aprender** | Nada más. En serio. |

## 2.2. Instalación paso a paso

1. **Descargá o cloná** el proyecto a tu computadora.

2. **Abrí una terminal** dentro de la carpeta del proyecto.

3. **Corré el script de preparación**. Crea un "entorno virtual" e instala lo necesario:

   ```bash
   bash setup.sh
   ```

4. **Activá el entorno** cada vez que vayas a trabajar:

   ```bash
   source venv/bin/activate
   ```

5. Cuando termines, lo desactivás con:

   ```bash
   deactivate
   ```

> ⚠️ Si `setup.sh` te da un error, no entres en pánico. Abrilo con un editor: está comentado línea por línea. Las primeras dos semanas son de Linux y no necesitan Python para los ejercicios de terminal.

---

# 3. La Liga Pokémon (¡la mejor forma de usar el curso!)

En vez de sentir que "hacés la tarea", vas a **subir de nivel**. La **Liga Pokémon** es un programa que convierte todo el curso en un videojuego.

## 3.1. Cómo se juega

Desde la carpeta del proyecto, escribí:

```bash
python aventura.py
```

Se abre tu **centro de mando**. Desde ahí podés:

- 🎴 Ver tu **Tarjeta de Entrenador** (tu nombre, nivel, EXP y rango).
- 🏋️ **Entrenar** una semana: la Liga corre **tus** ejercicios y te da **EXP** por cada test que pasás.
- 🗺️ Ver el **mapa de la región** y tu avance.
- 🏅 Ver tus **medallas** y ✨ **logros**.

## 3.2. Cómo funciona la EXP y los niveles

- Cada test que pasás suma **EXP** (puntos de experiencia).
- Cuando completás una semana entera, ganás un **bonus**.
- Con suficiente EXP, **subís de nivel** (como un Pokémon).

## 3.3. Las 8 medallas de gimnasio

Igual que en los juegos, hay **8 medallas** que ganás al completar grupos de semanas:

| Medalla | Líder | Cómo se gana |
|---------|-------|--------------|
| 🪨 Roca | Brock | Completar las semanas 1 y 2 (Linux) |
| 💧 Cascada | Misty | Semanas 3 y 4 |
| ⚡ Trueno | Tnte. Surge | Semanas 5 y 6 |
| 🌈 Arcoíris | Erika | Semana 7 |
| 💜 Alma | Koga | Semanas 8 y 9 |
| 🔮 Pantano | Sabrina | Semana 10 |
| 🌋 Volcán | Blaine | Semana 11 |
| 🌍 Tierra | Giovanni | Semana 12 |

Cuando tenés las 8, **¡sos Campeón de Kanto!** 🏆

## 3.4. Logros y racha

- **Logros**: se desbloquean por hitos (tu primer test, completar una semana, etc.).
- **Racha** 🔥: si entrenás días seguidos, tu racha crece. ¡No la cortes!

Tu progreso se guarda solo en un archivo `progreso.json`. La próxima vez que abras `aventura.py`, sigue donde lo dejaste.

---

# 4. Cómo está organizado el proyecto

```
(raíz del proyecto)
├── README.md            ← presentación general
├── ROADMAP.md           ← mapa visual del viaje
├── manual.pdf           ← este manual
├── recursos.md          ← links útiles
├── setup.sh             ← prepara el entorno
├── aventura.py          ← 🏆 LA LIGA POKÉMON (empezá por acá)
├── liga/                ← el código de la Liga
├── semana-01-... a semana-12-...   ← las 12 semanas
├── semana-git-...       ← la semana de descanso de Git
└── proyectos/           ← los 4 proyectos finales
```

Cada carpeta de semana contiene (según corresponda):

- 📖 **`teoria.md`** — La explicación del tema, con analogía Pokémon y ejemplos.
- ✏️ **`ejercicios.py`** o **`ejercicios.md`** — Los desafíos para practicar.
- ✅ **`soluciones.py`** o **`soluciones.md`** — Las respuestas, comentadas línea por línea.
- 🧪 **`test_ejercicios.py`** — Tests que verifican tus soluciones.
- 🎮 **`interactivo.py`** — Un programa jugable que aplica el tema.

---

# 5. Cómo trabajar cada semana (el método)

Seguí siempre estos pasos. **No saltees semanas**: cada una usa lo anterior.

1. 📖 **Leé** el `teoria.md` de la semana, con calma. No hace falta entender todo de una.
2. ✏️ **Resolvé** los ejercicios. En los `.py`, escribí tu código donde dice `# TU CÓDIGO ACÁ`.
3. 🧪 **Probá** tus soluciones corriendo los tests (ver sección 8).
4. 🎮 **Jugá** el `interactivo.py` para reforzar de forma divertida.
5. 🏋️ **Entrená** esa semana en la Liga (`python aventura.py`) para ganar EXP y medallas.
6. ➡️ **Pasá** a la siguiente semana.

> 💡 **Regla de oro:** equivocarse es parte del juego. Cada error es EXP. Escribí el código vos mismo, no copies y pegues: tipear te enseña.

---

# 6. Mapa de temas (índice completo)

Esta es la lista de **todos los temas** que vas a aprender, semana por semana.

## 6.1. Fase 1 — Linux 🐧

**Semana 01 — Linux: Fundamentos**
: Qué es Linux · la terminal · navegación de archivos · comandos `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`, `cat`, `echo` · rutas absolutas y relativas · permisos básicos.

**Semana 02 — Linux: Intermedio**
: Editor `nano` · variables de entorno · scripts bash · redirección (`>`, `>>`) · pipes (`|`) · `grep` · `find` · procesos (`ps`, `kill`) · `chmod` · usuarios y permisos · `apt` · introducción a SSH.

## 6.2. Fase 2 — Python básico 🐍

**Semana 03 — Python: Introducción**
: Qué es Python · el REPL · `print()` · variables · tipos de datos (int, float, str, bool) · `input()` · conversión de tipos · comentarios · f-strings.

**Semana 04 — Control de Flujo**
: `if` / `elif` / `else` · operadores de comparación · operadores lógicos (`and`, `or`, `not`) · `while` · `for` · `range()` · `break` · `continue`.

**Semana 05 — Funciones**
: `def` · parámetros · valores por defecto · `return` · scope (alcance) · funciones `lambda` · docstrings · recursión básica.

**Semana 06 — Listas y Colecciones**
: Listas · tuplas · sets · diccionarios · comprensiones de listas · métodos de listas · iteración · `enumerate` · `zip`.

**Semana 07 — Cadenas y Archivos**
: Métodos de strings · slicing · `open()` · lectura y escritura de archivos · `with` · CSV · manejo de excepciones (`try` / `except`).

## 6.3. Descanso — Git 🔀

**Semana de descanso — Git: Control de Versiones**
: Qué es Git · `git init` · `git status` · `git add` · `git commit` · `git log` · ramas (`branch`, `switch`, `merge`) · GitHub · `push` / `pull` / `clone` · `.gitignore`.

## 6.4. Fase 3 — Python avanzado 🧬

**Semana 08 — POO: Introducción**
: Clases · instancias · `__init__` · atributos · métodos · `self` · `__str__` · `__repr__` · encapsulamiento básico.

**Semana 09 — POO: Avanzado**
: Herencia · `super()` · polimorfismo · métodos de clase y estáticos · propiedades con `@property` · clases abstractas con `abc`.

**Semana 10 — Módulos y pip**
: `import` · módulos estándar (`os`, `sys`, `math`, `random`, `datetime`, `json`) · crear módulos propios · `pip` · `venv` · `requirements.txt` · introducción a `requests`.

## 6.5. Fase 4 — Proyectos 🏆

**Semana 11 — Proyecto Integrador: Agenda del Entrenador**
: App de consola completa y **modular** · registro de capturas · equipo activo · historial de batallas · estadísticas · persistencia en JSON · organización en módulos · tests.

**Semana 12 — Proyecto Final: Pokédex Web**
: Aplicación web con **Flask** · página principal · formulario · página de detalle · integración con la PokéAPI · persistencia · plantillas HTML + CSS · tests con el cliente de Flask.

---

# 7. Los interactivos

Los archivos `interactivo.py` son **programas para jugar y aprender**. Se corren así:

```bash
python semana-03-python-introduccion/interactivo.py
```

Algunos ejemplos:

- Semana 01: un **simulador de terminal** Pokémon con desafíos.
- Semana 04: un **simulador de batalla por turnos**.
- Semana 06: un **gestor de equipo** Pokémon.
- Semana 10: una **Pokédex online** que trae datos reales de internet.

> 💡 En algunos sistemas el comando es `python3` en vez de `python`.

---

# 8. Cómo correr los tests

Los **tests** te dicen si tus ejercicios están bien resueltos. Usamos una herramienta llamada **pytest**.

**Correr TODOS los tests del curso:**

```bash
pytest
```

**Correr los de una semana específica:**

```bash
pytest semana-04-python-control-de-flujo/
```

**Correr un archivo puntual con todo el detalle:**

```bash
pytest semana-05-python-funciones/test_ejercicios.py -v
```

> 🟢 **Verde = aprobado.** 🔴 **Rojo = revisá tu solución.** Los mensajes de error están en español para ayudarte.

**Importante:** por defecto los tests prueban las *soluciones* (para que todo esté en verde). Cuando entrenás en la **Liga** (`aventura.py`), la Liga corre los tests contra **tu** `ejercicios.py` para evaluar tu trabajo real y darte EXP.

---

# 9. La semana de descanso: Git

Después de tanto Python, conviene un respiro. La **semana de Git** te enseña a "guardar la partida" de tu código:

- Está en la carpeta `semana-git-control-de-versiones/`.
- Tiene su `teoria.md`, ejercicios, soluciones y un **simulador de Git** (`interactivo.py`).
- En la Liga, es una **misión bonus** que da EXP y un logro especial.

Se recomienda hacerla **después de la semana 7**, pero podés hacerla cuando quieras.

---

# 10. Los proyectos finales

En la carpeta `proyectos/` hay **4 aplicaciones completas** para coronar tu aprendizaje. Cada una tiene su propio `README.md` con instrucciones:

| Proyecto | Qué es |
|----------|--------|
| 🔴 **pokedex-cli** | Pokédex de consola que usa la PokéAPI, muestra stats y sprites en ASCII, y guarda favoritos. |
| ⚔️ **batalla-pokemon** | Simulador de batalla con tipos, movimientos, PP, estados alterados y dos modos (vs CPU y vs jugador). |
| 📒 **agenda-entrenador** | Versión pulida de la Agenda del Entrenador. |
| 🌐 **pokedex-web** | Versión pulida de la Pokédex Web (con Flask y base de datos SQLite). |

Para correr un proyecto, entrá a su carpeta y leé su `README.md`. Por ejemplo:

```bash
cd proyectos/pokedex-cli
python pokedex.py
```

---

# 11. Preguntas frecuentes

**¿Por dónde empiezo?**
: Por la Liga: `python aventura.py`. Después seguí la semana 01.

**Me sale "command not found: python".**
: Probá con `python3` en vez de `python`.

**Los tests me dan rojo. ¿Está mal?**
: Significa que tu solución todavía no es correcta. Leé el mensaje de error (está en español), corregí, y volvé a probar. Es parte normal del aprendizaje.

**¿Tengo que entender todo de una?**
: No. Programar es practicar. Releé, probá, equivocate. Se va fijando con el tiempo.

**¿Puedo ver las soluciones?**
: Sí, están en `soluciones.py` / `soluciones.md`. Pero **intentá primero vos**. Mirar sin intentar es como usar un truco: ganás, pero no aprendés.

**¿Necesito internet?**
: Solo para algunas partes (la semana 10, la Pokédex online y el autocompletado web). El resto funciona sin conexión.

---

# 12. Glosario para novatos

**Terminal / consola**
: La ventana donde escribís comandos de texto. Tu "Pokédex del sistema".

**Comando**
: Una orden que le das a la computadora escribiendo texto.

**Python**
: El lenguaje de programación que aprendés en el curso.

**Variable**
: Una "caja con nombre" donde guardás un dato.

**Función**
: Un bloque de código con nombre que podés reusar. Como un ataque que tu Pokémon aprende una vez.

**Test**
: Un programa que revisa si tu código funciona bien.

**EXP**
: Puntos de experiencia que ganás en la Liga al pasar tests.

**Repositorio / repo**
: Una carpeta que Git vigila para guardar la historia de tu código.

**Commit**
: Un "punto de guardado" de tu código en Git.

**Entorno virtual (venv)**
: Una cajita aislada donde se instalan las librerías del curso sin ensuciar tu sistema.

---

<p style="text-align:center; color:#888; margin-top:30px;">
⚡ <em>"El mejor momento para empezar a programar fue ayer. El segundo mejor momento es ahora."</em> ⚡<br>
¡A atraparlos a todos! 🔴⚪
</p>

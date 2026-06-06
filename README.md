# 🔴⚪ Python con Pokémon 🐍

[![🌐 jugar ahora](https://img.shields.io/badge/%F0%9F%8E%AE_jugar_ahora-online-e3350d?style=for-the-badge)](https://felipendelicia.github.io/luca-journey/)

![Astro](https://img.shields.io/badge/Astro-build-BC52EE?logo=astro&logoColor=white)
![Pyodide](https://img.shields.io/badge/Python-en%20el%20navegador-3776AB?logo=python&logoColor=white)
![NestJS](https://img.shields.io/badge/API-NestJS%20+%20Prisma-E0234E?logo=nestjs&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-offline-5A0FC8)
![license](https://img.shields.io/badge/license-MIT-green)

> Aprendé a programar **desde cero** —Linux y Python— jugando una aventura **Pokémon**. En español
> argentino, para principiantes absolutos, y **100% en el navegador**: no instalás nada.

El código Python corre de verdad gracias a **[Pyodide](https://pyodide.org)** (CPython compilado a
WebAssembly). Tus ejercicios se corrigen con **pytest real**, atrapás Pokémon, evolucionás, peleás
contra otros en vivo y te convertís en Campeón de cada región resolviendo código.

## 🌐 Entrá

### 👉 https://felipendelicia.github.io/luca-journey/

---

## ✨ Qué tiene

**Aprender**
- 📖 **Libro interactivo** — toda la teoría (Linux + Python) con ejemplos que **editás y ejecutás**
  ahí mismo, un **visualizador paso a paso** (estilo Python Tutor) y **quizzes** de comprensión.
- 🏋️ **Ejercicios en vivo** — los corregís con **tests reales en el navegador**. Si algo falla, te
  **traduzco el error de Python a español** (con causa y cómo arreglarlo) y te doy una pista del
  test (“esperaba X, devolviste Y”) sin spoilear la solución.
- 🏆 **La Liga** — ganás EXP, subís de nivel y rango, y conseguís **medallas** venciendo a los
  **líderes de gimnasio** (mini-proyectos por pasos) de cada región.

**Jugar**
- 🎒 **Safari** — tirás Pokéballs y atrapás Pokémon salvajes (con su nivel, shiny y suspenso).
- 📕 **Pokédex** — colección estilo GO: instancias con nivel, caramelos, **evolución animada**,
  estadísticas y un limpiador de repetidos por línea evolutiva.
- ⚔️ **Batalla** — combate por turnos con tipos, ataques y **estados** (veneno, sueño…); un **Súper**
  que se desata resolviendo código. Incluye **PvP en vivo** con **ranking ELO**.
- 🛒 **Tienda** — gastás Pokébolas en piedras evolutivas, pociones y mejores Pokéballs.

**Comunidad**
- 🧩 **Desafíos** — creás y resolvés retos de Python de la comunidad (estilo CodeWars).
- 👥 **Social** — perfil público con **Tarjeta de Entrenador**, amigos, **intercambios por instancia**
  y listas de “busco / ofrezco”.

## 📊 En números

| 🗺️ Regiones | 📚 Capítulos | 🏋️ Ejercicios | 🏟️ Proyectos | 🔴 Pokémon |
|:---:|:---:|:---:|:---:|:---:|
| **9** (Kanto → Paldea, gen 1-9) | **77** | **417** en 72 temas | **81** (líderes + integradores) | **1025** |

> Las regiones avanzadas suman **Automatizaciones**, **Asincronía y concurrencia** y **Algoritmos y
> estructuras de datos** (Alola · Galar · Paldea).

## 📸 Capturas

| Inicio | El libro (código ejecutable + quizzes) |
|:---:|:---:|
| ![Inicio](screenshots/home.png) | ![El libro](screenshots/libro.png) |
| **Ejercicios (corrección en vivo)** | **La Liga (medallas)** |
| ![Ejercicios](screenshots/ejercicios.png) | ![La Liga](screenshots/liga.png) |

## 🧱 Cómo está hecho

```
Navegador (GitHub Pages)                         Raspberry Pi (LAN)
┌─────────────────────────────┐                  ┌──────────────────────────────┐
│  Astro (estático)           │  fetch + JWT     │  NestJS 10 + Prisma v7        │
│  Pyodide  → Python en WASM  │ ───────────────▶ │  Postgres (Docker)            │
│  CodeMirror (editor)        │  socket.io (PvP) │  Google OAuth → JWT           │
│  Service Worker (PWA)       │ ◀─────────────── │  progreso · social · realtime │
└─────────────────────────────┘                  └──────────────────────────────┘
```

- **Frontend:** [Astro](https://astro.build) (sitio estático), **Pyodide** para correr Python,
  **CodeMirror** como editor, y un **service worker** que cachea Pyodide/sprites → carga rápida y
  uso parcial **offline** (PWA instalable).
- **Backend self-hosted:** **NestJS + Prisma + Postgres** en Docker, corriendo en una **Raspberry Pi**.
  Auth con **Google OAuth → JWT**, sincronización de progreso en la nube, y **socket.io** para el
  PvP en vivo y la presencia de amigos.
- **Sin servidor también funciona:** sin sesión, todo se guarda en `localStorage` (modo solo-local).
- **Tests:** unitarios con **jest** (motor de combate, colección) y end-to-end con **Playwright**.

## 🛠️ Desarrollo

La app web vive en **`web/`**:

```bash
cd web
npm install
npm run dev          # http://localhost:4321  (hot-reload)
npm run build        # genera el sitio en ../docs (lo que publica GitHub Pages)
npm run test:e2e     # tests end-to-end (Playwright, usa el Chrome del sistema)
```

La API self-hosted vive en **`api/`** (NestJS) y corre con Docker:

```bash
docker compose up -d --build     # levanta Postgres + la API
```

> Detalles de configuración, variables de entorno y deploy a la Raspberry Pi: ver **`CLAUDE.md`**.

## 📁 Estructura

```
web/                          la app Astro (frontend)
  src/content/libro/          la teoría del libro (markdown — única fuente)
  src/ejercicios/<tema>/      ejercicios.py + soluciones.py + test_ejercicios.py por tema
  src/proyectos/<slug>/       proyectos de líder de gimnasio (pasos auto-corregidos)
  src/pages/                  inicio, libro, ejercicios, liga, safari, pokedex, batalla, tienda…
  src/lib/                    runner.py (pytest en Pyodide), combate-core.ts (motor), regiones.mjs…
  scripts/                    generan los datos (Pokémon, ejercicios, proyectos) en build
api/                          backend NestJS + Prisma (auth, progreso, social, PvP)
docs/                         build publicado en GitHub Pages (no se edita a mano)
```

## 🙌 Créditos

Datos y sprites de Pokémon vía [PokéAPI](https://pokeapi.co). Python en el navegador con
[Pyodide](https://pyodide.org). Hecho con ❤️ para enseñar a programar jugando.

Licencia [MIT](LICENSE).

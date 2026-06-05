# Proyectos / Líderes de Gimnasio — Fase 1 (motor + piloto) — Plan

> Ejecutar con subagentes. Diseño: `superpowers/specs/2026-06-05-proyectos-lideres-gimnasio-design.md`.

**Goal:** Motor de mini-proyectos (pasos auto-corregidos + capstone) que aparecen como
"Líder de Gimnasio" en `/ejercicios`, bloqueados hasta terminar los ejercicios del tema, y
cuya victoria otorga la medalla. Incluye 1 piloto: "Líder Brock: Pokédex de consola".

**Tech Stack:** Astro (vanilla JS + getStaticPaths), Pyodide + pytest (reusa `runner.py`),
CodeMirror (`editor.js`). Sin DB nueva: contenido file-based + progreso vía `proy:` en la nube.

**Testing:** `npm run build` desde `web/` (corre el sync). Prueba manual + un test de la
corrección con `python3` (Task 7).

**Patrones del repo a ESPEJAR (el subagente debe LEERLOS):**
- `web/scripts/sync-ejercicios.mjs` — patrón del sync (array de slugs + empaquetado a JSON).
- `web/src/pages/ejercicios/[slug]/[ex].astro` — patrón de página con Pyodide + `runner.py` +
  `correr(slug, codigo, test, extra, solo)` + render de resultados.
- `web/src/pages/ejercicios/index.astro` — dónde va la card.
- `web/src/lib/coleccion.js` (`sincronizar`, `INSIGNIAS`, `LEGENDARIOS`) y
  `web/src/pages/liga.astro` — lógica de medallas/regiones a tocar.
- `web/src/lib/nube.js` — `PREFIJOS`.
- `web/package.json` — cómo se engancha `sync-ejercicios.mjs` (prebuild/dev) para enganchar el de proyectos igual.
- Reglas de commit: SIN atribución a Claude.

---

### Task 1: `web/scripts/sync-proyectos.mjs` + wiring

**Files:** Create `web/scripts/sync-proyectos.mjs`; Modify `web/package.json`

- [ ] **Step 1.** Leé `web/scripts/sync-ejercicios.mjs` y `web/package.json` para ver el patrón.
- [ ] **Step 2.** Crear `sync-proyectos.mjs`: recorre `web/src/proyectos/<slug>/`, y por cada
  uno lee `meta.json` y `test_proyecto.py`, y emite a `web/src/data/proyectos.json` un objeto
  `{ [slug]: { slug, tipo, tema, region, titulo, lider, premio, intro, preamble, packages,
  test, pasos } }` donde `test` = contenido de `test_proyecto.py` y `pasos`/`tipo`/etc. salen
  de `meta.json`. **NO emitir `proyecto.py`** (es la solución de referencia, anti-trampa).

```js
// sync-proyectos.mjs — empaqueta web/src/proyectos/<slug>/ a web/src/data/proyectos.json.
// Cada proyecto = un líder de gimnasio (o integrador): pasos auto-corregidos + capstone.
// NO emite proyecto.py (solución de referencia). El test_proyecto.py se emite como 'test'.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(HERE, '..', 'src', 'proyectos');
const OUT = path.resolve(HERE, '..', 'src', 'data', 'proyectos.json');
const out = {};
if (fs.existsSync(SRC)) {
  for (const slug of fs.readdirSync(SRC)) {
    const dir = path.join(SRC, slug);
    if (!fs.statSync(dir).isDirectory()) continue;
    const meta = JSON.parse(fs.readFileSync(path.join(dir, 'meta.json'), 'utf8'));
    const test = fs.existsSync(path.join(dir, 'test_proyecto.py'))
      ? fs.readFileSync(path.join(dir, 'test_proyecto.py'), 'utf8') : '';
    out[slug] = {
      slug, tipo: meta.tipo, tema: meta.tema || null, region: meta.region,
      titulo: meta.titulo, lider: meta.lider || '', premio: meta.premio || 0,
      intro: meta.intro || '', preamble: meta.preamble || '', packages: meta.packages || [],
      test, pasos: meta.pasos || [],
    };
  }
}
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(`✓ proyectos.json: ${Object.keys(out).length} proyectos`);
```

- [ ] **Step 3.** En `web/package.json`, donde se llama a `sync-ejercicios.mjs` (en el
  script `dev` y/o `prebuild`/`build`), agregar también `node scripts/sync-proyectos.mjs`
  (encadenado con `&&`). Mirar el formato exacto del script existente y mantenerlo.
- [ ] **Step 4.** Verificar — `cd web && npm run build`. Esperado: build OK; se crea
  `web/src/data/proyectos.json` con 1 proyecto (tras Task 2).

---

### Task 2: Contenido piloto — `web/src/proyectos/python-introduccion/`

**Files:** Create `web/src/proyectos/python-introduccion/{proyecto.py,test_proyecto.py,meta.json}`

- [ ] **Step 1: `proyecto.py`** (solución de referencia; NO se emite, pero TIENE que pasar
  los tests — el subagente debe validarla con python3, ver Step 4):

```python
# Líder Brock — Pokédex de consola (solución de referencia).
# El preamble (POKEDEX) está en meta.json y se antepone al corregir.

def buscar(nombre):
    return POKEDEX.get(nombre.lower())

def mostrar(poke):
    if poke is None:
        return "No encontrado."
    return "Tipo: %s · Nivel: %d" % (poke["tipo"], poke["nivel"])

def responder(nombre):
    return mostrar(buscar(nombre))

def pokedex(consultas):
    return [responder(n) for n in consultas]
```

- [ ] **Step 2: `test_proyecto.py`**:

```python
from ejercicios import buscar, mostrar, responder, pokedex  # CURSO_MODULO=ejercicios

def test_buscar():
    assert buscar("Pikachu") == {"tipo": "eléctrico", "nivel": 10}
    assert buscar("CHARIZARD") == {"tipo": "fuego", "nivel": 36}
    assert buscar("nada") is None

def test_mostrar():
    assert mostrar({"tipo": "fuego", "nivel": 36}) == "Tipo: fuego · Nivel: 36"
    assert mostrar(None) == "No encontrado."

def test_responder():
    assert responder("charizard") == "Tipo: fuego · Nivel: 36"
    assert responder("xxx") == "No encontrado."

def test_pokedex():
    assert pokedex(["pikachu", "xxx"]) == ["Tipo: eléctrico · Nivel: 10", "No encontrado."]
```

- [ ] **Step 3: `meta.json`** (el `preamble` define POKEDEX para todos los pasos):

```json
{
  "tipo": "lider",
  "tema": "python-introduccion",
  "region": "kanto",
  "titulo": "Líder Brock: Pokédex de consola",
  "lider": "Brock",
  "premio": 25,
  "intro": "Construí una Pokédex de consola paso a paso. Cada paso agrega una función; al final corre el programa entero. ¡Vencé a Brock!",
  "preamble": "POKEDEX = {\n    \"pikachu\": {\"tipo\": \"eléctrico\", \"nivel\": 10},\n    \"charizard\": {\"tipo\": \"fuego\", \"nivel\": 36},\n    \"bulbasaur\": {\"tipo\": \"planta\", \"nivel\": 5},\n}",
  "packages": [],
  "pasos": [
    { "id": "buscar", "titulo": "1 · Buscar", "consigna": "Hacé `buscar(nombre)` que devuelva el dict del Pokémon en POKEDEX (sin importar mayúsculas), o None si no está.", "starter": "def buscar(nombre):\n    ", "tests": ["test_buscar"] },
    { "id": "mostrar", "titulo": "2 · Mostrar", "consigna": "Hacé `mostrar(poke)` que devuelva 'Tipo: <tipo> · Nivel: <nivel>'. Si poke es None, devolvé 'No encontrado.'.", "starter": "def mostrar(poke):\n    ", "tests": ["test_mostrar"] },
    { "id": "responder", "titulo": "3 · Responder", "consigna": "Hacé `responder(nombre)` que combine buscar + mostrar: dado un nombre, devolvé el texto a mostrar.", "starter": "def responder(nombre):\n    ", "tests": ["test_responder"] },
    { "id": "pokedex", "titulo": "4 · Pokédex (capstone)", "consigna": "Hacé `pokedex(consultas)` que reciba una lista de nombres y devuelva la lista de respuestas (usando responder).", "starter": "def pokedex(consultas):\n    ", "tests": ["test_pokedex"] }
  ]
}
```

- [ ] **Step 4: Validar la solución con python3** (sin Pyodide):

```bash
cd /home/felipe/Documents/Repositories/luca-journey/web/src/proyectos/python-introduccion
python3 -c '
import json, os
meta = json.load(open("meta.json"))
g = {}
exec(meta["preamble"], g)
exec(open("proyecto.py").read(), g)
# correr cada test contra el modulo de referencia
ns = dict(g); ns["__name__"]="t"
src = open("test_proyecto.py").read().replace("from ejercicios import", "# from ejercicios import")
exec(src, ns)
for nm in [t for p in meta["pasos"] for t in p["tests"]]:
    ns[nm](); print("OK", nm)
'
```
Esperado: `OK test_buscar` … `OK test_pokedex`. Si falla, corregí `proyecto.py`/tests.

---

### Task 3: Página `web/src/pages/proyectos/[slug].astro`

**Files:** Create `web/src/pages/proyectos/[slug].astro`

- [ ] **Step 1.** Leé `web/src/pages/ejercicios/[slug]/[ex].astro` (patrón Pyodide + runner +
  `correr` + render). Crear la página con:
  - `getStaticPaths` desde `web/src/data/proyectos.json` (un path por slug), pasando el
    proyecto entero como prop.
  - UI: intro + lista de **pasos secuenciales**. El paso actual = el primero sin
    `proy:<slug>:<pasoId>:ok`. Cada paso muestra: título, consigna, un editor (`editorPython`,
    doc = `localStorage['proy:<slug>:<pasoId>'] ?? starter`), botón "✅ Corregir paso", y el
    resultado. Los pasos ya aprobados se muestran colapsados con ✅. Los pasos posteriores al
    actual quedan bloqueados 🔒.
  - **Corrección del paso N**: cargar Pyodide + `runnerPy` (importar
    `import runnerPy from '../../lib/runner.py?raw'`). Armar
    `codigo = proyecto.preamble + '\n\n' + [código guardado/actual de los pasos 0..N].join('\n\n')`
    y llamar `correr(proyecto.slug, codigo, proyecto.test, '{}', JSON.stringify(paso.tests))`.
    Parsear el JSON; si todos los tests del paso pasan → guardar `proy:<slug>:<pasoId>` +
    `proy:<slug>:<pasoId>:ok='1'`, avanzar al siguiente paso. Al aprobar el ÚLTIMO paso →
    `proy:<slug>:ok='1'`, mostrar "🏅 ¡Venciste a <lider>! Medalla obtenida" y llamar
    `sincronizar(temas)` (de `coleccion.js`) para otorgar la insignia. (Para `sincronizar`
    necesitás `temas`: importá `ejercicios.json` en el frontmatter y pasalo por el script
    como hacen otras páginas, o reusá el patrón de `safari.astro`.)
  - On change del editor: guardar en `proy:<slug>:<pasoId>` (debounced), como en la página de
    ejercicios.
- [ ] **Step 2.** Verificar — `cd web && npm run build`. Esperado: build OK (genera
  `/proyectos/python-introduccion`).

---

### Task 4: Card de Líder de Gimnasio en `web/src/pages/ejercicios/index.astro` + CSS

**Files:** Modify `web/src/pages/ejercicios/index.astro`, `web/src/styles/global.css`

- [ ] **Step 1.** Leé `ejercicios/index.astro`. Importá `proyectos.json`. Para cada tema que
  tenga un proyecto líder (`tipo==='lider' && tema===<slug>`), renderizá después de su bloque
  una **card dorada** `🏟️ Líder de Gimnasio: <lider>`:
  - Si los ejercicios del tema están todos hechos (client-side: todas las
    `ej:<slug>:<id>:ok==='1'`) → link a `/proyectos/<slug>` (clickeable). Mostrar ✅ si
    `proy:<slug>:ok`.
  - Si NO → bloqueada 🔒 con texto "Completá los ejercicios del tema para desafiar al líder".
  - El estado (desbloqueado/✅) se calcula en un `<script>` client-side (leyendo localStorage),
    como hace `liga.astro`. Para los integradores (`tipo==='integrador'`) renderizá una card
    `👑 Integrador` al final de la región, desbloqueada cuando todos los líderes de la región
    están vencidos. (En Fase 1 puede no haber integradores aún — la card solo aparece si
    existe el proyecto en `proyectos.json`.)
- [ ] **Step 2.** CSS en `global.css`:

```css
/* líder de gimnasio / proyectos */
.lider-card{ display:flex; align-items:center; gap:12px; background:linear-gradient(135deg,#3a2f12,#4a3a14); border:1px solid var(--yellow-deep); border-radius:14px; padding:12px 16px; margin:.6rem 0 1.2rem; text-decoration:none; color:var(--ink); }
.lider-card.bloq{ filter:grayscale(.6); opacity:.7; cursor:default; }
.lider-card .lc-ico{ font-size:1.6rem; flex:none; }
.lider-card .lc-tit{ font-weight:800; }
.lider-card .lc-sub{ color:var(--ink-soft); font-size:.85rem; }
.lider-card .lc-estado{ margin-left:auto; font-weight:800; }
.proy-paso{ background:var(--paper-2); border:1px solid var(--line); border-radius:14px; padding:14px; margin:.8rem 0; }
.proy-paso.bloq{ opacity:.5; }
.proy-paso.ok{ border-color:#1f8b4c; }
.proy-paso h3{ margin:0 0 .4rem; font-size:1rem; }
```

- [ ] **Step 3.** Verificar — `cd web && npm run build`. Esperado: build OK.

---

### Task 5: `proy:` en la sync de la nube — `web/src/lib/nube.js`

**Files:** Modify `web/src/lib/nube.js`

- [ ] **Step 1.** Cambiar `const PREFIJOS = ['ej:', 'col:'];` por
  `const PREFIJOS = ['ej:', 'col:', 'proy:'];` (para que el progreso de proyectos sincronice).
- [ ] **Step 2.** Verificar — `cd web && npm run build`. Esperado: build OK.

---

### Task 6: Gating + grandfather en `coleccion.js` y `liga.astro`

**Files:** Modify `web/src/lib/coleccion.js`, `web/src/pages/liga.astro`

- [ ] **Step 1.** Leé `coleccion.js` (`sincronizar`, `INSIGNIAS`, `LEGENDARIOS`,
  `regionesDesbloqueadas`) y `liga.astro` (cómo cuenta medallas/regiones).
- [ ] **Step 2. `coleccion.js` `sincronizar`:** un tema otorga su insignia cuando: TODOS sus
  ejercicios están hechos **Y** (`localStorage['proy:<slug>:ok']==='1'` **O** ya estaba en
  `col:hitos` el `tema:<slug>` — grandfather). Análogo para región/legendario: todos los temas
  completos **Y** `localStorage['proy:<region>-integrador:ok']==='1'` **O** ya estaba
  `region:<region>` en hitos. Helper: `const proyOk = (k) => localStorage.getItem('proy:'+k+':ok')==='1';`
  Concretamente, en el loop de temas, cambiar la condición de "tema completo" para la insignia
  a: `hechos === total && (proyOk(t.slug) || hitos.has('tema:'+t.slug))`. Y en regiones, la
  condición a: `completa && (proyOk(region+'-integrador') || hitos.has('region:'+region))`.
- [ ] **Step 3. `liga.astro`:** donde calcula `medallas`/`completo` por tema (medalla = todos
  los ejercicios), cambiar a: medalla cuenta si `done===total && (proyOk(slug) ||
  yaTeniaMedalla)`. Para grandfather, leer `col:hitos` (`tema:<slug>`). Definir
  `const proyOk = (k) => localStorage.getItem('proy:'+k+':ok')==='1';` y
  `const hitos = (() => { try { return new Set(JSON.parse(localStorage.getItem('col:hitos'))||[]); } catch { return new Set(); } })();`
  Mantener el resto del cálculo (rango, nivel, exp) igual.
- [ ] **Step 4. Verificar** — `cd web && npm run build`. Esperado: build OK. **Importante:**
  no romper el cálculo existente — un usuario que YA tenía la medalla (en `col:hitos`) debe
  seguir viéndola.

---

### Task 7: Build + test de corrección + commit (controller hace el commit)

- [ ] **Step 1.** `cd web && npm run build` (corre el sync) → OK, `proyectos.json` con 1.
- [ ] **Step 2.** Validar la corrección del piloto con python3 (Task 2 Step 4) → todos OK.
- [ ] **Step 3.** El subagente NO commitea. Reporta. El controller revisa, prueba y commitea.

## Self-Review
- Cobertura Fase 1: motor (Task 1 sync + Task 3 página) ✓; piloto (Task 2) ✓; card en
  /ejercicios con bloqueo (Task 4) ✓; sync `proy:` (Task 5) ✓; gating+grandfather (Task 6) ✓.
- Sin DB nueva. Ruta `/proyectos/[slug]` con `getStaticPaths` (slugs conocidos en build) ✓.
- Consistencia: `meta.json.pasos[].tests` (nombres) = `solo` de `runner.correr`; `test`
  emitido = `test_proyecto.py` ✓. `proy:<slug>:ok` setea/lee igual en página y gating ✓.
- Riesgo: Task 6 toca progresión existente — grandfather con `col:hitos` evita regresión.

# Safari v2 (rareza + animaciones) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Que el safari tenga rareza granular (10 tiers derivados del peso existente) y una animación de captura distinta por tier, con el drama escalando de común a legendario.

**Architecture:** `rareza.js` (puro) clasifica peso→tier. `coleccion.js > tirar()` suma `tier` al resultado (sin cambiar el pick ponderado). `safari.astro` lee `r.tier` y escala la animación de captura (clases CSS por nivel, partículas, shake, sonido, badge). CSS y `sonidos.js` proveen los efectos.

**Tech Stack:** Astro + JS vanilla + CSS (localStorage, sin backend). `web/` no tiene runner de tests JS → `rareza.js` se verifica con un script `node` puntual; el resto, visual (screenshots del dev server).

**Spec:** `superpowers/specs/2026-06-05-safari-rareza-animaciones-design.md`

---

## Estructura de archivos

| Archivo | Responsabilidad |
|---|---|
| `web/src/lib/rareza.js` | NUEVO. `TIERS` (config) + `tierDe(peso)`. Puro, sin DOM/env. |
| `web/src/lib/coleccion.js` | `tirar()` agrega `tier`. |
| `web/src/lib/sonidos.js` | agrega `sonarEpico()` para tiers altos. |
| `web/src/pages/safari.astro` | animación de captura escalada por tier + badge. |
| `web/src/styles/global.css` | clases `tier-N`, keyframes (shake/burst/confeti/glow). |

---

## Task 1: `rareza.js` — peso → tier (puro)

**Files:**
- Create: `web/src/lib/rareza.js`

- [ ] **Step 1: Escribir el módulo**

```javascript
// rareza.js — clasifica un Pokémon en 1 de 10 tiers según su PESO de aparición
// (el de aparicion.json: menor peso = más raro). Puro: sin DOM, sin import.meta.
export const TIERS = [
  { nivel: 1,  nombre: 'Común',       color: '#7d8b79', ico: '',     min: 200 },
  { nivel: 2,  nombre: 'Frecuente',   color: '#5fa84a', ico: '',     min: 165 },
  { nivel: 3,  nombre: 'Inusual',     color: '#3fae8e', ico: '',     min: 135 },
  { nivel: 4,  nombre: 'Poco común',  color: '#3aa6d8', ico: '✦',    min: 105 },
  { nivel: 5,  nombre: 'Raro',        color: '#3b6fe0', ico: '✦',    min: 80  },
  { nivel: 6,  nombre: 'Muy raro',    color: '#7a4fe0', ico: '✦✦',   min: 55  },
  { nivel: 7,  nombre: 'Épico',       color: '#a23bd8', ico: '✦✦',   min: 40  },
  { nivel: 8,  nombre: 'Excepcional', color: '#d83bb0', ico: '✦✦✦',  min: 20  },
  { nivel: 9,  nombre: 'Mítico',      color: '#e07b2a', ico: '★',     min: 6   },
  { nivel: 10, nombre: 'Legendario',  color: '#e8b923', ico: '★★',    min: 0   },
];

// peso → tier: el primero (de mayor a menor 'min') cuyo umbral cumple el peso.
export function tierDe(peso) {
  const w = Number(peso) || 1;
  for (const t of TIERS) if (w >= t.min) return t;
  return TIERS[TIERS.length - 1];
}
```

- [ ] **Step 2: Verificar con node (no hay jest en web/)**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
node --input-type=module -e "
import { tierDe } from './src/lib/rareza.js';
const casos = [[255,1],[200,1],[199,2],[150,3],[100,5],[55,6],[40,7],[20,8],[6,9],[5,10],[3,10],[1,10]];
let ok = true;
for (const [w, n] of casos) { const t = tierDe(w).nivel; if (t !== n) { console.log('FAIL peso', w, '→ T'+t, 'esperaba T'+n); ok = false; } }
console.log(ok ? 'rareza OK (12/12)' : 'rareza FALLA');
"
```
Expected: `rareza OK (12/12)`.

- [ ] **Step 3: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/rareza.js
git commit -m "safari: rareza.js (10 tiers, tierDe por peso) + verificacion node"
```

---

## Task 2: `tirar()` devuelve el tier

**Files:**
- Modify: `web/src/lib/coleccion.js`

- [ ] **Step 1: Importar `tierDe`** (arriba del archivo, junto a los otros datos):

```javascript
import { tierDe } from './rareza.js';
```

- [ ] **Step 2: Agregar `tier` al objeto que devuelve `tirar()`**

En `coleccion.js`, en el `return` de `tirar()` (la última línea de la función), agregá `tier`:
```javascript
  return { pokemon: elegido, cantidad: at[elegido.id], repetido: at[elegido.id] > 1, shiny, nuevoShiny, balls, prob, cadaCuantos, tier: tierDe(pesos[elegido.id] || 1) };
```
(No cambia nada del pick: el peso ya determina la frecuencia; `tierDe` solo lo etiqueta.)

- [ ] **Step 3: Verificar que importa bien (dev server compila)**

Run: `cd web && node --check src/lib/coleccion.js` (sintaxis) — y mirar que el dev server (`http://localhost:4321`) no tire error de import en la consola.

- [ ] **Step 4: Commit**

```bash
git add web/src/lib/coleccion.js
git commit -m "safari: tirar() devuelve el tier de rareza del Pokemon atrapado"
```

---

## Task 3: Sonido épico para tiers altos

**Files:**
- Modify: `web/src/lib/sonidos.js`

- [ ] **Step 1: Leer `sonidos.js`** para reusar el patrón de `sonarCaptura`/`sonarShiny` (WebAudio). Agregar una función `sonarEpico()` que haga un acorde ascendente más largo/grave (más épico que la captura normal). Exportarla.

> El código exacto depende del estilo de `sonidos.js` (osciladores WebAudio). Patrón: crear `AudioContext`, 2-3 osciladores con frecuencias ascendentes (ej. 440→660→880) y envolvente de ~0.6 s. Respetar el flag `localStorage 'sonido:off'` como las otras.

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/sonidos.js
git commit -m "safari: sonarEpico() para capturas de tier alto"
```

---

## Task 4: Animación de captura escalada por tier (el corazón)

**Files:**
- Modify: `web/src/pages/safari.astro` (la función `lanzarBall` + imports + el bloque de captura)
- Modify: `web/src/styles/global.css` (clases `tier-N`, keyframes)

- [ ] **Step 1: Importar lo nuevo en el `<script>` de safari.astro**

Agregá a los imports: `import { sonarEpico } from '../lib/sonidos.js';` (ya importa `sonarCaptura`, `sonarShiny`).

- [ ] **Step 2: En `lanzarBall`, derivar la intensidad del tier**

Tras obtener `r` y antes de la animación, definí los parámetros escalados:
```javascript
const t = r.tier || { nivel: 1, nombre: 'Común', color: '#7d8b79', ico: '' };
const nivel = t.nivel;
const escena = arena.querySelector('.escena');
escena.style.setProperty('--tier-color', t.color);
escena.classList.add('tier-' + nivel);
// nº de tambaleos y partículas escalan con el tier
const tambaleos = nivel >= 9 ? 5 : nivel >= 7 ? 4 : nivel >= 4 ? 3 : 2;
const nParticulas = nivel >= 9 ? 28 : nivel >= 7 ? 20 : nivel >= 4 ? 16 : 8;
const epico = nivel >= 7;
const legendario = nivel >= 9;
```

- [ ] **Step 3: Usar esos parámetros en la animación**

- Cambiar el loop de tambaleos para usar `tambaleos` en vez del `3` fijo.
- Reemplazar la llamada a `estrellas(...)` por una versión que reciba `nParticulas` y el color del tier (partículas del color del tier; doradas si shiny/legendario).
- Sonido: `if (r.shiny) sonarShiny(); else if (epico) sonarEpico(); else sonarCaptura();`
- Efecto de pantalla: el `shiny-flash` actual se reusa; agregar `body.classList.add('tier-shake')` por ~700 ms si `legendario` (pantalla temblando), y un `escena.classList.add('burst')` para la ráfaga dorada en `epico`.
- Duración: el suspenso (los tambaleos) ya escala por `tambaleos`; para tiers bajos baja el delay para que sea "pop rápido".

- [ ] **Step 4: Badge del tier en el texto de captura**

En el `txt.innerHTML`, reemplazar/where está `cap-prob` por un badge del tier:
```javascript
txt.innerHTML = titulo + ' <span class="cap-n">Nº ' + p.id + '</span>'
  + '<span class="cap-tier" style="--tier-color:' + t.color + '">' + (t.ico ? t.ico + ' ' : '') + t.nombre + '</span>'
  + '<span class="cap-prob">🎲 1 de cada ' + r.cadaCuantos + '</span>';
```

- [ ] **Step 5: CSS — clases por tier + keyframes** (en `global.css`)

```css
/* Safari v2: rareza por tier */
.cap-tier{ display:inline-block; margin-top:4px; padding:2px 10px; border-radius:999px;
  font:700 .72rem var(--font-mono); letter-spacing:.05em; color:#0a0a0a;
  background:var(--tier-color); box-shadow:0 0 14px -2px var(--tier-color); }
/* marco/glow del salvaje según tier (intensidad sube con el nivel) */
.escena.tier-4 .wild,.escena.tier-5 .wild,.escena.tier-6 .wild{ filter:drop-shadow(0 0 10px var(--tier-color)); }
.escena.tier-7 .wild,.escena.tier-8 .wild{ filter:drop-shadow(0 0 18px var(--tier-color)); }
.escena.tier-9 .wild,.escena.tier-10 .wild{ filter:drop-shadow(0 0 26px var(--tier-color)) drop-shadow(0 0 50px var(--tier-color)); }
/* ráfaga (épico+) */
.escena.burst::after{ content:""; position:absolute; inset:-40%; border-radius:50%;
  background:radial-gradient(circle, var(--tier-color) 0%, transparent 60%); opacity:0; animation:burst .8s ease-out; pointer-events:none; }
@keyframes burst{ 0%{opacity:.0; transform:scale(.4);} 25%{opacity:.6;} 100%{opacity:0; transform:scale(1.4);} }
/* pantalla temblando (legendario) */
@keyframes tierShake{ 0%,100%{transform:translate(0,0);} 20%{transform:translate(-6px,4px);} 40%{transform:translate(5px,-5px);} 60%{transform:translate(-4px,-3px);} 80%{transform:translate(4px,4px);} }
body.tier-shake{ animation:tierShake .55s ease-in-out 1; }
```

- [ ] **Step 6: Build + verificación visual**

Run: `cd web && npm run build` (compila). Luego, con el dev server, tirar varias veces y observar que: común = pop rápido sin marco; tiers medios = marco de color + estrellas; épico = ráfaga; legendario = pantalla temblando + dorado. Sacar screenshots de un común, un raro y un legendario (forzar tiers altos temporalmente bajando un umbral para testear, o tirar mucho).

- [ ] **Step 7: Commit**

```bash
git add web/src/pages/safari.astro web/src/styles/global.css
git commit -m "safari: animacion de captura escalada por tier (marco/particulas/ráfaga/shake) + badge de rareza"
```

---

## Task 5: Build final + deploy

- [ ] **Step 1:** `cd web && npm run build` (490 páginas, sin errores).
- [ ] **Step 2:** Commitear `docs/` + push (`git add docs && git commit -m "build: safari v2" && git push origin main`).
- [ ] **Step 3:** Verificar en el sitio (o dev) que el safari anda y se ve la escalada de rareza.

---

## Self-review (cobertura del spec)

- **10 tiers derivados del peso:** Task 1 (`rareza.js`). ✔
- **`tirar()` etiqueta el tier sin cambiar el pick:** Task 2. ✔
- **Animación por tier (drama escalado) + badge:** Task 4 (safari.astro + CSS). ✔
- **Shiny ortogonal (capa encima):** Task 4 Step 3 (sonarShiny + shiny-flash se mantienen, suman sobre el tier). ✔
- **Sonido épico tiers altos:** Task 3. ✔
- **Fuera de alcance (pokéballs/zonas):** no hay tasks. ✔

Sin placeholders en la lógica pura (rareza.js/coleccion.js completas). La capa visual (Task 3/4) describe el código clave + se afina con feedback visual al implementar (es UI iterativa).

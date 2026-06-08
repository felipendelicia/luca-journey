# Abrir al público: onboarding de username + landing `/conocer` — diseño

**Fecha:** 2026-06-07 · **Estado:** aprobado en el companion visual ("mandale").
**Objetivo:** dejar el proyecto listo para usuarios nuevos. Dos entregables independientes:
**(1)** sugerir un **nombre de usuario** al primer login (saltable, sin chocar con el tutorial), y
**(2)** una **landing pública** atractiva en `/conocer` (sin login), mantenida al día.

---

## Parte 1 — Onboarding de username (post-login, primera vez)

### Flujo (decidido)
1. El usuario entra por primera vez (login Google) → **NO tiene perfil/handle**.
2. Aparece un **modal**: "Elegí tu nombre de usuario", con un **handle sugerido pre-cargado** (editable),
   botón **Guardar** y botón **Saltar por ahora**.
3. Al **Guardar** o **Saltar** → se marca `onboard:visto = '1'` y **recién ahí arranca el tutorial**
   (username **primero**, tutorial **después** — nunca se pisan).

### Sugerencia del handle
El backend solo guarda el **email** (no el display name de Google). Sugerimos a partir del **local-part
del email**: `email.split('@')[0]` → `normHandle(...)`. Ej. `ana.perez@gmail.com` → `ana_perez`. Si está
ocupado al guardar, se reintenta con un número (`ana_perez2`).

### Detección de "primera vez"
Tras login + hidratación (`nube:listo`/`nube:cambio`): si `usuario()` existe, `onboard:visto !== '1'`, y el
usuario **no tiene handle** (`miPerfil()` → null/sin handle, y `liga:nombre` vacío) → mostrar el modal.
Returning users (con perfil) **no** lo ven.

### Coordinación con el tutorial (clave)
- El trigger del tutorial en `index.astro` (`setTimeout(iniciarTutorial, 900)`) se **gatea**: solo corre si
  `onboard:visto === '1'`. Así, si el onboarding está pendiente, el tutorial espera.
- El modal de onboarding, al cerrarse (guardar/saltar), si estamos en `index` dispara el tutorial
  (`iniciarTutorial()`); si estamos en otra página, el tutorial correrá normalmente al ir a `index`
  (ya con `onboard:visto = 1`). Nunca aparecen los dos a la vez.

### Arquitectura
- **`web/src/lib/onboarding.js`** (nuevo): `iniciarOnboarding()` — chequea las condiciones, arma el modal,
  guarda (reusa `guardarPerfil` de social.js + `normHandle`) o saltea, setea el flag, dispara el tutorial.
  Escucha `nube:listo`/`nube:cambio`.
- **`normHandle`**: extraerlo de `liga.astro` a `social.js` (export) y que ambos (liga + onboarding) lo usen.
- **`Base.astro`**: cargar `onboarding.js` (un `<script>`), para que el modal pueda aparecer tras el login en
  cualquier página. Reusa el estilo de modales existente.
- **`index.astro`**: gatear el `iniciarTutorial()` con `onboard:visto`.

### Accesibilidad / UX
- Modal `role="dialog" aria-modal`, foco al input, Esc = saltar. Validación: mín. 3 chars (minúsc/núm/_).
- "Saltar por ahora" deja al usuario sin handle (puede crearlo después en la Liga, como hoy).

---

## Parte 2 — Landing pública `/conocer`

### Qué es
Página **standalone** (no usa `Base.astro` → **sin el boot-overlay/login gate**), pública, pensada para que
gente ajena conozca el proyecto y se interese. Estética CRT/Pokédex (verde neón) consistente con la app.

### Secciones (aprobadas, según el mockup)
1. **Mini-nav** (lámpara + "Pokédex Codex" + botón "Entrar ▸").
2. **Hero:** kicker ("Gratis · en tu navegador · sin instalar"), título grande pixel ("Aprendé a
   **programar** jugando **Pokémon**"), lead, **CTA ⚡ Empezá gratis** + "Ver qué tiene", nota
   ("Google · 0$ · sin tarjeta") y 3 **stats** (1025 Pokémon · 9 regiones · 500+ ejercicios).
3. **Cómo funciona:** 3 pasos (leés y probás → resolvés → progresás).
4. **Features:** grilla de 6 tarjetas (libro interactivo, ejercicios autocorregidos, Pokédex+Safari, PvP en
   vivo, liga+medallas, desafíos de comunidad).
5. **"Se ve así":** capturas — en v1 con **capturas reales** de `screenshots/` (editor/batalla/pokédex) si las
   hay; si no, los mini-mockups CSS del diseño.
6. **CTA final** + footer.

### Arquitectura
- **`web/src/pages/conocer.astro`** (nuevo, standalone): `<html>` propio, importa `global.css` (tokens/fonts),
  el markup del mockup, CTAs que linkean a la **app** (`u('/')`, que dispara el login). Responsive (móvil:
  grids a 1 columna). **SEO/OG:** title, description y `og:image` (la `og.png` existente) para que comparta
  lindo.
- Links: el botón "Entrar"/"Empezá gratis" → `u('/')`. Opcional: un link "¿Qué es esto?" → `/conocer` desde
  la **pantalla de login** (boot-overlay) para que los visitantes la encuentren.
- **Sin tocar** el gate de las demás páginas.

### Mantenimiento (pedido del usuario)
- Agregar a **`CLAUDE.md`** una regla: *"Mantené `web/src/pages/conocer.astro` (la landing pública) al día
  cuando agregues/cambies features importantes —stats, grilla de features, capturas."* Así Claude la actualiza.

## Testing
- **Onboarding:** Playwright difícil (necesita login real). Verificar build verde; testear la lógica
  (`normHandle`, condición de "primera vez") y un smoke con sesión mockeada si se puede. e2e real = owner.
- **Landing:** Playwright → la página carga **sin login** (no aparece el boot-overlay), se ve el hero +
  secciones, CTAs apuntan a la app, responsive (móvil). Screenshot claro/oscuro (o solo el tema de la landing).
- `npm run build` verde.

## Alcance / no-objetivos
- Onboarding: la sugerencia sale del **email** (no se captura el display name de Google → eso sería cambio de
  backend + deploy; queda como mejora futura). No se fuerza el handle (sigue siendo saltable).
- Landing: estática (sin datos en vivo); los números/stats van hardcodeados (y se mantienen vía la regla de
  CLAUDE.md). No es la home (`/` sigue siendo la app gateada); `/conocer` es la puerta pública.

## Archivos
- `web/src/lib/onboarding.js` (nuevo) · `web/src/lib/social.js` (export `normHandle`) ·
  `web/src/layouts/Base.astro` (cargar onboarding) · `web/src/pages/index.astro` (gatear tutorial) ·
  `web/src/pages/liga.astro` (usar `normHandle` compartido).
- `web/src/pages/conocer.astro` (nuevo) · `web/src/styles/global.css` (si hace falta algún estilo extra) ·
  `CLAUDE.md` (regla de mantenimiento) · `web/src/layouts/Base.astro` (link "¿Qué es esto?" en el login, opcional).

# Diseño — Safari v2: rareza granular + animaciones por tier

Fecha: 2026-06-05
Estado: aprobado

> Ubicación `superpowers/` (raíz), NO `docs/` (el build limpia `docs/`).

## Objetivo

Arreglar las dos quejas del safari actual:
1. **"Siempre aparecen todos"** → se resuelve por **rareza dura**: los tiers altos son
   rarísimos y dramáticos, así deja de sentirse plano (los comunes llueven, un épico es un
   evento). NO se usan zonas/progreso (el owner los descartó).
2. **"Probabilidades muy genéricas"** → rareza **granular en 10 niveles**, cada uno con
   nombre, color, tasa propia y —el corazón del rediseño— **su propia animación de captura**.

Se mantiene **captura directa** (un tiro = una captura, sin fallo/huida). Foco: las animaciones.

## Estado actual (qué se cambia)

`coleccion.js > tirar()` elige un Pokémon del pool de regiones desbloqueadas **ponderado por
`aparicion.json`** (peso = BST + legendario: débil ~255 común, fuerte ~6 raro, legendario ≤5)
y devuelve `{pokemon, prob, cadaCuantos, shiny, ...}`. La captura en `safari.astro` tiene
**una sola animación** para todo. No hay concepto de "tier".

**No se toca la lógica de elección** (ya pondera por rareza). Lo nuevo es: **etiquetar** el
resultado con su tier y **animar según el tier**.

## A) Modelo de rareza — 10 tiers

Cada Pokémon cae en un tier según su peso (menor peso = más raro). Escalera:

| Nivel | Nombre | Color | Peso (aprox, rango 3–255) |
|---|---|---|---|
| 1 | Común | gris-verde | ≥ 200 |
| 2 | Frecuente | verde | 165–199 |
| 3 | Inusual | verde-azul | 135–164 |
| 4 | Poco común | celeste | 105–134 |
| 5 | Raro ✦ | azul | 80–104 |
| 6 | Muy raro | violeta | 55–79 |
| 7 | Épico ✦✦ | púrpura | 40–54 |
| 8 | Excepcional | magenta | 20–39 |
| 9 | Mítico ✦✦✦ | naranja | 6–19 |
| 10 | Legendario ★ | dorado | ≤ 5 |

- Umbrales calibrables; objetivo: comunes dominan, legendarios ~1 de cada cientos. La **tasa
  de aparición** de cada tier = suma de pesos del tier en el pool / total (emerge sola del
  pick ponderado existente — no se cambia el pick).
- **Shiny es ORTOGONAL** al tier: 1% sobre cualquier captura (como hoy), con su **capa visual
  propia** ENCIMA de la animación del tier.

## B) Animaciones por tier (la parte central)

El drama **escala con la rareza** (duración + efectos crecientes):

- **T1–3** (común/frecuente/inusual): pop rápido (~0.8 s), sin marco, sonido corto.
- **T4–6** (poco común/raro/muy raro): marco de color del tier, estrellas, sonido medio (~1.5 s).
- **T7–8** (épico/excepcional): la pokéball tiembla más, destello, leve cámara lenta,
  partículas del color del tier (~2.5 s).
- **T9–10** (mítico/legendario): **pantalla temblando**, ráfaga dorada, revelado lento,
  confeti, sonido épico (~3.5 s).
- **Shiny**: capa extra (flash + ✨ + sonido shiny) sumada encima del tier que toque.

La UI de captura muestra **nombre + color del tier** (badge), reemplazando el actual
"aparece 1 de cada X intentos" por algo más vivo (se puede mantener el dato chico abajo).

## Componentes / archivos

| Archivo | Cambio |
|---|---|
| `web/src/lib/rareza.js` | **NUEVO**: `TIERS` (array de `{nivel, nombre, color, ico, min}`), `tierDe(peso)` → objeto tier. Puro, sin DOM. |
| `web/src/lib/coleccion.js` | `tirar()` agrega `tier: tierDe(pesos[id]||1)` al objeto devuelto. **No** cambia el pick. |
| `web/src/pages/safari.astro` | la animación de captura lee `r.tier`: aplica clase `tier-N` + duración + partículas escalonadas; muestra el badge del tier; T9–10 y shiny suman efectos máximos. |
| `web/src/styles/global.css` | clases por tier (marco/glow/color del badge) + keyframes de las animaciones (shake, burst dorado, reveal lento) con intensidad por nivel. |
| `web/src/lib/sonidos.js` | sonido por tramo de tier (reusar `sonarCaptura`/`sonarShiny` + variante "épica" para T7–10). |

**Diseño por unidades:** `rareza.js` es pura y testeable (peso→tier). `coleccion.js` solo
suma un campo. Toda la lógica visual vive en `safari.astro` + CSS. Sin acoplar rareza con DOM.

## Datos

No hace falta archivo nuevo: el tier se **deriva en runtime** del peso que ya está en
`aparicion.json` (pasado a `tirar`). `tierDe` es determinista por peso.

## Testing

- **Unit** (si hay runner JS en `web/`; si no, asserts inline o manual): `tierDe` mapea
  pesos clave → tier esperado (255→T1, 5→T10, bordes de umbral 200/80/6).
- **Manual/visual**: tirar repetido y ver que cada tier dispara su animación; screenshots de
  un común, un raro y un legendario para confirmar la escalada de drama.

## Fuera de alcance (segunda vuelta)

- Tipos de Pokéball (mejor ball → más chance de tiers altos).
- Zonas/hábitats, rotación diaria, recorte real del pool.
- Encuentro con fallo/huida.

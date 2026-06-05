# Diseño — Desafíos de la comunidad (estilo CodeWars)

Fecha: 2026-06-04
Estado: aprobado

> Ubicación `superpowers/` (raíz), NO `docs/` (el build limpia `docs/`).

## Objetivo
Contenido de Python **infinito, no genérico y social**: cualquier usuario **crea** retos de
Python; la comunidad los **resuelve**; después de resolver podés **ver las soluciones de
todos**. Resuelve el problema de "los ejercicios del curso se acaban": cuando el currículum
termina, **la comunidad es el contenido**. Reusa el runner de Pyodide/pytest, Supabase,
perfiles y amigos.

## Decisiones (brainstorming)
- **Corrección por solución + casos** (no el autor escribe tests): al publicar, el navegador
  del autor corre la solución sobre los casos y guarda **los resultados esperados**; la
  solución **no viaja** al solver.
- **Ver soluciones de todos** después de resolver (gated, sin spoilers), con 👍 para votar.
- Recompensa atada a la economía actual (balls) + reputación.

## Modelo de datos (Supabase)

### `desafios`
`id uuid pk`, `autor uuid → auth.users`, `titulo text`, `consigna text`, `func text`
(nombre de la función a implementar), `starter text` (código inicial), `casos jsonb`
(`[{ args:[...], esperado:"<json>", ejemplo:bool }]` — `esperado` = `json.dumps(sol(*args),
sort_keys=True, default=str)`), `dificultad int` (1-8, lo pone el autor),
`region text` (categoría), `creado timestamptz`.
- **Categoría por región** (atada a los temas del curso): `kanto` (fundamentos Python),
  `johto` (análisis de datos), `hoenn` (APIs/Flask), `sinnoh` (SQL/BD), `unova` (IA),
  `kalos` (testing), o `libre` (general). El autor la elige al crear.
- RLS: **select público**. Insert/update solo por RPC (autor).

### `resoluciones`
`id uuid pk`, `desafio_id uuid → desafios on delete cascade`, `user_id uuid`, `codigo text`
(la solución del que resolvió), `creado timestamptz`. Único `(desafio_id, user_id)`.
- RLS select: podés leer las resoluciones de un desafío **solo si vos lo resolviste** (o sos
  el autor) → evita spoilers:
  `using (auth.uid() = user_id or exists (select 1 from resoluciones r where r.desafio_id =
  resoluciones.desafio_id and r.user_id = auth.uid()) or exists (select 1 from desafios d
  where d.id = resoluciones.desafio_id and d.autor = auth.uid()))`.

### `votos`
`resolucion_id uuid → resoluciones`, `user_id uuid`, único `(resolucion_id, user_id)`.
- RLS: select público (para contar); insert/delete propio.

## RPCs (`security definer`)
- `crear_desafio(titulo, consigna, func, starter, casos, dificultad, region)` — inserta;
  `autor = auth.uid()`. Valida `func` no vacío, `casos` no vacío, `region` en la lista. (La
  validación de que la solución corre se hace **en el cliente** con Pyodide antes de llamar;
  el server confía en los `esperados` precomputados.)
- `registrar_resolucion(desafio_id, codigo)` — upsert de la resolución del que llama; otorga
  recompensa la **primera vez** (balls, en `progreso` — o lo maneja el cliente). Idempotente.
- `votar(resolucion_id, on bool)` — agrega/saca tu voto.
- `listar_desafios(orden, q, region, limite, offset)` — público; filtra por `region` (o
  todas); devuelve título, autor (handle), dificultad, region, # resoluciones, si **vos** lo
  resolviste. Orden: recientes / más resueltos / dificultad.
- `mis_stats_desafios()` — resueltos/creados para el perfil.

## Cliente

### `web/src/lib/desafios.js`
API sobre Supabase: `crear`, `leer(id)`, `listar(...)`, `registrarResolucion(id, codigo)`,
`solucionesDe(id)` (gated por RLS), `votar(id, on)`, `misStats()`.

### Corrección (reusa Pyodide; en `desafios.js` o un helper)
- **Al crear**: cargar Pyodide, correr la solución del autor; para cada caso computar
  `esperado = json.dumps(func(*args), sort_keys=True, default=str)`. Si algo falla → no deja
  publicar (mostrar el error). Guardar `casos` con `esperado` por caso.
- **Al resolver**: correr el código del solver (debe definir `func`); para cada caso
  comparar `json.dumps(func(*args), sort_keys=True, default=str) === caso.esperado`. Todos
  OK → resuelto. Mostrar qué caso falló (con el input visible solo de los `ejemplo`).
- **Timeout** por corrida (corta loops). Solo se muestran los inputs marcados `ejemplo`.

### Páginas
- **`/desafios`** (lista/explorar) — buscador, **filtro por región** (chips Kanto…Kalos +
  Libre), orden (recientes / más resueltos / dificultad), badge "✅ resuelto". Botón
  **+ Crear desafío**.
- **`/desafios/crear`** — form: título, consigna, **región** (selector), nombre de función,
  starter, solución, editor de casos (agregar args + marcar ejemplo), botón **Validar y
  publicar** (corre la solución en Pyodide y publica).
- **`/desafios/[id]`** (resolver) — consigna + ejemplos + editor (reusa `editor.js`) +
  ▶ Probar / Enviar. Tras resolver: pestaña **"Soluciones de la comunidad"** (ordenadas por
  👍) — visible solo si lo resolviste.

### Integración
- Resolver da **+balls** (primera vez) y suma a tu perfil público (`publico.desafios`).
- Nav: entrada **"Desafíos"**. Ranking de autores/solvers (futuro o en `/amigos`).

## Seguridad / moderación
- Todo corre en **Pyodide** (sandbox del navegador) con timeout.
- La solución del autor no viaja al solver (solo `esperado` por caso). *Limitación
  conocida:* al ser client-side, un usuario avanzado podría leer los `esperados` y
  hardcodear; aceptable para un juego de aprendizaje, mitigado por casos ocultos (no
  `ejemplo`).
- **Reportar** un desafío (flag) + los rotos no se publican (validación al crear).

## Fases (para el plan)
1. **MVP**: tablas `desafios`/`resoluciones` + RPCs core; `/desafios/crear`, `/desafios/[id]`
   (resolver + corrección Pyodide), `/desafios` (lista). Recompensa balls.
2. **Social**: ver soluciones (gated) + `votos` + ordenar; stats en el perfil; nav + ranking.
3. **Pulido**: reportar, filtros, dificultad por votos.

## Verificación
- `npm run build` + prueba manual: crear un desafío, resolverlo desde otra cuenta, ver
  soluciones tras resolver, votar. Sin runner JS; la corrección se prueba a mano en Pyodide.
- Migraciones SQL aplicadas con `supabase db push --yes`.

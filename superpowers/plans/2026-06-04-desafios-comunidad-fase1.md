# Desafíos de la comunidad — Fase 1 (MVP) — Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development.
> Ubicación `superpowers/` (raíz), NO `docs/`. Diseño:
> `superpowers/specs/2026-06-04-desafios-comunidad-design.md`.

**Goal:** Que cualquier usuario cree retos de Python (solución + casos) y que la comunidad
los resuelva con corrección automática en Pyodide, ganando Pokéballs.

**Architecture:** Tablas Supabase `desafios`/`resoluciones` + RPCs `security definer`. La
corrección corre 100% en el navegador con Pyodide (sin pytest: se compara `json.dumps` de la
función del solver vs los `esperados` que el autor precomputó al publicar). 3 páginas Astro
(`/desafios`, `/desafios/crear`, `/desafios/[id]`) que reusan `editor.js` + el patrón de
carga de Pyodide de los ejercicios.

**Tech Stack:** Astro (vanilla JS), Supabase (Postgres RPC), Pyodide (CDN), CodeMirror.

**Testing:** sin runner JS. Cada tarea verifica con `npm run build` (desde `web/`) + prueba
manual. Migración: `supabase db push --yes`.

**Nota de contexto del repo (para subagentes):**
- Migraciones en `supabase/migrations/` (timestamp-prefijo). Patrón de RPC `security
  definer set search_path = public`; mutaciones sensibles SIEMPRE por RPC.
- `web/src/lib/supa.js` exporta `supa` y `haySupabase`. `web/src/lib/nube.js` exporta
  `usuario()`, `refrescarDesdeNube()`. `web/src/lib/social.js` es el patrón de "API sobre
  RPCs".
- Editor: `web/src/lib/editor.js` → `editorPython({ doc, parent, onRun, onChange })`.
- Pyodide se carga con `<script is:inline src="https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"></script>`
  y `await window.loadPyodide()` (ver `web/src/pages/ejercicios/[slug]/[ex].astro`).
- Nav en `web/src/layouts/Base.astro` (array `nav`). Links internos con `u('/ruta')`.
- Build desde `web/`: `npm run build` (regenera `../docs`). Commitear `web/` + `docs/` juntos.
- Reglas de commit del repo: NO agregar atribución a Claude/Anthropic.

---

### Task 1: Migración SQL — `desafios` + `resoluciones` + RPCs

**Files:**
- Create: `supabase/migrations/20260605000001_desafios.sql`

- [ ] **Step 1: Escribir la migración**

```sql
-- Desafíos de la comunidad (estilo CodeWars). Corrección client-side en Pyodide:
-- el autor precomputa los 'esperados' al publicar; acá solo se guardan.

create table if not exists public.desafios (
  id          uuid primary key default gen_random_uuid(),
  autor       uuid not null references auth.users(id) on delete cascade,
  titulo      text not null,
  consigna    text not null default '',
  func        text not null,                          -- nombre de la función a implementar
  starter     text not null default '',
  casos       jsonb not null default '[]'::jsonb,     -- [{args:[...], esperado:"<json>", ejemplo:bool}]
  dificultad  int  not null default 3,                -- 1..8
  region      text not null default 'libre',          -- kanto|johto|hoenn|sinnoh|unova|kalos|libre
  creado      timestamptz not null default now()
);
alter table public.desafios enable row level security;
drop policy if exists "desafios select publico" on public.desafios;
create policy "desafios select publico" on public.desafios for select using (true);

create table if not exists public.resoluciones (
  id         uuid primary key default gen_random_uuid(),
  desafio_id uuid not null references public.desafios(id) on delete cascade,
  user_id    uuid not null references auth.users(id) on delete cascade,
  codigo     text not null default '',
  creado     timestamptz not null default now(),
  unique (desafio_id, user_id)
);
alter table public.resoluciones enable row level security;
-- spoiler-gate: ves resoluciones de un desafío solo si vos lo resolviste (o sos el autor)
drop policy if exists "resoluciones select gated" on public.resoluciones;
create policy "resoluciones select gated" on public.resoluciones for select using (
  auth.uid() = user_id
  or exists (select 1 from public.resoluciones r where r.desafio_id = resoluciones.desafio_id and r.user_id = auth.uid())
  or exists (select 1 from public.desafios d where d.id = resoluciones.desafio_id and d.autor = auth.uid())
);

create or replace function public.crear_desafio(
  p_titulo text, p_consigna text, p_func text, p_starter text,
  p_casos jsonb, p_dificultad int, p_region text)
returns uuid language plpgsql security definer set search_path = public as $$
declare nid uuid;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  if coalesce(trim(p_titulo),'') = '' then raise exception 'falta el título'; end if;
  if coalesce(trim(p_func),'') = '' then raise exception 'falta el nombre de la función'; end if;
  if p_casos is null or jsonb_array_length(p_casos) = 0 then raise exception 'faltan casos'; end if;
  insert into desafios(autor, titulo, consigna, func, starter, casos, dificultad, region)
    values (auth.uid(), trim(p_titulo), coalesce(p_consigna,''), trim(p_func), coalesce(p_starter,''),
            p_casos, greatest(1, least(8, coalesce(p_dificultad,3))),
            case when p_region in ('kanto','johto','hoenn','sinnoh','unova','kalos','libre') then p_region else 'libre' end)
    returning id into nid;
  return nid;
end; $$;

-- registrar resolución + recompensar balls la PRIMERA vez (sobre progreso).
create or replace function public.registrar_resolucion(p_desafio_id uuid, p_codigo text)
returns int language plpgsql security definer set search_path = public as $$
declare ya boolean; dif int; est jsonb; balls int; premio int;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  select exists(select 1 from resoluciones where desafio_id = p_desafio_id and user_id = auth.uid()) into ya;
  insert into resoluciones(desafio_id, user_id, codigo)
    values (p_desafio_id, auth.uid(), coalesce(p_codigo,''))
    on conflict (desafio_id, user_id) do update set codigo = excluded.codigo, creado = now();
  if ya then return 0; end if;                          -- ya estaba resuelto: sin premio
  select dificultad into dif from desafios where id = p_desafio_id;
  premio := 2 * coalesce(dif, 3);                       -- balls = 2 × dificultad
  select estado into est from progreso where user_id = auth.uid() for update;
  est := coalesce(est, '{}'::jsonb);
  balls := coalesce((est->>'col:balls')::int, 0) + premio;
  est := jsonb_set(est, '{col:balls}', to_jsonb(balls::text));
  insert into progreso(user_id, estado) values (auth.uid(), est)
    on conflict (user_id) do update set estado = excluded.estado, actualizado = now();
  return premio;
end; $$;

create or replace function public.listar_desafios(p_orden text, p_q text, p_region text, p_limite int, p_offset int)
returns table(id uuid, titulo text, dificultad int, region text, autor_handle text,
              resoluciones bigint, resuelto boolean)
language sql security definer set search_path = public as $$
  select d.id, d.titulo, d.dificultad, d.region, p.handle,
         (select count(*) from resoluciones r where r.desafio_id = d.id),
         exists(select 1 from resoluciones r2 where r2.desafio_id = d.id and r2.user_id = auth.uid())
  from desafios d
  left join perfiles p on p.user_id = d.autor
  where (p_region is null or p_region = '' or p_region = 'todas' or d.region = p_region)
    and (p_q is null or trim(p_q) = '' or d.titulo ilike '%'||trim(p_q)||'%')
  order by case when p_orden = 'resueltos' then (select count(*) from resoluciones r where r.desafio_id = d.id) end desc nulls last,
           case when p_orden = 'dificultad' then d.dificultad end desc nulls last,
           d.creado desc
  limit greatest(1, least(coalesce(p_limite, 30), 60)) offset greatest(0, coalesce(p_offset, 0));
$$;
```

- [ ] **Step 2: Verificar sintaxis a ojo.** No se aplica todavía (Task 8 hace el `db push`).

---

### Task 2: API cliente — `web/src/lib/desafios.js`

**Files:**
- Create: `web/src/lib/desafios.js`

- [ ] **Step 1: Crear el archivo**

```js
// desafios.js — API de los desafíos de la comunidad (RPCs + lecturas).
import { supa, haySupabase } from './supa.js';

export async function crearDesafio(d) {
  const { data, error } = await supa.rpc('crear_desafio', {
    p_titulo: d.titulo, p_consigna: d.consigna, p_func: d.func, p_starter: d.starter,
    p_casos: d.casos, p_dificultad: d.dificultad, p_region: d.region,
  });
  if (error) throw error;
  return data; // id
}
export async function leerDesafio(id) {
  const { data, error } = await supa.from('desafios').select('*').eq('id', id).maybeSingle();
  if (error) throw error;
  return data;
}
export async function listarDesafios({ orden = 'recientes', q = '', region = 'todas', limite = 30, offset = 0 } = {}) {
  const { data, error } = await supa.rpc('listar_desafios', {
    p_orden: orden, p_q: q, p_region: region, p_limite: limite, p_offset: offset,
  });
  if (error) throw error;
  return data || [];
}
export async function registrarResolucion(desafioId, codigo) {
  const { data, error } = await supa.rpc('registrar_resolucion', { p_desafio_id: desafioId, p_codigo: codigo });
  if (error) throw error;
  return data; // balls ganadas (0 si ya estaba)
}
export { haySupabase };
```

- [ ] **Step 2: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 3: Helper de corrección en Pyodide — `web/src/lib/desafios-eval.py`

**Files:**
- Create: `web/src/lib/desafios-eval.py`

- [ ] **Step 1: Crear el helper Python** (se inyecta en Pyodide y expone `evaluar`)

```python
# desafios-eval.py — corre el código del usuario y evalúa la función sobre los casos.
import json

def _norm(v):
    # representación canónica para comparar (independiente del orden de claves de dict)
    return json.dumps(v, sort_keys=True, default=str)

def computar_esperados(codigo, func, casos_json):
    """Para el AUTOR al publicar: corre la solución y devuelve los casos con 'esperado'.
    casos_json = [{"args":[...], "ejemplo":bool}, ...]. Devuelve JSON o {error:...}."""
    casos = json.loads(casos_json)
    g = {"__name__": "__main__"}
    try:
        exec(codigo, g)
        fn = g.get(func)
        if not callable(fn):
            return json.dumps({"error": "No se encontró la función '%s'." % func})
        out = []
        for c in casos:
            args = c.get("args", [])
            esperado = _norm(fn(*args))
            out.append({"args": args, "esperado": esperado, "ejemplo": bool(c.get("ejemplo"))})
        return json.dumps({"casos": out})
    except Exception as e:
        return json.dumps({"error": "%s: %s" % (type(e).__name__, e)})

def evaluar(codigo, func, casos_json):
    """Para el SOLVER: corre su código y compara contra los 'esperado' guardados.
    Devuelve JSON {ok:bool, fallos:[{i, args, esperado, obtenido|error}]}."""
    casos = json.loads(casos_json)
    g = {"__name__": "__main__"}
    try:
        exec(codigo, g)
    except Exception as e:
        return json.dumps({"ok": False, "error": "Tu código tiene un error: %s: %s" % (type(e).__name__, e)})
    fn = g.get(func)
    if not callable(fn):
        return json.dumps({"ok": False, "error": "Definí una función llamada '%s'." % func})
    fallos = []
    for i, c in enumerate(casos):
        args = c.get("args", [])
        try:
            obtenido = _norm(fn(*args))
            if obtenido != c.get("esperado"):
                fallos.append({"i": i, "args": args if c.get("ejemplo") else None,
                               "esperado": c.get("esperado") if c.get("ejemplo") else None,
                               "obtenido": obtenido if c.get("ejemplo") else None})
        except Exception as e:
            fallos.append({"i": i, "args": args if c.get("ejemplo") else None,
                           "error": "%s: %s" % (type(e).__name__, e)})
    return json.dumps({"ok": len(fallos) == 0, "fallos": fallos})
```

- [ ] **Step 2: Verificar** — `cd web && npm run build`. El `.py` se importa con `?raw` en
  las páginas (Task 4/5); acá solo confirmar que el build sigue OK.

---

### Task 4: Página crear — `web/src/pages/desafios/crear.astro`

**Files:**
- Create: `web/src/pages/desafios/crear.astro`

- [ ] **Step 1: Crear la página.** Form con: título, región (select), consigna, nombre de
  función, starter, solución (editor), y casos (textarea con un array JSON de
  `[{args:[...], ejemplo:true}]`). Botón "Validar y publicar": carga Pyodide, corre
  `computar_esperados(solucion, func, casos)`; si OK, llama `crearDesafio` con los casos
  (que ya incluyen `esperado`) y redirige a `/desafios/<id>`.

```astro
---
import Base from '../../layouts/Base.astro';
import { u } from '../../lib/url.ts';
const REGIONES = [['libre','Libre'],['kanto','Kanto · fundamentos'],['johto','Johto · datos'],['hoenn','Hoenn · Flask'],['sinnoh','Sinnoh · SQL'],['unova','Unova · IA'],['kalos','Kalos · testing']];
---
<Base title="Crear desafío — Python con Pokémon" active="Desafíos">
  <main class="wrap">
    <h1>✍️ Crear un desafío</h1>
    <p>Definí una función a implementar, escribí tu solución de referencia y los casos de prueba. Al publicar, calculamos los resultados esperados (tu solución no se muestra a nadie).</p>
    <div class="df-form">
      <label>Título<input id="d-titulo" maxlength="80" placeholder="Sumar los pares de una lista" /></label>
      <label>Región<select id="d-region">{REGIONES.map(([v,t]) => <option value={v}>{t}</option>)}</select></label>
      <label>Dificultad (1-8)<input id="d-dif" type="number" min="1" max="8" value="3" /></label>
      <label>Consigna<textarea id="d-consigna" rows="3" placeholder="Devolvé la suma de los números pares de la lista."></textarea></label>
      <label>Nombre de la función<input id="d-func" placeholder="sumar_pares" /></label>
      <label>Código inicial (starter, opcional)<textarea id="d-starter" rows="2" placeholder="def sumar_pares(nums):\n    pass"></textarea></label>
      <label>Tu solución (no se publica)<div class="cw"><div class="cw-bar"><span class="cw-lang">python</span></div><div id="d-sol"></div></div></label>
      <label>Casos de prueba — array JSON: cada uno <code>{`{"args": [...], "ejemplo": true}`}</code><textarea id="d-casos" rows="4" placeholder='[{"args": [[1,2,3,4]], "ejemplo": true}, {"args": [[]], "ejemplo": false}]'></textarea></label>
      <button class="btn-grande" id="d-publicar" type="button">✅ Validar y publicar</button>
      <p class="auth-msg err" id="d-err" hidden></p>
    </div>
  </main>
  <script is:inline src="https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"></script>
  <script>
    import { editorPython } from '../../lib/editor.js';
    import evalPy from '../../lib/desafios-eval.py?raw';
    import { crearDesafio } from '../../lib/desafios.js';
    import { usuario } from '../../lib/nube.js';
    const $ = (id) => document.getElementById(id);
    const B = (window.__BASE || '/').replace(/\/$/, '');
    const sol = editorPython({ doc: '', parent: $('d-sol') });
    let py = null;
    async function getPy() {
      if (!py) { py = await window.loadPyodide(); await py.runPythonAsync(evalPy); }
      return py;
    }
    $('d-publicar').addEventListener('click', async () => {
      const err = $('d-err'); err.hidden = true;
      if (!usuario()) { err.textContent = 'Iniciá sesión para crear desafíos.'; err.hidden = false; return; }
      const func = $('d-func').value.trim();
      let casos;
      try { casos = JSON.parse($('d-casos').value); if (!Array.isArray(casos) || !casos.length) throw 0; }
      catch { err.textContent = 'Los casos deben ser un array JSON no vacío.'; err.hidden = false; return; }
      const b = $('d-publicar'); b.disabled = true; b.textContent = 'Validando…';
      try {
        const p = await getPy();
        p.globals.set('_cod', sol.state.doc.toString());
        p.globals.set('_func', func);
        p.globals.set('_casos', JSON.stringify(casos));
        const res = JSON.parse(await p.runPythonAsync('computar_esperados(_cod, _func, _casos)'));
        if (res.error) { err.textContent = '⚠️ ' + res.error; err.hidden = false; return; }
        const id = await crearDesafio({
          titulo: $('d-titulo').value, consigna: $('d-consigna').value, func,
          starter: $('d-starter').value, casos: res.casos,
          dificultad: Number($('d-dif').value) || 3, region: $('d-region').value,
        });
        location.href = B + '/desafios/' + id;
      } catch (e) { err.textContent = '⚠️ ' + (e.message || e); err.hidden = false; }
      finally { b.disabled = false; b.textContent = '✅ Validar y publicar'; }
    });
  </script>
</Base>
```

- [ ] **Step 2: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 5: Página resolver — `web/src/pages/desafios/[id].astro`

**Files:**
- Create: `web/src/pages/desafios/[id].astro`

- [ ] **Step 1: Crear la página.** Es dinámica por id pero **sin prerender de todos los ids**
  (los desafíos viven en la DB). Astro necesita `getStaticPaths` para rutas `[id]`; con
  output estático no se puede prerenderizar ids desconocidos. **Solución:** usar una ruta
  estática `/desafios/ver` que lee `?id=` del query (igual que `/u?h=`), NO `[id]`.

  → **Renombrar esta tarea: crear `web/src/pages/desafios/ver.astro`** (lee `?id=`), y los
  links a desafíos usan `/desafios/ver?id=<id>`. (Coherente con cómo `/u` resuelve por query.)

```astro
---
import Base from '../../layouts/Base.astro';
---
<Base title="Desafío — Python con Pokémon" active="Desafíos">
  <main class="wrap">
    <p id="dv-cargando">Cargando…</p>
    <article id="dv-cont" hidden>
      <div class="df-cab"><span class="df-region" id="dv-region"></span><span class="df-dif" id="dv-dif"></span></div>
      <h1 id="dv-titulo"></h1>
      <p class="df-autor" id="dv-autor"></p>
      <p class="ej-prompt" id="dv-consigna"></p>
      <div class="df-ejemplos" id="dv-ejemplos"></div>
      <div class="cw"><div class="cw-bar"><span class="cw-lang">python</span><span class="cw-hint">✎ tu solución</span></div><div id="dv-editor"></div></div>
      <div class="ejer-acciones">
        <button class="btn-corregir" id="dv-enviar" type="button">▶ Probar / Enviar</button>
        <span class="ejer-estado" id="dv-estado"></span>
      </div>
      <div class="ejer-result" id="dv-result"></div>
    </article>
  </main>
  <script is:inline src="https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"></script>
  <script>
    import { editorPython } from '../../lib/editor.js';
    import evalPy from '../../lib/desafios-eval.py?raw';
    import { leerDesafio, registrarResolucion } from '../../lib/desafios.js';
    import { usuario, refrescarDesdeNube } from '../../lib/nube.js';
    const $ = (id) => document.getElementById(id);
    const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ '&':'&amp;','<':'&lt;','>':'&gt;' }[c]));
    const REGN = { kanto:'🔴 Kanto', johto:'⚪ Johto', hoenn:'🟢 Hoenn', sinnoh:'🔵 Sinnoh', unova:'⚫ Unova', kalos:'🟠 Kalos', libre:'🎲 Libre' };
    const id = new URLSearchParams(location.search).get('id');
    let des = null, editor = null, py = null;
    async function getPy() { if (!py) { py = await window.loadPyodide(); await py.runPythonAsync(evalPy); } return py; }

    async function arrancar() {
      if (!id) { $('dv-cargando').textContent = 'Desafío no encontrado.'; return; }
      des = await leerDesafio(id);
      if (!des) { $('dv-cargando').textContent = 'Desafío no encontrado.'; return; }
      $('dv-cargando').hidden = true; $('dv-cont').hidden = false;
      $('dv-region').textContent = REGN[des.region] || des.region;
      $('dv-dif').textContent = '★'.repeat(des.dificultad);
      $('dv-titulo').textContent = des.titulo;
      $('dv-consigna').textContent = des.consigna;
      const ejs = (des.casos || []).filter((c) => c.ejemplo);
      $('dv-ejemplos').innerHTML = ejs.length ? '<b>Ejemplos:</b>' + ejs.map((c) =>
        '<div class="df-ej"><code>' + esc(des.func) + '(' + esc(c.args.map((a) => JSON.stringify(a)).join(', ')) + ')</code> → <code>' + esc(c.esperado) + '</code></div>').join('') : '';
      editor = editorPython({ doc: des.starter || ('def ' + des.func + '():\n    '), parent: $('dv-editor'), onRun: enviar });
    }
    async function enviar() {
      if (!usuario()) { $('dv-estado').textContent = 'Iniciá sesión para enviar.'; return; }
      const b = $('dv-enviar'); b.disabled = true; $('dv-estado').textContent = 'Corriendo…';
      try {
        const p = await getPy();
        p.globals.set('_cod', editor.state.doc.toString());
        p.globals.set('_func', des.func);
        p.globals.set('_casos', JSON.stringify(des.casos));
        const res = JSON.parse(await p.runPythonAsync('evaluar(_cod, _func, _casos)'));
        const box = $('dv-result');
        if (res.ok) {
          let premio = 0;
          try { premio = await registrarResolucion(id, editor.state.doc.toString()); await refrescarDesdeNube(); } catch {}
          box.innerHTML = '<div class="ejer-resumen win">✅ ¡Resuelto!' + (premio ? ' +' + premio + ' 🔴 Pokéballs' : '') + '</div>';
        } else if (res.error) {
          box.innerHTML = '<div class="ejer-err">⚠️ ' + esc(res.error) + '</div>';
        } else {
          const f = res.fallos[0];
          let det = 'Falló ' + res.fallos.length + ' caso(s).';
          if (f && f.args) det += ' Ej: <code>' + esc(des.func) + '(' + esc(f.args.map((a) => JSON.stringify(a)).join(', ')) + ')</code> esperaba <code>' + esc(f.esperado) + '</code>' + (f.obtenido != null ? ', diste <code>' + esc(f.obtenido) + '</code>' : (f.error ? ' (' + esc(f.error) + ')' : ''));
          box.innerHTML = '<div class="ejer-err">❌ ' + det + '</div>';
        }
      } catch (e) { $('dv-result').innerHTML = '<div class="ejer-err">⚠️ ' + esc((e && e.message) || e) + '</div>'; }
      finally { b.disabled = false; $('dv-estado').textContent = ''; }
    }
    $('dv-enviar').addEventListener('click', enviar);
    arrancar();
  </script>
</Base>
```

- [ ] **Step 2: Verificar** — `cd web && npm run build`. Esperado: build OK (la página es
  `desafios/ver.astro`, estática, lee `?id=`).

---

### Task 6: Página lista — `web/src/pages/desafios/index.astro`

**Files:**
- Create: `web/src/pages/desafios/index.astro`

- [ ] **Step 1: Crear la página.** Buscador + chips de región + orden + botón Crear; lista
  desde `listarDesafios`. Cada item linkea a `/desafios/ver?id=<id>`.

```astro
---
import Base from '../../layouts/Base.astro';
import { u } from '../../lib/url.ts';
const REGIONES = [['todas','Todas'],['libre','🎲 Libre'],['kanto','🔴 Kanto'],['johto','⚪ Johto'],['hoenn','🟢 Hoenn'],['sinnoh','🔵 Sinnoh'],['unova','⚫ Unova'],['kalos','🟠 Kalos']];
---
<Base title="Desafíos de la comunidad — Python con Pokémon" active="Desafíos">
  <main class="wrap">
    <div class="safari-head"><h1>🧩 Desafíos de la comunidad</h1><a class="btn-grande" href={u('/desafios/crear')}>✍️ Crear desafío</a></div>
    <p>Retos de Python hechos por la comunidad. Resolvelos y ganá Pokéballs. ¡Creá los tuyos!</p>
    <div class="dex-controles">
      <input class="dex-buscar" id="df-q" type="search" placeholder="🔍 Buscar por título…" />
      <select id="df-orden"><option value="recientes">Recientes</option><option value="resueltos">Más resueltos</option><option value="dificultad">Dificultad</option></select>
    </div>
    <div class="dex-filtros" id="df-regiones">{REGIONES.map(([v,t],i) => <button class={'dex-f' + (i===0?' activo':'')} data-r={v} type="button">{t}</button>)}</div>
    <div class="df-lista" id="df-lista"></div>
    <p id="df-login" hidden>Iniciá sesión para crear y resolver desafíos.</p>
  </main>
  <script>
    import { listarDesafios } from '../../lib/desafios.js';
    import { usuario } from '../../lib/nube.js';
    const $ = (id) => document.getElementById(id);
    const B = (window.__BASE || '/').replace(/\/$/, '');
    const REGN = { kanto:'🔴', johto:'⚪', hoenn:'🟢', sinnoh:'🔵', unova:'⚫', kalos:'🟠', libre:'🎲' };
    let region = 'todas';
    async function cargar() {
      const lista = await listarDesafios({ orden: $('df-orden').value, q: $('df-q').value, region }).catch(() => []);
      const cont = $('df-lista');
      cont.innerHTML = lista.length ? lista.map((d) =>
        '<a class="df-item' + (d.resuelto ? ' ok' : '') + '" href="' + B + '/desafios/ver?id=' + d.id + '">' +
        '<span class="df-reg">' + (REGN[d.region]||'🎲') + '</span><span class="df-tit">' + (d.resuelto ? '✅ ' : '') + d.titulo + '</span>' +
        '<span class="df-meta">★' + d.dificultad + ' · ' + d.resoluciones + ' resueltos · @' + (d.autor_handle || '?') + '</span></a>').join('')
        : '<p class="tr-colec-vacio">No hay desafíos todavía. ¡Creá el primero!</p>';
    }
    $('df-q').addEventListener('input', cargar);
    $('df-orden').addEventListener('change', cargar);
    $('df-regiones').querySelectorAll('.dex-f').forEach((b) => b.addEventListener('click', () => {
      $('df-regiones').querySelectorAll('.dex-f').forEach((x) => x.classList.remove('activo'));
      b.classList.add('activo'); region = b.dataset.r; cargar();
    }));
    cargar();
  </script>
</Base>
```

- [ ] **Step 2: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 7: Nav + estilos

**Files:**
- Modify: `web/src/layouts/Base.astro` (array `nav`)
- Modify: `web/src/styles/global.css`

- [ ] **Step 1: Nav** — en el array `nav` de Base.astro, agregar `['Desafíos', '/desafios'],`
  después de `['Amigos', '/amigos'],`.

- [ ] **Step 2: Estilos** — agregar al final del bloque de estilos de intercambio/social en
  `global.css`:

```css
/* desafíos de la comunidad */
.df-form{ display:flex; flex-direction:column; gap:12px; max-width:680px; }
.df-form label{ display:flex; flex-direction:column; gap:5px; font-weight:700; font-size:.9rem; }
.df-form input, .df-form select, .df-form textarea{ font:inherit; font-weight:400; padding:9px 12px; border:1px solid var(--line); border-radius:12px; background:var(--card); color:var(--ink); }
.df-form textarea{ font-family:var(--font-mono); }
.df-form code{ font-size:.85em; }
.df-lista{ display:flex; flex-direction:column; gap:8px; margin-top:.8rem; }
.df-item{ display:flex; align-items:center; gap:10px; background:var(--paper-2); border:1px solid var(--line); border-radius:12px; padding:10px 14px; text-decoration:none; color:var(--ink); }
.df-item.ok{ border-color:#1f8b4c; }
.df-item .df-reg{ font-size:1.1rem; flex:none; }
.df-item .df-tit{ flex:1; font-weight:700; }
.df-item .df-meta{ color:var(--ink-soft); font-size:.8rem; flex:none; }
.df-cab{ display:flex; gap:10px; align-items:center; }
.df-region{ background:var(--paper-2); border:1px solid var(--line); border-radius:9px; padding:2px 9px; font-size:.85rem; }
.df-dif{ color:var(--yellow-deep); }
.df-autor{ color:var(--ink-soft); font-size:.85rem; }
.df-ejemplos{ background:var(--paper-2); border:1px solid var(--line); border-radius:12px; padding:10px 14px; margin:.6rem 0; font-size:.9rem; }
.df-ej{ font-family:var(--font-mono); font-size:.82rem; margin-top:4px; }
.df-ej code{ background:var(--card); border:1px solid var(--line); border-radius:5px; padding:0 4px; }
@media(max-width:560px){ .df-item{ flex-wrap:wrap; } .df-item .df-meta{ flex-basis:100%; } }
```

- [ ] **Step 3: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 8: Aplicar migración + build + prueba manual + commit

**Files:** ninguno nuevo

- [ ] **Step 1: Aplicar la migración** — `supabase db push --yes` (desde la raíz del repo).
  Esperado: aplica `20260605000001_desafios.sql`.
- [ ] **Step 2: Build** — `cd web && npm run build`. Esperado: build OK.
- [ ] **Step 3: Commit** — `git add -A && git commit` con `web/`, `docs/`, `supabase/migrations/`,
  `superpowers/`. (Sin atribución a Claude.)
- [ ] **Step 4: Prueba manual (post-deploy, manual del owner):** crear un desafío, resolverlo
  desde otra cuenta, ver que da balls y aparece "✅ resuelto" en la lista.

---

## Self-Review
- **Cobertura del spec (Fase 1):** crear (Task 1 RPC + Task 4 página) ✓; resolver+corrección
  Pyodide (Task 3 helper + Task 5 página) ✓; lista+filtro región (Task 1 `listar_desafios` +
  Task 6) ✓; recompensa balls (Task 1 `registrar_resolucion`) ✓; categorías por región (Task 1
  `region` + Task 4/6) ✓; nav (Task 7) ✓. Las soluciones-de-la-comunidad + votos son **Fase 2**
  (no en este plan).
- **Ruta dinámica:** el sitio es estático → no se pueden prerenderizar ids desconocidos; se usa
  `desafios/ver.astro` con `?id=` (patrón de `/u`). Los links usan `/desafios/ver?id=`.
- **Consistencia:** `crearDesafio`/`leerDesafio`/`listarDesafios`/`registrarResolucion` (desafios.js)
  = `crear_desafio`/`listar_desafios`/`registrar_resolucion` (SQL) ✓; `computar_esperados`/`evaluar`
  (desafios-eval.py) usadas en Task 4/5 ✓; shape de `casos` `{args, esperado, ejemplo}` consistente ✓.
- **Sin placeholders:** SQL/JS/Python completos.

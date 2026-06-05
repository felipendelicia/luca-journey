# Desafíos de la comunidad — Fase 2 (social) — Plan

> Ejecutar con subagentes. Ubicación `superpowers/`. Diseño:
> `superpowers/specs/2026-06-04-desafios-comunidad-design.md`. Construye sobre Fase 1
> (commit `456d6c1d`): tablas `desafios`/`resoluciones`, RPCs `crear_desafio`/
> `registrar_resolucion`/`listar_desafios`, páginas `/desafios`, `/desafios/crear`,
> `/desafios/ver?id=`, `web/src/lib/desafios.js`, `web/src/lib/desafios-eval.py`.

**Goal:** Después de resolver un desafío, ver las soluciones de toda la comunidad (gated,
sin spoilers), votarlas con 👍, y mostrar en el perfil cuántos resolviste/creaste.

**Tech Stack:** Astro, Supabase (RPC), CodeMirror (solo lectura para mostrar código).

**Testing:** `npm run build` desde `web/` + prueba manual. Migración: `supabase db push --yes`
(la aplica el controller, NO el subagente).

---

### Task 1: Migración — `votos` + RPCs sociales

**Files:** Create `supabase/migrations/20260605000002_desafios_social.sql`

```sql
-- Votos a soluciones + ver soluciones (gated) + stats de desafíos.

create table if not exists public.votos (
  resolucion_id uuid not null references public.resoluciones(id) on delete cascade,
  user_id       uuid not null references auth.users(id) on delete cascade,
  primary key (resolucion_id, user_id)
);
alter table public.votos enable row level security;
-- lectura/escritura solo por RPC security definer (sin policies directas)

-- Soluciones de un desafío: SOLO si vos lo resolviste (o sos el autor). Sin spoilers.
create or replace function public.soluciones_de(p_desafio_id uuid)
returns table(id uuid, codigo text, autor_handle text, votos bigint, mi_voto boolean, es_mia boolean)
language sql security definer set search_path = public as $$
  select r.id, r.codigo, p.handle,
         (select count(*) from votos v where v.resolucion_id = r.id),
         exists(select 1 from votos v2 where v2.resolucion_id = r.id and v2.user_id = auth.uid()),
         (r.user_id = auth.uid())
  from resoluciones r
  left join perfiles p on p.user_id = r.user_id
  where r.desafio_id = p_desafio_id
    and (exists(select 1 from resoluciones rr where rr.desafio_id = p_desafio_id and rr.user_id = auth.uid())
         or exists(select 1 from desafios d where d.id = p_desafio_id and d.autor = auth.uid()))
  order by (select count(*) from votos v where v.resolucion_id = r.id) desc, r.creado;
$$;

create or replace function public.votar(p_resolucion_id uuid, p_on boolean)
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  if p_on then
    insert into votos(resolucion_id, user_id) values (p_resolucion_id, auth.uid()) on conflict do nothing;
  else
    delete from votos where resolucion_id = p_resolucion_id and user_id = auth.uid();
  end if;
end; $$;

-- Conteos públicos de un usuario (para el perfil): cuántos resolvió / creó.
create or replace function public.stats_desafios(p_user_id uuid)
returns table(resueltos bigint, creados bigint)
language sql security definer set search_path = public as $$
  select (select count(*) from resoluciones where user_id = p_user_id),
         (select count(*) from desafios where autor = p_user_id);
$$;
```

- [ ] Verificar sintaxis a ojo. (La aplica el controller con `db push`.)

---

### Task 2: API cliente — agregar a `web/src/lib/desafios.js`

**Files:** Modify `web/src/lib/desafios.js`

Agregar antes de `export { haySupabase };`:

```js
export async function solucionesDe(desafioId) {
  const { data, error } = await supa.rpc('soluciones_de', { p_desafio_id: desafioId });
  if (error) throw error;
  return data || [];
}
export async function votar(resolucionId, on) {
  const { error } = await supa.rpc('votar', { p_resolucion_id: resolucionId, p_on: on });
  if (error) throw error;
}
export async function statsDesafios(userId) {
  const { data, error } = await supa.rpc('stats_desafios', { p_user_id: userId });
  if (error) throw error;
  return Array.isArray(data) ? data[0] : data; // {resueltos, creados}
}
```

- [ ] Verificar — `cd web && npm run build`. Esperado: build OK.

---

### Task 3: Mostrar soluciones de la comunidad en `web/src/pages/desafios/ver.astro`

**Files:** Modify `web/src/pages/desafios/ver.astro`

- [ ] **Step 1: Markup** — agregar, dentro de `<article id="dv-cont">`, después del
  `<div class="ejer-result" id="dv-result"></div>`:

```html
      <section class="df-sols" id="dv-sols" hidden>
        <h2 class="liga-h">💡 Soluciones de la comunidad</h2>
        <div id="dv-sols-lista"></div>
      </section>
```

- [ ] **Step 2: Imports** — en el `<script>`, agregar a la línea de import de `desafios.js`
  las funciones `solucionesDe, votar`:

```js
    import { leerDesafio, registrarResolucion, solucionesDe, votar } from '../../lib/desafios.js';
```

- [ ] **Step 3: Render de soluciones** — agregar estas funciones en el `<script>` (antes de
  `arrancar`):

```js
    async function pintarSoluciones() {
      let sols = [];
      try { sols = await solucionesDe(id); } catch { sols = []; }
      if (!sols.length) { $('dv-sols').hidden = true; return; }   // gated: aún no resolviste
      $('dv-sols').hidden = false;
      const cont = $('dv-sols-lista'); cont.innerHTML = '';
      sols.forEach((s) => {
        const card = document.createElement('div'); card.className = 'df-sol';
        const pre = document.createElement('pre'); pre.className = 'df-sol-cod'; pre.textContent = s.codigo;
        const bar = document.createElement('div'); bar.className = 'df-sol-bar';
        const quien = document.createElement('span'); quien.textContent = (s.es_mia ? 'Tu solución' : ('@' + (s.autor_handle || '?')));
        const vbtn = document.createElement('button');
        vbtn.className = 'df-voto' + (s.mi_voto ? ' on' : '');
        vbtn.type = 'button'; vbtn.textContent = '👍 ' + s.votos;
        let voto = s.mi_voto, n = Number(s.votos);
        vbtn.addEventListener('click', async () => {
          voto = !voto; n += voto ? 1 : -1;
          vbtn.classList.toggle('on', voto); vbtn.textContent = '👍 ' + n;
          try { await votar(s.id, voto); } catch {}
        });
        bar.appendChild(quien); bar.appendChild(vbtn);
        card.appendChild(bar); card.appendChild(pre); cont.appendChild(card);
      });
    }
```

- [ ] **Step 4: Llamar pintarSoluciones** — al final de `arrancar()` (después de crear el
  editor) agregar `pintarSoluciones();`. Y en `enviar()`, dentro del `if (res.ok)` después
  de setear el `box.innerHTML`, agregar `pintarSoluciones();` (para que tras resolver se
  revelen).

- [ ] **Step 5: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 4: Stats de desafíos en el perfil público `web/src/pages/u.astro`

**Files:** Modify `web/src/pages/u.astro`

- [ ] **Step 1: Import** — agregar `statsDesafios` desde `desafios.js`:

```js
    import { statsDesafios } from '../lib/desafios.js';
```

- [ ] **Step 2:** En `pintarPerfil(p)`, después de armar `$('u-counts').innerHTML = ...`,
  agregar (al final de la función) una llamada async para sumar los conteos de desafíos al
  bloque de conteos:

```js
      statsDesafios(p.user_id).then((s) => {
        if (!s) return;
        const extra = '<div><b>' + (s.resueltos || 0) + '</b><small>desafíos</small></div>'
          + '<div><b>' + (s.creados || 0) + '</b><small>creados</small></div>';
        $('u-counts').insertAdjacentHTML('beforeend', extra);
      }).catch(() => {});
```

- [ ] **Step 3: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 5: Estilos

**Files:** Modify `web/src/styles/global.css`

Agregar después del bloque `/* desafíos de la comunidad */` (al final de esos estilos):

```css
.df-sols{ margin-top:1.6rem; }
.df-sols[hidden]{ display:none; }
.df-sol{ background:var(--paper-2); border:1px solid var(--line); border-radius:12px; margin-top:10px; overflow:hidden; }
.df-sol-bar{ display:flex; align-items:center; justify-content:space-between; padding:7px 12px; border-bottom:1px solid var(--line); font-size:.85rem; color:var(--ink-soft); }
.df-sol-cod{ margin:0; padding:11px 14px; background:var(--code-bg); color:#e8eaf2; font-family:var(--font-mono); font-size:12.5px; line-height:1.5; overflow:auto; white-space:pre; }
.df-voto{ border:1px solid var(--line); background:var(--card); color:var(--ink); border-radius:9px; font-weight:700; font-size:.8rem; padding:4px 10px; cursor:pointer; }
.df-voto.on{ background:var(--red); border-color:var(--red); color:#fff; }
```

- [ ] Verificar — `cd web && npm run build`. Esperado: build OK.

---

### Task 6: Aplicar migración + build + commit (controller)

- [ ] `supabase db push --yes` (controller).
- [ ] `cd web && npm run build`.
- [ ] Commit `web/` + `docs/` + `supabase/migrations/` + `superpowers/`. Sin atribución a Claude.

## Self-Review
- Cobertura Fase 2: ver soluciones gated (Task 1 `soluciones_de` + Task 3) ✓; votos (Task 1
  `votar`/`votos` + Task 3) ✓; stats en perfil (Task 1 `stats_desafios` + Task 4) ✓.
- Consistencia: `solucionesDe`/`votar`/`statsDesafios` (desafios.js) = `soluciones_de`/`votar`/
  `stats_desafios` (SQL) ✓; `soluciones_de` devuelve `es_mia` usado en Task 3 ✓.
- Gate: `soluciones_de` devuelve filas solo si resolviste o sos autor → si vuelve vacío, no
  se muestra la sección (no spoilers) ✓.

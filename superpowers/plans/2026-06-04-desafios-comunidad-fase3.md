# Desafíos de la comunidad — Fase 3 (moderación) — Plan

> Ejecutar con subagentes. Construye sobre Fase 1+2. Diseño:
> `superpowers/specs/2026-06-04-desafios-comunidad-design.md`.

**Goal:** Que un UGC sea sano: reportar desafíos rotos/inapropiados (auto-ocultar al juntar
varios reportes) y que el autor pueda borrar el suyo.

**Testing:** `npm run build` desde `web/`. Migración la aplica el controller.

---

### Task 1: Migración — `reportes` + RPCs + ocultar reportados

**Files:** Create `supabase/migrations/20260605000003_desafios_moderacion.sql`

```sql
-- Reportes a desafíos + borrar el propio. Un desafío con >=3 reporteros distintos se oculta
-- de los listados (salvo para su autor).

create table if not exists public.reportes (
  desafio_id uuid not null references public.desafios(id) on delete cascade,
  user_id    uuid not null references auth.users(id) on delete cascade,
  motivo     text not null default '',
  creado     timestamptz not null default now(),
  primary key (desafio_id, user_id)
);
alter table public.reportes enable row level security;
-- solo por RPC (sin policies directas)

create or replace function public.reportar_desafio(p_desafio_id uuid, p_motivo text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  insert into reportes(desafio_id, user_id, motivo)
    values (p_desafio_id, auth.uid(), left(coalesce(p_motivo,''), 200))
    on conflict (desafio_id, user_id) do update set motivo = excluded.motivo, creado = now();
end; $$;

create or replace function public.borrar_desafio(p_desafio_id uuid)
returns void language plpgsql security definer set search_path = public as $$
declare a uuid;
begin
  select autor into a from desafios where id = p_desafio_id;
  if a is null then raise exception 'no existe'; end if;
  if a <> auth.uid() then raise exception 'solo el autor puede borrarlo'; end if;
  delete from desafios where id = p_desafio_id;   -- cascade borra resoluciones/votos/reportes
end; $$;

-- listar_desafios: igual que antes pero ocultando los que juntaron >=3 reportes (salvo al autor).
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
    and (d.autor = auth.uid()
         or (select count(*) from reportes rp where rp.desafio_id = d.id) < 3)
  order by case when p_orden = 'resueltos' then (select count(*) from resoluciones r where r.desafio_id = d.id) end desc nulls last,
           case when p_orden = 'dificultad' then d.dificultad end desc nulls last,
           d.creado desc
  limit greatest(1, least(coalesce(p_limite, 30), 60)) offset greatest(0, coalesce(p_offset, 0));
$$;
```

- [ ] Verificar a ojo. (La aplica el controller.)

---

### Task 2: API cliente — agregar a `web/src/lib/desafios.js`

**Files:** Modify `web/src/lib/desafios.js`

Agregar antes de `export { haySupabase };`:

```js
export async function reportarDesafio(desafioId, motivo) {
  const { error } = await supa.rpc('reportar_desafio', { p_desafio_id: desafioId, p_motivo: motivo || '' });
  if (error) throw error;
}
export async function borrarDesafio(desafioId) {
  const { error } = await supa.rpc('borrar_desafio', { p_desafio_id: desafioId });
  if (error) throw error;
}
```

- [ ] Verificar — `cd web && npm run build`. Esperado: build OK.

---

### Task 3: Botones reportar / borrar en `web/src/pages/desafios/ver.astro`

**Files:** Modify `web/src/pages/desafios/ver.astro`

- [ ] **Step 1: Markup** — agregar, dentro de `<article id="dv-cont">`, justo después del
  `<p class="df-autor" id="dv-autor"></p>`:

```html
      <div class="df-mod"><button class="df-modbtn" id="dv-reportar" type="button">🚩 Reportar</button><button class="df-modbtn danger" id="dv-borrar" type="button" hidden>🗑️ Borrar (autor)</button></div>
```

- [ ] **Step 2: Imports** — agregar `reportarDesafio, borrarDesafio` al import de `desafios.js`:

```js
    import { leerDesafio, registrarResolucion, solucionesDe, votar, reportarDesafio, borrarDesafio } from '../../lib/desafios.js';
```

- [ ] **Step 3: Lógica** — importar `usuario` ya está. Al final de `arrancar()` (después de
  `pintarSoluciones();`) agregar:

```js
      if (usuario() && des.autor === usuario().id) $('dv-borrar').hidden = false;
      $('dv-reportar').addEventListener('click', async () => {
        if (!usuario()) { $('dv-estado').textContent = 'Iniciá sesión para reportar.'; return; }
        const motivo = prompt('¿Por qué lo reportás? (roto, inapropiado, etc.)') || '';
        try { await reportarDesafio(id, motivo); $('dv-reportar').textContent = '✓ reportado'; $('dv-reportar').disabled = true; } catch (e) { alert(e.message || e); }
      });
      $('dv-borrar').addEventListener('click', async () => {
        if (!confirm('¿Borrar este desafío? Se va para siempre.')) return;
        try { await borrarDesafio(id); location.href = B + '/desafios'; } catch (e) { alert(e.message || e); }
      });
```

  (Nota: `B` ya está definido en el script — `const B = (window.__BASE...`. Si no estuviera,
  agregarlo: `const B = (window.__BASE || '/').replace(/\/$/, '');`.)

- [ ] **Step 4: Verificar** — `cd web && npm run build`. Esperado: build OK.

---

### Task 4: Estilos

**Files:** Modify `web/src/styles/global.css`

Agregar después de los estilos de soluciones (`.df-voto.on{...}`):

```css
.df-mod{ display:flex; gap:8px; margin:.4rem 0 .8rem; }
.df-modbtn{ border:1px solid var(--line); background:var(--paper-2); color:var(--ink-mute); border-radius:9px; font-size:.78rem; font-weight:700; padding:4px 10px; cursor:pointer; }
.df-modbtn:hover{ color:var(--ink); }
.df-modbtn.danger:hover{ color:var(--red-deep); border-color:var(--red-deep); }
```

- [ ] Verificar — `cd web && npm run build`. Esperado: build OK.

---

### Task 5: Aplicar migración + build + commit (controller)

- [ ] `supabase db push --yes` (controller).
- [ ] `cd web && npm run build`.
- [ ] Commit `web/` + `docs/` + `supabase/migrations/` + `superpowers/`. Sin atribución a Claude.

## Self-Review
- Cobertura Fase 3: reportar (Task 1 `reportar_desafio` + Task 3) ✓; borrar propio (Task 1
  `borrar_desafio` + Task 3, botón solo si sos autor) ✓; auto-ocultar reportados (Task 1
  `listar_desafios` con `< 3 reportes`) ✓.
- Consistencia: `reportarDesafio`/`borrarDesafio` (desafios.js) = `reportar_desafio`/
  `borrar_desafio` (SQL) ✓. `listar_desafios` mantiene la MISMA firma/columnas que Fase 1
  (solo agrega el filtro de reportes) ✓.

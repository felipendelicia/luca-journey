# Intercambios de Pokémon — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permitir que dos usuarios logueados intercambien lotes de Pokémon en una sala en vivo, con swap atómico server-side.

**Architecture:** Sala = una fila en la tabla `intercambios` (Supabase). Toda mutación va por RPCs `SECURITY DEFINER` (control por columna). Realtime (`postgres_changes`) empuja los cambios de la fila a ambos clientes. Cuando los dos confirman, una función Postgres atómica valida y swapea las dos colecciones (dentro de `progreso.estado`).

**Tech Stack:** Astro estático (`web/`), Supabase (Postgres + Realtime + Auth), `@supabase/supabase-js` en el cliente. Verificación: scripts node con supabase-js (backend) y puppeteer-core (UI) — el patrón existente del repo (no hay framework de unit-test JS).

**Spec:** `specs/2026-06-04-intercambios-pokemon-design.md`

---

## Notas de entorno (leer antes de empezar)

- El CLI de Supabase ya está logueado y el proyecto linkeado (`ref cvknrqphepwzpdqdyegv`, región sa-east-1).
- Las migraciones viven en `supabase/migrations/`. Se aplican con `supabase db push` (pide la DB password con `-p`).
- **Secretos:** la `service_role` key se usa SOLO en scripts de verificación, vía variable de entorno `SUPABASE_SR`. **Nunca** hardcodear ni commitear la service key ni la DB password. La `anon` key y la URL ya están en `web/.env` (públicas).
- Verificación backend: scripts node ESM en `/tmp/trades-test/` con `@supabase/supabase-js`.
- Verificación UI: puppeteer-core en `/tmp/pptr/` apuntando a `google-chrome` del sistema, contra `npm run dev` en `:4321`.
- Tras tocar la UI: `npm run build` (genera `docs/`) y commitear `docs/` junto con `web/`.

Exportá una vez por sesión de ejecución (reemplazá `<...>`):

```bash
export SUPA_URL="https://cvknrqphepwzpdqdyegv.supabase.co"
export SUPA_ANON="$(grep PUBLIC_SUPABASE_ANON_KEY /home/felipe/Documents/Repositories/luca-journey/web/.env | cut -d= -f2)"
export SUPA_SR="<pegá la service_role key — NO la commitees>"   # supabase projects api-keys --project-ref cvknrqphepwzpdqdyegv
export DBPW="<DB password>"
export CHROME="$(which google-chrome)"
```

---

## File Structure

| Archivo | Crear/Modificar | Responsabilidad |
|---|---|---|
| `supabase/migrations/<ts>_intercambios.sql` | Crear | Tabla `intercambios` + RLS + Realtime + helpers jsonb + RPCs |
| `web/src/lib/trades.js` | Crear | Wrappers de los RPC + suscripción Realtime + presencia |
| `web/src/lib/nube.js` | Modificar | Agregar `refrescarDesdeNube()` |
| `web/src/pages/intercambio.astro` | Crear | Página/sala (estados: inicio, esperando, sala, completado) |
| `web/src/pages/pokedex.astro` | Modificar | Botón "🔄 Intercambiar" |
| `web/src/styles/global.css` | Modificar | Estilos de la sala + picker |

---

## Task 1: Migración — tabla `intercambios` + RLS + Realtime

**Files:**
- Create: `supabase/migrations/20260604120000_intercambios.sql`

- [ ] **Step 1: Crear el archivo de migración con la tabla, RLS y Realtime**

```sql
-- Sala de intercambio en vivo entre dos usuarios.
create table if not exists public.intercambios (
  id            uuid primary key default gen_random_uuid(),
  codigo        text unique not null,
  creador_id    uuid not null references auth.users (id) on delete cascade,
  invitado_id   uuid references auth.users (id) on delete cascade,
  creador_nombre  text not null default '',
  invitado_nombre text not null default '',
  creador_lote   jsonb not null default '[]'::jsonb,   -- [{id:int, shiny:bool}]
  invitado_lote  jsonb not null default '[]'::jsonb,
  creador_ok    boolean not null default false,
  invitado_ok   boolean not null default false,
  estado        text not null default 'abierta',       -- abierta | completada | cancelada
  creado        timestamptz not null default now(),
  actualizado   timestamptz not null default now()
);

alter table public.intercambios enable row level security;

-- Solo los dos participantes pueden VER la sala (Realtime respeta esta RLS).
drop policy if exists "ver intercambio propio" on public.intercambios;
create policy "ver intercambio propio" on public.intercambios for select
  using (auth.uid() = creador_id or auth.uid() = invitado_id);
-- (sin políticas de insert/update/delete: todo va por RPC SECURITY DEFINER)

-- Realtime: emitir cambios de filas de esta tabla.
alter table public.intercambios replica identity full;
do $$ begin
  alter publication supabase_realtime add table public.intercambios;
exception when duplicate_object then null; end $$;
```

- [ ] **Step 2: Aplicar la migración**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
printf 'y\n' | supabase db push -p "$DBPW" 2>&1 | tail -5
```
Expected: `Applying migration 20260604120000_intercambios.sql...` y `Finished supabase db push.`

- [ ] **Step 3: Verificar que la tabla existe y la RLS bloquea anónimos**

Create `/tmp/trades-test/t1.mjs`:
```javascript
import { createClient } from '@supabase/supabase-js';
const cli = createClient(process.env.SUPA_URL, process.env.SUPA_ANON);
const r = await cli.from('intercambios').select('*');
console.log('SELECT anónimo -> filas:', (r.data||[]).length, '| error:', r.error?.message || 'ninguno');
```
Run:
```bash
mkdir -p /tmp/trades-test && cd /tmp/trades-test && npm i @supabase/supabase-js >/dev/null 2>&1
node t1.mjs
```
Expected: `SELECT anónimo -> filas: 0 | error: ninguno` (RLS oculta todo a anónimos).

- [ ] **Step 4: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add supabase/migrations/20260604120000_intercambios.sql
git commit -m "Intercambios: tabla intercambios + RLS + Realtime"
```

---

## Task 2: Helpers jsonb + RPCs `crear_intercambio`, `unirse`, `cancelar`

**Files:**
- Modify: `supabase/migrations/20260604120000_intercambios.sql` (append)

- [ ] **Step 1: Agregar helpers jsonb y los 3 RPCs al final del archivo de migración**

```sql
-- ===== Helpers jsonb para la colección =====
-- col:atrapados = objeto {"<id>": <cantidad>} ; col:shiny = array [<id num>...]
create or replace function public._mapa_inc(m jsonb, k text) returns jsonb language sql immutable as $$
  select jsonb_set(coalesce(m,'{}'::jsonb), array[k], to_jsonb(coalesce((m->>k)::int,0) + 1));
$$;
create or replace function public._mapa_dec(m jsonb, k text) returns jsonb language sql immutable as $$
  select case when coalesce((m->>k)::int,0) <= 1 then (coalesce(m,'{}'::jsonb) - k)
              else jsonb_set(m, array[k], to_jsonb(((m->>k)::int) - 1)) end;
$$;
create or replace function public._arr_tiene(a jsonb, k text) returns boolean language sql immutable as $$
  select exists (select 1 from jsonb_array_elements(coalesce(a,'[]'::jsonb)) e where e = to_jsonb(k::int));
$$;
create or replace function public._arr_add(a jsonb, k text) returns jsonb language sql immutable as $$
  select case when public._arr_tiene(a,k) then coalesce(a,'[]'::jsonb) else coalesce(a,'[]'::jsonb) || to_jsonb(k::int) end;
$$;
create or replace function public._arr_del(a jsonb, k text) returns jsonb language sql immutable as $$
  select coalesce((select jsonb_agg(e) from jsonb_array_elements(coalesce(a,'[]'::jsonb)) e where e <> to_jsonb(k::int)), '[]'::jsonb);
$$;

-- ===== RPCs =====
create or replace function public.crear_intercambio(mi_nombre text)
returns table(id uuid, codigo text)
language plpgsql security definer set search_path = public as $$
declare nuevo_codigo text; nuevo_id uuid; alfabeto text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  loop
    nuevo_codigo := '';
    for i in 1..6 loop nuevo_codigo := nuevo_codigo || substr(alfabeto, floor(random()*length(alfabeto))::int + 1, 1); end loop;
    exit when not exists (select 1 from intercambios i where i.codigo = nuevo_codigo);
  end loop;
  insert into intercambios(codigo, creador_id, creador_nombre)
    values (nuevo_codigo, auth.uid(), coalesce(mi_nombre,''))
    returning intercambios.id, intercambios.codigo into nuevo_id, nuevo_codigo;
  return query select nuevo_id, nuevo_codigo;
end; $$;

create or replace function public.unirse(p_codigo text, mi_nombre text)
returns uuid language plpgsql security definer set search_path = public as $$
declare s intercambios;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  select * into s from intercambios where codigo = upper(p_codigo) and estado = 'abierta' for update;
  if not found then raise exception 'sala no encontrada o cerrada'; end if;
  if s.creador_id = auth.uid() then raise exception 'no podés unirte a tu propia sala'; end if;
  if s.invitado_id is not null and s.invitado_id <> auth.uid() then raise exception 'la sala ya está completa'; end if;
  update intercambios set invitado_id = auth.uid(), invitado_nombre = coalesce(mi_nombre,''), actualizado = now() where id = s.id;
  return s.id;
end; $$;

create or replace function public.cancelar(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
declare s intercambios;
begin
  select * into s from intercambios where id = p_id for update;
  if not found then raise exception 'sala no encontrada'; end if;
  if auth.uid() not in (s.creador_id, s.invitado_id) then raise exception 'no sos participante'; end if;
  if s.estado = 'abierta' then update intercambios set estado = 'cancelada', actualizado = now() where id = p_id; end if;
end; $$;
```

- [ ] **Step 2: Aplicar la migración (re-push del mismo archivo)**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
printf 'y\n' | supabase db push -p "$DBPW" 2>&1 | tail -4
```
Expected: aplica los `create or replace`. (Si dice "Remote database is up to date", forzá con `supabase db push --include-all`; o ejecutá el SQL del Step 1 vía `psql`/SQL editor. El push reaplica el archivo modificado.)

- [ ] **Step 3: Verificar crear + unirse con dos usuarios reales**

Create `/tmp/trades-test/t2.mjs`:
```javascript
import { createClient } from '@supabase/supabase-js';
const admin = createClient(process.env.SUPA_URL, process.env.SUPA_SR, { auth:{ persistSession:false }});
async function nuevoUsuario(tag) {
  const email = `t_${tag}_${Date.now()}@example.com`, password = 'Test12345!';
  const { data } = await admin.auth.admin.createUser({ email, password, email_confirm:true });
  const cli = createClient(process.env.SUPA_URL, process.env.SUPA_ANON, { auth:{ persistSession:false }});
  await cli.auth.signInWithPassword({ email, password });
  return { id: data.user.id, cli };
}
const A = await nuevoUsuario('A'), B = await nuevoUsuario('B');
const cre = await A.cli.rpc('crear_intercambio', { mi_nombre:'Ana' });
console.log('crear ->', cre.error?.message || JSON.stringify(cre.data));
const codigo = cre.data[0].codigo, id = cre.data[0].id;
const uni = await B.cli.rpc('unirse', { p_codigo: codigo, mi_nombre:'Beto' });
console.log('unirse ->', uni.error?.message || uni.data);
const propio = await A.cli.rpc('unirse', { p_codigo: codigo, mi_nombre:'Ana' });
console.log('unirse a la propia (debe fallar) ->', propio.error?.message || 'NO falló ⚠️');
await admin.auth.admin.deleteUser(A.id); await admin.auth.admin.deleteUser(B.id);
```
Run:
```bash
cd /tmp/trades-test && node t2.mjs
```
Expected:
```
crear -> [{"id":"...","codigo":"XXXXXX"}]
unirse -> <el mismo id>
unirse a la propia (debe fallar) -> no podés unirte a tu propia sala
```

- [ ] **Step 4: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add supabase/migrations/20260604120000_intercambios.sql
git commit -m "Intercambios: RPCs crear/unirse/cancelar + helpers jsonb"
```

---

## Task 3: RPC `poner_lote` + `confirmar` (sin swap todavía)

**Files:**
- Modify: `supabase/migrations/20260604120000_intercambios.sql` (append)

- [ ] **Step 1: Agregar `poner_lote` y `confirmar` (confirmar todavía NO ejecuta el swap; eso se agrega en Task 4)**

```sql
create or replace function public.poner_lote(p_id uuid, p_lote jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare s intercambios;
begin
  select * into s from intercambios where id = p_id for update;
  if not found then raise exception 'sala no encontrada'; end if;
  if s.estado <> 'abierta' then raise exception 'la sala no está abierta'; end if;
  if auth.uid() = s.creador_id then
    update intercambios set creador_lote = p_lote, creador_ok = false, invitado_ok = false, actualizado = now() where id = p_id;
  elsif auth.uid() = s.invitado_id then
    update intercambios set invitado_lote = p_lote, creador_ok = false, invitado_ok = false, actualizado = now() where id = p_id;
  else raise exception 'no sos participante'; end if;
end; $$;

create or replace function public.confirmar(p_id uuid)
returns text language plpgsql security definer set search_path = public as $$
declare s intercambios;
begin
  select * into s from intercambios where id = p_id for update;
  if not found then raise exception 'sala no encontrada'; end if;
  if s.estado <> 'abierta' then raise exception 'la sala no está abierta'; end if;
  if auth.uid() = s.creador_id then update intercambios set creador_ok = true, actualizado = now() where id = p_id;
  elsif auth.uid() = s.invitado_id then update intercambios set invitado_ok = true, actualizado = now() where id = p_id;
  else raise exception 'no sos participante'; end if;
  select * into s from intercambios where id = p_id;
  if s.creador_ok and s.invitado_ok then return 'completada'; end if;  -- swap se agrega en Task 4
  return 'abierta';
end; $$;
```

- [ ] **Step 2: Aplicar**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey && printf 'y\n' | supabase db push -p "$DBPW" 2>&1 | tail -3
```
Expected: aplica sin error.

- [ ] **Step 3: Verificar que poner_lote resetea los OK**

Create `/tmp/trades-test/t3.mjs`:
```javascript
import { createClient } from '@supabase/supabase-js';
const admin = createClient(process.env.SUPA_URL, process.env.SUPA_SR, { auth:{ persistSession:false }});
async function nuevoUsuario(tag){ const email=`t_${tag}_${Date.now()}@example.com`,password='Test12345!';
  const {data}=await admin.auth.admin.createUser({email,password,email_confirm:true});
  const cli=createClient(process.env.SUPA_URL,process.env.SUPA_ANON,{auth:{persistSession:false}});
  await cli.auth.signInWithPassword({email,password}); return {id:data.user.id,cli}; }
const A=await nuevoUsuario('A'), B=await nuevoUsuario('B');
const {data:[s]}=await A.cli.rpc('crear_intercambio',{mi_nombre:'Ana'});
await B.cli.rpc('unirse',{p_codigo:s.codigo,mi_nombre:'Beto'});
await A.cli.rpc('poner_lote',{p_id:s.id,p_lote:[{id:6,shiny:false}]});
await A.cli.rpc('confirmar',{p_id:s.id});
let row=(await admin.from('intercambios').select('*').eq('id',s.id).single()).data;
console.log('tras A confirma -> creador_ok:',row.creador_ok);   // true
await B.cli.rpc('poner_lote',{p_id:s.id,p_lote:[{id:25,shiny:false}]});  // B cambia su lote
row=(await admin.from('intercambios').select('*').eq('id',s.id).single()).data;
console.log('tras B cambia lote -> creador_ok:',row.creador_ok,'(debe ser false)');
await admin.auth.admin.deleteUser(A.id); await admin.auth.admin.deleteUser(B.id);
```
Run:
```bash
cd /tmp/trades-test && node t3.mjs
```
Expected:
```
tras A confirma -> creador_ok: true
tras B cambia lote -> creador_ok: false (debe ser false)
```

- [ ] **Step 4: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add supabase/migrations/20260604120000_intercambios.sql
git commit -m "Intercambios: RPCs poner_lote + confirmar (reset de OK al cambiar)"
```

---

## Task 4: RPC `ejecutar_intercambio` — el swap atómico

**Files:**
- Modify: `supabase/migrations/20260604120000_intercambios.sql` (append + editar `confirmar`)

- [ ] **Step 1: Agregar `ejecutar_intercambio` y hacer que `confirmar` lo llame**

Agregar al final:
```sql
create or replace function public.ejecutar_intercambio(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
declare
  s intercambios;
  c_estado jsonb; i_estado jsonb;
  c_atra jsonb; c_shi jsonb; i_atra jsonb; i_shi jsonb;
  tmp jsonb; item jsonb; v_id text; v_shiny boolean;
begin
  select * into s from intercambios where id = p_id for update;
  if not found or s.estado <> 'abierta' then raise exception 'intercambio no ejecutable'; end if;
  if not (s.creador_ok and s.invitado_ok) then raise exception 'faltan confirmaciones'; end if;

  select estado into c_estado from progreso where user_id = s.creador_id for update;
  select estado into i_estado from progreso where user_id = s.invitado_id for update;
  c_estado := coalesce(c_estado, '{}'::jsonb); i_estado := coalesce(i_estado, '{}'::jsonb);
  c_atra := coalesce((c_estado->>'col:atrapados')::jsonb, '{}'::jsonb);
  c_shi  := coalesce((c_estado->>'col:shiny')::jsonb, '[]'::jsonb);
  i_atra := coalesce((i_estado->>'col:atrapados')::jsonb, '{}'::jsonb);
  i_shi  := coalesce((i_estado->>'col:shiny')::jsonb, '[]'::jsonb);

  -- VALIDAR (sobre copias, respetando multiplicidad por cantidad)
  tmp := c_atra;
  for item in select * from jsonb_array_elements(s.creador_lote) loop
    v_id := item->>'id'; v_shiny := coalesce((item->>'shiny')::boolean,false);
    if coalesce((tmp->>v_id)::int,0) < 1 then raise exception 'creador no tiene suficiente %', v_id; end if;
    if v_shiny and not public._arr_tiene(c_shi, v_id) then raise exception 'creador no tiene shiny %', v_id; end if;
    tmp := public._mapa_dec(tmp, v_id);
  end loop;
  tmp := i_atra;
  for item in select * from jsonb_array_elements(s.invitado_lote) loop
    v_id := item->>'id'; v_shiny := coalesce((item->>'shiny')::boolean,false);
    if coalesce((tmp->>v_id)::int,0) < 1 then raise exception 'invitado no tiene suficiente %', v_id; end if;
    if v_shiny and not public._arr_tiene(i_shi, v_id) then raise exception 'invitado no tiene shiny %', v_id; end if;
    tmp := public._mapa_dec(tmp, v_id);
  end loop;

  -- APLICAR: creador da su lote -> invitado ; invitado da su lote -> creador
  for item in select * from jsonb_array_elements(s.creador_lote) loop
    v_id := item->>'id'; v_shiny := coalesce((item->>'shiny')::boolean,false);
    c_atra := public._mapa_dec(c_atra, v_id); i_atra := public._mapa_inc(i_atra, v_id);
    if v_shiny then c_shi := public._arr_del(c_shi, v_id); i_shi := public._arr_add(i_shi, v_id); end if;
  end loop;
  for item in select * from jsonb_array_elements(s.invitado_lote) loop
    v_id := item->>'id'; v_shiny := coalesce((item->>'shiny')::boolean,false);
    i_atra := public._mapa_dec(i_atra, v_id); c_atra := public._mapa_inc(c_atra, v_id);
    if v_shiny then i_shi := public._arr_del(i_shi, v_id); c_shi := public._arr_add(c_shi, v_id); end if;
  end loop;

  -- guardar (col:atrapados y col:shiny se almacenan como STRING dentro del jsonb)
  c_estado := jsonb_set(jsonb_set(c_estado, '{col:atrapados}', to_jsonb(c_atra::text)), '{col:shiny}', to_jsonb(c_shi::text));
  i_estado := jsonb_set(jsonb_set(i_estado, '{col:atrapados}', to_jsonb(i_atra::text)), '{col:shiny}', to_jsonb(i_shi::text));
  insert into progreso(user_id, estado) values (s.creador_id, c_estado)
    on conflict (user_id) do update set estado = excluded.estado, actualizado = now();
  insert into progreso(user_id, estado) values (s.invitado_id, i_estado)
    on conflict (user_id) do update set estado = excluded.estado, actualizado = now();

  update intercambios set estado = 'completada', actualizado = now() where id = p_id;
end; $$;
```

Editar `confirmar`: reemplazar la línea
```sql
  if s.creador_ok and s.invitado_ok then return 'completada'; end if;  -- swap se agrega en Task 4
```
por:
```sql
  if s.creador_ok and s.invitado_ok then perform public.ejecutar_intercambio(p_id); return 'completada'; end if;
```

- [ ] **Step 2: Aplicar**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey && printf 'y\n' | supabase db push -p "$DBPW" 2>&1 | tail -3
```
Expected: aplica sin error.

- [ ] **Step 3: Verificar el swap completo (dos usuarios, colección sembrada, flujo entero)**

Create `/tmp/trades-test/t4.mjs`:
```javascript
import { createClient } from '@supabase/supabase-js';
const admin = createClient(process.env.SUPA_URL, process.env.SUPA_SR, { auth:{ persistSession:false }});
async function nuevoUsuario(tag, estado){ const email=`t_${tag}_${Date.now()}@example.com`,password='Test12345!';
  const {data}=await admin.auth.admin.createUser({email,password,email_confirm:true});
  await admin.from('progreso').upsert({ user_id:data.user.id, estado });
  const cli=createClient(process.env.SUPA_URL,process.env.SUPA_ANON,{auth:{persistSession:false}});
  await cli.auth.signInWithPassword({email,password}); return {id:data.user.id,cli}; }
// A tiene 2 Charizard(6) (uno shiny) ; B tiene 1 Pikachu(25)
const A=await nuevoUsuario('A',{ 'col:atrapados':'{"6":2}', 'col:shiny':'[6]' });
const B=await nuevoUsuario('B',{ 'col:atrapados':'{"25":1}', 'col:shiny':'[]' });
const {data:[s]}=await A.cli.rpc('crear_intercambio',{mi_nombre:'Ana'});
await B.cli.rpc('unirse',{p_codigo:s.codigo,mi_nombre:'Beto'});
await A.cli.rpc('poner_lote',{p_id:s.id,p_lote:[{id:6,shiny:true}]});   // A da su Charizard shiny
await B.cli.rpc('poner_lote',{p_id:s.id,p_lote:[{id:25,shiny:false}]}); // B da su Pikachu
await A.cli.rpc('confirmar',{p_id:s.id});
const res=await B.cli.rpc('confirmar',{p_id:s.id});
console.log('confirmar final ->', res.error?.message || res.data);   // completada
const a=(await admin.from('progreso').select('estado').eq('user_id',A.id).single()).data.estado;
const b=(await admin.from('progreso').select('estado').eq('user_id',B.id).single()).data.estado;
console.log('A atrapados:', a['col:atrapados'], '| A shiny:', a['col:shiny']);  // {"6":1,"25":1} | []
console.log('B atrapados:', b['col:atrapados'], '| B shiny:', b['col:shiny']);  // {"6":1} | [6]
await admin.auth.admin.deleteUser(A.id); await admin.auth.admin.deleteUser(B.id);
```
Run:
```bash
cd /tmp/trades-test && node t4.mjs
```
Expected:
```
confirmar final -> completada
A atrapados: {"6": 1, "25": 1} | A shiny: []
B atrapados: {"6": 1} | B shiny: [6]
```
(A: pierde 1 Charizard y su shiny, gana Pikachu. B: pierde Pikachu, gana Charizard shiny. Atómico, sin duplicar.)

- [ ] **Step 4: Verificar que no se puede ejecutar dos veces (one-shot)**

Append a `/tmp/trades-test/t4b.mjs` (copiá t4.mjs y agregá antes del deleteUser):
```javascript
const dup = await B.cli.rpc('confirmar',{p_id:s.id});
console.log('confirmar de nuevo (debe fallar) ->', dup.error?.message || 'NO falló ⚠️');
```
Expected: `confirmar de nuevo (debe fallar) -> la sala no está abierta`

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add supabase/migrations/20260604120000_intercambios.sql
git commit -m "Intercambios: swap atomico ejecutar_intercambio + confirmar lo dispara"
```

---

## Task 5: `nube.js` — `refrescarDesdeNube()`

**Files:**
- Modify: `web/src/lib/nube.js`

- [ ] **Step 1: Agregar la función exportada `refrescarDesdeNube`**

En `web/src/lib/nube.js`, después de `export function usuario() { return _user; }`, agregar:
```javascript
// Baja el progreso de la nube y lo aplica a localStorage (úsalo cuando la nube cambió
// por fuera, ej: un intercambio). Devuelve true si había sesión y se aplicó.
export async function refrescarDesdeNube() {
  if (!haySupabase || !_user) return false;
  const nube = await bajar(_user.id);
  if (nube && Object.keys(nube).length) {
    limpiarLocal();
    aplicar(nube);
    _ultima = serial(nube);   // evitar que el watcher re-suba lo viejo
  }
  return true;
}
```

- [ ] **Step 2: Verificar que el build no rompe**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web && timeout 240 npm run build 2>&1 | tail -2
```
Expected: `[build] Complete!`

- [ ] **Step 3: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/nube.js docs
git commit -m "nube.js: refrescarDesdeNube() para releer la coleccion tras un trade"
```

---

## Task 6: `trades.js` — wrappers de RPC + Realtime + presencia

**Files:**
- Create: `web/src/lib/trades.js`

- [ ] **Step 1: Crear `web/src/lib/trades.js`**

```javascript
// trades.js — API de intercambios: RPCs + suscripción Realtime + presencia.
import { supa, haySupabase } from './supa.js';

const nombreLocal = () => localStorage.getItem('liga:nombre') || 'Entrenador/a';

export async function crear() {
  const { data, error } = await supa.rpc('crear_intercambio', { mi_nombre: nombreLocal() });
  if (error) throw error;
  return data[0]; // { id, codigo }
}
export async function unirse(codigo) {
  const { data, error } = await supa.rpc('unirse', { p_codigo: codigo.trim().toUpperCase(), mi_nombre: nombreLocal() });
  if (error) throw error;
  return data; // id
}
export async function ponerLote(id, lote) {
  const { error } = await supa.rpc('poner_lote', { p_id: id, p_lote: lote });
  if (error) throw error;
}
export async function confirmar(id) {
  const { data, error } = await supa.rpc('confirmar', { p_id: id });
  if (error) throw error;
  return data; // 'abierta' | 'completada'
}
export async function cancelar(id) {
  const { error } = await supa.rpc('cancelar', { p_id: id });
  if (error) throw error;
}
export async function leerSala(id) {
  const { data, error } = await supa.from('intercambios').select('*').eq('id', id).maybeSingle();
  if (error) throw error;
  return data;
}

// Suscribe a los cambios de la sala (postgres_changes) + presencia del otro.
// onCambio(row) cada vez que cambia la fila; onPresencia(hayOtro) cuando entra/sale.
// Devuelve una función para desuscribir.
export function suscribir(id, miId, { onCambio, onPresencia }) {
  const canal = supa.channel(`sala:${id}`, { config: { presence: { key: miId } } });
  canal.on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'intercambios', filter: `id=eq.${id}` },
    (payload) => onCambio && onCambio(payload.new));
  canal.on('presence', { event: 'sync' }, () => {
    const estado = canal.presenceState();
    const otros = Object.keys(estado).filter((k) => k !== miId).length;
    onPresencia && onPresencia(otros > 0);
  });
  canal.subscribe((status) => { if (status === 'SUBSCRIBED') canal.track({ at: Date.now() }); });
  return () => supa.removeChannel(canal);
}

export { haySupabase };
```

- [ ] **Step 2: Verificar build**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web && timeout 240 npm run build 2>&1 | tail -2
```
Expected: `[build] Complete!`

- [ ] **Step 3: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/trades.js docs
git commit -m "trades.js: RPCs + suscripcion Realtime + presencia"
```

---

## Task 7: Página `intercambio.astro` — estados + sala

**Files:**
- Create: `web/src/pages/intercambio.astro`

- [ ] **Step 1: Crear la página con su markup, datos y el script de la sala**

```astro
---
import Base from '../layouts/Base.astro';
import pokemon from '../data/pokemon.json';
import { u } from '../lib/url.ts';
const nombres = Object.fromEntries(pokemon.map((p) => [p.id, p.nombre]));
---
<Base title="Intercambio — Python con Pokémon" active="">
  <main class="wrap">
    <h1>🔄 Intercambio</h1>

    <p class="tr-login" id="tr-login" hidden>Necesitás <b>iniciar sesión</b> (botón ☁️ arriba) para intercambiar.</p>

    <section class="tr-pane" id="tr-inicio" hidden>
      <p>Creá una sala y pasale el código a la otra persona (por WhatsApp), o uní con un código.</p>
      <div class="tr-acciones">
        <button class="btn-grande" id="tr-crear">Crear sala</button>
        <form class="tr-unir" id="tr-unir-form">
          <input id="tr-codigo" placeholder="CÓDIGO" maxlength="6" />
          <button class="btn-grande sec" type="submit">Unirme</button>
        </form>
      </div>
      <p class="auth-msg err" id="tr-err" hidden></p>
    </section>

    <section class="tr-pane" id="tr-espera" hidden>
      <p>Compartí este código (o el link) y esperá a que se una:</p>
      <div class="tr-codigo-box"><span id="tr-codigo-ver"></span><button class="btn-sec" id="tr-copiar">📋 copiar link</button></div>
      <p class="auth-fine">Esperando al otro entrenador… 🟡</p>
      <button class="btn-sec" id="tr-cancelar-espera">Cancelar</button>
    </section>

    <section class="tr-pane" id="tr-sala" hidden>
      <div class="tr-mesa">
        <div class="tr-lado">
          <h3>Vos <span class="tr-pres" id="tr-pres-yo">🟢</span></h3>
          <div class="tr-lote" id="tr-lote-yo"></div>
          <button class="btn-sec" id="tr-elegir">+ Elegir Pokémon</button>
          <div class="tr-estado" id="tr-estado-yo">sin confirmar</div>
        </div>
        <div class="tr-vs">⇄</div>
        <div class="tr-lado">
          <h3 id="tr-nombre-otro">El otro</h3>
          <div class="tr-lote" id="tr-lote-otro"></div>
          <div class="tr-estado" id="tr-estado-otro">sin confirmar</div>
        </div>
      </div>
      <div class="tr-botones">
        <button class="btn-grande" id="tr-confirmar">✅ Confirmar</button>
        <button class="btn-sec" id="tr-cancelar">✕ Cancelar</button>
      </div>
    </section>

    <section class="tr-pane" id="tr-listo" hidden>
      <h2>🎉 ¡Intercambio listo!</h2>
      <p id="tr-resumen"></p>
      <a class="btn-grande" href={u('/pokedex')}>Ver mi Pokédex</a>
    </section>

    <!-- modal picker de la colección -->
    <div class="av-modal" id="tr-modal" hidden>
      <div class="av-card">
        <div class="av-head"><b>🎒 Elegí qué ofrecer</b><button class="av-x" id="tr-modal-x" type="button">✕</button></div>
        <p class="av-sub">Tocá para sumar al lote. ✨ = ofrecé el shiny (si lo tenés).</p>
        <div class="av-grid" id="tr-grid"></div>
        <button class="btn-grande" id="tr-modal-ok" type="button">Listo</button>
      </div>
    </div>
  </main>

  <script type="application/json" id="tr-data" set:html={JSON.stringify({ nombres })}></script>
  <script>
    import { crear, unirse, ponerLote, confirmar, cancelar, leerSala, suscribir, haySupabase } from '../lib/trades.js';
    import { usuario, init as initNube, refrescarDesdeNube } from '../lib/nube.js';

    const D = JSON.parse(document.getElementById('tr-data').textContent);
    const nombres = D.nombres;
    const sprite = (id, sh) => `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${sh ? 'shiny/' : ''}${id}.png`;
    const $ = (id) => document.getElementById(id);
    const panes = ['tr-login', 'tr-inicio', 'tr-espera', 'tr-sala', 'tr-listo'];
    const ver = (cual) => panes.forEach((p) => $(p).hidden = (p !== cual));

    const atrapados = () => { try { return JSON.parse(localStorage.getItem('col:atrapados')) || {}; } catch { return {}; } };
    const shinySet = () => { try { return new Set(JSON.parse(localStorage.getItem('col:shiny')) || []); } catch { return new Set(); } };

    let sala = null;       // fila actual
    let salaId = null;
    let miLote = [];       // [{id,shiny}]
    let desuscribir = null;
    const soyCreador = () => sala && usuario() && sala.creador_id === usuario().id;

    function pintarLote(el, lote) {
      el.innerHTML = lote.length
        ? lote.map((x) => `<img src="${sprite(x.id, x.shiny)}" title="${nombres[x.id] || x.id}${x.shiny ? ' ✨' : ''}" />`).join('')
        : '<span class="tr-vacio">(vacío)</span>';
    }
    function pintarSala() {
      if (!sala) return;
      const otroNombre = soyCreador() ? sala.invitado_nombre : sala.creador_nombre;
      const otroLote = soyCreador() ? sala.invitado_lote : sala.creador_lote;
      const yoOk = soyCreador() ? sala.creador_ok : sala.invitado_ok;
      const otroOk = soyCreador() ? sala.invitado_ok : sala.creador_ok;
      $('tr-nombre-otro').textContent = otroNombre || 'El otro';
      pintarLote($('tr-lote-yo'), miLote);
      pintarLote($('tr-lote-otro'), otroLote || []);
      $('tr-estado-yo').textContent = yoOk ? '✅ confirmado' : 'sin confirmar';
      $('tr-estado-otro').textContent = otroOk ? '✅ confirmado' : 'sin confirmar';
    }

    async function onCambioSala(row) {
      sala = row;
      if (row.estado === 'completada') { await terminar('completada'); return; }
      if (row.estado === 'cancelada') { alert('El intercambio se canceló.'); location.reload(); return; }
      if (row.invitado_id) ver('tr-sala');
      pintarSala();
    }

    async function entrarSala(id) {
      salaId = id;
      sala = await leerSala(id);
      $('tr-codigo-ver').textContent = sala.codigo;   // mostrar el código en el pane "esperando"
      ver(sala.invitado_id ? 'tr-sala' : 'tr-espera');
      pintarSala();
      desuscribir = suscribir(id, usuario().id, {
        onCambio: onCambioSala,
        onPresencia: (hay) => { const o = $('tr-pres-yo'); if (o) o.textContent = '🟢'; const el = document.querySelector('#tr-nombre-otro'); if (el) el.dataset.pres = hay ? '1' : '0'; },
      });
    }

    async function terminar(estado) {
      if (desuscribir) desuscribir();
      await refrescarDesdeNube();
      $('tr-resumen').textContent = '¡Tu colección se actualizó!';
      ver('tr-listo');
    }

    // ---- picker ----
    function abrirPicker() {
      const at = atrapados(), shi = shinySet();
      const ids = Object.keys(at).sort((a, b) => a - b);
      $('tr-grid').innerHTML = ids.map((id) => {
        const tieneShiny = shi.has(Number(id));
        return `<div class="tr-pick" data-id="${id}">
          <img src="${sprite(id, false)}" alt="${nombres[id] || id}" title="${nombres[id] || id} (x${at[id]})" />
          <button class="tr-add" data-id="${id}" data-shiny="0" type="button">+</button>
          ${tieneShiny ? `<button class="tr-add shiny" data-id="${id}" data-shiny="1" type="button">✨+</button>` : ''}
        </div>`;
      }).join('');
      $('tr-grid').querySelectorAll('.tr-add').forEach((b) => b.addEventListener('click', () => {
        const id = Number(b.dataset.id), shiny = b.dataset.shiny === '1';
        const enLote = miLote.filter((x) => x.id === id).length;
        if (enLote >= at[id]) { return; }            // no más que lo que tenés
        miLote.push({ id, shiny });
        pintarLote($('tr-lote-yo'), miLote);
      }));
      $('tr-modal').hidden = false;
    }

    // ---- init ----
    function arrancar() {
      if (!haySupabase) { ver('tr-login'); return; }
      initNube();
      const refrescarSesion = () => {
        if (!usuario()) { ver('tr-login'); return; }
        const params = new URLSearchParams(location.search);
        const codigoURL = params.get('codigo');
        if (salaId) return;             // ya en una sala
        if (codigoURL) { unirse(codigoURL).then(entrarSala).catch((e) => { mostrarError(e); ver('tr-inicio'); }); }
        else ver('tr-inicio');
      };
      window.addEventListener('nube:cambio', refrescarSesion);
      refrescarSesion();
    }
    const mostrarError = (e) => { const el = $('tr-err'); el.textContent = e.message || String(e); el.hidden = false; };

    $('tr-crear').addEventListener('click', async () => {
      try { const { id } = await crear(); history.replaceState(null, '', `?codigo=`); await entrarSala(id); }
      catch (e) { mostrarError(e); }
    });
    $('tr-unir-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      try { const id = await unirse($('tr-codigo').value); await entrarSala(id); }
      catch (e2) { mostrarError(e2); }
    });
    $('tr-copiar').addEventListener('click', () => {
      const link = `${location.origin}${window.__BASE || ''}/intercambio?codigo=${sala.codigo}`;
      navigator.clipboard.writeText(link); $('tr-copiar').textContent = '✓ copiado';
    });
    $('tr-elegir').addEventListener('click', abrirPicker);
    $('tr-modal-x').addEventListener('click', () => { $('tr-modal').hidden = true; });
    $('tr-modal-ok').addEventListener('click', async () => { $('tr-modal').hidden = true; await ponerLote(salaId, miLote); });
    $('tr-confirmar').addEventListener('click', async () => { try { await confirmar(salaId); } catch (e) { alert(e.message); } });
    $('tr-cancelar').addEventListener('click', async () => { await cancelar(salaId); location.reload(); });
    $('tr-cancelar-espera').addEventListener('click', async () => { await cancelar(salaId); location.reload(); });

    arrancar();
  </script>
</Base>
```

- [ ] **Step 2: Verificar build + que la página responde**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web && timeout 240 npm run build 2>&1 | tail -2
lsof -ti:4321 | xargs -r kill; sleep 1; nohup npm run dev -- --port 4321 --host >/tmp/dev.log 2>&1 & sleep 8
curl -s -o /dev/null -w "intercambio:%{http_code}\n" http://localhost:4321/intercambio
```
Expected: `[build] Complete!` y `intercambio:200`.

- [ ] **Step 3: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/pages/intercambio.astro docs
git commit -m "Intercambio: pagina/sala (estados inicio/espera/sala/listo + picker)"
```

---

## Task 8: Estilos de la sala + botón en la Pokédex

**Files:**
- Modify: `web/src/styles/global.css` (append)
- Modify: `web/src/pages/pokedex.astro`

- [ ] **Step 1: Agregar estilos al final de `web/src/styles/global.css`**

```css
/* intercambios */
.tr-pane{ margin:1.2rem 0; }
.tr-acciones{ display:flex; flex-wrap:wrap; gap:14px; align-items:center; margin:1rem 0; }
.tr-unir{ display:flex; gap:8px; }
.tr-unir input{ font:inherit; text-transform:uppercase; letter-spacing:.15em; text-align:center; width:140px; padding:10px; border:1px solid var(--line); border-radius:12px; background:var(--card); }
.tr-codigo-box{ display:flex; align-items:center; gap:14px; margin:.6rem 0; }
.tr-codigo-box span{ font-family:var(--font-pixel); font-size:1.8rem; letter-spacing:.2em; background:var(--paper-2); border:1px dashed var(--line); border-radius:12px; padding:8px 18px; }
.tr-mesa{ display:grid; grid-template-columns:1fr auto 1fr; gap:14px; align-items:start; margin:1rem 0; }
.tr-lado{ background:var(--paper-2); border:1px solid var(--line); border-radius:16px; padding:14px; }
.tr-lado h3{ margin:0 0 .5rem; font-size:1.05rem; }
.tr-lote{ display:flex; flex-wrap:wrap; gap:6px; min-height:62px; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:8px; margin-bottom:.6rem; }
.tr-lote img{ width:50px; height:50px; image-rendering:pixelated; }
.tr-vacio{ color:var(--ink-mute); font-size:.85rem; align-self:center; }
.tr-vs{ font-size:1.8rem; color:var(--red); align-self:center; }
.tr-estado{ font-size:.85rem; color:var(--ink-soft); }
.tr-botones{ display:flex; gap:12px; flex-wrap:wrap; }
.tr-login{ background:var(--paper-2); border:1px solid var(--line); border-radius:12px; padding:14px; }
.tr-pick{ position:relative; }
.tr-add{ position:absolute; bottom:2px; right:2px; font-size:.7rem; border:0; border-radius:8px; background:var(--red); color:#fff; cursor:pointer; padding:1px 5px; }
.tr-add.shiny{ right:auto; left:2px; background:var(--yellow-deep); }
@media(max-width:560px){ .tr-mesa{ grid-template-columns:1fr; } .tr-vs{ transform:rotate(90deg); } }
```

- [ ] **Step 2: Agregar el botón "🔄 Intercambiar" en la Pokédex**

En `web/src/pages/pokedex.astro`, buscar el link "Ir al Safari" (clase `Ir al Safari` / el header de la página) y agregar al lado un link. Concretamente, localizar:
```astro
    <a class="dex-safari" href={u('/safari')}>🎒 Ir al Safari</a>
```
y reemplazar por:
```astro
    <a class="dex-safari" href={u('/safari')}>🎒 Ir al Safari</a>
    <a class="dex-safari" href={u('/intercambio')}>🔄 Intercambiar</a>
```
(Si el texto exacto difiere, buscar `u('/safari')` en ese archivo y agregar el link `u('/intercambio')` inmediatamente después, con la misma clase.)

- [ ] **Step 3: Build + screenshot de la página**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web && timeout 240 npm run build 2>&1 | tail -2
lsof -ti:4321 | xargs -r kill; sleep 1; nohup npm run dev -- --port 4321 --host >/tmp/dev.log 2>&1 & sleep 8
timeout 60 google-chrome --headless=new --no-sandbox --disable-gpu --window-size=1000,700 --screenshot=/tmp/tr.png "http://localhost:4321/intercambio" 2>/dev/null
echo done
```
Expected: `[build] Complete!`. Abrir `/tmp/tr.png` y confirmar que se ve la página (probablemente el estado "iniciá sesión", que es lo correcto sin login).

- [ ] **Step 4: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/styles/global.css web/src/pages/pokedex.astro docs
git commit -m "Intercambios: estilos de la sala + boton en la Pokedex"
```

---

## Task 9: Verificación e2e en vivo (dos usuarios) + cierre

**Files:** (sin cambios de código; test de integración)

- [ ] **Step 1: Test e2e con dos contextos de navegador (sesiones inyectadas)**

Create `/tmp/pptr/trade-e2e.mjs`:
```javascript
import { createClient } from '@supabase/supabase-js';
import puppeteer from 'puppeteer-core';
const REF='cvknrqphepwzpdqdyegv';
const admin=createClient(process.env.SUPA_URL, process.env.SUPA_SR, { auth:{persistSession:false}});
async function usuario(tag, estado){ const email=`e2e_${tag}_${Date.now()}@example.com`,password='Test12345!';
  const {data}=await admin.auth.admin.createUser({email,password,email_confirm:true});
  await admin.from('progreso').upsert({user_id:data.user.id,estado});
  const cli=createClient(process.env.SUPA_URL,process.env.SUPA_ANON,{auth:{persistSession:false}});
  const {data:si}=await cli.auth.signInWithPassword({email,password});
  return {id:data.user.id, session:si.session}; }
async function pagina(browser, session, estadoLocal){
  const p=await browser.newPage(); await p.setViewport({width:760,height:720});
  await p.goto('http://localhost:4321/intercambio',{waitUntil:'networkidle2'});
  await p.evaluate((sess,ref,est)=>{ localStorage.clear();
    for(const k in est) localStorage.setItem(k,est[k]);
    localStorage.setItem('liga:nombre', est.__nombre||'Jug');
    localStorage.setItem(`sb-${ref}-auth-token`, JSON.stringify(sess));
  }, session, REF, estadoLocal);
  return p; }
const A=await usuario('A',{'col:atrapados':'{"6":2}','col:shiny':'[6]'});
const B=await usuario('B',{'col:atrapados':'{"25":1}','col:shiny':'[]'});
const browser=await puppeteer.launch({executablePath:process.env.CHROME,headless:'new',args:['--no-sandbox','--disable-gpu']});
const pa=await pagina(browser,A.session,{'col:atrapados':'{"6":2}','col:shiny':'[6]',__nombre:'Ana'});
await pa.goto('http://localhost:4321/intercambio',{waitUntil:'networkidle2'});
await pa.waitForSelector('#tr-crear',{visible:true,timeout:8000});
await pa.click('#tr-crear');
await pa.waitForSelector('#tr-codigo-ver',{visible:true});
const codigo=await pa.$eval('#tr-codigo-ver',el=>el.textContent.trim());
console.log('codigo:',codigo);
const pb=await pagina(browser,B.session,{'col:atrapados':'{"25":1}','col:shiny':'[]',__nombre:'Beto'});
await pb.goto(`http://localhost:4321/intercambio?codigo=${codigo}`,{waitUntil:'networkidle2'});
await pb.waitForSelector('#tr-sala:not([hidden])',{timeout:8000});
// A pone su Charizard shiny, B su Pikachu (vía picker)
for(const [pg,addSel] of [[pa,'.tr-add.shiny'],[pb,'.tr-add']]){
  await pg.click('#tr-elegir'); await pg.waitForSelector('#tr-grid .tr-add',{visible:true});
  await pg.click(addSel); await pg.click('#tr-modal-ok'); await new Promise(r=>setTimeout(r,800));
}
await pa.click('#tr-confirmar'); await new Promise(r=>setTimeout(r,600));
await pb.click('#tr-confirmar'); await new Promise(r=>setTimeout(r,2500));
const aDex=(await admin.from('progreso').select('estado').eq('user_id',A.id).single()).data.estado;
const bDex=(await admin.from('progreso').select('estado').eq('user_id',B.id).single()).data.estado;
console.log('A:',aDex['col:atrapados'],aDex['col:shiny']);  // {"6":1,"25":1} []
console.log('B:',bDex['col:atrapados'],bDex['col:shiny']);  // {"6":1} [6]
await browser.close();
await admin.auth.admin.deleteUser(A.id); await admin.auth.admin.deleteUser(B.id);
```
Run:
```bash
cd /tmp/pptr && npm i @supabase/supabase-js puppeteer-core >/dev/null 2>&1
node trade-e2e.mjs
```
Expected:
```
codigo: XXXXXX
A: {"6": 1, "25": 1} []
B: {"6": 1} [6]
```
(Confirma el flujo completo en vivo: crear, unir vía link, poner lotes con el picker, confirmar ambos, swap aplicado en la nube.)

- [ ] **Step 2: Si algo falla, depurá**

Si el invitado no entra a `#tr-sala`, revisar: (a) que `intercambios` esté en la publicación Realtime (Task 1), (b) que la RLS SELECT permita a ambos ver la fila, (c) el formato del token `sb-<ref>-auth-token`. Tomar screenshot con `await pb.screenshot({path:'/tmp/pb.png'})` antes del `waitForSelector`.

- [ ] **Step 3: Build final + commit + deploy**

```bash
cd /home/felipe/Documents/Repositories/luca-journey/web && timeout 240 npm run build 2>&1 | tail -2
cd /home/felipe/Documents/Repositories/luca-journey
git add -A
git commit -m "Intercambios: verificacion e2e en vivo OK (dos usuarios, swap atomico)"
git push
```
Expected: build Complete, push OK.

---

## Self-Review (hecho por el autor del plan)

**Cobertura del spec:**
- Tabla + RLS + Realtime → Task 1 ✓
- RPCs crear/unirse/cancelar → Task 2 ✓; poner_lote/confirmar → Task 3 ✓; swap atómico → Task 4 ✓
- Detalle shiny (presencia) → Task 4 (helpers `_arr_*`, validación + apply) ✓
- `refrescarDesdeNube` → Task 5 ✓
- `trades.js` (RPCs + Realtime + presencia) → Task 6 ✓
- Página/sala (4 estados + picker) → Task 7 ✓
- Estilos + botón Pokédex → Task 8 ✓
- E2E dos usuarios → Task 9 ✓
- Anti-abuso (RPC-only writes, validación server, one-shot) → Tasks 2-4 ✓

**Consistencia de tipos/nombres:** lote = `[{id:int, shiny:bool}]` en todo (cliente envía números; SQL lee `item->>'id'` text y castea). `col:atrapados`/`col:shiny` se leen y escriben como STRING dentro del jsonb (Task 4 `to_jsonb(...::text)`), consistente con cómo `nube.js` guarda localStorage. RPC names consistentes entre `trades.js` y la migración (`crear_intercambio`, `unirse`, `poner_lote`, `confirmar`, `cancelar`).

**Sin placeholders:** todos los pasos tienen código/comandos concretos.

**Riesgo conocido:** el e2e (Task 9) depende del formato del token de sesión en localStorage y de Realtime; el Step 2 de Task 9 da la guía de depuración.

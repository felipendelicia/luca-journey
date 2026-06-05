# Social: perfiles, amigos e intercambios asíncronos — Plan

> Ubicación `superpowers/` (raíz), NO `docs/`. Ejecutar con executing-plans (inline).
> Diseño: `superpowers/specs/2026-06-04-social-perfiles-amigos-design.md`.

**Goal:** Perfiles públicos compartibles (handle + código), amigos (solicitud/aceptar +
búsqueda) e intercambios asíncronos (doy X ↔ pido Y) entre amigos.

**Architecture:** 3 tablas Supabase (`perfiles` con select público, `amistades`,
`ofertas`) + RPCs `security definer`. Snapshot público mantenido por el cliente (como
`nube.js`). Página pública client-rendered `/u?h=<handle>`. Nuevas páginas `/amigos`,
cambios en `liga.astro` y nav.

**Tech Stack:** Astro (vanilla JS), Supabase (Postgres RPC + Realtime), sprites PokeAPI.

**Testing:** sin runner JS. Verificación: `npm run build` + screenshots + prueba manual de
2 sesiones. Migración: `supabase db push --yes`.

---

## Etapa 1 — Perfiles + identidad

### Task 1: Migración `perfiles`
**Files:** Create `supabase/migrations/20260604140000_social_perfiles.sql`

- [ ] Tabla `perfiles` + RPCs `guardar_perfil`, `buscar_perfiles`, `perfil_publico`.

```sql
create table if not exists public.perfiles (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  handle       text unique not null,
  nombre       text not null default '',
  avatar       int  not null default 0,
  codigo_amigo text unique not null,
  publico      jsonb not null default '{}'::jsonb,
  actualizado  timestamptz not null default now()
);
alter table public.perfiles enable row level security;
drop policy if exists "perfil select publico" on public.perfiles;
create policy "perfil select publico" on public.perfiles for select using (true);
-- insert/update solo via RPC security definer (no policy de escritura directa)

create or replace function public._codigo_amigo() returns text language plpgsql as $$
declare alf text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; c text;
begin
  loop
    c := ''; for i in 1..6 loop c := c || substr(alf, floor(random()*length(alf))::int+1, 1); end loop;
    exit when not exists (select 1 from perfiles where codigo_amigo = c);
  end loop; return c;
end; $$;

create or replace function public.guardar_perfil(p_handle text, p_nombre text, p_avatar int, p_publico jsonb)
returns perfiles language plpgsql security definer set search_path = public as $$
declare h text := lower(trim(p_handle)); r perfiles;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  if h !~ '^[a-z0-9_]{3,20}$' then raise exception 'handle inválido (3-20, minúsculas/números/_)'; end if;
  if exists (select 1 from perfiles where handle = h and user_id <> auth.uid()) then raise exception 'ese @ ya está tomado'; end if;
  insert into perfiles(user_id, handle, nombre, avatar, codigo_amigo, publico, actualizado)
    values (auth.uid(), h, coalesce(p_nombre,''), coalesce(p_avatar,0), public._codigo_amigo(), coalesce(p_publico,'{}'::jsonb), now())
  on conflict (user_id) do update set handle = excluded.handle, nombre = excluded.nombre,
    avatar = excluded.avatar, publico = excluded.publico, actualizado = now()
  returning * into r;
  return r;
end; $$;

create or replace function public.perfil_publico(p_handle text)
returns perfiles language sql security definer set search_path = public as $$
  select * from perfiles where handle = lower(trim(p_handle));
$$;

create or replace function public.buscar_perfiles(q text)
returns table(handle text, nombre text, avatar int)
language sql security definer set search_path = public as $$
  select handle, nombre, avatar from perfiles
  where q is not null and length(trim(q)) >= 2
    and (handle ilike '%'||trim(q)||'%' or nombre ilike '%'||trim(q)||'%')
  order by handle limit 20;
$$;
```

### Task 2: `web/src/lib/social.js` (API perfiles)
**Files:** Create `web/src/lib/social.js`

```js
import { supa, haySupabase } from './supa.js';

export async function miPerfil() {
  const { data: u } = await supa.auth.getUser();
  if (!u || !u.user) return null;
  const { data } = await supa.from('perfiles').select('*').eq('user_id', u.user.id).maybeSingle();
  return data;
}
export async function guardarPerfil({ handle, nombre, avatar, publico }) {
  const { data, error } = await supa.rpc('guardar_perfil', { p_handle: handle, p_nombre: nombre, p_avatar: avatar, p_publico: publico });
  if (error) throw error; return data[0] || data;
}
export async function perfilPublico(handle) {
  const { data, error } = await supa.rpc('perfil_publico', { p_handle: handle });
  if (error) throw error; return Array.isArray(data) ? data[0] : data;
}
export async function buscar(q) {
  const { data, error } = await supa.rpc('buscar_perfiles', { q });
  if (error) throw error; return data || [];
}
export { haySupabase };
```

### Task 3: snapshot público en `coleccion.js` + sync en `nube.js`
**Files:** Modify `web/src/lib/coleccion.js`, `web/src/lib/nube.js`

- [ ] En `coleccion.js` agregar `snapshotPublico(temas)` que arma
  `{ atrapados, shiny, conteos:{unicos,total,shinies,ejercicios}, medallas, titulos, logros }`
  desde `estado()` + `regionesDesbloqueadas` + `logros.js`.
- [ ] En `nube.js`, en `subir()`, tras subir `progreso`, llamar `guardar_perfil` con el
  snapshot SOLO si el usuario ya tiene perfil (handle). Para no acoplar de más: exponer
  `window.dispatchEvent('progreso:subido')` y que `liga.astro`/social escuchen; o un
  callback. (Implementación: helper `actualizarSnapshot()` en social.js que liga llama.)

### Task 4: `liga.astro` como hub + edición de perfil
**Files:** Modify `web/src/pages/liga.astro`
- [ ] Sección "Tu perfil social": input `@handle`, guardar (`guardarPerfil`), mostrar
  `codigo_amigo`, botón copiar link `/u?h=<handle>`, link a `/amigos`. Usa el `nombre`/
  `avatar` que la Liga ya maneja.

### Task 5: `u.astro` perfil público
**Files:** Create `web/src/pages/u.astro`
- [ ] Lee `?h=<handle>`, baja `perfilPublico`, renderiza tarjeta + medallas + conteos +
  Pokédex + logros (read-only). Botones según sesión: Agregar amigo / Proponer intercambio
  (si amigos) / Copiar link. Sin handle/encontrado → mensaje "perfil no encontrado".

**Build + screenshot** tras Etapa 1.

---

## Etapa 2 — Amigos + búsqueda

### Task 6: Migración `amistades` + RPCs
**Files:** Create `supabase/migrations/20260604150000_social_amigos.sql`

```sql
create table if not exists public.amistades (
  id uuid primary key default gen_random_uuid(),
  de_id uuid not null references auth.users(id) on delete cascade,
  a_id  uuid not null references auth.users(id) on delete cascade,
  estado text not null default 'pendiente',  -- pendiente | aceptada
  creado timestamptz not null default now(),
  unique (de_id, a_id)
);
alter table public.amistades enable row level security;
drop policy if exists "amistad select" on public.amistades;
create policy "amistad select" on public.amistades for select
  using (auth.uid() in (de_id, a_id));

create or replace function public.solicitar_amistad(p_handle text, p_codigo text)
returns void language plpgsql security definer set search_path = public as $$
declare destino uuid;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  select user_id into destino from perfiles
    where (p_handle is not null and handle = lower(trim(p_handle)))
       or (p_codigo is not null and codigo_amigo = upper(trim(p_codigo))) limit 1;
  if destino is null then raise exception 'usuario no encontrado'; end if;
  if destino = auth.uid() then raise exception 'no podés agregarte a vos mismo'; end if;
  -- si ya existe relación (en cualquier sentido), no duplicar
  if exists (select 1 from amistades where (de_id=auth.uid() and a_id=destino) or (de_id=destino and a_id=auth.uid())) then return; end if;
  insert into amistades(de_id, a_id, estado) values (auth.uid(), destino, 'pendiente');
end; $$;

create or replace function public.responder_amistad(p_id uuid, p_aceptar boolean)
returns void language plpgsql security definer set search_path = public as $$
declare s amistades;
begin
  select * into s from amistades where id = p_id for update;
  if not found or s.a_id <> auth.uid() then raise exception 'no podés responder esta solicitud'; end if;
  if p_aceptar then update amistades set estado='aceptada' where id=p_id;
  else delete from amistades where id=p_id; end if;
end; $$;

create or replace function public.quitar_amigo(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
declare s amistades;
begin
  select * into s from amistades where id=p_id;
  if not found or auth.uid() not in (s.de_id, s.a_id) then raise exception 'no autorizado'; end if;
  delete from amistades where id=p_id;
end; $$;

-- amigos aceptados (con datos de perfil) y solicitudes entrantes pendientes
create or replace function public.mis_amigos()
returns table(id uuid, user_id uuid, handle text, nombre text, avatar int)
language sql security definer set search_path = public as $$
  select a.id, p.user_id, p.handle, p.nombre, p.avatar
  from amistades a
  join perfiles p on p.user_id = case when a.de_id = auth.uid() then a.a_id else a.de_id end
  where a.estado='aceptada' and auth.uid() in (a.de_id, a.a_id);
$$;
create or replace function public.solicitudes_entrantes()
returns table(id uuid, user_id uuid, handle text, nombre text, avatar int)
language sql security definer set search_path = public as $$
  select a.id, p.user_id, p.handle, p.nombre, p.avatar
  from amistades a join perfiles p on p.user_id = a.de_id
  where a.estado='pendiente' and a.a_id = auth.uid();
$$;
create or replace function public.son_amigos(p_otro uuid)
returns boolean language sql security definer set search_path = public as $$
  select exists(select 1 from amistades where estado='aceptada'
    and ((de_id=auth.uid() and a_id=p_otro) or (de_id=p_otro and a_id=auth.uid())));
$$;
```

### Task 7: social.js — amigos
**Files:** Modify `web/src/lib/social.js`
- [ ] `solicitar({handle, codigo})`, `responder(id, aceptar)`, `quitar(id)`,
  `amigos()`→rpc `mis_amigos`, `solicitudes()`→rpc `solicitudes_entrantes`,
  `sonAmigos(otroUserId)`→rpc `son_amigos`.

### Task 8: `amigos.astro`
**Files:** Create `web/src/pages/amigos.astro`
- [ ] Buscador (`buscar`), resultados con "Agregar"; solicitudes entrantes (aceptar/✕);
  lista de amigos (link a `/u?h=`, "Proponer intercambio"); badge de pendientes.

### Task 9: nav "Amigos" en `Base.astro`
**Files:** Modify `web/src/layouts/Base.astro`
- [ ] Link a `/amigos` con badge (cuenta de solicitudes+ofertas pendientes, leída client-side).

**Build + screenshot** tras Etapa 2.

---

## Etapa 3 — Intercambios asíncronos

### Task 10: Migración `ofertas` + RPCs
**Files:** Create `supabase/migrations/20260604160000_social_ofertas.sql`

```sql
create table if not exists public.ofertas (
  id uuid primary key default gen_random_uuid(),
  de_id uuid not null references auth.users(id) on delete cascade,
  a_id  uuid not null references auth.users(id) on delete cascade,
  doy  jsonb not null default '[]'::jsonb,   -- lo que da de_id  [{id,shiny}]
  pido jsonb not null default '[]'::jsonb,   -- lo que da a_id
  estado text not null default 'pendiente',  -- pendiente|aceptada|rechazada|cancelada
  creado timestamptz not null default now(),
  resuelto timestamptz
);
alter table public.ofertas enable row level security;
drop policy if exists "oferta select" on public.ofertas;
create policy "oferta select" on public.ofertas for select using (auth.uid() in (de_id, a_id));
alter table public.ofertas replica identity full;
do $$ begin alter publication supabase_realtime add table public.ofertas;
exception when duplicate_object then null; end $$;

create or replace function public.crear_oferta(p_a_id uuid, p_doy jsonb, p_pido jsonb)
returns uuid language plpgsql security definer set search_path = public as $$
declare nid uuid;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  if not public.son_amigos(p_a_id) then raise exception 'solo podés ofertar a un amigo'; end if;
  insert into ofertas(de_id, a_id, doy, pido) values (auth.uid(), p_a_id, coalesce(p_doy,'[]'::jsonb), coalesce(p_pido,'[]'::jsonb))
    returning id into nid;
  return nid;
end; $$;

create or replace function public.cancelar_oferta(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
declare o ofertas;
begin
  select * into o from ofertas where id=p_id for update;
  if not found or o.de_id <> auth.uid() then raise exception 'no autorizado'; end if;
  if o.estado='pendiente' then update ofertas set estado='cancelada', resuelto=now() where id=p_id; end if;
end; $$;

-- aceptar = validar y ejecutar swap sobre progreso (de_id da 'doy', a_id da 'pido')
create or replace function public.responder_oferta(p_id uuid, p_aceptar boolean)
returns text language plpgsql security definer set search_path = public as $$
declare o ofertas; d_est jsonb; a_est jsonb; d_at jsonb; d_sh jsonb; a_at jsonb; a_sh jsonb;
  tmp jsonb; item jsonb; v_id text; v_sh boolean;
begin
  select * into o from ofertas where id=p_id for update;
  if not found or o.a_id <> auth.uid() then raise exception 'no podés responder esta oferta'; end if;
  if o.estado <> 'pendiente' then raise exception 'la oferta ya no está pendiente'; end if;
  if not p_aceptar then update ofertas set estado='rechazada', resuelto=now() where id=p_id; return 'rechazada'; end if;

  select estado into d_est from progreso where user_id=o.de_id for update;
  select estado into a_est from progreso where user_id=o.a_id for update;
  d_est := coalesce(d_est,'{}'::jsonb); a_est := coalesce(a_est,'{}'::jsonb);
  d_at := coalesce((d_est->>'col:atrapados')::jsonb,'{}'::jsonb); d_sh := coalesce((d_est->>'col:shiny')::jsonb,'[]'::jsonb);
  a_at := coalesce((a_est->>'col:atrapados')::jsonb,'{}'::jsonb); a_sh := coalesce((a_est->>'col:shiny')::jsonb,'[]'::jsonb);

  -- validar de_id tiene 'doy'
  tmp := d_at;
  for item in select * from jsonb_array_elements(o.doy) loop
    v_id := item->>'id'; v_sh := coalesce((item->>'shiny')::boolean,false);
    if coalesce((tmp->>v_id)::int,0) < 1 then raise exception 'el que ofrece ya no tiene %', v_id; end if;
    if v_sh and not public._arr_tiene(d_sh, v_id) then raise exception 'ya no tiene el shiny %', v_id; end if;
    tmp := public._mapa_dec(tmp, v_id);
  end loop;
  -- validar a_id tiene 'pido'
  tmp := a_at;
  for item in select * from jsonb_array_elements(o.pido) loop
    v_id := item->>'id'; v_sh := coalesce((item->>'shiny')::boolean,false);
    if coalesce((tmp->>v_id)::int,0) < 1 then raise exception 'no tenés %', v_id; end if;
    if v_sh and not public._arr_tiene(a_sh, v_id) then raise exception 'no tenés el shiny %', v_id; end if;
    tmp := public._mapa_dec(tmp, v_id);
  end loop;

  -- aplicar: de_id da 'doy' -> a_id ; a_id da 'pido' -> de_id
  for item in select * from jsonb_array_elements(o.doy) loop
    v_id := item->>'id'; v_sh := coalesce((item->>'shiny')::boolean,false);
    d_at := public._mapa_dec(d_at, v_id); a_at := public._mapa_inc(a_at, v_id);
    if v_sh then d_sh := public._arr_del(d_sh, v_id); a_sh := public._arr_add(a_sh, v_id); end if;
  end loop;
  for item in select * from jsonb_array_elements(o.pido) loop
    v_id := item->>'id'; v_sh := coalesce((item->>'shiny')::boolean,false);
    a_at := public._mapa_dec(a_at, v_id); d_at := public._mapa_inc(d_at, v_id);
    if v_sh then a_sh := public._arr_del(a_sh, v_id); d_sh := public._arr_add(d_sh, v_id); end if;
  end loop;

  d_est := jsonb_set(jsonb_set(d_est,'{col:atrapados}', to_jsonb(d_at::text)),'{col:shiny}', to_jsonb(d_sh::text));
  a_est := jsonb_set(jsonb_set(a_est,'{col:atrapados}', to_jsonb(a_at::text)),'{col:shiny}', to_jsonb(a_sh::text));
  insert into progreso(user_id,estado) values (o.de_id,d_est) on conflict (user_id) do update set estado=excluded.estado, actualizado=now();
  insert into progreso(user_id,estado) values (o.a_id,a_est) on conflict (user_id) do update set estado=excluded.estado, actualizado=now();
  update ofertas set estado='aceptada', resuelto=now() where id=p_id;
  return 'aceptada';
end; $$;

create or replace function public.mis_ofertas()
returns table(id uuid, de_id uuid, a_id uuid, doy jsonb, pido jsonb, estado text, creado timestamptz,
              otro_handle text, otro_nombre text, soy_de boolean)
language sql security definer set search_path = public as $$
  select o.id, o.de_id, o.a_id, o.doy, o.pido, o.estado, o.creado,
         p.handle, p.nombre, (o.de_id = auth.uid())
  from ofertas o
  join perfiles p on p.user_id = case when o.de_id = auth.uid() then o.a_id else o.de_id end
  where auth.uid() in (o.de_id, o.a_id) and o.estado in ('pendiente')
  order by o.creado desc;
$$;
```

### Task 11: social.js — ofertas
**Files:** Modify `web/src/lib/social.js`
- [ ] `crearOferta(aUserId, doy, pido)`, `responderOferta(id, aceptar)`,
  `cancelarOferta(id)`, `ofertas()`→rpc `mis_ofertas`.

### Task 12: UI de oferta (en `u.astro`) + inbox (en `amigos.astro`)
**Files:** Modify `web/src/pages/u.astro`, `web/src/pages/amigos.astro`
- [ ] En `u.astro` (perfil de un amigo): botón "Proponer intercambio" → modal: elegí `doy`
  de tu colección (picker como el del intercambio), `pido` de la Pokédex pública del perfil;
  `crearOferta`.
- [ ] En `amigos.astro`: sección "Intercambios" con ofertas entrantes (Aceptar/Rechazar →
  `responderOferta`) y salientes (Cancelar → `cancelarOferta`). Tras aceptar:
  `refrescarDesdeNube()` para reflejar la colección nueva.

**Build + screenshots** tras Etapa 3.

---

### Task 13: Aplicar migraciones + commit
- [ ] `supabase db push --yes` (aplica las 3 migraciones nuevas).
- [ ] `npm run build`; commit `web/` + `docs/` + `supabase/migrations/` + `superpowers/`.
- [ ] Prueba manual de 2 sesiones (perfil, amistad, oferta async).

## Self-Review
- **Cobertura spec:** perfiles+identidad (T1-5), amigos+búsqueda (T6-9), async (T10-12),
  privacidad/opt-in (T1 handle, T5 público), async friends-only (T10 `crear_oferta` usa
  `son_amigos`), sin lock (T10 valida al aceptar). ✓
- **Consistencia:** `son_amigos` (T6) usada en `crear_oferta` (T10) ✓; helpers
  `_mapa_inc/_mapa_dec/_arr_*` ya existen en la migración de intercambios ✓; shape `{id,shiny}`
  consistente con el intercambio ✓.
- **Placeholders:** SQL completo; el JS de páginas se detalla al implementar (estructura +
  APIs fijadas). Sin TODOs en el SQL/contratos.

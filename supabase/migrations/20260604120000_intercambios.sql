-- Intercambios (trades) de Pokémon: sala en vivo entre dos usuarios.
-- Toda mutación va por RPCs SECURITY DEFINER (control a nivel de columna).

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

drop policy if exists "ver intercambio propio" on public.intercambios;
create policy "ver intercambio propio" on public.intercambios for select
  using (auth.uid() = creador_id or auth.uid() = invitado_id);
-- (sin insert/update/delete directos: todo por RPC)

alter table public.intercambios replica identity full;
do $$ begin
  alter publication supabase_realtime add table public.intercambios;
exception when duplicate_object then null; end $$;

-- ===== Helpers jsonb para la colección =====
-- col:atrapados = {"<id>": <cantidad>} ; col:shiny = [<id num>...]
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

  c_estado := jsonb_set(jsonb_set(c_estado, '{col:atrapados}', to_jsonb(c_atra::text)), '{col:shiny}', to_jsonb(c_shi::text));
  i_estado := jsonb_set(jsonb_set(i_estado, '{col:atrapados}', to_jsonb(i_atra::text)), '{col:shiny}', to_jsonb(i_shi::text));
  insert into progreso(user_id, estado) values (s.creador_id, c_estado)
    on conflict (user_id) do update set estado = excluded.estado, actualizado = now();
  insert into progreso(user_id, estado) values (s.invitado_id, i_estado)
    on conflict (user_id) do update set estado = excluded.estado, actualizado = now();

  update intercambios set estado = 'completada', actualizado = now() where id = p_id;
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
  if s.creador_ok and s.invitado_ok then perform public.ejecutar_intercambio(p_id); return 'completada'; end if;
  return 'abierta';
end; $$;

-- Intercambios asíncronos: oferta directa (doy X ↔ pido Y) entre amigos.
-- Aceptar valida y ejecuta el swap sobre progreso (reusa helpers _mapa_*/_arr_*).

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
  insert into ofertas(de_id, a_id, doy, pido)
    values (auth.uid(), p_a_id, coalesce(p_doy,'[]'::jsonb), coalesce(p_pido,'[]'::jsonb))
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

  -- validar: de_id tiene 'doy'
  tmp := d_at;
  for item in select * from jsonb_array_elements(o.doy) loop
    v_id := item->>'id'; v_sh := coalesce((item->>'shiny')::boolean,false);
    if coalesce((tmp->>v_id)::int,0) < 1 then raise exception 'el que ofrece ya no tiene %', v_id; end if;
    if v_sh and not public._arr_tiene(d_sh, v_id) then raise exception 'ya no tiene el shiny %', v_id; end if;
    tmp := public._mapa_dec(tmp, v_id);
  end loop;
  -- validar: a_id (vos) tiene 'pido'
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

-- contador para el badge del nav (solicitudes de amistad + ofertas entrantes pendientes)
create or replace function public.social_pendientes()
returns int language sql security definer set search_path = public as $$
  select (select count(*) from amistades where estado='pendiente' and a_id = auth.uid())
       + (select count(*) from ofertas   where estado='pendiente' and a_id = auth.uid());
$$;

create or replace function public.mis_ofertas()
returns table(id uuid, de_id uuid, a_id uuid, doy jsonb, pido jsonb, estado text, creado timestamptz,
              otro_handle text, otro_nombre text, soy_de boolean)
language sql security definer set search_path = public as $$
  select o.id, o.de_id, o.a_id, o.doy, o.pido, o.estado, o.creado,
         p.handle, p.nombre, (o.de_id = auth.uid())
  from ofertas o
  join perfiles p on p.user_id = case when o.de_id = auth.uid() then o.a_id else o.de_id end
  where auth.uid() in (o.de_id, o.a_id) and o.estado = 'pendiente'
  order by o.creado desc;
$$;

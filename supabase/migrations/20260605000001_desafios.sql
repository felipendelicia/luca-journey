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

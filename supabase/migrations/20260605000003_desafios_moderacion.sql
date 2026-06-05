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

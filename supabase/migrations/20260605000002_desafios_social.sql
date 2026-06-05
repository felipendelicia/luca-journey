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

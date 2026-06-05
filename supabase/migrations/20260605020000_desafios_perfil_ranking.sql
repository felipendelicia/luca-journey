-- Listas para el perfil (desafíos creados + resueltos de un usuario, SIN código → sin
-- spoilers) y ranking de la comunidad (top creadores/solvers).

create or replace function public.desafios_de_usuario(p_user_id uuid)
returns table(id uuid, titulo text, region text, dificultad int, rol text)
language sql security definer set search_path = public as $$
  select d.id, d.titulo, d.region, d.dificultad, 'creado'::text
  from desafios d where d.autor = p_user_id
  union all
  select d.id, d.titulo, d.region, d.dificultad, 'resuelto'::text
  from resoluciones r join desafios d on d.id = r.desafio_id
  where r.user_id = p_user_id
  order by 5 desc, 2;   -- rol (resuelto/creado), luego título
$$;

create or replace function public.ranking_desafios()
returns table(handle text, avatar int, creados bigint, resueltos bigint)
language sql security definer set search_path = public as $$
  select p.handle, p.avatar,
         (select count(*) from desafios d where d.autor = p.user_id) as creados,
         (select count(*) from resoluciones r where r.user_id = p.user_id) as resueltos
  from perfiles p
  where (select count(*) from desafios d where d.autor = p.user_id) > 0
     or (select count(*) from resoluciones r where r.user_id = p.user_id) > 0
  order by creados desc, resueltos desc
  limit 20;
$$;

-- listar_desafios ahora devuelve la consigna (descripción) para mostrarla en cada item,
-- y la búsqueda matchea título O consigna. (DROP+CREATE porque cambia el tipo de retorno.)
drop function if exists public.listar_desafios(text, text, text, int, int);
create or replace function public.listar_desafios(p_orden text, p_q text, p_region text, p_limite int, p_offset int)
returns table(id uuid, titulo text, consigna text, dificultad int, region text, autor_handle text,
              resoluciones bigint, resuelto boolean)
language sql security definer set search_path = public as $$
  select d.id, d.titulo, d.consigna, d.dificultad, d.region, p.handle,
         (select count(*) from resoluciones r where r.desafio_id = d.id),
         exists(select 1 from resoluciones r2 where r2.desafio_id = d.id and r2.user_id = auth.uid())
  from desafios d
  left join perfiles p on p.user_id = d.autor
  where (p_region is null or p_region = '' or p_region = 'todas' or d.region = p_region)
    and (p_q is null or trim(p_q) = '' or d.titulo ilike '%'||trim(p_q)||'%' or d.consigna ilike '%'||trim(p_q)||'%')
    and (d.autor = auth.uid()
         or (select count(*) from reportes rp where rp.desafio_id = d.id) < 3)
  order by case when p_orden = 'resueltos' then (select count(*) from resoluciones r where r.desafio_id = d.id) end desc nulls last,
           case when p_orden = 'dificultad' then d.dificultad end desc nulls last,
           d.creado desc
  limit greatest(1, least(coalesce(p_limite, 30), 60)) offset greatest(0, coalesce(p_offset, 0));
$$;

-- Listado paginado de todos los perfiles, ordenado por cantidad de Pokémon (ranking).
-- Somos pocos usuarios. Excluye al que llama. 'pokes' = total de Pokémon (conteos.total).
create or replace function public.listar_perfiles(p_limite int, p_offset int)
returns table(handle text, nombre text, avatar int, pokes int, total bigint)
language sql security definer set search_path = public as $$
  select handle, nombre, avatar,
         coalesce((publico->'conteos'->>'total')::int, 0) as pokes,
         count(*) over() as total
  from perfiles
  where user_id <> coalesce(auth.uid(), '00000000-0000-0000-0000-000000000000'::uuid)
  order by coalesce((publico->'conteos'->>'total')::int, 0) desc,
           coalesce((publico->'conteos'->>'unicos')::int, 0) desc,
           handle
  limit  greatest(1, least(coalesce(p_limite, 10), 50))
  offset greatest(0, coalesce(p_offset, 0));
$$;

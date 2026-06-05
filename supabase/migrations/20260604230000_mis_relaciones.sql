-- Devuelve, por cada relación de amistad del que llama, el handle del OTRO + el estado.
-- Sirve para ocultar "Agregar" en listados cuando ya hay amistad/pendiente.
create or replace function public.mis_relaciones()
returns table(handle text, estado text)
language sql security definer set search_path = public as $$
  select p.handle, a.estado
  from amistades a
  join perfiles p on p.user_id = case when a.de_id = auth.uid() then a.a_id else a.de_id end
  where auth.uid() in (a.de_id, a.a_id);
$$;

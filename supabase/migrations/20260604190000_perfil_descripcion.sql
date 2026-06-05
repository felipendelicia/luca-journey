-- Descripción editable del perfil (bio). Máx 200 chars.
alter table public.perfiles add column if not exists descripcion text not null default '';

create or replace function public.actualizar_descripcion(p_desc text)
returns void language plpgsql security definer set search_path = public as $$
begin
  update perfiles set descripcion = left(coalesce(p_desc, ''), 200), actualizado = now()
    where user_id = auth.uid();
end; $$;

-- re-crear para que el rowtype incluya la columna nueva
create or replace function public.perfil_publico(p_handle text)
returns perfiles language sql security definer set search_path = public as $$
  select * from perfiles where handle = lower(trim(p_handle));
$$;

-- El nombre de usuario (@handle) es inmutable: una vez creado el perfil, guardar_perfil
-- solo actualiza avatar y snapshot; el handle/nombre quedan fijos.
create or replace function public.guardar_perfil(p_handle text, p_nombre text, p_avatar int, p_publico jsonb)
returns perfiles language plpgsql security definer set search_path = public as $$
declare h text := lower(trim(p_handle)); r perfiles; existe perfiles;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  select * into existe from perfiles where user_id = auth.uid();
  if found then
    update perfiles set avatar = coalesce(p_avatar, existe.avatar),
                        publico = coalesce(p_publico, existe.publico),
                        actualizado = now()
      where user_id = auth.uid() returning * into r;
    return r;     -- handle/nombre inmutables
  end if;
  if h !~ '^[a-z0-9_]{3,20}$' then raise exception 'usuario inválido (3-20, minúsculas, números o _)'; end if;
  if exists (select 1 from perfiles where handle = h) then raise exception 'ese @ ya está tomado'; end if;
  insert into perfiles(user_id, handle, nombre, avatar, codigo_amigo, publico, actualizado)
    values (auth.uid(), h, coalesce(p_nombre, h), coalesce(p_avatar, 0), public._codigo_amigo(), coalesce(p_publico, '{}'::jsonb), now())
    returning * into r;
  return r;
end; $$;

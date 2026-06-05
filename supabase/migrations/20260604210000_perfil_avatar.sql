-- El avatar elegido (col:avatar) ahora se sincroniza al perfil público junto con el snapshot.
create or replace function public.actualizar_publico(p_publico jsonb, p_avatar int default null)
returns void language plpgsql security definer set search_path = public as $$
begin
  update perfiles set publico = coalesce(p_publico, '{}'::jsonb),
                      avatar  = coalesce(p_avatar, avatar),
                      actualizado = now()
    where user_id = auth.uid();
end; $$;

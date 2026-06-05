-- one-off (pedido del owner): +100 Pokébolas a @lucario.
do $$
declare v_uid uuid; v_antes int; v_despues int;
begin
  select user_id into v_uid from public.perfiles where handle = 'lucario';
  if v_uid is null then raise notice 'perfil lucario no encontrado'; return; end if;
  select coalesce((estado->>'col:balls')::int, 0) into v_antes from public.progreso where user_id = v_uid;
  update public.progreso
     set estado = jsonb_set(coalesce(estado, '{}'::jsonb), '{col:balls}',
           to_jsonb((coalesce((estado->>'col:balls')::int, 0) + 100)::text)),
         actualizado = now()
   where user_id = v_uid;
  select coalesce((estado->>'col:balls')::int, 0) into v_despues from public.progreso where user_id = v_uid;
  raise notice 'lucario balls: % -> %', v_antes, v_despues;
end $$;

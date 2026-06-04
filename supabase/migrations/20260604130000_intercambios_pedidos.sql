-- Pedidos (wishlist) + ver la colección del otro durante un trade abierto.

alter table public.intercambios
  add column if not exists creador_pedido  jsonb not null default '[]'::jsonb,
  add column if not exists invitado_pedido jsonb not null default '[]'::jsonb;

-- Ver la colección del OTRO participante. Solo dentro de un trade 'abierta' y solo
-- entre los dos participantes (privacidad acotada al intercambio en curso).
create or replace function public.coleccion_del_otro(p_id uuid)
returns jsonb language plpgsql security definer set search_path = public as $$
declare s intercambios; otro uuid; est jsonb;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  select * into s from intercambios where id = p_id;
  if not found then raise exception 'sala no encontrada'; end if;
  if auth.uid() not in (s.creador_id, s.invitado_id) then raise exception 'no sos participante'; end if;
  if s.estado <> 'abierta' then raise exception 'la sala no está abierta'; end if;
  otro := case when auth.uid() = s.creador_id then s.invitado_id else s.creador_id end;
  if otro is null then
    return jsonb_build_object('atrapados', '{}'::jsonb, 'shiny', '[]'::jsonb);
  end if;
  select estado into est from progreso where user_id = otro;
  est := coalesce(est, '{}'::jsonb);
  return jsonb_build_object(
    'atrapados', coalesce((est->>'col:atrapados')::jsonb, '{}'::jsonb),
    'shiny',     coalesce((est->>'col:shiny')::jsonb, '[]'::jsonb)
  );
end; $$;

-- Setear el pedido (wishlist) del que llama. NO resetea confirmaciones: el pedido no
-- mueve bienes hasta que el dueño lo acepta (eso pasa por poner_lote).
create or replace function public.poner_pedido(p_id uuid, p_pedido jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare s intercambios;
begin
  select * into s from intercambios where id = p_id for update;
  if not found then raise exception 'sala no encontrada'; end if;
  if s.estado <> 'abierta' then raise exception 'la sala no está abierta'; end if;
  if auth.uid() = s.creador_id then
    update intercambios set creador_pedido = p_pedido, actualizado = now() where id = p_id;
  elsif auth.uid() = s.invitado_id then
    update intercambios set invitado_pedido = p_pedido, actualizado = now() where id = p_id;
  else raise exception 'no sos participante'; end if;
end; $$;

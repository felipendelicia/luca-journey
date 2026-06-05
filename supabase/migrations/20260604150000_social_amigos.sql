-- Amigos: solicitud → aceptar (mutuo). Toda mutación por RPC security definer.

create table if not exists public.amistades (
  id uuid primary key default gen_random_uuid(),
  de_id uuid not null references auth.users(id) on delete cascade,
  a_id  uuid not null references auth.users(id) on delete cascade,
  estado text not null default 'pendiente',  -- pendiente | aceptada
  creado timestamptz not null default now(),
  unique (de_id, a_id)
);
alter table public.amistades enable row level security;
drop policy if exists "amistad select" on public.amistades;
create policy "amistad select" on public.amistades for select using (auth.uid() in (de_id, a_id));

create or replace function public.solicitar_amistad(p_handle text, p_codigo text)
returns void language plpgsql security definer set search_path = public as $$
declare destino uuid;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  select user_id into destino from perfiles
    where (p_handle is not null and handle = lower(trim(p_handle)))
       or (p_codigo is not null and codigo_amigo = upper(trim(p_codigo))) limit 1;
  if destino is null then raise exception 'usuario no encontrado'; end if;
  if destino = auth.uid() then raise exception 'no podés agregarte a vos mismo'; end if;
  if exists (select 1 from amistades where (de_id=auth.uid() and a_id=destino) or (de_id=destino and a_id=auth.uid())) then return; end if;
  insert into amistades(de_id, a_id, estado) values (auth.uid(), destino, 'pendiente');
end; $$;

create or replace function public.responder_amistad(p_id uuid, p_aceptar boolean)
returns void language plpgsql security definer set search_path = public as $$
declare s amistades;
begin
  select * into s from amistades where id = p_id for update;
  if not found or s.a_id <> auth.uid() then raise exception 'no podés responder esta solicitud'; end if;
  if p_aceptar then update amistades set estado='aceptada' where id=p_id;
  else delete from amistades where id=p_id; end if;
end; $$;

create or replace function public.quitar_amigo(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
declare s amistades;
begin
  select * into s from amistades where id=p_id;
  if not found or auth.uid() not in (s.de_id, s.a_id) then raise exception 'no autorizado'; end if;
  delete from amistades where id=p_id;
end; $$;

create or replace function public.mis_amigos()
returns table(id uuid, user_id uuid, handle text, nombre text, avatar int)
language sql security definer set search_path = public as $$
  select a.id, p.user_id, p.handle, p.nombre, p.avatar
  from amistades a
  join perfiles p on p.user_id = case when a.de_id = auth.uid() then a.a_id else a.de_id end
  where a.estado='aceptada' and auth.uid() in (a.de_id, a.a_id);
$$;

create or replace function public.solicitudes_entrantes()
returns table(id uuid, user_id uuid, handle text, nombre text, avatar int)
language sql security definer set search_path = public as $$
  select a.id, p.user_id, p.handle, p.nombre, p.avatar
  from amistades a join perfiles p on p.user_id = a.de_id
  where a.estado='pendiente' and a.a_id = auth.uid();
$$;

create or replace function public.son_amigos(p_otro uuid)
returns boolean language sql security definer set search_path = public as $$
  select exists(select 1 from amistades where estado='aceptada'
    and ((de_id=auth.uid() and a_id=p_otro) or (de_id=p_otro and a_id=auth.uid())));
$$;

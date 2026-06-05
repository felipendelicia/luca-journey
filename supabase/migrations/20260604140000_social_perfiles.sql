-- Perfiles públicos: identidad social (handle único + código de amigo) + snapshot público.
-- progreso sigue privado; acá vive solo lo que se muestra (select público).

create table if not exists public.perfiles (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  handle       text unique not null,
  nombre       text not null default '',
  avatar       int  not null default 0,
  codigo_amigo text unique not null,
  publico      jsonb not null default '{}'::jsonb,
  actualizado  timestamptz not null default now()
);
alter table public.perfiles enable row level security;
drop policy if exists "perfil select publico" on public.perfiles;
create policy "perfil select publico" on public.perfiles for select using (true);
-- insert/update solo via RPC security definer (sin policy de escritura directa)

create or replace function public._codigo_amigo() returns text language plpgsql as $$
declare alf text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; c text;
begin
  loop
    c := ''; for i in 1..6 loop c := c || substr(alf, floor(random()*length(alf))::int+1, 1); end loop;
    exit when not exists (select 1 from perfiles where codigo_amigo = c);
  end loop; return c;
end; $$;

create or replace function public.guardar_perfil(p_handle text, p_nombre text, p_avatar int, p_publico jsonb)
returns perfiles language plpgsql security definer set search_path = public as $$
declare h text := lower(trim(p_handle)); r perfiles;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  if h !~ '^[a-z0-9_]{3,20}$' then raise exception 'handle inválido (3-20, minúsculas/números/_)'; end if;
  if exists (select 1 from perfiles where handle = h and user_id <> auth.uid()) then raise exception 'ese @ ya está tomado'; end if;
  insert into perfiles(user_id, handle, nombre, avatar, codigo_amigo, publico, actualizado)
    values (auth.uid(), h, coalesce(p_nombre,''), coalesce(p_avatar,0), public._codigo_amigo(), coalesce(p_publico,'{}'::jsonb), now())
  on conflict (user_id) do update set handle = excluded.handle, nombre = excluded.nombre,
    avatar = excluded.avatar, publico = excluded.publico, actualizado = now()
  returning * into r;
  return r;
end; $$;

-- actualizar solo el snapshot público (no-op si el usuario aún no tiene perfil)
create or replace function public.actualizar_publico(p_publico jsonb)
returns void language plpgsql security definer set search_path = public as $$
begin
  update perfiles set publico = coalesce(p_publico,'{}'::jsonb), actualizado = now() where user_id = auth.uid();
end; $$;

create or replace function public.perfil_publico(p_handle text)
returns perfiles language sql security definer set search_path = public as $$
  select * from perfiles where handle = lower(trim(p_handle));
$$;

create or replace function public.buscar_perfiles(q text)
returns table(handle text, nombre text, avatar int)
language sql security definer set search_path = public as $$
  select handle, nombre, avatar from perfiles
  where q is not null and length(trim(q)) >= 2
    and (handle ilike '%'||trim(q)||'%' or nombre ilike '%'||trim(q)||'%')
  order by handle limit 20;
$$;

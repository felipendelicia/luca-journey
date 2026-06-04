-- Progreso del usuario en la nube. Un blob jsonb por usuario que espeja el
-- localStorage del navegador (ejercicios, colección, balls, shiny, logros).
-- Seguridad: RLS estricta — cada usuario SOLO puede ver/editar su propia fila.

create table if not exists public.progreso (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  estado      jsonb       not null default '{}'::jsonb,
  actualizado timestamptz not null default now()
);

alter table public.progreso enable row level security;

-- Políticas: auth.uid() (el usuario logueado) debe coincidir con user_id.
drop policy if exists "leer propio" on public.progreso;
create policy "leer propio"
  on public.progreso for select
  using (auth.uid() = user_id);

drop policy if exists "insertar propio" on public.progreso;
create policy "insertar propio"
  on public.progreso for insert
  with check (auth.uid() = user_id);

drop policy if exists "actualizar propio" on public.progreso;
create policy "actualizar propio"
  on public.progreso for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "borrar propio" on public.progreso;
create policy "borrar propio"
  on public.progreso for delete
  using (auth.uid() = user_id);

-- Mantener 'actualizado' al día en cada update.
create or replace function public.tocar_actualizado()
returns trigger
language plpgsql
as $$
begin
  new.actualizado = now();
  return new;
end;
$$;

drop trigger if exists trg_progreso_actualizado on public.progreso;
create trigger trg_progreso_actualizado
  before update on public.progreso
  for each row execute function public.tocar_actualizado();

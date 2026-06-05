-- Realtime sobre progreso: cuando un intercambio (async o en vivo) cambia tu colección
-- en el server, el cliente recibe el UPDATE de SU propia fila y la aplica sin re-login.
-- RLS sigue acotando: cada usuario solo recibe cambios de su propia fila.
alter table public.progreso replica identity full;
do $$ begin
  alter publication supabase_realtime add table public.progreso;
exception when duplicate_object then null; end $$;

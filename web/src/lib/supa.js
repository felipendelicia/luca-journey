// Cliente de Supabase. La URL y la anon key son PÚBLICAS por diseño: la seguridad
// la da RLS (cada usuario solo accede a su fila). Se leen de variables de entorno
// con prefijo PUBLIC_ (Astro las expone al navegador).
//
// Si no están configuradas, `supa` queda en null y la app funciona igual que antes
// (solo localStorage). Eso es el modo HÍBRIDO: la nube es opcional.
import { createClient } from '@supabase/supabase-js';

const URL = import.meta.env.PUBLIC_SUPABASE_URL || '';
const ANON = import.meta.env.PUBLIC_SUPABASE_ANON_KEY || '';

export const haySupabase = Boolean(URL && ANON);
export const supa = haySupabase ? createClient(URL, ANON) : null;

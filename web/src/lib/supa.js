// supa.js — shim de compatibilidad. La app ya no usa Supabase; este archivo solo re-exporta
// `haySupabase` (= hayApi) para no romper imports existentes (ej. Base.astro). `supa` queda null.
export { hayApi as haySupabase } from './api.js';
export const supa = null;

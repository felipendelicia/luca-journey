// Prefija los links con el base path del sitio (import.meta.env.BASE_URL).
// En dev es '/', en el build de producción es '/luca-journey/'. Así los links
// funcionan tanto local como en GitHub Pages sin tocar nada.
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');
export const u = (p = '/') => BASE + (p.startsWith('/') ? p : '/' + p);

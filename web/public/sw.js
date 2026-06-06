// Service worker mínimo y seguro para instalar como app (PWA).
// - Base-aware: deriva la ruta del scope (sirve en dev '/' y en Pages '/luca-journey/').
// - HTML: network-first (siempre fresco tras un deploy; fallback a caché si no hay red).
// - Assets de Astro (/_astro/, con hash en el nombre): cache-first (el nombre cambia
//   en cada build, así que cachear es seguro y da carga offline/rápida).
// - Pyodide (jsdelivr) y sprites/cries (githubusercontent): cache-first en un caché aparte,
//   para que la 2da carga sea casi instantánea y funcione parcialmente offline.
const VERSION = 'v4';
const CACHE = 'pokedex-codex-' + VERSION;
const CDN = 'pokedex-cdn-v1';   // pyodide + sprites + cries (inmutables/versionados) — sobrevive deploys
const SCOPE = new URL(self.registration.scope).pathname; // '/' o '/luca-journey/'
const CDN_HOSTS = ['cdn.jsdelivr.net', 'raw.githubusercontent.com'];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll([SCOPE]).catch(() => {})));
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys.filter((k) => k.startsWith('pokedex-codex-') && k !== CACHE).map((k) => caches.delete(k))
    );   // (no se borra CDN: pyodide/sprites son inmutables y caros de re-bajar)
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) {
    // Pyodide + sprites/cries: cache-first (inmutables). El resto de CDNs → red directa.
    if (CDN_HOSTS.includes(url.host)) {
      e.respondWith(caches.open(CDN).then(async (c) => {
        const hit = await c.match(req);
        if (hit) return hit;
        try {
          const res = await fetch(req);   // puede ser opaca (cross-origin sin CORS): igual sirve
          if (res && (res.ok || res.type === 'opaque')) c.put(req, res.clone());
          return res;
        } catch { return (await c.match(req)) || Response.error(); }
      }));
    }
    return;
  }

  if (url.pathname.includes('/_astro/')) {
    e.respondWith(caches.open(CACHE).then(async (c) => {
      const hit = await c.match(req);
      if (hit) return hit;
      const res = await fetch(req);
      if (res.ok) c.put(req, res.clone());
      return res;
    }));
    return;
  }

  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        // no-store: nunca tomar el HTML del caché HTTP del browser (evita HTML viejo que
        // apunta a assets hasheados que ya no existen tras un deploy).
        const res = await fetch(req, { cache: 'no-store' });
        (await caches.open(CACHE)).put(req, res.clone());
        return res;
      } catch {
        const c = await caches.open(CACHE);
        return (await c.match(req)) || (await c.match(SCOPE)) || Response.error();
      }
    })());
    return;
  }

  e.respondWith(fetch(req).catch(() => caches.match(req)));
});

# Diseño — API self-hosted (NestJS + Prisma + Postgres) reemplazando Supabase

Fecha: 2026-06-05
Estado: aprobado

> Ubicación `superpowers/` (raíz), NO `docs/` (el build limpia `docs/`).

## Objetivo

Sacar **todas** las responsabilidades de Supabase (Postgres + Auth Google + Realtime +
RPCs) y llevarlas a una **API propia self-hosted** con **Docker**, de modo que la app Astro
funcione **exactamente como ahora**. Motivación: propiedad/control total del backend (no es
un fix a límites de cupo — esos están lejísimos a esta escala).

Enfoque elegido: **reimplementar toda la lógica en TypeScript (NestJS) sobre Prisma**, sin
reusar plpgsql. Stack confirmado: **NestJS**. Login: **Google** (igual que hoy). Datos:
**migrar todo** desde Supabase. Frontend: **sigue en GitHub Pages** (→ CORS).

## Decisiones

- **Toda la lógica en Nest/Prisma.** Los ~30 RPCs `security definer` y las RLS de Supabase
  se reimplementan como métodos de servicio + guards. Sin Postgres functions, sin RLS.
- **El servidor controla todas las escrituras** → el realtime no necesita `postgres_changes`:
  cada mutación emite su evento WS al terminar.
- **Páginas sin tocar.** Se reescriben los *internals* de `nube/social/trades/presencia/
  desafios.js` manteniendo **idénticas las firmas exportadas**. `amigos/intercambio/liga/u/
  Base` no cambian.
- **`supa.js` → `api.js`** (fetch+JWT). `haySupabase` se mantiene como **alias exportado**
  (`hayApi`) para no romper imports existentes.
- **JWT único ~30 días, sin refresh token** (re-login al vencer). Simplicidad sobre rotación.
- **Presence/broadcast en memoria** en el gateway WS (asumimos **1 instancia**).
- **`supabase/`** queda en git como referencia y se deja de usar.

## Riesgos asumidos

- Reimplementar el **swap atómico de colección** (trade en vivo + oferta async) en TS es la
  parte sensible: un bug mete doble-gasto o races en la economía de Pokémon. Mitigación:
  transacción Prisma `Serializable` + `SELECT … FOR UPDATE` sobre las filas de `progreso`
  de ambos usuarios (orden fijo por id → sin deadlock), validación de multiplicidad/shiny
  idéntica al plpgsql, y **tests** del swap (casos: cantidades, shiny, falta de stock,
  doble confirmación, cancelación).
- Operación pasa a ser tuya: uptime, backups, parches, TLS. Fuera del alcance del código
  pero se documenta (`docker-compose` + nota de reverse proxy/backup).

## Arquitectura / layout

```
luca-journey/
  api/                          ← NestJS (nuevo)
    prisma/
      schema.prisma
      migrations/
      seed-import.ts            ← importador one-off del dump de Supabase
    src/
      main.ts                   ← CORS, bootstrap WS
      prisma/prisma.service.ts
      auth/                     ← Google OAuth + JWT (guard + @CurrentUser)
      progreso/
      intercambios/
      social/                   ← perfiles + amigos + ofertas
      desafios/
      realtime/                 ← EventsGateway + RealtimeService (inyectable)
    Dockerfile
    .env.example
  docker-compose.yml            ← db (postgres:17) + api
  web/
    .env                        ← PUBLIC_API_URL (reemplaza PUBLIC_SUPABASE_*)
    src/lib/
      api.js                    ← fetch+JWT + auth (reemplaza supa.js)
      realtime.js               ← cliente WS
      nube.js social.js trades.js presencia.js desafios.js  ← internals reescritos
  supabase/                     ← referencia histórica, sin uso
```

## Modelo de datos (Prisma)

Diez modelos: las 9 tablas actuales + `User` (que reemplaza `auth.users`). `estado` de
`Progreso` queda **Json opaco** (espeja localStorage). Solo el swap y `registrar_resolucion`
leen/escriben claves internas (`col:atrapados` mapa `{id:cant}`, `col:shiny` array `[id]`,
`col:balls` int), manipuladas en JS.

```prisma
model User {
  id         String   @id @default(uuid())   // UUID; se preservan los de Supabase al migrar
  email      String   @unique
  googleSub  String?  @unique                 // se completa en el primer login (match por email)
  creado     DateTime @default(now())
  // relaciones inversas: progreso, perfil, etc.
}
model Progreso {
  userId      String   @id
  estado      Json     @default("{}")
  actualizado DateTime @updatedAt
}
model Perfil {
  userId      String   @id
  handle      String   @unique               // 3-20 [a-z0-9_], INMUTABLE tras creación
  nombre      String   @default("")
  avatar      Int      @default(0)
  codigoAmigo String   @unique               // 6 chars alfabeto sin ambiguos
  publico     Json     @default("{}")
  descripcion String   @default("")          // máx 200
  actualizado DateTime @updatedAt
}
model Amistad {
  id     String  @id @default(uuid())
  deId   String
  aId    String
  estado String  @default("pendiente")       // pendiente | aceptada
  creado DateTime @default(now())
  @@unique([deId, aId])
}
model Oferta {
  id       String   @id @default(uuid())
  deId     String
  aId      String
  doy      Json     @default("[]")            // [{id, shiny}]
  pido     Json     @default("[]")
  estado   String   @default("pendiente")     // pendiente|aceptada|rechazada|cancelada
  creado   DateTime @default(now())
  resuelto DateTime?
}
model Intercambio {
  id             String   @id @default(uuid())
  codigo         String   @unique
  creadorId      String
  invitadoId     String?
  creadorNombre  String   @default("")
  invitadoNombre String   @default("")
  creadorLote    Json     @default("[]")
  invitadoLote   Json     @default("[]")
  creadorPedido  Json     @default("[]")
  invitadoPedido Json     @default("[]")
  creadorOk      Boolean  @default(false)
  invitadoOk     Boolean  @default(false)
  estado         String   @default("abierta") // abierta|completada|cancelada
  creado         DateTime @default(now())
  actualizado    DateTime @updatedAt
}
model Desafio {
  id         String   @id @default(uuid())
  autor      String
  titulo     String
  consigna   String   @default("")
  func       String
  starter    String   @default("")
  casos      Json     @default("[]")          // [{args, esperado, ejemplo}]
  dificultad Int      @default(3)             // 1..8
  region     String   @default("libre")
  creado     DateTime @default(now())
}
model Resolucion {
  id        String   @id @default(uuid())
  desafioId String
  userId    String
  codigo    String   @default("")
  creado    DateTime @default(now())
  @@unique([desafioId, userId])
}
model Voto {
  resolucionId String
  userId       String
  @@id([resolucionId, userId])
}
model Reporte {
  desafioId String
  userId    String
  motivo    String   @default("")
  creado    DateTime @default(now())
  @@id([desafioId, userId])
}
```

FKs con `onDelete: Cascade` (igual que el `references … on delete cascade` actual). Sin RLS:
cada método de servicio aplica el control de acceso que hacían los RPCs.

## API REST (mapeo RPC → endpoint)

JWT en `Authorization: Bearer <jwt>`. `JwtAuthGuard` global salvo rutas marcadas
`@Public()`. `@CurrentUser()` inyecta el `userId` del token. Cada handler replica **exacto**
las validaciones del RPC equivalente (mensajes de error incluidos).

| Módulo | Endpoint | RPC original |
|---|---|---|
| auth | `GET /auth/google` | (Supabase OAuth) |
| auth | `GET /auth/google/callback` → redirige a `FRONTEND/#token=<jwt>` | (OAuth callback) |
| auth | `GET /auth/me` | `auth.getUser` |
| progreso | `GET /progreso` | `from('progreso').select` |
| progreso | `PUT /progreso` (upsert propio) | `from('progreso').upsert` |
| intercambios | `POST /trades` | `crear_intercambio` |
| intercambios | `POST /trades/join` | `unirse` |
| intercambios | `GET /trades/:id` | `from('intercambios').select` (leerSala) |
| intercambios | `POST /trades/:id/lote` | `poner_lote` |
| intercambios | `POST /trades/:id/pedido` | `poner_pedido` |
| intercambios | `GET /trades/:id/otro` | `coleccion_del_otro` |
| intercambios | `POST /trades/:id/confirm` | `confirmar` (→ `ejecutar_intercambio`) |
| intercambios | `POST /trades/:id/cancel` | `cancelar` |
| social·perfil | `GET /perfil/me` | `from('perfiles').select` (miPerfil) |
| social·perfil | `POST /perfil` | `guardar_perfil` (handle inmutable) |
| social·perfil | `POST /perfil/publico` | `actualizar_publico` |
| social·perfil | `POST /perfil/descripcion` | `actualizar_descripcion` |
| social·perfil | `GET /perfil/:handle` | `perfil_publico` |
| social·perfil | `GET /perfiles?q=` | `buscar_perfiles` |
| social·perfil | `GET /perfiles/listar?limite&offset` | `listar_perfiles` |
| social·amigos | `POST /amigos/solicitar` | `solicitar_amistad` |
| social·amigos | `POST /amigos/:id/responder` | `responder_amistad` |
| social·amigos | `DELETE /amigos/:id` | `quitar_amigo` |
| social·amigos | `GET /amigos` | `mis_amigos` |
| social·amigos | `GET /amigos/solicitudes` | `solicitudes_entrantes` |
| social·amigos | `GET /amigos/son/:otro` | `son_amigos` |
| social·amigos | `GET /amigos/relaciones` | `mis_relaciones` |
| social·ofertas | `POST /ofertas` | `crear_oferta` |
| social·ofertas | `POST /ofertas/:id/responder` | `responder_oferta` (→ swap) |
| social·ofertas | `DELETE /ofertas/:id` | `cancelar_oferta` |
| social·ofertas | `GET /ofertas` | `mis_ofertas` |
| social·ofertas | `GET /social/pendientes` | `social_pendientes` |
| desafios | `POST /desafios` | `crear_desafio` |
| desafios | `GET /desafios?orden&q&region&limite&offset` | `listar_desafios` |
| desafios | `GET /desafios/:id` | `from('desafios').select` (leerDesafio) |
| desafios | `POST /desafios/:id/resolver` | `registrar_resolucion` (→ balls) |
| desafios | `GET /desafios/:id/soluciones` | `soluciones_de` (gated) |
| desafios | `POST /resoluciones/:id/votar` | `votar` |
| desafios | `GET /usuarios/:id/desafios` | `desafios_de_usuario` |
| desafios | `GET /desafios/ranking` | `ranking_desafios` |
| desafios | `GET /usuarios/:id/stats` | `stats_desafios` |
| desafios | `POST /desafios/:id/reportar` | `reportar_desafio` |
| desafios | `DELETE /desafios/:id` | `borrar_desafio` |

### Reglas de negocio a preservar (no obvias)

- **`guardar_perfil`**: handle/nombre **inmutables** tras crear; updates solo tocan avatar +
  publico. Handle válido `^[a-z0-9_]{3,20}$`, único. Genera `codigoAmigo` al crear.
- **`solicitar_amistad`**: por handle o por código; no a vos mismo; no duplicar si ya existe
  relación en cualquier dirección.
- **Spoiler-gate `soluciones_de` / `GET /desafios/:id/soluciones`**: solo si el que llama
  **resolvió** ese desafío o es el **autor**.
- **`listar_desafios`**: oculta desafíos con **≥3 reportes** (salvo a su autor); ordena por
  `orden` (recientes|resueltos|dificultad); busca en título **o** consigna; devuelve
  consigna + flag `resuelto` por usuario.
- **`registrar_resolucion`**: premia `2 × dificultad` balls **solo la primera vez** (upsert
  con on-conflict que no re-premia). Modifica `col:balls` del progreso propio.
- **`coleccion_del_otro`**: solo dentro de un trade `abierta` y solo entre participantes.
- **`social_pendientes`**: solicitudes de amistad entrantes + ofertas entrantes pendientes.

### Swap atómico (confirmar trade / aceptar oferta)

```
prisma.$transaction(async tx => {
  // lock determinista (orden por userId) de ambas filas de progreso
  SELECT estado FROM "Progreso" WHERE "userId" IN ($a,$b) ORDER BY "userId" FOR UPDATE;
  // validar sobre copias: cantidad >= 1 por item, y si shiny → presente en col:shiny
  // aplicar: dec/inc en col:atrapados, mover ids en col:shiny (helpers mapaInc/mapaDec/arr*)
  // escribir ambas filas
  // marcar intercambio=completada / oferta=aceptada
}, { isolationLevel: 'Serializable' });
// fuera de la tx, al commitear OK → emitir WS progreso a ambos + sala
```

Helpers `mapaInc/mapaDec/arrTiene/arrAdd/arrDel` portados 1:1 desde el plpgsql, en TS.

## Realtime (WebSocket gateway)

NestJS `@WebSocketGateway` (socket.io o ws nativo). El cliente conecta con el JWT. Como
**todas** las escrituras pasan por la API, el server emite tras la mutación (no hay
`postgres_changes`). `RealtimeService` (provider compartido) se inyecta en los módulos para
emitir.

Topics:

- **`progreso:<uid>`** — tras swap de trade/oferta, emite el nuevo `estado` a las sockets de
  ese user. `nube.js` lo aplica al cache y muestra el toast "🔄 tu colección se actualizó".
- **`sala:<id>`** — tras cada mutación del intercambio (unirse/lote/pedido/confirm/cancel)
  emite la fila nueva a los participantes; además **presence** de la sala (quién está
  dentro). `trades.js`.
- **`presencia-global`** — **presence** set de online + **broadcast `invitacion`** ruteado
  al destinatario (`{to, codigo, de}`). `presencia.js`.

Presence (quién está online / en una sala) y ruteo de invitaciones: **en memoria** en el
gateway. Estructuras: `Map<userId, Set<socket>>` global y `Map<salaId, Set<userId>>` por
sala. En connect/subscribe/disconnect se recalcula y se emite `sync` a los suscriptores
(misma semántica que `presenceState()` de Supabase: las keys son user ids).

## Auth Google + sesión cliente

Flujo (mantiene la UX actual: overlay de boot, redirect, captura de token en el hash):

1. Cliente: `loginGoogle()` → `window.location = {API}/auth/google?redirect=<frontendURL>`.
2. `GET /auth/google` → redirige al consent de Google (passport-google-oauth20 o flujo
   manual con `GOOGLE_CLIENT_ID/SECRET`, `GOOGLE_CALLBACK_URL`).
3. Google → `GET /auth/google/callback?code=…`: intercambia el code, obtiene `{sub, email}`,
   **upsert User** (si `email` existe por migración, completa `googleSub`; si no, crea),
   emite JWT (~30 d, payload `{ sub: userId, email }`), redirige a `FRONTEND/#token=<jwt>`.
4. Cliente `api.js` al cargar: parsea `#token`, lo guarda en `localStorage`, limpia el hash.
   `getUser()` decodifica el JWT (o llama `/auth/me`). `onAuthStateChange(cb)` se emula con
   un EventTarget interno que dispara al setear/borrar token. `logout()` borra token + reload.

`api.js` adjunta `Authorization: Bearer` en cada request; base URL desde `PUBLIC_API_URL`.
Si `PUBLIC_API_URL` falta → `hayApi=false` y la app corre en modo solo-localStorage (igual
que el `haySupabase=false` de hoy).

## Cliente — reescritura de internals (páginas intactas)

- `supa.js` → `api.js`: exporta `hayApi` (+ alias `haySupabase = hayApi`), un objeto `auth`
  (`loginGoogle/logout/getUser/onAuthStateChange`) y helpers `apiGet/apiPost/apiPut/apiDelete`.
- `realtime.js`: `conectar(jwt)`, `suscribir(topic, handlers)`, `presence(topic)`, `enviar`/
  `broadcast`, `desuscribir`. Expone lo que `nube/trades/presencia` necesitan.
- `nube.js`: `bajar`→`GET /progreso`, `subir`→`PUT /progreso`, `suscribirProgreso`→
  `realtime.suscribir('progreso:<uid>')`. Auth via `api.auth`. Mismas firmas exportadas
  (`init/usuario/loginGoogle/logout/refrescarDesdeNube`).
- `social.js`, `desafios.js`: cada `supa.rpc(...)` → `apiPost/apiGet` al endpoint mapeado.
  Mismas firmas exportadas.
- `trades.js`: RPCs → endpoints; `suscribir(id, miId, {onCambio, onPresencia})` →
  `realtime` sobre `sala:<id>`. Misma firma.
- `presencia.js`: canal global → `realtime` `presencia-global` (presence + broadcast).
- `Base.astro` solo cambia el import (`haySupabase` sigue existiendo como alias) — sin tocar
  la lógica del overlay/auth.

## Migración de datos

1. **Export** desde Supabase: `pg_dump` del schema `public` (todas las tablas) + un
   `select id, email from auth.users` (para poblar `User`).
2. **Import** (`api/prisma/seed-import.ts`, one-off): crea `User` con el **UUID existente**
   (FKs intactas) y `email`; copia todas las filas de las 9 tablas verbatim (los nombres de
   columna pasan de snake_case del SQL a los del schema Prisma). `googleSub` queda null hasta
   el primer login (match por email en el callback).
3. Se corre una sola vez contra la DB nueva, antes de apuntar el frontend.

## Docker / deploy

`docker-compose.yml`:

- `db`: `postgres:17`, volume persistente, env `POSTGRES_*`.
- `api`: build de `api/Dockerfile`, depende de `db`, corre `prisma migrate deploy` al
  arrancar y luego `node dist/main`. Env: `DATABASE_URL, JWT_SECRET, GOOGLE_CLIENT_ID,
  GOOGLE_CLIENT_SECRET, GOOGLE_CALLBACK_URL, FRONTEND_URL, CORS_ORIGINS`.

TLS y reverse proxy (Caddy/nginx) quedan **fuera del compose** (los pone el server del
owner). Backups: nota en el README (`pg_dump` por cron) — fuera del alcance del código.

Frontend: `web/.env` define `PUBLIC_API_URL` apuntando al host de la API; el build de Pages
lo expone al navegador. Hay que habilitar **CORS** (origen de GitHub Pages) y WS en la API.

## Testing

- **Unit (Nest)**: servicios de swap (trade + oferta) con los casos del plpgsql; spoiler-gate
  de soluciones; inmutabilidad de handle; premio de balls una sola vez; oculta-reportes.
- **e2e (Nest)**: flujo OAuth mockeado → JWT → CRUD por endpoint; un trade completo de 2
  usuarios; una oferta async.
- **Manual / 2 sesiones**: trade en vivo + oferta async + presencia + invitación (replica los
  "falta test de 2 sesiones" pendientes de las features sociales).

## Fuera de alcance

- Refresh tokens / rotación (JWT 30 d, re-login al vencer).
- Multi-instancia del gateway (presence en memoria asume 1 instancia).
- Migrar el frontend fuera de GitHub Pages.
- Automatizar backups/TLS (documentados, no codificados).

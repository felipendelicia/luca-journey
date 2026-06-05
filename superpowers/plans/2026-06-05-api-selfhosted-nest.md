# API self-hosted (NestJS + Prisma) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar todas las responsabilidades de Supabase (Postgres + Auth Google + Realtime + ~30 RPC) por una API propia en NestJS + Prisma + Postgres dockerizada, manteniendo la app Astro funcionando idéntica.

**Architecture:** API Nest delgada con toda la lógica en TS sobre Prisma (sin plpgsql, sin RLS). El servidor controla todas las escrituras → el realtime emite por WebSocket tras cada mutación (no usa `postgres_changes`). El cliente reescribe los *internals* de `nube/social/trades/presencia/desafios.js` manteniendo idénticas las firmas exportadas, así las páginas no cambian. Datos migrados desde Supabase preservando UUIDs.

**Tech Stack:** NestJS 10, Prisma 5 + `@prisma/client`, Postgres 17, `@nestjs/jwt` + `passport-google-oauth20`, `@nestjs/platform-socket.io` (socket.io), `socket.io-client` en el front, Jest + supertest para tests, Docker Compose.

**Spec:** `superpowers/specs/2026-06-05-api-selfhosted-nest-design.md`

---

## Decisiones cerradas (resuelven los puntos abiertos del spec)

- **WS lib:** socket.io (`@nestjs/platform-socket.io` + `socket.io-client`). Rooms nativos = topics; presence con `Map` en memoria.
- **Auth:** `passport-google-oauth20` para el flujo OAuth + `@nestjs/jwt` para emitir el JWT (30 d, sin refresh). `JwtAuthGuard` global + decorador `@Public()` para las rutas de `/auth`.
- **Tests con DB:** Jest contra una base Postgres de test (`luca_test`) levantada por el mismo `db` del compose. Cada suite limpia las tablas que toca en `beforeEach`.
- **Validación:** manual en los servicios (espeja los mensajes de error exactos de los RPC), no DTOs con class-validator.

## Estructura de archivos

**Backend nuevo (`api/`):**

| Archivo | Responsabilidad |
|---|---|
| `api/package.json`, `api/tsconfig*.json`, `api/nest-cli.json` | proyecto Nest (generados) |
| `api/.env.example` | plantilla de env |
| `api/Dockerfile` | build de la API |
| `api/prisma/schema.prisma` | 10 modelos |
| `api/prisma/seed-import.ts` | importador one-off del dump de Supabase |
| `api/src/main.ts` | bootstrap: CORS, socket.io adapter |
| `api/src/app.module.ts` | wiring de módulos + guard global |
| `api/src/prisma/prisma.service.ts` + `prisma.module.ts` | cliente Prisma compartido |
| `api/src/auth/` | `auth.module/controller/service`, `google.strategy.ts`, `jwt.strategy.ts`, `jwt-auth.guard.ts`, `public.decorator.ts`, `current-user.decorator.ts` |
| `api/src/realtime/` | `realtime.module.ts`, `events.gateway.ts`, `realtime.service.ts` |
| `api/src/coleccion/coleccion.ts` | helpers `mapaInc/mapaDec/arrTiene/arrAdd/arrDel` + `swapColeccion` |
| `api/src/progreso/` | `progreso.module/controller/service` |
| `api/src/intercambios/` | `intercambios.module/controller/service` |
| `api/src/social/` | `social.module`, `perfiles.*`, `amigos.*`, `ofertas.*` (controller+service por sub-área) |
| `api/src/desafios/` | `desafios.module/controller/service` |
| `docker-compose.yml` (raíz) | `db` + `api` |

**Frontend (`web/`) — internals reescritos, exports iguales:**

| Archivo | Cambio |
|---|---|
| `web/src/lib/api.js` | NUEVO: fetch+JWT + objeto `auth`; exporta `hayApi` y alias `haySupabase` |
| `web/src/lib/realtime.js` | NUEVO: cliente socket.io (suscribir/presence/broadcast) |
| `web/src/lib/nube.js` | internals → `api.js`/`realtime.js`; mismas firmas |
| `web/src/lib/social.js` | `supa.rpc` → `apiGet/apiPost`; mismas firmas |
| `web/src/lib/trades.js` | RPC → endpoints; `suscribir` → realtime; misma firma |
| `web/src/lib/presencia.js` | canal global → realtime; mismas firmas |
| `web/src/lib/desafios.js` | RPC → endpoints; mismas firmas |
| `web/src/lib/supa.js` | ELIMINAR (o dejar re-exportando de `api.js`) |
| `web/.env` / `web/.env.example` | `PUBLIC_API_URL` (reemplaza `PUBLIC_SUPABASE_*`) |
| `web/package.json` | quita `@supabase/supabase-js`, agrega `socket.io-client` |

---

## Fase 0 — Scaffold del backend + Docker + Postgres

### Task 0.1: Crear el proyecto Nest

**Files:**
- Create: `api/` (proyecto Nest completo)

- [ ] **Step 1: Generar el proyecto**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
npx -y @nestjs/cli@10 new api --package-manager npm --skip-git
```
Expected: crea `api/` con `src/main.ts`, `src/app.module.ts`, `package.json`, etc. Instala deps.

- [ ] **Step 2: Verificar que arranca**

Run: `cd api && npm run build`
Expected: compila sin errores (genera `api/dist`).

- [ ] **Step 3: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add api
git commit -m "API: scaffold NestJS en api/"
```

### Task 0.2: Instalar dependencias

**Files:**
- Modify: `api/package.json`

- [ ] **Step 1: Instalar runtime + dev deps**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
npm i @prisma/client @nestjs/jwt @nestjs/passport passport passport-jwt passport-google-oauth20 @nestjs/platform-socket.io @nestjs/websockets socket.io
npm i -D prisma @types/passport-jwt @types/passport-google-oauth20 supertest @types/supertest
```
Expected: instala sin errores.

- [ ] **Step 2: Commit**

```bash
git add package.json package-lock.json
git commit -m "API: deps (prisma, jwt, passport-google, socket.io)"
```

### Task 0.3: docker-compose con Postgres

**Files:**
- Create: `docker-compose.yml`
- Create: `api/.env.example`
- Create: `api/.env` (local, no se commitea)

- [ ] **Step 1: Escribir `docker-compose.yml`**

```yaml
services:
  db:
    image: postgres:17
    restart: unless-stopped
    environment:
      POSTGRES_USER: luca
      POSTGRES_PASSWORD: luca
      POSTGRES_DB: luca
    ports:
      - "5433:5432"   # 5433 host para no chocar con un postgres local
    volumes:
      - dbdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U luca"]
      interval: 5s
      timeout: 5s
      retries: 10

  api:
    build: ./api
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgres://luca:luca@db:5432/luca
      JWT_SECRET: ${JWT_SECRET}
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}
      GOOGLE_CALLBACK_URL: ${GOOGLE_CALLBACK_URL}
      FRONTEND_URL: ${FRONTEND_URL}
      CORS_ORIGINS: ${CORS_ORIGINS}
      PORT: "3000"
    ports:
      - "3000:3000"

volumes:
  dbdata:
```

- [ ] **Step 2: Escribir `api/.env.example`**

```bash
# Conexión local (dev fuera de docker apunta al puerto host 5433)
DATABASE_URL="postgres://luca:luca@localhost:5433/luca"
JWT_SECRET="cambiame-por-un-secreto-largo"
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
GOOGLE_CALLBACK_URL="http://localhost:3000/auth/google/callback"
FRONTEND_URL="http://localhost:4321/"
CORS_ORIGINS="http://localhost:4321"
PORT="3000"
```

- [ ] **Step 3: Crear `api/.env` local (copia) y agregar a gitignore**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
cp .env.example .env
grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
```

- [ ] **Step 4: Levantar la DB**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
docker compose up -d db
docker compose ps
```
Expected: `db` en estado healthy.

- [ ] **Step 5: Commit**

```bash
git add docker-compose.yml api/.env.example api/.gitignore
git commit -m "API: docker-compose con Postgres 17 + .env.example"
```

---

## Fase 1 — Prisma: schema + migración + servicio

### Task 1.1: Inicializar Prisma y escribir el schema

**Files:**
- Create: `api/prisma/schema.prisma`

- [ ] **Step 1: Init Prisma**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
npx prisma init --datasource-provider postgresql
```
Expected: crea `prisma/schema.prisma` y agrega `DATABASE_URL` a `.env` (ya existe; dejá el de `.env`).

- [ ] **Step 2: Escribir el schema completo**

Reemplazá `api/prisma/schema.prisma` por:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  googleSub String?  @unique @map("google_sub")
  creado    DateTime @default(now())

  @@map("users")
}

model Progreso {
  userId      String   @id @map("user_id")
  estado      Json     @default("{}")
  actualizado DateTime @updatedAt

  @@map("progreso")
}

model Perfil {
  userId      String   @id @map("user_id")
  handle      String   @unique
  nombre      String   @default("")
  avatar      Int      @default(0)
  codigoAmigo String   @unique @map("codigo_amigo")
  publico     Json     @default("{}")
  descripcion String   @default("")
  actualizado DateTime @updatedAt

  @@map("perfiles")
}

model Amistad {
  id     String   @id @default(uuid())
  deId   String   @map("de_id")
  aId    String   @map("a_id")
  estado String   @default("pendiente")
  creado DateTime @default(now())

  @@unique([deId, aId])
  @@map("amistades")
}

model Oferta {
  id       String    @id @default(uuid())
  deId     String    @map("de_id")
  aId      String    @map("a_id")
  doy      Json      @default("[]")
  pido     Json      @default("[]")
  estado   String    @default("pendiente")
  creado   DateTime  @default(now())
  resuelto DateTime?

  @@map("ofertas")
}

model Intercambio {
  id             String   @id @default(uuid())
  codigo         String   @unique
  creadorId      String   @map("creador_id")
  invitadoId     String?  @map("invitado_id")
  creadorNombre  String   @default("") @map("creador_nombre")
  invitadoNombre String   @default("") @map("invitado_nombre")
  creadorLote    Json     @default("[]") @map("creador_lote")
  invitadoLote   Json     @default("[]") @map("invitado_lote")
  creadorPedido  Json     @default("[]") @map("creador_pedido")
  invitadoPedido Json     @default("[]") @map("invitado_pedido")
  creadorOk      Boolean  @default(false) @map("creador_ok")
  invitadoOk     Boolean  @default(false) @map("invitado_ok")
  estado         String   @default("abierta")
  creado         DateTime @default(now())
  actualizado    DateTime @updatedAt

  @@map("intercambios")
}

model Desafio {
  id         String   @id @default(uuid())
  autor      String
  titulo     String
  consigna   String   @default("")
  func       String
  starter    String   @default("")
  casos      Json     @default("[]")
  dificultad Int      @default(3)
  region     String   @default("libre")
  creado     DateTime @default(now())

  @@map("desafios")
}

model Resolucion {
  id        String   @id @default(uuid())
  desafioId String   @map("desafio_id")
  userId    String   @map("user_id")
  codigo    String   @default("")
  creado    DateTime @default(now())

  @@unique([desafioId, userId])
  @@map("resoluciones")
}

model Voto {
  resolucionId String @map("resolucion_id")
  userId       String @map("user_id")

  @@id([resolucionId, userId])
  @@map("votos")
}

model Reporte {
  desafioId String   @map("desafio_id")
  userId    String   @map("user_id")
  motivo    String   @default("")
  creado    DateTime @default(now())

  @@id([desafioId, userId])
  @@map("reportes")
}
```

> Nota: las FK se manejan a nivel app (sin `relation`) para mantener el modelo simple y porque el control de borrado-cascada de usuarios no es crítico (no se borran usuarios desde la app). Si más adelante se quiere cascade, se agregan relaciones explícitas.

- [ ] **Step 3: Crear la migración inicial**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
npx prisma migrate dev --name init
```
Expected: crea `prisma/migrations/<ts>_init/migration.sql`, aplica a la DB, genera el client.

- [ ] **Step 4: Verificar las tablas**

Run: `npx prisma db pull --print | head -5` (o `docker compose exec db psql -U luca -d luca -c '\dt'`)
Expected: lista las 10 tablas (`users, progreso, perfiles, amistades, ofertas, intercambios, desafios, resoluciones, votos, reportes`).

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add api/prisma
git commit -m "API: schema Prisma (10 modelos) + migracion init"
```

### Task 1.2: PrismaService + módulo

**Files:**
- Create: `api/src/prisma/prisma.service.ts`
- Create: `api/src/prisma/prisma.module.ts`

- [ ] **Step 1: Escribir `prisma.service.ts`**

```typescript
import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
```

- [ ] **Step 2: Escribir `prisma.module.ts`**

```typescript
import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

- [ ] **Step 3: Registrar en `app.module.ts`**

En `api/src/app.module.ts`, agregá `PrismaModule` a `imports`:
```typescript
import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';

@Module({
  imports: [PrismaModule],
})
export class AppModule {}
```

- [ ] **Step 4: Build**

Run: `cd api && npm run build`
Expected: compila OK.

- [ ] **Step 5: Commit**

```bash
git add api/src
git commit -m "API: PrismaService global"
```

---

## Fase 2 — Auth (Google OAuth + JWT)

### Task 2.1: Config + main.ts (CORS + env)

**Files:**
- Modify: `api/src/main.ts`

- [ ] **Step 1: Reescribir `main.ts`**

```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const origins = (process.env.CORS_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  app.enableCors({ origin: origins.length ? origins : true, credentials: true });
  await app.listen(Number(process.env.PORT) || 3000);
}
bootstrap();
```

- [ ] **Step 2: Build**

Run: `cd api && npm run build`
Expected: OK.

- [ ] **Step 3: Commit**

```bash
git add api/src/main.ts
git commit -m "API: CORS desde CORS_ORIGINS"
```

### Task 2.2: Decoradores y guard de JWT

**Files:**
- Create: `api/src/auth/public.decorator.ts`
- Create: `api/src/auth/current-user.decorator.ts`
- Create: `api/src/auth/jwt-auth.guard.ts`
- Create: `api/src/auth/jwt.strategy.ts`

- [ ] **Step 1: `public.decorator.ts`**

```typescript
import { SetMetadata } from '@nestjs/common';
export const IS_PUBLIC = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC, true);
```

- [ ] **Step 2: `current-user.decorator.ts`**

```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

// Devuelve el userId (sub) del JWT validado.
export const CurrentUser = createParamDecorator(
  (_data: unknown, ctx: ExecutionContext): string => {
    const req = ctx.switchToHttp().getRequest();
    return req.user?.userId;
  },
);
```

- [ ] **Step 3: `jwt.strategy.ts`**

```typescript
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET || 'dev-secret',
    });
  }
  // el payload es { sub, email }; lo exponemos como req.user
  async validate(payload: { sub: string; email: string }) {
    return { userId: payload.sub, email: payload.email };
  }
}
```

- [ ] **Step 4: `jwt-auth.guard.ts` (global, respeta @Public)**

```typescript
import { ExecutionContext, Injectable } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import { IS_PUBLIC } from './public.decorator';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }
  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) return true;
    return super.canActivate(context);
  }
}
```

- [ ] **Step 5: Commit**

```bash
git add api/src/auth
git commit -m "API: JWT strategy + guard global + decoradores Public/CurrentUser"
```

### Task 2.3: Google OAuth strategy + AuthService + AuthController

**Files:**
- Create: `api/src/auth/google.strategy.ts`
- Create: `api/src/auth/auth.service.ts`
- Create: `api/src/auth/auth.controller.ts`
- Create: `api/src/auth/auth.module.ts`
- Modify: `api/src/app.module.ts`

- [ ] **Step 1: `google.strategy.ts`**

```typescript
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { Strategy, VerifyCallback } from 'passport-google-oauth20';

@Injectable()
export class GoogleStrategy extends PassportStrategy(Strategy, 'google') {
  constructor() {
    super({
      clientID: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      callbackURL: process.env.GOOGLE_CALLBACK_URL || '',
      scope: ['email', 'profile'],
    });
  }
  async validate(_at: string, _rt: string, profile: any, done: VerifyCallback) {
    const email = profile.emails?.[0]?.value || '';
    done(null, { googleSub: profile.id, email });
  }
}
```

- [ ] **Step 2: `auth.service.ts` (upsert user + emite JWT)**

```typescript
import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class AuthService {
  constructor(private prisma: PrismaService, private jwt: JwtService) {}

  // Match por email (cubre datos migrados sin googleSub); si no existe, crea.
  async loginConGoogle(googleSub: string, email: string) {
    let user = await this.prisma.user.findUnique({ where: { email } });
    if (!user) {
      user = await this.prisma.user.create({ data: { email, googleSub } });
    } else if (!user.googleSub) {
      user = await this.prisma.user.update({ where: { id: user.id }, data: { googleSub } });
    }
    const token = await this.jwt.signAsync(
      { sub: user.id, email: user.email },
      { secret: process.env.JWT_SECRET || 'dev-secret', expiresIn: '30d' },
    );
    return { token, user };
  }
}
```

- [ ] **Step 3: `auth.controller.ts`**

```typescript
import { Controller, Get, Req, Res, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Response } from 'express';
import { Public } from './public.decorator';
import { CurrentUser } from './current-user.decorator';
import { AuthService } from './auth.service';

@Controller('auth')
export class AuthController {
  constructor(private auth: AuthService) {}

  // 1) arranca el flujo OAuth (passport redirige a Google)
  @Public()
  @UseGuards(AuthGuard('google'))
  @Get('google')
  google() {}

  // 2) callback: emite JWT y redirige al front con #token=...
  @Public()
  @UseGuards(AuthGuard('google'))
  @Get('google/callback')
  async callback(@Req() req: any, @Res() res: Response) {
    const { googleSub, email } = req.user;
    const { token } = await this.auth.loginConGoogle(googleSub, email);
    const front = process.env.FRONTEND_URL || '/';
    const base = front.endsWith('/') ? front : front + '/';
    res.redirect(`${base}#token=${encodeURIComponent(token)}`);
  }

  // 3) datos del usuario logueado
  @Get('me')
  me(@CurrentUser() userId: string, @Req() req: any) {
    return { id: userId, email: req.user?.email };
  }
}
```

- [ ] **Step 4: `auth.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { GoogleStrategy } from './google.strategy';
import { JwtStrategy } from './jwt.strategy';

@Module({
  imports: [PassportModule, JwtModule.register({})],
  controllers: [AuthController],
  providers: [AuthService, GoogleStrategy, JwtStrategy],
})
export class AuthModule {}
```

- [ ] **Step 5: Registrar AuthModule + guard global en `app.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { APP_GUARD } from '@nestjs/core';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { JwtAuthGuard } from './auth/jwt-auth.guard';

@Module({
  imports: [PrismaModule, AuthModule],
  providers: [{ provide: APP_GUARD, useClass: JwtAuthGuard }],
})
export class AppModule {}
```

- [ ] **Step 6: Build**

Run: `cd api && npm run build`
Expected: compila OK.

- [ ] **Step 7: Commit**

```bash
git add api/src
git commit -m "API: auth Google OAuth -> JWT (callback redirige a FRONTEND/#token), /auth/me"
```

### Task 2.4: Test e2e de auth (JWT protege rutas)

**Files:**
- Create: `api/test/auth.e2e-spec.ts`
- Create: `api/test/util.ts`

- [ ] **Step 1: Helper de test `api/test/util.ts`**

```typescript
import { Test } from '@nestjs/testing';
import { JwtService } from '@nestjs/jwt';
import { INestApplication } from '@nestjs/common';
import { AppModule } from '../src/app.module';

export async function crearApp(): Promise<INestApplication> {
  const mod = await Test.createTestingModule({ imports: [AppModule] }).compile();
  const app = mod.createNestApplication();
  await app.init();
  return app;
}

// Firma un JWT válido para un userId (evita el flujo OAuth real en tests).
export function tokenDe(userId: string, email = 'x@test'): string {
  const jwt = new JwtService({});
  return jwt.sign({ sub: userId, email }, { secret: process.env.JWT_SECRET || 'dev-secret', expiresIn: '1h' });
}
```

- [ ] **Step 2: `auth.e2e-spec.ts`**

```typescript
import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';

describe('auth', () => {
  let app: INestApplication;
  beforeAll(async () => { app = await crearApp(); });
  afterAll(async () => { await app.close(); });

  it('/auth/me sin token -> 401', async () => {
    await request(app.getHttpServer()).get('/auth/me').expect(401);
  });

  it('/auth/me con token -> userId', async () => {
    const t = tokenDe('user-1', 'a@test');
    const r = await request(app.getHttpServer()).get('/auth/me').set('Authorization', `Bearer ${t}`).expect(200);
    expect(r.body.id).toBe('user-1');
    expect(r.body.email).toBe('a@test');
  });
});
```

- [ ] **Step 3: Correr (debe fallar si algo del wiring está mal, pasar si OK)**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
JWT_SECRET=test-secret DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npm run test:e2e -- auth
```
Expected: PASS (2 tests). Requiere `db` levantada.

- [ ] **Step 4: Commit**

```bash
git add api/test
git commit -m "API: e2e auth (guard JWT protege /auth/me)"
```

---

## Fase 3 — Helpers de colección + swap atómico (la parte sensible, TDD)

> **Fidelidad clave:** el blob `estado` espeja localStorage → **todos los valores son strings**.
> `col:atrapados` es un string JSON `'{"25":3}'`, `col:shiny` un string `'[25,7]'`, `col:balls`
> un string `'"42"'`/`'42'`. Por eso los helpers parsean al entrar y `JSON.stringify` al salir,
> igual que el plpgsql hacía `(->>'k')::jsonb` y `to_jsonb(x::text)`.

### Task 3.1: Helpers puros `mapaInc/mapaDec/arr*` (TDD)

**Files:**
- Create: `api/src/coleccion/coleccion.ts`
- Test: `api/src/coleccion/coleccion.spec.ts`

- [ ] **Step 1: Test que falla**

```typescript
import { mapaInc, mapaDec, arrTiene, arrAdd, arrDel } from './coleccion';

describe('helpers coleccion', () => {
  it('mapaInc suma 1', () => {
    expect(mapaInc({ '25': 2 }, '25')).toEqual({ '25': 3 });
    expect(mapaInc({}, '7')).toEqual({ '7': 1 });
  });
  it('mapaDec resta y borra al llegar a 0', () => {
    expect(mapaDec({ '25': 2 }, '25')).toEqual({ '25': 1 });
    expect(mapaDec({ '25': 1 }, '25')).toEqual({});
  });
  it('arr add/del/tiene sin duplicar', () => {
    expect(arrTiene([25, 7], '25')).toBe(true);
    expect(arrAdd([25], '7')).toEqual([25, 7]);
    expect(arrAdd([25], '25')).toEqual([25]);
    expect(arrDel([25, 7], '25')).toEqual([7]);
  });
});
```

- [ ] **Step 2: Correr → falla**

Run: `cd api && npx jest coleccion.spec --silent=false`
Expected: FAIL ("Cannot find module './coleccion'").

- [ ] **Step 3: Implementar helpers**

```typescript
// coleccion.ts — operan sobre estructuras JS ya parseadas.
export type MapaAtrapados = Record<string, number>;

export function mapaInc(m: MapaAtrapados, k: string): MapaAtrapados {
  return { ...m, [k]: (m[k] || 0) + 1 };
}
export function mapaDec(m: MapaAtrapados, k: string): MapaAtrapados {
  const n = (m[k] || 0) - 1;
  const out = { ...m };
  if (n <= 0) delete out[k];
  else out[k] = n;
  return out;
}
export function arrTiene(a: number[], k: string): boolean {
  return a.includes(Number(k));
}
export function arrAdd(a: number[], k: string): number[] {
  return arrTiene(a, k) ? a : [...a, Number(k)];
}
export function arrDel(a: number[], k: string): number[] {
  return a.filter((x) => x !== Number(k));
}
```

- [ ] **Step 4: Correr → pasa**

Run: `cd api && npx jest coleccion.spec`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add api/src/coleccion
git commit -m "API: helpers de coleccion (mapaInc/Dec, arr*) con tests"
```

### Task 3.2: `swapColeccion` puro (validar + aplicar, TDD)

**Files:**
- Modify: `api/src/coleccion/coleccion.ts`
- Modify: `api/src/coleccion/coleccion.spec.ts`

- [ ] **Step 1: Tests que fallan (cubren los casos del plpgsql)**

Agregá a `coleccion.spec.ts`:
```typescript
import { swapColeccion, leerCol, escribirCol } from './coleccion';

const blob = (atra: Record<string, number>, shiny: number[] = [], balls = 0) => ({
  'col:atrapados': JSON.stringify(atra),
  'col:shiny': JSON.stringify(shiny),
  'col:balls': String(balls),
});

describe('swapColeccion', () => {
  it('mueve por cantidad: A da 25 -> B', () => {
    const a = blob({ '25': 2 });
    const b = blob({ '7': 1 });
    const { estadoA, estadoB } = swapColeccion(a, [{ id: 25 }], 'A', b, [], 'B');
    expect(leerCol(estadoA).atra).toEqual({ '25': 1 });
    expect(leerCol(estadoB).atra).toEqual({ '7': 1, '25': 1 });
  });
  it('mueve shiny en ambos sentidos', () => {
    const a = blob({ '25': 1 }, [25]);
    const b = blob({ '7': 1 }, [7]);
    const { estadoA, estadoB } = swapColeccion(a, [{ id: 25, shiny: true }], 'A', b, [{ id: 7, shiny: true }], 'B');
    expect(leerCol(estadoA).shiny).toEqual([7]);
    expect(leerCol(estadoB).shiny).toEqual([25]);
  });
  it('falla si A no tiene stock', () => {
    expect(() => swapColeccion(blob({}), [{ id: 25 }], 'A', blob({}), [], 'B')).toThrow(/A no tiene/);
  });
  it('falla si pide shiny que no tiene', () => {
    expect(() => swapColeccion(blob({ '25': 1 }, []), [{ id: 25, shiny: true }], 'A', blob({}), [], 'B')).toThrow(/shiny/);
  });
});
```

- [ ] **Step 2: Correr → falla**

Run: `cd api && npx jest coleccion.spec`
Expected: FAIL (swapColeccion/leerCol/escribirCol no existen).

- [ ] **Step 3: Implementar `leerCol/escribirCol/swapColeccion`**

Agregá a `coleccion.ts`:
```typescript
export type Estado = Record<string, any>;
export type Item = { id: number | string; shiny?: boolean };

export function leerCol(estado: Estado) {
  const atra = JSON.parse((estado['col:atrapados'] as string) || '{}');
  const shiny = JSON.parse((estado['col:shiny'] as string) || '[]');
  return { atra: atra as MapaAtrapados, shiny: shiny as number[] };
}
export function escribirCol(estado: Estado, atra: MapaAtrapados, shiny: number[]): Estado {
  return { ...estado, 'col:atrapados': JSON.stringify(atra), 'col:shiny': JSON.stringify(shiny) };
}

// A entrega loteA a B; B entrega loteB a A. Valida multiplicidad + shiny sobre copias,
// luego aplica. Lanza con el label del lado que no cumple. Pura: no toca DB.
export function swapColeccion(
  estadoA: Estado, loteA: Item[], labelA: string,
  estadoB: Estado, loteB: Item[], labelB: string,
): { estadoA: Estado; estadoB: Estado } {
  let { atra: aAt, shiny: aSh } = leerCol(estadoA);
  let { atra: bAt, shiny: bSh } = leerCol(estadoB);

  const validar = (at: MapaAtrapados, sh: number[], lote: Item[], label: string) => {
    let tmp = { ...at };
    for (const it of lote) {
      const id = String(it.id);
      if ((tmp[id] || 0) < 1) throw new Error(`${label} no tiene suficiente ${id}`);
      if (it.shiny && !arrTiene(sh, id)) throw new Error(`${label} no tiene shiny ${id}`);
      tmp = mapaDec(tmp, id);
    }
  };
  validar(aAt, aSh, loteA, labelA);
  validar(bAt, bSh, loteB, labelB);

  for (const it of loteA) {
    const id = String(it.id);
    aAt = mapaDec(aAt, id); bAt = mapaInc(bAt, id);
    if (it.shiny) { aSh = arrDel(aSh, id); bSh = arrAdd(bSh, id); }
  }
  for (const it of loteB) {
    const id = String(it.id);
    bAt = mapaDec(bAt, id); aAt = mapaInc(aAt, id);
    if (it.shiny) { bSh = arrDel(bSh, id); aSh = arrAdd(aSh, id); }
  }
  return { estadoA: escribirCol(estadoA, aAt, aSh), estadoB: escribirCol(estadoB, bAt, bSh) };
}
```

- [ ] **Step 4: Correr → pasa**

Run: `cd api && npx jest coleccion.spec`
Expected: PASS (todos).

- [ ] **Step 5: Commit**

```bash
git add api/src/coleccion
git commit -m "API: swapColeccion puro (valida multiplicidad+shiny, aplica) con tests"
```

---

## Fase 4 — Progreso (GET / PUT propio)

### Task 4.1: ProgresoService + Controller

**Files:**
- Create: `api/src/progreso/progreso.service.ts`
- Create: `api/src/progreso/progreso.controller.ts`
- Create: `api/src/progreso/progreso.module.ts`
- Modify: `api/src/app.module.ts`

- [ ] **Step 1: `progreso.service.ts`**

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ProgresoService {
  constructor(private prisma: PrismaService) {}

  async bajar(userId: string): Promise<Record<string, any>> {
    const row = await this.prisma.progreso.findUnique({ where: { userId } });
    return (row?.estado as Record<string, any>) || {};
  }

  async subir(userId: string, estado: Record<string, any>) {
    await this.prisma.progreso.upsert({
      where: { userId },
      create: { userId, estado },
      update: { estado },
    });
    return { ok: true };
  }
}
```

- [ ] **Step 2: `progreso.controller.ts`**

```typescript
import { Body, Controller, Get, Put } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { ProgresoService } from './progreso.service';

@Controller('progreso')
export class ProgresoController {
  constructor(private svc: ProgresoService) {}

  @Get()
  async get(@CurrentUser() userId: string) {
    return { estado: await this.svc.bajar(userId) };
  }

  @Put()
  async put(@CurrentUser() userId: string, @Body() body: { estado: Record<string, any> }) {
    return this.svc.subir(userId, body.estado || {});
  }
}
```

- [ ] **Step 3: `progreso.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { ProgresoController } from './progreso.controller';
import { ProgresoService } from './progreso.service';

@Module({
  controllers: [ProgresoController],
  providers: [ProgresoService],
  exports: [ProgresoService],
})
export class ProgresoModule {}
```

- [ ] **Step 4: Registrar en `app.module.ts`** (agregá `ProgresoModule` a `imports`).

- [ ] **Step 5: Test e2e**

Create `api/test/progreso.e2e-spec.ts`:
```typescript
import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('progreso', () => {
  let app: INestApplication; let prisma: PrismaService;
  beforeAll(async () => {
    app = await crearApp();
    prisma = app.get(PrismaService);
    await prisma.user.upsert({ where: { email: 'p@test' }, create: { id: 'u-prog', email: 'p@test' }, update: {} });
  });
  afterAll(async () => { await prisma.progreso.deleteMany({ where: { userId: 'u-prog' } }); await app.close(); });

  it('PUT luego GET devuelve el estado', async () => {
    const t = tokenDe('u-prog', 'p@test');
    await request(app.getHttpServer()).put('/progreso').set('Authorization', `Bearer ${t}`)
      .send({ estado: { 'col:balls': '5' } }).expect(200);
    const r = await request(app.getHttpServer()).get('/progreso').set('Authorization', `Bearer ${t}`).expect(200);
    expect(r.body.estado['col:balls']).toBe('5');
  });
});
```

- [ ] **Step 6: Correr**

Run: `cd api && JWT_SECRET=test-secret DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npm run test:e2e -- progreso`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add api/src api/test
git commit -m "API: progreso GET/PUT (upsert propio) + e2e"
```

---

## Fase 5 — Realtime (gateway socket.io + RealtimeService)

### Task 5.1: EventsGateway + RealtimeService

**Files:**
- Create: `api/src/realtime/events.gateway.ts`
- Create: `api/src/realtime/realtime.service.ts`
- Create: `api/src/realtime/realtime.module.ts`
- Modify: `api/src/app.module.ts`

- [ ] **Step 1: `events.gateway.ts`**

```typescript
import {
  OnGatewayConnection, OnGatewayDisconnect, SubscribeMessage,
  WebSocketGateway, WebSocketServer, MessageBody, ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { JwtService } from '@nestjs/jwt';

// Topics: `progreso:<uid>`, `sala:<id>`, `presencia-global`.
@WebSocketGateway({ cors: { origin: true } })
export class EventsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server: Server;
  private jwt = new JwtService({});

  // presencia: topic -> Set<userId>; y userId -> sockets (para emitir a "su" progreso)
  private presentes = new Map<string, Set<string>>();

  private uidDe(client: Socket): string | null {
    const token = (client.handshake.auth?.token || '') as string;
    try {
      const p: any = this.jwt.verify(token, { secret: process.env.JWT_SECRET || 'dev-secret' });
      return p.sub;
    } catch { return null; }
  }

  handleConnection(client: Socket) {
    const uid = this.uidDe(client);
    if (!uid) { client.disconnect(true); return; }
    (client.data as any).uid = uid;
    client.join(`progreso:${uid}`); // recibe cambios externos de su propia colección
  }

  handleDisconnect(client: Socket) {
    const uid = (client.data as any)?.uid;
    for (const [topic, set] of this.presentes) {
      if (uid && set.delete(uid)) this.emitirPresencia(topic);
    }
  }

  // suscribir a un topic con presencia (sala:<id> o presencia-global)
  @SubscribeMessage('join')
  onJoin(@ConnectedSocket() client: Socket, @MessageBody() topic: string) {
    const uid = (client.data as any)?.uid;
    client.join(topic);
    if (!this.presentes.has(topic)) this.presentes.set(topic, new Set());
    this.presentes.get(topic)!.add(uid);
    this.emitirPresencia(topic);
  }

  @SubscribeMessage('leave')
  onLeave(@ConnectedSocket() client: Socket, @MessageBody() topic: string) {
    const uid = (client.data as any)?.uid;
    client.leave(topic);
    this.presentes.get(topic)?.delete(uid);
    this.emitirPresencia(topic);
  }

  // broadcast de invitación: { topic, to, payload } -> sólo al user destino
  @SubscribeMessage('broadcast')
  onBroadcast(@MessageBody() msg: { topic: string; payload: any }) {
    this.server.to(msg.topic).emit('broadcast', msg.payload);
  }

  private emitirPresencia(topic: string) {
    const ids = Array.from(this.presentes.get(topic) || []);
    this.server.to(topic).emit('presencia', { topic, ids });
  }

  // API para los servicios (vía RealtimeService)
  emitirProgreso(uid: string, estado: Record<string, any>) {
    this.server.to(`progreso:${uid}`).emit('progreso', estado);
  }
  emitirSala(id: string, row: any) {
    this.server.to(`sala:${id}`).emit('sala', row);
  }
}
```

- [ ] **Step 2: `realtime.service.ts` (fachada inyectable)**

```typescript
import { Injectable } from '@nestjs/common';
import { EventsGateway } from './events.gateway';

@Injectable()
export class RealtimeService {
  constructor(private gw: EventsGateway) {}
  progreso(uid: string, estado: Record<string, any>) { this.gw.emitirProgreso(uid, estado); }
  sala(id: string, row: any) { this.gw.emitirSala(id, row); }
}
```

- [ ] **Step 3: `realtime.module.ts`**

```typescript
import { Global, Module } from '@nestjs/common';
import { EventsGateway } from './events.gateway';
import { RealtimeService } from './realtime.service';

@Global()
@Module({
  providers: [EventsGateway, RealtimeService],
  exports: [RealtimeService],
})
export class RealtimeModule {}
```

- [ ] **Step 4: Registrar `RealtimeModule` en `app.module.ts`** (a `imports`).

- [ ] **Step 5: Build**

Run: `cd api && npm run build`
Expected: compila OK.

- [ ] **Step 6: Commit**

```bash
git add api/src
git commit -m "API: realtime gateway socket.io (topics progreso/sala/presencia) + RealtimeService"
```

---

## Fase 6 — Intercambios en vivo (incl. swap atómico)

### Task 6.1: IntercambiosService

**Files:**
- Create: `api/src/intercambios/intercambios.service.ts`

- [ ] **Step 1: Escribir el servicio**

```typescript
import { ForbiddenException, Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { RealtimeService } from '../realtime/realtime.service';
import { swapColeccion, Item } from '../coleccion/coleccion';

const ALF = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const code6 = () => Array.from({ length: 6 }, () => ALF[Math.floor(Math.random() * ALF.length)]).join('');

@Injectable()
export class IntercambiosService {
  constructor(private prisma: PrismaService, private rt: RealtimeService) {}

  async crear(uid: string, nombre: string) {
    let codigo = code6();
    while (await this.prisma.intercambio.findUnique({ where: { codigo } })) codigo = code6();
    const row = await this.prisma.intercambio.create({
      data: { codigo, creadorId: uid, creadorNombre: nombre || '' },
    });
    return { id: row.id, codigo: row.codigo };
  }

  async unirse(uid: string, codigo: string, nombre: string) {
    const s = await this.prisma.intercambio.findUnique({ where: { codigo: codigo.toUpperCase() } });
    if (!s || s.estado !== 'abierta') throw new NotFoundException('sala no encontrada o cerrada');
    if (s.creadorId === uid) throw new BadRequestException('no podés unirte a tu propia sala');
    if (s.invitadoId && s.invitadoId !== uid) throw new BadRequestException('la sala ya está completa');
    await this.prisma.intercambio.update({ where: { id: s.id }, data: { invitadoId: uid, invitadoNombre: nombre || '' } });
    this.rt.sala(s.id, await this.leer(uid, s.id));
    return s.id;
  }

  async leer(uid: string, id: string) {
    const s = await this.prisma.intercambio.findUnique({ where: { id } });
    if (!s) throw new NotFoundException('sala no encontrada');
    if (uid !== s.creadorId && uid !== s.invitadoId) throw new ForbiddenException('no sos participante');
    return s;
  }

  async ponerLote(uid: string, id: string, lote: Item[]) {
    const s = await this.leer(uid, id);
    if (s.estado !== 'abierta') throw new BadRequestException('la sala no está abierta');
    const data = uid === s.creadorId
      ? { creadorLote: lote as any, creadorOk: false, invitadoOk: false }
      : { invitadoLote: lote as any, creadorOk: false, invitadoOk: false };
    await this.prisma.intercambio.update({ where: { id }, data });
    this.rt.sala(id, await this.prisma.intercambio.findUnique({ where: { id } }));
  }

  async ponerPedido(uid: string, id: string, pedido: Item[]) {
    const s = await this.leer(uid, id);
    if (s.estado !== 'abierta') throw new BadRequestException('la sala no está abierta');
    const data = uid === s.creadorId ? { creadorPedido: pedido as any } : { invitadoPedido: pedido as any };
    await this.prisma.intercambio.update({ where: { id }, data });
    this.rt.sala(id, await this.prisma.intercambio.findUnique({ where: { id } }));
  }

  // colección del OTRO participante (solo en sala abierta, solo entre los dos)
  async coleccionDelOtro(uid: string, id: string) {
    const s = await this.leer(uid, id);
    if (s.estado !== 'abierta') throw new BadRequestException('la sala no está abierta');
    const otro = uid === s.creadorId ? s.invitadoId : s.creadorId;
    if (!otro) return { atrapados: {}, shiny: [] };
    const p = await this.prisma.progreso.findUnique({ where: { userId: otro } });
    const est = (p?.estado as any) || {};
    return {
      atrapados: JSON.parse(est['col:atrapados'] || '{}'),
      shiny: JSON.parse(est['col:shiny'] || '[]'),
    };
  }

  async cancelar(uid: string, id: string) {
    const s = await this.leer(uid, id);
    if (s.estado === 'abierta') {
      await this.prisma.intercambio.update({ where: { id }, data: { estado: 'cancelada' } });
      this.rt.sala(id, await this.prisma.intercambio.findUnique({ where: { id } }));
    }
  }

  // confirma; si ambos confirmaron, ejecuta el swap atómico y devuelve 'completada'
  async confirmar(uid: string, id: string): Promise<'abierta' | 'completada'> {
    const s0 = await this.leer(uid, id);
    if (s0.estado !== 'abierta') throw new BadRequestException('la sala no está abierta');
    await this.prisma.intercambio.update({
      where: { id },
      data: uid === s0.creadorId ? { creadorOk: true } : { invitadoOk: true },
    });
    const s = await this.prisma.intercambio.findUnique({ where: { id } });
    if (!(s!.creadorOk && s!.invitadoOk)) {
      this.rt.sala(id, s);
      return 'abierta';
    }
    await this.ejecutar(s!);
    this.rt.sala(id, await this.prisma.intercambio.findUnique({ where: { id } }));
    return 'completada';
  }

  // swap atómico: lock de ambas filas de progreso (orden fijo) + intercambio, validar, aplicar
  private async ejecutar(s: any) {
    const [ca, ia] = await this.prisma.$transaction(async (tx) => {
      // lock determinista para evitar deadlock
      await tx.$queryRawUnsafe(
        `SELECT user_id FROM progreso WHERE user_id IN ($1,$2) ORDER BY user_id FOR UPDATE`,
        s.creadorId, s.invitadoId,
      );
      const cP = await tx.progreso.findUnique({ where: { userId: s.creadorId } });
      const iP = await tx.progreso.findUnique({ where: { userId: s.invitadoId } });
      const cEst = (cP?.estado as any) || {};
      const iEst = (iP?.estado as any) || {};
      const { estadoA, estadoB } = swapColeccion(
        cEst, s.creadorLote, 'creador', iEst, s.invitadoLote, 'invitado',
      );
      await tx.progreso.upsert({ where: { userId: s.creadorId }, create: { userId: s.creadorId, estado: estadoA }, update: { estado: estadoA } });
      await tx.progreso.upsert({ where: { userId: s.invitadoId }, create: { userId: s.invitadoId, estado: estadoB }, update: { estado: estadoB } });
      await tx.intercambio.update({ where: { id: s.id }, data: { estado: 'completada' } });
      return [estadoA, estadoB];
    }, { isolationLevel: 'Serializable' });
    // emitir a cada participante su nuevo progreso (cambio externo)
    this.rt.progreso(s.creadorId, ca);
    this.rt.progreso(s.invitadoId, ia);
  }
}
```

- [ ] **Step 2: Build**

Run: `cd api && npm run build`
Expected: OK.

### Task 6.2: IntercambiosController + módulo

**Files:**
- Create: `api/src/intercambios/intercambios.controller.ts`
- Create: `api/src/intercambios/intercambios.module.ts`
- Modify: `api/src/app.module.ts`

- [ ] **Step 1: `intercambios.controller.ts`**

```typescript
import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { IntercambiosService } from './intercambios.service';

@Controller('trades')
export class IntercambiosController {
  constructor(private svc: IntercambiosService) {}

  @Post()
  crear(@CurrentUser() uid: string, @Body() b: { nombre: string }) { return this.svc.crear(uid, b?.nombre || ''); }

  @Post('join')
  unirse(@CurrentUser() uid: string, @Body() b: { codigo: string; nombre: string }) {
    return this.svc.unirse(uid, b.codigo, b?.nombre || '').then((id) => ({ id }));
  }

  @Get(':id')
  leer(@CurrentUser() uid: string, @Param('id') id: string) { return this.svc.leer(uid, id); }

  @Get(':id/otro')
  otro(@CurrentUser() uid: string, @Param('id') id: string) { return this.svc.coleccionDelOtro(uid, id); }

  @Post(':id/lote')
  lote(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { lote: any[] }) {
    return this.svc.ponerLote(uid, id, b.lote || []).then(() => ({ ok: true }));
  }

  @Post(':id/pedido')
  pedido(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { pedido: any[] }) {
    return this.svc.ponerPedido(uid, id, b.pedido || []).then(() => ({ ok: true }));
  }

  @Post(':id/confirm')
  confirmar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.confirmar(uid, id).then((estado) => ({ estado }));
  }

  @Delete(':id')
  cancelar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.cancelar(uid, id).then(() => ({ ok: true }));
  }
}
```

- [ ] **Step 2: `intercambios.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { IntercambiosController } from './intercambios.controller';
import { IntercambiosService } from './intercambios.service';

@Module({
  controllers: [IntercambiosController],
  providers: [IntercambiosService],
})
export class IntercambiosModule {}
```

- [ ] **Step 3: Registrar `IntercambiosModule` en `app.module.ts`.**

- [ ] **Step 4: Test e2e — trade completo de 2 usuarios**

Create `api/test/trades.e2e-spec.ts`:
```typescript
import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('trades', () => {
  let app: INestApplication; let prisma: PrismaService; let http: any;
  const A = 'u-a', B = 'u-b';
  const tA = () => tokenDe(A, 'a@test'), tB = () => tokenDe(B, 'b@test');
  const blob = (atra: any, shiny: number[] = []) => ({ 'col:atrapados': JSON.stringify(atra), 'col:shiny': JSON.stringify(shiny) });

  beforeAll(async () => {
    app = await crearApp(); http = app.getHttpServer(); prisma = app.get(PrismaService);
    for (const [id, email] of [[A, 'a@test'], [B, 'b@test']] as const)
      await prisma.user.upsert({ where: { email }, create: { id, email }, update: {} });
  });
  beforeEach(async () => {
    await prisma.intercambio.deleteMany({});
    await prisma.progreso.upsert({ where: { userId: A }, create: { userId: A, estado: blob({ '25': 2 }) }, update: { estado: blob({ '25': 2 }) } });
    await prisma.progreso.upsert({ where: { userId: B }, create: { userId: B, estado: blob({ '7': 1 }) }, update: { estado: blob({ '7': 1 }) } });
  });
  afterAll(async () => { await prisma.intercambio.deleteMany({}); await prisma.progreso.deleteMany({ where: { userId: { in: [A, B] } } }); await app.close(); });

  it('crear→unirse→lotes→confirmar x2 ejecuta el swap', async () => {
    const c = await request(http).post('/trades').set('Authorization', `Bearer ${tA()}`).send({ nombre: 'A' }).expect(201);
    const id = c.body.id;
    await request(http).post('/trades/join').set('Authorization', `Bearer ${tB()}`).send({ codigo: c.body.codigo, nombre: 'B' }).expect(201);
    await request(http).post(`/trades/${id}/lote`).set('Authorization', `Bearer ${tA()}`).send({ lote: [{ id: 25 }] }).expect(201);
    await request(http).post(`/trades/${id}/lote`).set('Authorization', `Bearer ${tB()}`).send({ lote: [{ id: 7 }] }).expect(201);
    await request(http).post(`/trades/${id}/confirm`).set('Authorization', `Bearer ${tA()}`).expect(201);
    const fin = await request(http).post(`/trades/${id}/confirm`).set('Authorization', `Bearer ${tB()}`).expect(201);
    expect(fin.body.estado).toBe('completada');
    const pa = await prisma.progreso.findUnique({ where: { userId: A } });
    const pb = await prisma.progreso.findUnique({ where: { userId: B } });
    expect(JSON.parse((pa!.estado as any)['col:atrapados'])).toEqual({ '25': 1, '7': 1 });
    expect(JSON.parse((pb!.estado as any)['col:atrapados'])).toEqual({ '7': 1, '25': 1 });
  });
});
```

- [ ] **Step 5: Correr**

Run: `cd api && JWT_SECRET=test-secret DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npm run test:e2e -- trades`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/src api/test
git commit -m "API: intercambios en vivo (crear/unirse/lote/pedido/otro/confirm/cancel) + swap atomico + e2e"
```

---

## Fase 7 — Social: perfiles

### Task 7.1: PerfilesService

**Files:**
- Create: `api/src/social/perfiles.service.ts`

- [ ] **Step 1: Escribir el servicio**

```typescript
import { BadRequestException, Injectable, UnauthorizedException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

const ALF = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const code6 = () => Array.from({ length: 6 }, () => ALF[Math.floor(Math.random() * ALF.length)]).join('');
const HANDLE_RE = /^[a-z0-9_]{3,20}$/;

@Injectable()
export class PerfilesService {
  constructor(private prisma: PrismaService) {}

  async mio(uid: string) {
    return this.prisma.perfil.findUnique({ where: { userId: uid } });
  }

  // handle/nombre INMUTABLES tras creación: updates solo tocan avatar + publico.
  async guardar(uid: string, p: { handle: string; nombre: string; avatar: number; publico: any }) {
    if (!uid) throw new UnauthorizedException('no autenticado');
    const existe = await this.prisma.perfil.findUnique({ where: { userId: uid } });
    if (existe) {
      return this.prisma.perfil.update({
        where: { userId: uid },
        data: { avatar: p.avatar ?? existe.avatar, publico: p.publico ?? (existe.publico as any) },
      });
    }
    const h = (p.handle || '').trim().toLowerCase();
    if (!HANDLE_RE.test(h)) throw new BadRequestException('usuario inválido (3-20, minúsculas, números o _)');
    if (await this.prisma.perfil.findUnique({ where: { handle: h } })) throw new BadRequestException('ese @ ya está tomado');
    let codigoAmigo = code6();
    while (await this.prisma.perfil.findUnique({ where: { codigoAmigo } })) codigoAmigo = code6();
    return this.prisma.perfil.create({
      data: { userId: uid, handle: h, nombre: p.nombre || h, avatar: p.avatar || 0, codigoAmigo, publico: p.publico || {} },
    });
  }

  async actualizarPublico(uid: string, publico: any, avatar?: number) {
    const existe = await this.prisma.perfil.findUnique({ where: { userId: uid } });
    if (!existe) return; // no-op si no tiene perfil
    await this.prisma.perfil.update({
      where: { userId: uid },
      data: { publico: publico || {}, avatar: avatar ?? existe.avatar },
    });
  }

  async actualizarDescripcion(uid: string, desc: string) {
    const existe = await this.prisma.perfil.findUnique({ where: { userId: uid } });
    if (!existe) return;
    await this.prisma.perfil.update({ where: { userId: uid }, data: { descripcion: (desc || '').slice(0, 200) } });
  }

  async porHandle(handle: string) {
    return this.prisma.perfil.findUnique({ where: { handle: (handle || '').trim().toLowerCase() } });
  }

  async buscar(q: string) {
    const t = (q || '').trim();
    if (t.length < 2) return [];
    const rows = await this.prisma.perfil.findMany({
      where: { OR: [{ handle: { contains: t, mode: 'insensitive' } }, { nombre: { contains: t, mode: 'insensitive' } }] },
      orderBy: { handle: 'asc' }, take: 20,
      select: { handle: true, nombre: true, avatar: true },
    });
    return rows;
  }

  // ranking por cantidad de pokémon (publico.conteos.total). Pocos usuarios → orden en JS.
  async listar(uid: string, limite: number, offset: number) {
    const todos = await this.prisma.perfil.findMany({ where: { userId: { not: uid } } });
    const total = todos.length;
    const tot = (p: any) => Number(p.publico?.conteos?.total || 0);
    const uni = (p: any) => Number(p.publico?.conteos?.unicos || 0);
    todos.sort((a, b) => tot(b) - tot(a) || uni(b) - uni(a) || a.handle.localeCompare(b.handle));
    const lim = Math.max(1, Math.min(limite || 10, 50));
    const off = Math.max(0, offset || 0);
    return todos.slice(off, off + lim).map((p) => ({
      handle: p.handle, nombre: p.nombre, avatar: p.avatar, pokes: tot(p), total,
    }));
  }
}
```

### Task 7.2: PerfilesController

**Files:**
- Create: `api/src/social/perfiles.controller.ts`

- [ ] **Step 1: Escribir el controller**

```typescript
import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { PerfilesService } from './perfiles.service';

@Controller()
export class PerfilesController {
  constructor(private svc: PerfilesService) {}

  @Get('perfil/me') mio(@CurrentUser() uid: string) { return this.svc.mio(uid); }

  @Post('perfil') guardar(@CurrentUser() uid: string, @Body() b: any) {
    return this.svc.guardar(uid, b);
  }
  @Post('perfil/publico') publico(@CurrentUser() uid: string, @Body() b: { publico: any; avatar?: number }) {
    return this.svc.actualizarPublico(uid, b.publico, b.avatar).then(() => ({ ok: true }));
  }
  @Post('perfil/descripcion') desc(@CurrentUser() uid: string, @Body() b: { desc: string }) {
    return this.svc.actualizarDescripcion(uid, b.desc).then(() => ({ ok: true }));
  }
  @Get('perfil/:handle') porHandle(@Param('handle') h: string) { return this.svc.porHandle(h); }
  @Get('perfiles') buscar(@Query('q') q: string) { return this.svc.buscar(q); }
  @Get('perfiles/listar') listar(@CurrentUser() uid: string, @Query('limite') l: string, @Query('offset') o: string) {
    return this.svc.listar(uid, Number(l), Number(o));
  }
}
```

> Nota de ruteo: `GET /perfiles` y `GET /perfiles/listar` son rutas distintas; `GET /perfil/:handle` no choca con `/perfil/me` porque `me` se declara antes y Nest matchea literales antes que params.

---

## Fase 8 — Social: amigos

### Task 8.1: AmigosService

**Files:**
- Create: `api/src/social/amigos.service.ts`

- [ ] **Step 1: Escribir el servicio**

```typescript
import { BadRequestException, ForbiddenException, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class AmigosService {
  constructor(private prisma: PrismaService) {}

  async solicitar(uid: string, handle?: string, codigo?: string) {
    let destino = null as null | { userId: string };
    if (handle) destino = await this.prisma.perfil.findUnique({ where: { handle: handle.trim().toLowerCase() }, select: { userId: true } });
    if (!destino && codigo) destino = await this.prisma.perfil.findUnique({ where: { codigoAmigo: codigo.trim().toUpperCase() }, select: { userId: true } });
    if (!destino) throw new NotFoundException('usuario no encontrado');
    if (destino.userId === uid) throw new BadRequestException('no podés agregarte a vos mismo');
    const ya = await this.prisma.amistad.findFirst({
      where: { OR: [{ deId: uid, aId: destino.userId }, { deId: destino.userId, aId: uid }] },
    });
    if (ya) return; // ya existe relación
    await this.prisma.amistad.create({ data: { deId: uid, aId: destino.userId, estado: 'pendiente' } });
  }

  async responder(uid: string, id: string, aceptar: boolean) {
    const s = await this.prisma.amistad.findUnique({ where: { id } });
    if (!s || s.aId !== uid) throw new ForbiddenException('no podés responder esta solicitud');
    if (aceptar) await this.prisma.amistad.update({ where: { id }, data: { estado: 'aceptada' } });
    else await this.prisma.amistad.delete({ where: { id } });
  }

  async quitar(uid: string, id: string) {
    const s = await this.prisma.amistad.findUnique({ where: { id } });
    if (!s || (s.deId !== uid && s.aId !== uid)) throw new ForbiddenException('no autorizado');
    await this.prisma.amistad.delete({ where: { id } });
  }

  // helper: junta perfiles por userId
  private async conPerfil(rows: { id: string; otro: string }[]) {
    const perfiles = await this.prisma.perfil.findMany({ where: { userId: { in: rows.map((r) => r.otro) } } });
    const m = new Map(perfiles.map((p) => [p.userId, p]));
    return rows.filter((r) => m.has(r.otro)).map((r) => {
      const p = m.get(r.otro)!;
      return { id: r.id, user_id: p.userId, handle: p.handle, nombre: p.nombre, avatar: p.avatar };
    });
  }

  async misAmigos(uid: string) {
    const a = await this.prisma.amistad.findMany({ where: { estado: 'aceptada', OR: [{ deId: uid }, { aId: uid }] } });
    return this.conPerfil(a.map((r) => ({ id: r.id, otro: r.deId === uid ? r.aId : r.deId })));
  }

  async solicitudes(uid: string) {
    const a = await this.prisma.amistad.findMany({ where: { estado: 'pendiente', aId: uid } });
    return this.conPerfil(a.map((r) => ({ id: r.id, otro: r.deId })));
  }

  async sonAmigos(uid: string, otro: string) {
    const a = await this.prisma.amistad.findFirst({
      where: { estado: 'aceptada', OR: [{ deId: uid, aId: otro }, { deId: otro, aId: uid }] },
    });
    return !!a;
  }

  // Map(handle del otro -> estado) de todas las relaciones del que llama
  async misRelaciones(uid: string) {
    const a = await this.prisma.amistad.findMany({ where: { OR: [{ deId: uid }, { aId: uid }] } });
    const otros = a.map((r) => ({ estado: r.estado, otro: r.deId === uid ? r.aId : r.deId }));
    const perfiles = await this.prisma.perfil.findMany({ where: { userId: { in: otros.map((o) => o.otro) } } });
    const m = new Map(perfiles.map((p) => [p.userId, p.handle]));
    return otros.filter((o) => m.has(o.otro)).map((o) => ({ handle: m.get(o.otro), estado: o.estado }));
  }
}
```

### Task 8.2: AmigosController

**Files:**
- Create: `api/src/social/amigos.controller.ts`

- [ ] **Step 1: Escribir el controller**

```typescript
import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { AmigosService } from './amigos.service';

@Controller('amigos')
export class AmigosController {
  constructor(private svc: AmigosService) {}

  @Post('solicitar') solicitar(@CurrentUser() uid: string, @Body() b: { handle?: string; codigo?: string }) {
    return this.svc.solicitar(uid, b.handle, b.codigo).then(() => ({ ok: true }));
  }
  @Post(':id/responder') responder(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { aceptar: boolean }) {
    return this.svc.responder(uid, id, !!b.aceptar).then(() => ({ ok: true }));
  }
  @Delete(':id') quitar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.quitar(uid, id).then(() => ({ ok: true }));
  }
  @Get() mis(@CurrentUser() uid: string) { return this.svc.misAmigos(uid); }
  @Get('solicitudes') solicitudes(@CurrentUser() uid: string) { return this.svc.solicitudes(uid); }
  @Get('relaciones') relaciones(@CurrentUser() uid: string) { return this.svc.misRelaciones(uid); }
  @Get('son/:otro') son(@CurrentUser() uid: string, @Param('otro') otro: string) {
    return this.svc.sonAmigos(uid, otro).then((v) => ({ son: v }));
  }
}
```

> Ruteo: `GET /amigos/solicitudes`, `/amigos/relaciones`, `/amigos/son/:otro` son literales antes que cualquier param; `GET /amigos` (lista) en la raíz. No hay colisión.

---

## Fase 9 — Social: ofertas (intercambio async, incl. swap)

### Task 9.1: OfertasService

**Files:**
- Create: `api/src/social/ofertas.service.ts`

- [ ] **Step 1: Escribir el servicio**

```typescript
import { BadRequestException, ForbiddenException, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { RealtimeService } from '../realtime/realtime.service';
import { AmigosService } from './amigos.service';
import { swapColeccion, Item } from '../coleccion/coleccion';

@Injectable()
export class OfertasService {
  constructor(private prisma: PrismaService, private amigos: AmigosService, private rt: RealtimeService) {}

  async crear(uid: string, aId: string, doy: Item[], pido: Item[]) {
    if (!(await this.amigos.sonAmigos(uid, aId))) throw new ForbiddenException('solo podés ofertar a un amigo');
    const o = await this.prisma.oferta.create({ data: { deId: uid, aId, doy: doy as any, pido: pido as any } });
    return o.id;
  }

  async cancelar(uid: string, id: string) {
    const o = await this.prisma.oferta.findUnique({ where: { id } });
    if (!o || o.deId !== uid) throw new ForbiddenException('no autorizado');
    if (o.estado === 'pendiente') await this.prisma.oferta.update({ where: { id }, data: { estado: 'cancelada', resuelto: new Date() } });
  }

  async responder(uid: string, id: string, aceptar: boolean): Promise<'aceptada' | 'rechazada'> {
    const o0 = await this.prisma.oferta.findUnique({ where: { id } });
    if (!o0 || o0.aId !== uid) throw new ForbiddenException('no podés responder esta oferta');
    if (o0.estado !== 'pendiente') throw new BadRequestException('la oferta ya no está pendiente');
    if (!aceptar) {
      await this.prisma.oferta.update({ where: { id }, data: { estado: 'rechazada', resuelto: new Date() } });
      return 'rechazada';
    }
    const [de, a] = [o0.deId, o0.aId];
    const [estDe, estA] = await this.prisma.$transaction(async (tx) => {
      await tx.$queryRawUnsafe(`SELECT user_id FROM progreso WHERE user_id IN ($1,$2) ORDER BY user_id FOR UPDATE`, de, a);
      const dP = await tx.progreso.findUnique({ where: { userId: de } });
      const aP = await tx.progreso.findUnique({ where: { userId: a } });
      // de da 'doy' -> a ; a (vos) da 'pido' -> de
      const { estadoA: dEst, estadoB: aEst } = swapColeccion(
        (dP?.estado as any) || {}, o0.doy as any, 'el que ofrece',
        (aP?.estado as any) || {}, o0.pido as any, 'vos',
      );
      await tx.progreso.upsert({ where: { userId: de }, create: { userId: de, estado: dEst }, update: { estado: dEst } });
      await tx.progreso.upsert({ where: { userId: a }, create: { userId: a, estado: aEst }, update: { estado: aEst } });
      await tx.oferta.update({ where: { id }, data: { estado: 'aceptada', resuelto: new Date() } });
      return [dEst, aEst];
    }, { isolationLevel: 'Serializable' });
    this.rt.progreso(de, estDe);
    this.rt.progreso(a, estA);
    return 'aceptada';
  }

  async mias(uid: string) {
    const rows = await this.prisma.oferta.findMany({
      where: { estado: 'pendiente', OR: [{ deId: uid }, { aId: uid }] }, orderBy: { creado: 'desc' },
    });
    const otros = rows.map((o) => (o.deId === uid ? o.aId : o.deId));
    const perfiles = await this.prisma.perfil.findMany({ where: { userId: { in: otros } } });
    const m = new Map(perfiles.map((p) => [p.userId, p]));
    return rows.map((o) => {
      const otro = o.deId === uid ? o.aId : o.deId;
      const p = m.get(otro);
      return {
        id: o.id, de_id: o.deId, a_id: o.aId, doy: o.doy, pido: o.pido, estado: o.estado, creado: o.creado,
        otro_handle: p?.handle || '', otro_nombre: p?.nombre || '', soy_de: o.deId === uid,
      };
    });
  }

  // badge: solicitudes de amistad entrantes + ofertas entrantes pendientes
  async pendientes(uid: string) {
    const [am, of] = await this.prisma.$transaction([
      this.prisma.amistad.count({ where: { estado: 'pendiente', aId: uid } }),
      this.prisma.oferta.count({ where: { estado: 'pendiente', aId: uid } }),
    ]);
    return am + of;
  }
}
```

### Task 9.2: OfertasController + SocialModule (perfiles+amigos+ofertas)

**Files:**
- Create: `api/src/social/ofertas.controller.ts`
- Create: `api/src/social/social.module.ts`
- Modify: `api/src/app.module.ts`

- [ ] **Step 1: `ofertas.controller.ts`**

```typescript
import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { OfertasService } from './ofertas.service';

@Controller()
export class OfertasController {
  constructor(private svc: OfertasService) {}

  @Post('ofertas') crear(@CurrentUser() uid: string, @Body() b: { aId: string; doy: any[]; pido: any[] }) {
    return this.svc.crear(uid, b.aId, b.doy || [], b.pido || []).then((id) => ({ id }));
  }
  @Post('ofertas/:id/responder') responder(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { aceptar: boolean }) {
    return this.svc.responder(uid, id, !!b.aceptar).then((estado) => ({ estado }));
  }
  @Delete('ofertas/:id') cancelar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.cancelar(uid, id).then(() => ({ ok: true }));
  }
  @Get('ofertas') mias(@CurrentUser() uid: string) { return this.svc.mias(uid); }
  @Get('social/pendientes') pendientes(@CurrentUser() uid: string) {
    return this.svc.pendientes(uid).then((n) => ({ n }));
  }
}
```

- [ ] **Step 2: `social.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { PerfilesService } from './perfiles.service';
import { PerfilesController } from './perfiles.controller';
import { AmigosService } from './amigos.service';
import { AmigosController } from './amigos.controller';
import { OfertasService } from './ofertas.service';
import { OfertasController } from './ofertas.controller';

@Module({
  controllers: [PerfilesController, AmigosController, OfertasController],
  providers: [PerfilesService, AmigosService, OfertasService],
})
export class SocialModule {}
```

- [ ] **Step 3: Registrar `SocialModule` en `app.module.ts`.**

- [ ] **Step 4: Build + test e2e de amigos+oferta**

Create `api/test/social.e2e-spec.ts`:
```typescript
import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('social', () => {
  let app: INestApplication; let prisma: PrismaService; let http: any;
  const A = 'u-sa', B = 'u-sb';
  const blob = (atra: any) => ({ 'col:atrapados': JSON.stringify(atra), 'col:shiny': '[]' });
  beforeAll(async () => {
    app = await crearApp(); http = app.getHttpServer(); prisma = app.get(PrismaService);
    for (const [id, email, handle] of [[A, 'sa@test', 'usera'], [B, 'sb@test', 'userb']] as const) {
      await prisma.user.upsert({ where: { email }, create: { id, email }, update: {} });
      await prisma.perfil.upsert({ where: { userId: id }, create: { userId: id, handle, codigoAmigo: handle.toUpperCase().slice(0, 6) }, update: {} });
    }
  });
  beforeEach(async () => {
    await prisma.oferta.deleteMany({}); await prisma.amistad.deleteMany({});
    await prisma.progreso.upsert({ where: { userId: A }, create: { userId: A, estado: blob({ '25': 1 }) }, update: { estado: blob({ '25': 1 }) } });
    await prisma.progreso.upsert({ where: { userId: B }, create: { userId: B, estado: blob({ '7': 1 }) }, update: { estado: blob({ '7': 1 }) } });
  });
  afterAll(async () => { await app.close(); });

  it('amistad + oferta aceptada ejecuta swap', async () => {
    const tA = tokenDe(A, 'sa@test'), tB = tokenDe(B, 'sb@test');
    // A solicita a B, B acepta
    await request(http).post('/amigos/solicitar').set('Authorization', `Bearer ${tA}`).send({ handle: 'userb' }).expect(201);
    const sol = await request(http).get('/amigos/solicitudes').set('Authorization', `Bearer ${tB}`).expect(200);
    await request(http).post(`/amigos/${sol.body[0].id}/responder`).set('Authorization', `Bearer ${tB}`).send({ aceptar: true }).expect(201);
    // A oferta: doy 25 <-> pido 7 ; B acepta
    const of = await request(http).post('/ofertas').set('Authorization', `Bearer ${tA}`).send({ aId: B, doy: [{ id: 25 }], pido: [{ id: 7 }] }).expect(201);
    const r = await request(http).post(`/ofertas/${of.body.id}/responder`).set('Authorization', `Bearer ${tB}`).send({ aceptar: true }).expect(201);
    expect(r.body.estado).toBe('aceptada');
    const pa = await prisma.progreso.findUnique({ where: { userId: A } });
    expect(JSON.parse((pa!.estado as any)['col:atrapados'])).toEqual({ '7': 1 });
  });
});
```

- [ ] **Step 5: Correr**

Run: `cd api && JWT_SECRET=test-secret DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npm run test:e2e -- social`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/src api/test
git commit -m "API: social (perfiles handle-inmutable, amigos, ofertas async con swap) + e2e"
```

---

## Fase 10 — Desafíos de la comunidad

### Task 10.1: DesafiosService

**Files:**
- Create: `api/src/desafios/desafios.service.ts`

- [ ] **Step 1: Escribir el servicio**

```typescript
import { BadRequestException, ForbiddenException, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

const REGIONES = ['kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos', 'libre'];

@Injectable()
export class DesafiosService {
  constructor(private prisma: PrismaService) {}

  async crear(uid: string, d: any) {
    if (!String(d.titulo || '').trim()) throw new BadRequestException('falta el título');
    if (!String(d.func || '').trim()) throw new BadRequestException('falta el nombre de la función');
    if (!Array.isArray(d.casos) || d.casos.length === 0) throw new BadRequestException('faltan casos');
    const row = await this.prisma.desafio.create({
      data: {
        autor: uid, titulo: d.titulo.trim(), consigna: d.consigna || '', func: d.func.trim(),
        starter: d.starter || '', casos: d.casos, dificultad: Math.max(1, Math.min(8, d.dificultad || 3)),
        region: REGIONES.includes(d.region) ? d.region : 'libre',
      },
    });
    return row.id;
  }

  async leer(id: string) {
    const d = await this.prisma.desafio.findUnique({ where: { id } });
    if (!d) throw new NotFoundException('no existe');
    return d;
  }

  // oculta desafíos con >=3 reportes (salvo al autor); flag resuelto por usuario.
  async listar(uid: string, q: any) {
    const { orden = 'recientes', q: texto = '', region = 'todas', limite = 30, offset = 0 } = q;
    const desafios = await this.prisma.desafio.findMany();
    const conteoRes = new Map<string, number>();
    const conteoRep = new Map<string, number>();
    const resueltosMios = new Set<string>();
    for (const r of await this.prisma.resolucion.findMany()) {
      conteoRes.set(r.desafioId, (conteoRes.get(r.desafioId) || 0) + 1);
      if (r.userId === uid) resueltosMios.add(r.desafioId);
    }
    for (const r of await this.prisma.reporte.findMany())
      conteoRep.set(r.desafioId, (conteoRep.get(r.desafioId) || 0) + 1);
    const autores = await this.prisma.perfil.findMany();
    const handle = new Map(autores.map((p) => [p.userId, p.handle]));
    const t = String(texto).trim().toLowerCase();
    let rows = desafios.filter((d) => {
      if (region && region !== '' && region !== 'todas' && d.region !== region) return false;
      if (t && !(d.titulo.toLowerCase().includes(t) || d.consigna.toLowerCase().includes(t))) return false;
      if (d.autor !== uid && (conteoRep.get(d.id) || 0) >= 3) return false; // moderación
      return true;
    }).map((d) => ({
      id: d.id, titulo: d.titulo, consigna: d.consigna, dificultad: d.dificultad, region: d.region,
      autor_handle: handle.get(d.autor) || null, resoluciones: conteoRes.get(d.id) || 0,
      resuelto: resueltosMios.has(d.id), _creado: d.creado,
    }));
    if (orden === 'resueltos') rows.sort((a, b) => b.resoluciones - a.resoluciones || +b._creado - +a._creado);
    else if (orden === 'dificultad') rows.sort((a, b) => b.dificultad - a.dificultad || +b._creado - +a._creado);
    else rows.sort((a, b) => +b._creado - +a._creado);
    const lim = Math.max(1, Math.min(limite || 30, 60));
    return rows.slice(Math.max(0, offset || 0), Math.max(0, offset || 0) + lim).map(({ _creado, ...r }) => r);
  }

  // registra (upsert) y premia 2×dificultad balls SOLO la primera vez.
  async registrarResolucion(uid: string, desafioId: string, codigo: string): Promise<number> {
    const ya = await this.prisma.resolucion.findUnique({ where: { desafioId_userId: { desafioId, userId: uid } } });
    await this.prisma.resolucion.upsert({
      where: { desafioId_userId: { desafioId, userId: uid } },
      create: { desafioId, userId: uid, codigo: codigo || '' },
      update: { codigo: codigo || '', creado: new Date() },
    });
    if (ya) return 0;
    const d = await this.prisma.desafio.findUnique({ where: { id: desafioId } });
    const premio = 2 * (d?.dificultad || 3);
    const p = await this.prisma.progreso.findUnique({ where: { userId: uid } });
    const est = ((p?.estado as any) || {}) as Record<string, any>;
    // col:balls se guarda como STRING plana (espeja localStorage), no JSON-quoted.
    const balls = Number(est['col:balls'] || 0) + premio;
    est['col:balls'] = String(balls);
    await this.prisma.progreso.upsert({ where: { userId: uid }, create: { userId: uid, estado: est }, update: { estado: est } });
    return premio;
  }

  // spoiler-gate: ves soluciones solo si resolviste el desafío o sos el autor.
  async solucionesDe(uid: string, desafioId: string) {
    const yo = await this.prisma.resolucion.findUnique({ where: { desafioId_userId: { desafioId, userId: uid } } });
    const d = await this.prisma.desafio.findUnique({ where: { id: desafioId } });
    if (!yo && d?.autor !== uid) return [];
    const res = await this.prisma.resolucion.findMany({ where: { desafioId } });
    const handle = new Map((await this.prisma.perfil.findMany({ where: { userId: { in: res.map((r) => r.userId) } } })).map((p) => [p.userId, p.handle]));
    const out = [];
    for (const r of res) {
      const votos = await this.prisma.voto.count({ where: { resolucionId: r.id } });
      const miVoto = !!(await this.prisma.voto.findUnique({ where: { resolucionId_userId: { resolucionId: r.id, userId: uid } } }));
      out.push({ id: r.id, codigo: r.codigo, autor_handle: handle.get(r.userId) || null, votos, mi_voto: miVoto, es_mia: r.userId === uid, _creado: r.creado });
    }
    out.sort((a, b) => b.votos - a.votos || +a._creado - +b._creado);
    return out.map(({ _creado, ...r }) => r);
  }

  async votar(uid: string, resolucionId: string, on: boolean) {
    if (on) await this.prisma.voto.upsert({ where: { resolucionId_userId: { resolucionId, userId: uid } }, create: { resolucionId, userId: uid }, update: {} });
    else await this.prisma.voto.deleteMany({ where: { resolucionId, userId: uid } });
  }

  async deUsuario(userId: string) {
    const creados = await this.prisma.desafio.findMany({ where: { autor: userId } });
    const resol = await this.prisma.resolucion.findMany({ where: { userId } });
    const dres = await this.prisma.desafio.findMany({ where: { id: { in: resol.map((r) => r.desafioId) } } });
    const rows = [
      ...creados.map((d) => ({ id: d.id, titulo: d.titulo, region: d.region, dificultad: d.dificultad, rol: 'creado' })),
      ...dres.map((d) => ({ id: d.id, titulo: d.titulo, region: d.region, dificultad: d.dificultad, rol: 'resuelto' })),
    ];
    rows.sort((a, b) => b.rol.localeCompare(a.rol) || a.titulo.localeCompare(b.titulo));
    return rows;
  }

  async ranking() {
    const perfiles = await this.prisma.perfil.findMany();
    const out = [];
    for (const p of perfiles) {
      const creados = await this.prisma.desafio.count({ where: { autor: p.userId } });
      const resueltos = await this.prisma.resolucion.count({ where: { userId: p.userId } });
      if (creados || resueltos) out.push({ handle: p.handle, avatar: p.avatar, creados, resueltos });
    }
    out.sort((a, b) => b.creados - a.creados || b.resueltos - a.resueltos);
    return out.slice(0, 20);
  }

  async stats(userId: string) {
    const [resueltos, creados] = await this.prisma.$transaction([
      this.prisma.resolucion.count({ where: { userId } }),
      this.prisma.desafio.count({ where: { autor: userId } }),
    ]);
    return { resueltos, creados };
  }

  async reportar(uid: string, desafioId: string, motivo: string) {
    await this.prisma.reporte.upsert({
      where: { desafioId_userId: { desafioId, userId: uid } },
      create: { desafioId, userId: uid, motivo: (motivo || '').slice(0, 200) },
      update: { motivo: (motivo || '').slice(0, 200), creado: new Date() },
    });
  }

  async borrar(uid: string, desafioId: string) {
    const d = await this.prisma.desafio.findUnique({ where: { id: desafioId } });
    if (!d) throw new NotFoundException('no existe');
    if (d.autor !== uid) throw new ForbiddenException('solo el autor puede borrarlo');
    // cascade manual (no hay FK relacionales en el schema)
    await this.prisma.$transaction([
      this.prisma.voto.deleteMany({ where: { resolucionId: { in: (await this.prisma.resolucion.findMany({ where: { desafioId } })).map((r) => r.id) } } }),
      this.prisma.resolucion.deleteMany({ where: { desafioId } }),
      this.prisma.reporte.deleteMany({ where: { desafioId } }),
      this.prisma.desafio.delete({ where: { id: desafioId } }),
    ]);
  }
}
```

### Task 10.2: DesafiosController + módulo

**Files:**
- Create: `api/src/desafios/desafios.controller.ts`
- Create: `api/src/desafios/desafios.module.ts`
- Modify: `api/src/app.module.ts`

- [ ] **Step 1: `desafios.controller.ts`**

```typescript
import { Body, Controller, Delete, Get, Param, Post, Query } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { DesafiosService } from './desafios.service';

@Controller()
export class DesafiosController {
  constructor(private svc: DesafiosService) {}

  @Post('desafios') crear(@CurrentUser() uid: string, @Body() b: any) {
    return this.svc.crear(uid, b).then((id) => ({ id }));
  }
  @Get('desafios/ranking') ranking() { return this.svc.ranking(); }
  @Get('desafios') listar(@CurrentUser() uid: string, @Query() q: any) { return this.svc.listar(uid, q); }
  @Get('desafios/:id') leer(@Param('id') id: string) { return this.svc.leer(id); }
  @Post('desafios/:id/resolver') resolver(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { codigo: string }) {
    return this.svc.registrarResolucion(uid, id, b.codigo).then((balls) => ({ balls }));
  }
  @Get('desafios/:id/soluciones') soluciones(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.solucionesDe(uid, id);
  }
  @Post('desafios/:id/reportar') reportar(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { motivo: string }) {
    return this.svc.reportar(uid, id, b.motivo).then(() => ({ ok: true }));
  }
  @Delete('desafios/:id') borrar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.borrar(uid, id).then(() => ({ ok: true }));
  }
  @Post('resoluciones/:id/votar') votar(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { on: boolean }) {
    return this.svc.votar(uid, id, !!b.on).then(() => ({ ok: true }));
  }
  @Get('usuarios/:id/desafios') deUsuario(@Param('id') id: string) { return this.svc.deUsuario(id); }
  @Get('usuarios/:id/stats') stats(@Param('id') id: string) { return this.svc.stats(id); }
}
```

> Ruteo: `desafios/ranking` se declara antes que `desafios/:id` para que no lo capture el param.

- [ ] **Step 2: `desafios.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { DesafiosController } from './desafios.controller';
import { DesafiosService } from './desafios.service';

@Module({ controllers: [DesafiosController], providers: [DesafiosService] })
export class DesafiosModule {}
```

- [ ] **Step 3: Registrar `DesafiosModule` en `app.module.ts`.**

- [ ] **Step 4: Test e2e (spoiler-gate + balls primera vez)**

Create `api/test/desafios.e2e-spec.ts`:
```typescript
import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('desafios', () => {
  let app: INestApplication; let prisma: PrismaService; let http: any;
  const A = 'u-da', B = 'u-db';
  beforeAll(async () => {
    app = await crearApp(); http = app.getHttpServer(); prisma = app.get(PrismaService);
    for (const [id, email] of [[A, 'da@test'], [B, 'db@test']] as const)
      await prisma.user.upsert({ where: { email }, create: { id, email }, update: {} });
  });
  beforeEach(async () => {
    await prisma.voto.deleteMany({}); await prisma.resolucion.deleteMany({}); await prisma.desafio.deleteMany({});
    await prisma.progreso.upsert({ where: { userId: B }, create: { userId: B, estado: { 'col:balls': '0' } }, update: { estado: { 'col:balls': '0' } } });
  });
  afterAll(async () => { await app.close(); });

  it('soluciones gated + balls solo la primera vez', async () => {
    const tA = tokenDe(A, 'da@test'), tB = tokenDe(B, 'db@test');
    const d = await request(http).post('/desafios').set('Authorization', `Bearer ${tA}`)
      .send({ titulo: 'Suma', func: 'suma', casos: [{ args: [1, 2], esperado: '3' }], dificultad: 3 }).expect(201);
    const id = d.body.id;
    // B no resolvió -> soluciones vacías (gated)
    const g = await request(http).get(`/desafios/${id}/soluciones`).set('Authorization', `Bearer ${tB}`).expect(200);
    expect(g.body.length).toBe(0);
    // B resuelve -> gana 6 balls (2×3)
    const r1 = await request(http).post(`/desafios/${id}/resolver`).set('Authorization', `Bearer ${tB}`).send({ codigo: 'x' }).expect(201);
    expect(r1.body.balls).toBe(6);
    // re-resolver no vuelve a premiar
    const r2 = await request(http).post(`/desafios/${id}/resolver`).set('Authorization', `Bearer ${tB}`).send({ codigo: 'y' }).expect(201);
    expect(r2.body.balls).toBe(0);
    // ahora sí ve soluciones
    const g2 = await request(http).get(`/desafios/${id}/soluciones`).set('Authorization', `Bearer ${tB}`).expect(200);
    expect(g2.body.length).toBe(1);
  });
});
```

- [ ] **Step 5: Correr**

Run: `cd api && JWT_SECRET=test-secret DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npm run test:e2e -- desafios`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/src api/test
git commit -m "API: desafios (crear/listar+moderacion/resolver+balls/soluciones gated/votar/ranking/stats/reportar/borrar) + e2e"
```

---

## Fase 11 — Migración de datos desde Supabase

### Task 11.1: Export del proyecto Supabase

**Files:**
- Create: `api/prisma/dump/` (carpeta para los CSV/SQL exportados; gitignored)

- [ ] **Step 1: Exportar usuarios + tablas públicas**

> La CLI ya está linkeada (ver CLAUDE.md). Usás la connection string del proyecto remoto.
> Reemplazá `<DB_URL_SUPABASE>` por la del dashboard (Settings → Database → Connection string).

Run (desde la raíz del repo):
```bash
mkdir -p api/prisma/dump
PGU="<DB_URL_SUPABASE>"
# usuarios (id+email) desde auth.users
psql "$PGUSER_URL" -c "\copy (select id, email from auth.users) to 'api/prisma/dump/users.csv' csv header" 2>/dev/null || \
psql "$PGU" -c "\copy (select id, email from auth.users) to 'api/prisma/dump/users.csv' csv header"
# cada tabla pública
for t in progreso perfiles amistades ofertas intercambios desafios resoluciones votos reportes; do
  psql "$PGU" -c "\copy (select * from public.$t) to 'api/prisma/dump/$t.csv' csv header"
done
ls -la api/prisma/dump
```
Expected: 10 CSV en `api/prisma/dump/`.

- [ ] **Step 2: gitignore del dump**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
grep -qxF 'prisma/dump/' .gitignore || echo 'prisma/dump/' >> .gitignore
```

- [ ] **Step 3: Commit (solo el gitignore)**

```bash
git add api/.gitignore
git commit -m "API: ignorar dump de migracion"
```

### Task 11.2: Importador `seed-import.ts`

**Files:**
- Create: `api/prisma/seed-import.ts`

- [ ] **Step 1: Escribir el importador**

> Lee los CSV y los inserta preservando UUIDs. Mapea snake_case → campos Prisma. `googleSub`
> queda null (se completa en el primer login por email). Idempotente: usa `upsert`/`createMany skipDuplicates`.

```typescript
import { PrismaClient } from '@prisma/client';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const prisma = new PrismaClient();
const DIR = join(__dirname, 'dump');

// parser CSV mínimo (campos sin comas internas en este dataset; jsonb va quoteado)
function leerCsv(nombre: string): Record<string, string>[] {
  const path = join(DIR, nombre);
  if (!existsSync(path)) { console.log(`(skip) ${nombre} no existe`); return []; }
  const txt = readFileSync(path, 'utf8').trim();
  if (!txt) return [];
  const lineas = txt.split('\n');
  const cols = parseLinea(lineas[0]);
  return lineas.slice(1).map((l) => Object.fromEntries(parseLinea(l).map((v, i) => [cols[i], v])));
}
function parseLinea(l: string): string[] {
  const out: string[] = []; let cur = ''; let q = false;
  for (let i = 0; i < l.length; i++) {
    const c = l[i];
    if (q) { if (c === '"' && l[i + 1] === '"') { cur += '"'; i++; } else if (c === '"') q = false; else cur += c; }
    else { if (c === '"') q = true; else if (c === ',') { out.push(cur); cur = ''; } else cur += c; }
  }
  out.push(cur); return out;
}
const J = (s: string, def: any) => { try { return s ? JSON.parse(s) : def; } catch { return def; } };
const D = (s: string) => (s ? new Date(s) : undefined);

async function main() {
  for (const u of leerCsv('users.csv'))
    await prisma.user.upsert({ where: { id: u.id }, create: { id: u.id, email: u.email }, update: { email: u.email } });

  for (const r of leerCsv('progreso.csv'))
    await prisma.progreso.upsert({ where: { userId: r.user_id }, create: { userId: r.user_id, estado: J(r.estado, {}) }, update: { estado: J(r.estado, {}) } });

  for (const r of leerCsv('perfiles.csv'))
    await prisma.perfil.upsert({ where: { userId: r.user_id }, create: {
      userId: r.user_id, handle: r.handle, nombre: r.nombre || '', avatar: Number(r.avatar) || 0,
      codigoAmigo: r.codigo_amigo, publico: J(r.publico, {}), descripcion: r.descripcion || '',
    }, update: {} });

  for (const r of leerCsv('amistades.csv'))
    await prisma.amistad.upsert({ where: { id: r.id }, create: { id: r.id, deId: r.de_id, aId: r.a_id, estado: r.estado, creado: D(r.creado) }, update: {} });

  for (const r of leerCsv('ofertas.csv'))
    await prisma.oferta.upsert({ where: { id: r.id }, create: {
      id: r.id, deId: r.de_id, aId: r.a_id, doy: J(r.doy, []), pido: J(r.pido, []), estado: r.estado, creado: D(r.creado), resuelto: D(r.resuelto),
    }, update: {} });

  for (const r of leerCsv('intercambios.csv'))
    await prisma.intercambio.upsert({ where: { id: r.id }, create: {
      id: r.id, codigo: r.codigo, creadorId: r.creador_id, invitadoId: r.invitado_id || null,
      creadorNombre: r.creador_nombre || '', invitadoNombre: r.invitado_nombre || '',
      creadorLote: J(r.creador_lote, []), invitadoLote: J(r.invitado_lote, []),
      creadorPedido: J(r.creador_pedido, []), invitadoPedido: J(r.invitado_pedido, []),
      creadorOk: r.creador_ok === 't' || r.creador_ok === 'true', invitadoOk: r.invitado_ok === 't' || r.invitado_ok === 'true',
      estado: r.estado, creado: D(r.creado),
    }, update: {} });

  for (const r of leerCsv('desafios.csv'))
    await prisma.desafio.upsert({ where: { id: r.id }, create: {
      id: r.id, autor: r.autor, titulo: r.titulo, consigna: r.consigna || '', func: r.func, starter: r.starter || '',
      casos: J(r.casos, []), dificultad: Number(r.dificultad) || 3, region: r.region || 'libre', creado: D(r.creado),
    }, update: {} });

  for (const r of leerCsv('resoluciones.csv'))
    await prisma.resolucion.upsert({ where: { id: r.id }, create: { id: r.id, desafioId: r.desafio_id, userId: r.user_id, codigo: r.codigo || '', creado: D(r.creado) }, update: {} });

  for (const r of leerCsv('votos.csv'))
    await prisma.voto.upsert({ where: { resolucionId_userId: { resolucionId: r.resolucion_id, userId: r.user_id } }, create: { resolucionId: r.resolucion_id, userId: r.user_id }, update: {} });

  for (const r of leerCsv('reportes.csv'))
    await prisma.reporte.upsert({ where: { desafioId_userId: { desafioId: r.desafio_id, userId: r.user_id } }, create: { desafioId: r.desafio_id, userId: r.user_id, motivo: r.motivo || '', creado: D(r.creado) }, update: {} });

  console.log('import OK');
}
main().finally(() => prisma.$disconnect());
```

- [ ] **Step 2: Correr el import contra la DB nueva**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/api
DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npx ts-node prisma/seed-import.ts
```
Expected: `import OK`. (Si no hay CSV, salta cada tabla sin romper.)

- [ ] **Step 3: Verificar conteos**

Run: `docker compose exec db psql -U luca -d luca -c "select (select count(*) from users) u, (select count(*) from perfiles) p, (select count(*) from progreso) pr;"`
Expected: conteos > 0 si había datos.

- [ ] **Step 4: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add api/prisma/seed-import.ts
git commit -m "API: importador de datos de Supabase (preserva UUIDs, googleSub se completa al loguear)"
```

---

## Fase 12 — Dockerfile de la API

### Task 12.1: Build de la imagen + arranque con migraciones

**Files:**
- Create: `api/Dockerfile`
- Create: `api/.dockerignore`

- [ ] **Step 1: `api/Dockerfile`**

```dockerfile
FROM node:24-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*
COPY package*.json ./
RUN npm ci
COPY . .
RUN npx prisma generate && npm run build

FROM node:24-slim
WORKDIR /app
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/prisma ./prisma
COPY package*.json ./
# migra y arranca
CMD npx prisma migrate deploy && node dist/main
```

- [ ] **Step 2: `api/.dockerignore`**

```
node_modules
dist
.env
prisma/dump
```

- [ ] **Step 3: Build + up del stack completo**

Run (con `.env` en la raíz que defina `JWT_SECRET`, `GOOGLE_*`, `FRONTEND_URL`, `CORS_ORIGINS`):
```bash
cd /home/felipe/Documents/Repositories/luca-journey
docker compose up -d --build
docker compose logs api --tail 20
curl -s localhost:3000/auth/me ; echo   # 401 esperado (sin token)
```
Expected: `api` levanta, migra, y `/auth/me` responde 401.

- [ ] **Step 4: Commit**

```bash
git add api/Dockerfile api/.dockerignore
git commit -m "API: Dockerfile (build + prisma migrate deploy + arranque)"
```

---

## Fase 12b — DTOs snake_case (fidelidad de campos con las páginas)

> Las páginas leen el row **crudo** con nombres snake_case (`sala.creador_lote`,
> `sala.invitado_id`, `perfil.codigo_amigo`, `perfil.user_id`). Prisma devuelve camelCase →
> hay que serializar a snake_case en las respuestas que devuelven el **row entero**
> (intercambio y perfil). Los endpoints "tipo RPC" (mis_amigos, mis_ofertas, listar_perfiles,
> listar_desafios) ya devuelven snake_case por diseño.

### Task 12b.1: Helpers de DTO

**Files:**
- Create: `api/src/common/dto.ts`

- [ ] **Step 1: Escribir los mappers**

```typescript
export function salaDTO(s: any) {
  if (!s) return s;
  return {
    id: s.id, codigo: s.codigo, estado: s.estado,
    creador_id: s.creadorId, invitado_id: s.invitadoId,
    creador_nombre: s.creadorNombre, invitado_nombre: s.invitadoNombre,
    creador_lote: s.creadorLote, invitado_lote: s.invitadoLote,
    creador_pedido: s.creadorPedido, invitado_pedido: s.invitadoPedido,
    creador_ok: s.creadorOk, invitado_ok: s.invitadoOk,
  };
}
export function perfilDTO(p: any) {
  if (!p) return p;
  return {
    user_id: p.userId, handle: p.handle, nombre: p.nombre, avatar: p.avatar,
    codigo_amigo: p.codigoAmigo, publico: p.publico, descripcion: p.descripcion,
  };
}
```

### Task 12b.2: Aplicar `salaDTO` en intercambios

**Files:**
- Modify: `api/src/intercambios/intercambios.service.ts`
- Modify: `api/src/intercambios/intercambios.controller.ts`

- [ ] **Step 1: En el service, importar y envolver los emits realtime**

Agregá el import arriba: `import { salaDTO } from '../common/dto';`
Reemplazá **cada** llamada `this.rt.sala(<id>, <row>)` por `this.rt.sala(<id>, salaDTO(<row>))`. Son 5: en `unirse`, `ponerLote`, `ponerPedido`, `cancelar`, y las dos de `confirmar` (la parcial y la final). El método interno `leer()` sigue devolviendo el row Prisma (camelCase) para la lógica.

- [ ] **Step 2: En el controller, devolver DTO en GET :id**

Reemplazá el handler `leer`:
```typescript
import { salaDTO } from '../common/dto';
// ...
  @Get(':id')
  async leer(@CurrentUser() uid: string, @Param('id') id: string) {
    return salaDTO(await this.svc.leer(uid, id));
  }
```

### Task 12b.3: Aplicar `perfilDTO` en perfiles

**Files:**
- Modify: `api/src/social/perfiles.controller.ts`

- [ ] **Step 1: Envolver `mio`, `guardar` y `porHandle`**

```typescript
import { perfilDTO } from '../common/dto';
// ...
  @Get('perfil/me') async mio(@CurrentUser() uid: string) { return perfilDTO(await this.svc.mio(uid)); }
  @Post('perfil') async guardar(@CurrentUser() uid: string, @Body() b: any) { return perfilDTO(await this.svc.guardar(uid, b)); }
  @Get('perfil/:handle') async porHandle(@Param('handle') h: string) { return perfilDTO(await this.svc.porHandle(h)); }
```

- [ ] **Step 2: Build + re-correr e2e de trades**

Run: `cd api && JWT_SECRET=test-secret DATABASE_URL="postgres://luca:luca@localhost:5433/luca" npm run test:e2e -- trades social`
Expected: PASS (siguen verdes; las aserciones leen Prisma directo, no el DTO).

- [ ] **Step 3: Commit**

```bash
git add api/src
git commit -m "API: DTOs snake_case (salaDTO/perfilDTO) para fidelidad con las paginas"
```

---

## Fase 13 — Cliente: `api.js` + `realtime.js`

### Task 13.1: `web/src/lib/api.js` (fetch + JWT + auth)

**Files:**
- Create: `web/src/lib/api.js`

- [ ] **Step 1: Escribir el cliente**

```javascript
// api.js — cliente HTTP de la API self-hosted + sesión por JWT.
// Reemplaza a supa.js. La URL viene de PUBLIC_API_URL (Astro la expone al navegador).
// Si falta, hayApi=false y la app corre en modo solo-localStorage (igual que antes sin Supabase).
const BASE = (import.meta.env.PUBLIC_API_URL || '').replace(/\/$/, '');
export const hayApi = Boolean(BASE);
export { hayApi as haySupabase };   // alias de compatibilidad

const TOKEN_KEY = 'api:token';
const getToken = () => { try { return localStorage.getItem(TOKEN_KEY) || ''; } catch { return ''; } };
const setToken = (t) => { try { t ? localStorage.setItem(TOKEN_KEY, t) : localStorage.removeItem(TOKEN_KEY); } catch {} };

const b64 = (s) => { try { return JSON.parse(atob(s.replace(/-/g, '+').replace(/_/g, '/'))); } catch { return null; } };
const payload = (t) => (t ? b64(t.split('.')[1] || '') : null);
const vigente = (p) => p && (!p.exp || p.exp * 1000 > Date.now());

export function usuarioActual() {
  const p = payload(getToken());
  return vigente(p) ? { id: p.sub, email: p.email } : null;
}

const listeners = new Set();
const emitir = () => { const u = usuarioActual(); listeners.forEach((fn) => fn(u)); };

export const auth = {
  onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
  loginGoogle() { window.location.href = `${BASE}/auth/google`; },
  logout() { setToken(''); emitir(); },
  token: getToken,
  user: usuarioActual,
};

// Captura el #token=... del callback OAuth y limpia el hash.
(function capturar() {
  if (typeof location === 'undefined' || !location.hash) return;
  const m = new URLSearchParams(location.hash.slice(1));
  const t = m.get('token');
  if (t) { setToken(t); history.replaceState(null, '', location.pathname + location.search); }
})();

async function req(method, path, body) {
  const headers = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(BASE + path, { method, headers, body: body != null ? JSON.stringify(body) : undefined });
  if (!res.ok) {
    let msg = res.statusText;
    try { const j = await res.json(); msg = j.message || msg; } catch {}
    const e = new Error(Array.isArray(msg) ? msg.join(', ') : msg); e.status = res.status; throw e;
  }
  if (res.status === 204) return null;
  const txt = await res.text(); return txt ? JSON.parse(txt) : null;
}
export const apiGet = (p) => req('GET', p);
export const apiPost = (p, b) => req('POST', p, b);
export const apiPut = (p, b) => req('PUT', p, b);
export const apiDelete = (p) => req('DELETE', p);
```

- [ ] **Step 2: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/api.js
git commit -m "web: api.js (fetch+JWT, auth Google emulada, captura #token)"
```

### Task 13.2: `web/src/lib/realtime.js` (socket.io)

**Files:**
- Create: `web/src/lib/realtime.js`
- Modify: `web/package.json` (agrega `socket.io-client`)

- [ ] **Step 1: Instalar el cliente socket.io**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
npm i socket.io-client
```

- [ ] **Step 2: Escribir `realtime.js`**

```javascript
// realtime.js — cliente WebSocket (socket.io) de la API. Topics: `progreso:<uid>` (auto),
// `sala:<id>` y `presencia-global` (join/leave). Eventos del server: 'progreso','sala',
// 'presencia','broadcast'.
import { io } from 'socket.io-client';
import { auth, hayApi } from './api.js';

const BASE = (import.meta.env.PUBLIC_API_URL || '').replace(/\/$/, '');
let socket = null;

export function conectar() {
  if (!hayApi) return null;
  if (socket && socket.connected) return socket;
  if (!socket) {
    socket = io(BASE, { auth: { token: auth.token() }, transports: ['websocket'], autoConnect: true });
  }
  return socket;
}
export function unir(topic) { const s = conectar(); s && s.emit('join', topic); }
export function salir(topic) { socket && socket.emit('leave', topic); }
// registra un handler de un evento del server; devuelve función de baja.
export function on(evento, fn) { const s = conectar(); s && s.on(evento, fn); return () => socket && socket.off(evento, fn); }
export function broadcast(topic, payload) { const s = conectar(); s && s.emit('broadcast', { topic, payload }); }
export function desconectar() { if (socket) { socket.disconnect(); socket = null; } }
```

- [ ] **Step 3: Commit**

```bash
git add web/src/lib/realtime.js web/package.json web/package-lock.json
git commit -m "web: realtime.js (socket.io-client: join/leave/on/broadcast)"
```

---

## Fase 14 — Cliente: reescritura de internals (exports idénticos)

> Regla de oro: **no cambian las firmas exportadas**. Solo cambian los internals (de `supa.*`
> a `api.js`/`realtime.js`). Las páginas (`amigos/intercambio/liga/u/Base`) no se tocan.

### Task 14.1: Reescribir `web/src/lib/nube.js`

**Files:**
- Modify: `web/src/lib/nube.js` (reemplazo completo)

- [ ] **Step 1: Reemplazar el archivo entero**

```javascript
// nube.js — la NUBE (API self-hosted) es la única fuente de verdad. Login obligatorio.
// localStorage es cache descartable; en cada boot la nube manda; escrituras write-through;
// los cambios externos (intercambios) llegan por realtime.
import { hayApi, auth, apiGet, apiPut } from './api.js';
import * as rt from './realtime.js';

const haySupabase = hayApi;            // alias interno
const PREFIJOS = ['ej:', 'col:', 'proy:'];
let _user = null;
let _ultima = (() => { try { return localStorage.getItem('nube:ultima') || ''; } catch { return ''; } })();
let _subiendo = false;
function setUltima(s) { _ultima = s; try { localStorage.setItem('nube:ultima', s); } catch {} }

function snapshot() {
  const o = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (PREFIJOS.some((p) => k.startsWith(p))) o[k] = localStorage.getItem(k);
  }
  return o;
}
function aplicar(o) {
  for (const [k, v] of Object.entries(o)) { if (v === null || v === undefined) continue; localStorage.setItem(k, v); }
}
const serial = (o) => JSON.stringify(Object.keys(o).sort().reduce((a, k) => ((a[k] = o[k]), a), {}));
function limpiarLocal() {
  const claves = [];
  for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (PREFIJOS.some((p) => k.startsWith(p))) claves.push(k); }
  claves.forEach((k) => localStorage.removeItem(k));
}
function aplicarNube(estado) { limpiarLocal(); aplicar(estado); setUltima(serial(snapshot())); }

// ---- I/O contra la API ----
async function bajar() {
  try { const r = await apiGet('/progreso'); return (r && r.estado) || {}; }
  catch (e) { console.warn('[nube] bajar:', e.message); return {}; }
}
async function subir(estado) {
  try { await apiPut('/progreso', { estado }); setUltima(serial(estado)); }
  catch (e) { console.warn('[nube] subir:', e.message); }
}

// ---- boot: la NUBE manda ----
let _booteado = false;
async function boot() {
  if (_booteado || !_user) return;
  _booteado = true;
  const yaHidratado = sessionStorage.getItem('nube:hidratado') === '1';
  const persistida = (() => { try { return localStorage.getItem('nube:ultima') || ''; } catch { return ''; } })();
  const localSerial = serial(snapshot());
  const hayLocal = Object.keys(snapshot()).length > 0;
  const cloud = await bajar();
  const hayCloud = cloud && Object.keys(cloud).length > 0;
  const cloudSerial = hayCloud ? serial(cloud) : '';

  if (!hayCloud) {
    if (hayLocal) await subir(snapshot()); else setUltima(localSerial);
  } else if (hayLocal && localSerial !== persistida && cloudSerial === persistida) {
    await subir(snapshot());
  } else {
    aplicarNube(cloud);
    const cambio = localSerial !== serial(snapshot());
    if (cambio && !yaHidratado) { sessionStorage.setItem('nube:hidratado', '1'); location.reload(); return; }
    if (cambio) window.dispatchEvent(new CustomEvent('nube:sincronizado'));
  }
  sessionStorage.setItem('nube:hidratado', '1');
  window.dispatchEvent(new CustomEvent('nube:listo'));
}

// ---- watcher ----
let _t = null;
function vigilar() {
  setInterval(() => {
    if (!_user) return;
    const s = serial(snapshot());
    if (s !== _ultima && !_subiendo) {
      clearTimeout(_t);
      _t = setTimeout(async () => { _subiendo = true; await subir(snapshot()); _subiendo = false; }, 600);
    }
  }, 2000);
  const flush = () => { if (_user && serial(snapshot()) !== _ultima) subir(snapshot()); };
  window.addEventListener('pagehide', flush);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flush(); });
}

export function usuario() { return _user; }

export async function refrescarDesdeNube() {
  if (!haySupabase || !_user) return false;
  const nube = await bajar();
  if (nube && Object.keys(nube).length) aplicarNube(nube);
  return true;
}

function toast(msg) {
  try {
    const d = document.createElement('div');
    d.textContent = msg;
    d.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);max-width:90%;'
      + 'background:#0c1713;color:#cdebd2;border:1px solid #2b5b41;border-radius:12px;padding:10px 16px;'
      + 'z-index:9999;box-shadow:0 12px 34px rgba(0,0,0,.45);font:600 14px system-ui,sans-serif;text-align:center';
    document.body.appendChild(d);
    setTimeout(() => { d.style.transition = 'opacity .5s'; d.style.opacity = '0'; setTimeout(() => d.remove(), 500); }, 3800);
  } catch {}
}

// cambios EXTERNOS de mi propio progreso (intercambio hecho por el otro)
let _offProg = null;
function suscribirProgreso() {
  if (_offProg) { _offProg(); _offProg = null; }
  _offProg = rt.on('progreso', (estado) => {
    if (!estado) return;
    if (serial(estado) === _ultima) return;        // eco de mi propia subida
    aplicarNube(estado);
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    window.dispatchEvent(new CustomEvent('nube:sincronizado'));
    toast('🔄 Tu colección se actualizó (intercambio)');
  });
}

export async function loginGoogle() { auth.loginGoogle(); return {}; }   // redirige; {} evita romper el destructure

export async function logout() {
  sessionStorage.removeItem('nube:hidratado');
  sessionStorage.removeItem('nube:fusionado');
  _booteado = false;
  auth.logout();
  location.reload();
}

let _inicializado = false;
export function init() {
  if (!haySupabase || _inicializado) return;
  _inicializado = true;
  const aplicarSesion = (user) => {
    _user = user || null;
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    if (_user) { rt.conectar(); suscribirProgreso(); boot(); }
    else {
      sessionStorage.removeItem('nube:hidratado');
      if (_offProg) { _offProg(); _offProg = null; }
      window.dispatchEvent(new CustomEvent('nube:sinsesion'));
    }
  };
  auth.onChange(aplicarSesion);
  aplicarSesion(auth.user());   // estado inicial (api.js ya capturó el #token del OAuth)
  vigilar();
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/nube.js
git commit -m "web: nube.js usa api.js/realtime.js (mismas firmas: init/usuario/loginGoogle/logout/refrescarDesdeNube)"
```

### Task 14.2: Reescribir `web/src/lib/social.js`

**Files:**
- Modify: `web/src/lib/social.js`

- [ ] **Step 1: Reemplazar solo los imports y los cuerpos que usaban `supa` (mantené `snapshotPublico` igual)**

Cabecera nueva (reemplaza la línea de import de supa):
```javascript
// social.js — perfiles públicos, amigos e intercambios asíncronos (sobre la API self-hosted).
import { hayApi, auth, apiGet, apiPost, apiDelete } from './api.js';
import { estado } from './coleccion.js';
import { evaluar, contexto } from './logros.js';
const haySupabase = hayApi;
```

`snapshotPublico(temas)` queda **idéntico** (no usa supa).

Reemplazá de `uid()` para abajo por:
```javascript
const uid = () => (auth.user() ? auth.user().id : null);

// ---- perfil propio ----
export async function miPerfil() { if (!uid()) return null; return apiGet('/perfil/me'); }
export async function guardarPerfil({ handle, nombre, avatar, publico }) {
  return apiPost('/perfil', { handle, nombre: nombre || '', avatar: avatar || 0, publico: publico || {} });
}
export async function actualizarSnapshot(temas) {
  if (!hayApi || !uid()) return;
  const avatar = Number(localStorage.getItem('col:avatar')) || 0;
  try { await apiPost('/perfil/publico', { publico: snapshotPublico(temas), avatar }); } catch {}
}
export async function guardarDescripcion(desc) { await apiPost('/perfil/descripcion', { desc }); }

// ---- perfiles públicos / búsqueda ----
export async function perfilPublico(handle) { return apiGet(`/perfil/${encodeURIComponent(handle)}`); }
export async function buscar(q) { return apiGet(`/perfiles?q=${encodeURIComponent(q || '')}`); }

// ---- amigos ----
export async function solicitar({ handle, codigo }) { await apiPost('/amigos/solicitar', { handle: handle || null, codigo: codigo || null }); }
export async function responder(id, aceptar) { await apiPost(`/amigos/${id}/responder`, { aceptar }); }
export async function quitar(id) { await apiDelete(`/amigos/${id}`); }
export async function amigos() { return apiGet('/amigos'); }
export async function solicitudes() { return apiGet('/amigos/solicitudes'); }
export async function sonAmigos(otroUserId) { const r = await apiGet(`/amigos/son/${otroUserId}`); return !!(r && r.son); }
export async function misRelaciones() {
  try {
    const data = await apiGet('/amigos/relaciones');
    const m = new Map(); (data || []).forEach((r) => m.set(r.handle, r.estado)); return m;
  } catch { return new Map(); }
}

// ---- ofertas ----
export async function crearOferta(aUserId, doy, pido) { const r = await apiPost('/ofertas', { aId: aUserId, doy, pido }); return r && r.id; }
export async function responderOferta(id, aceptar) { const r = await apiPost(`/ofertas/${id}/responder`, { aceptar }); return r && r.estado; }
export async function cancelarOferta(id) { await apiDelete(`/ofertas/${id}`); }
export async function ofertas() { return apiGet('/ofertas'); }
export async function pendientes() { try { const r = await apiGet('/social/pendientes'); return (r && r.n) || 0; } catch { return 0; } }
export async function listarPerfiles(limite, offset) { return apiGet(`/perfiles/listar?limite=${limite}&offset=${offset}`); }

export { haySupabase };
```

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/social.js
git commit -m "web: social.js usa la API (mismas firmas exportadas)"
```

### Task 14.3: Reescribir `web/src/lib/trades.js`

**Files:**
- Modify: `web/src/lib/trades.js` (reemplazo completo)

- [ ] **Step 1: Reemplazar el archivo entero**

```javascript
// trades.js — intercambios en vivo: REST + realtime (sala:<id>) + presencia de sala.
import { hayApi, apiGet, apiPost, apiDelete } from './api.js';
import * as rt from './realtime.js';
const haySupabase = hayApi;
const nombreLocal = () => localStorage.getItem('liga:nombre') || 'Entrenador/a';

export async function crear() { return apiPost('/trades', { nombre: nombreLocal() }); } // {id, codigo}
export async function unirse(codigo) {
  const r = await apiPost('/trades/join', { codigo: codigo.trim().toUpperCase(), nombre: nombreLocal() });
  return r && r.id;
}
export async function ponerLote(id, lote) { await apiPost(`/trades/${id}/lote`, { lote }); }
export async function confirmar(id) { const r = await apiPost(`/trades/${id}/confirm`); return r && r.estado; } // 'abierta'|'completada'
export async function cancelar(id) { await apiDelete(`/trades/${id}`); }
export async function leerSala(id) { return apiGet(`/trades/${id}`); }
export async function coleccionOtro(id) { return apiGet(`/trades/${id}/otro`); } // {atrapados, shiny}
export async function ponerPedido(id, pedido) { await apiPost(`/trades/${id}/pedido`, { pedido }); }

// Suscribe a la sala (cambios de la fila + presencia del otro). Devuelve baja.
export function suscribir(id, miId, { onCambio, onPresencia }) {
  rt.unir(`sala:${id}`);
  const off1 = rt.on('sala', (row) => { if (row && row.id === id && onCambio) onCambio(row); });
  const off2 = rt.on('presencia', (p) => {
    if (p && p.topic === `sala:${id}` && onPresencia) onPresencia((p.ids || []).filter((k) => k !== miId).length > 0);
  });
  return () => { rt.salir(`sala:${id}`); off1(); off2(); };
}

export { haySupabase };
```

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/trades.js
git commit -m "web: trades.js usa la API + realtime (misma firma, incl. suscribir)"
```

### Task 14.4: Reescribir `web/src/lib/presencia.js`

**Files:**
- Modify: `web/src/lib/presencia.js` (reemplazo completo)

- [ ] **Step 1: Reemplazar el archivo entero**

```javascript
// presencia.js — presencia GLOBAL (canal 'presencia-global'): quién está online + recibir
// invitaciones a intercambiar. Se inicia desde Base.astro.
import { hayApi } from './api.js';
import * as rt from './realtime.js';
const haySupabase = hayApi;

let _iniciado = false;
let _presentes = new Set();
let _onInvite = null;
let _miId = null;
const _subs = new Set();

export function iniciarPresencia(userId, handle, onInvitacion) {
  if (!hayApi || !userId || _iniciado) return;
  _iniciado = true; _miId = userId; _onInvite = onInvitacion;
  rt.unir('presencia-global');
  rt.on('presencia', (p) => {
    if (!p || p.topic !== 'presencia-global') return;
    _presentes = new Set(p.ids || []);
    _subs.forEach((fn) => fn(_presentes));
  });
  rt.on('broadcast', (payload) => { if (payload && payload.to === _miId && _onInvite) _onInvite(payload); });
}

export function estaOnline(userId) { return _presentes.has(userId); }
export function presentes() { return _presentes; }

export function onPresencia(fn) { _subs.add(fn); fn(_presentes); return () => _subs.delete(fn); }

export function invitar(toId, codigo, deHandle) {
  rt.broadcast('presencia-global', { to: toId, codigo, de: deHandle });
}

export function detenerPresencia() { rt.salir('presencia-global'); _presentes = new Set(); _iniciado = false; }

export { haySupabase };
```

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/presencia.js
git commit -m "web: presencia.js usa realtime (presence + broadcast invitacion)"
```

### Task 14.5: Reescribir `web/src/lib/desafios.js`

**Files:**
- Modify: `web/src/lib/desafios.js` (reemplazo completo)

- [ ] **Step 1: Reemplazar el archivo entero**

```javascript
// desafios.js — API de los desafíos de la comunidad (sobre la API self-hosted).
import { hayApi, apiGet, apiPost, apiDelete } from './api.js';
const haySupabase = hayApi;
const bump = (k) => { try { localStorage.setItem(k, String((Number(localStorage.getItem(k)) || 0) + 1)); } catch {} };

export async function crearDesafio(d) {
  const r = await apiPost('/desafios', {
    titulo: d.titulo, consigna: d.consigna, func: d.func, starter: d.starter,
    casos: d.casos, dificultad: d.dificultad, region: d.region,
  });
  bump('col:desafios_creados');
  return r && r.id;
}
export async function leerDesafio(id) { return apiGet(`/desafios/${id}`); }
export async function listarDesafios({ orden = 'recientes', q = '', region = 'todas', limite = 30, offset = 0 } = {}) {
  const qs = new URLSearchParams({ orden, q, region, limite: String(limite), offset: String(offset) });
  return apiGet(`/desafios?${qs.toString()}`);
}
export async function registrarResolucion(desafioId, codigo) {
  const r = await apiPost(`/desafios/${desafioId}/resolver`, { codigo });
  const balls = (r && r.balls) || 0;
  if (balls > 0) bump('col:desafios_resueltos');
  return balls;
}
export async function desafiosDeUsuario(userId) { return apiGet(`/usuarios/${userId}/desafios`); }
export async function rankingDesafios() { return apiGet('/desafios/ranking'); }
export async function solucionesDe(desafioId) { return apiGet(`/desafios/${desafioId}/soluciones`); }
export async function votar(resolucionId, on) { await apiPost(`/resoluciones/${resolucionId}/votar`, { on }); }
export async function statsDesafios(userId) { return apiGet(`/usuarios/${userId}/stats`); }
export async function reportarDesafio(desafioId, motivo) { await apiPost(`/desafios/${desafioId}/reportar`, { motivo: motivo || '' }); }
export async function borrarDesafio(desafioId) { await apiDelete(`/desafios/${desafioId}`); }
export { haySupabase };
```

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/desafios.js
git commit -m "web: desafios.js usa la API (mismas firmas)"
```

---

## Fase 15 — Shim de `supa.js`, env, deps, build y verificación

### Task 15.1: Convertir `supa.js` en shim de compatibilidad + env

**Files:**
- Modify: `web/src/lib/supa.js`
- Modify: `web/.env` y `web/.env.example`

- [ ] **Step 1: Reemplazar `web/src/lib/supa.js`**

```javascript
// supa.js — shim de compatibilidad. La app ya no usa Supabase; este archivo solo re-exporta
// `haySupabase` (= hayApi) para no romper imports existentes (ej. Base.astro). `supa` queda null.
export { hayApi as haySupabase } from './api.js';
export const supa = null;
```

- [ ] **Step 2: Setear `PUBLIC_API_URL` en `web/.env`** (crealo si no existe)

```bash
PUBLIC_API_URL=http://localhost:3000
```

- [ ] **Step 3: `web/.env.example`**

```bash
# URL de la API self-hosted (NestJS). Sin esto, la web corre en modo solo-localStorage.
PUBLIC_API_URL=http://localhost:3000
```

- [ ] **Step 4: Quitar la dependencia de Supabase**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
npm uninstall @supabase/supabase-js
```

- [ ] **Step 5: Verificar que no queda ningún uso de `supa.` ni de `@supabase`**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
grep -rn "supa\.\|@supabase\|supabase-js\|PUBLIC_SUPABASE" src && echo "QUEDAN USOS ↑ (revisar)" || echo "limpio"
```
Expected: `limpio`. (Si aparece algo, corregir antes de seguir; `haySupabase` como nombre está OK.)

- [ ] **Step 6: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/supa.js web/.env.example web/package.json web/package-lock.json
git commit -m "web: supa.js shim (haySupabase=hayApi), PUBLIC_API_URL, quita @supabase/supabase-js"
```

### Task 15.2: Build de la web

**Files:**
- (sin cambios; valida que compila)

- [ ] **Step 1: Build**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
npm run build
```
Expected: build OK (genera `../docs`). Sin errores de import (api.js/realtime.js resuelven).

- [ ] **Step 2: Commit del build**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add docs
git commit -m "build: web contra la API self-hosted"
```

### Task 15.3: Verificación end-to-end (2 sesiones, manual)

> Requiere credenciales de Google OAuth apuntando a tu server (Authorized redirect URI =
> `GOOGLE_CALLBACK_URL`). El flujo OAuth real no se automatiza acá.

**Files:** (ninguno)

- [ ] **Step 1: Levantar el stack**

Run:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
docker compose up -d --build
```
Con `web/.env` → `PUBLIC_API_URL=http://localhost:3000`, en otra terminal:
```bash
cd web && npm run dev
```

- [ ] **Step 2: Login + progreso**

- Abrí `http://localhost:4321/`, entrá con Google. Verificá: vuelve con `#token`, el overlay de boot desaparece, el avatar/email aparece en el botón ☁️.
- Resolvé un ejercicio → recargá → el progreso persiste (vino de la API, no del cache).

- [ ] **Step 3: Trade en vivo (2 navegadores/usuarios)**

- Usuario A crea sala (`/intercambio`), B se une con el código. Verificá presencia ("el otro entró"), que cada uno ve la colección del otro, poner lotes, confirmar ambos → la colección se intercambia y a cada uno le llega el toast "🔄 tu colección se actualizó" (realtime `progreso:<uid>`).

- [ ] **Step 4: Oferta async + amigos + desafíos**

- A y B se hacen amigos (`/amigos`), A oferta, B acepta → swap aplicado.
- Crear un desafío, resolverlo con otro usuario → gana balls la primera vez; ver soluciones gateadas.

- [ ] **Step 5: Commit (si hubo ajustes)**

```bash
git add -A && git commit -m "fix: ajustes de verificacion e2e de la migracion"
```

### Task 15.4: Actualizar docs del proyecto

**Files:**
- Modify: `CLAUDE.md`
- Modify: `web/src/pages/ayuda.astro` (si menciona Supabase)

- [ ] **Step 1: Actualizar la sección backend de `CLAUDE.md`**

Reemplazá la sección "Supabase" por una "API self-hosted (NestJS + Prisma + Docker)" que describa: `api/` (módulos auth/progreso/intercambios/social/desafios/realtime), `docker compose up`, `prisma migrate deploy`, env (`DATABASE_URL`, `JWT_SECRET`, `GOOGLE_*`, `FRONTEND_URL`, `CORS_ORIGINS`), y que el cliente usa `api.js`/`realtime.js` (con `supa.js` como shim). Marcá `supabase/` como histórico.

- [ ] **Step 2: Revisar `ayuda.astro`** y cambiar cualquier mención a Supabase/login por la nueva (si aplica).

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md web/src/pages/ayuda.astro
git commit -m "docs: backend self-hosted (Nest+Prisma+Docker) en CLAUDE.md y ayuda"
```

---

## Notas de operación (fuera del código, para el deploy real)

- **TLS / dominio:** poné un reverse proxy (Caddy/nginx) delante de `api:3000`. `GOOGLE_CALLBACK_URL` y `CORS_ORIGINS` deben usar el dominio público (https). `FRONTEND_URL` = la URL de GitHub Pages (`https://<user>.github.io/luca-journey/`).
- **Google OAuth:** en la consola de Google Cloud, Authorized redirect URI = `https://tu-api/auth/google/callback`.
- **Backups:** cron con `pg_dump` del volumen `dbdata` a un disco/Drive externo (el motivo original de migrar).
- **Realtime 1 instancia:** la presence vive en memoria del gateway; no escales `api` a >1 réplica sin mover presence a Redis.

---

## Self-review (cobertura del spec)

- **Auth Google → JWT, captura #token:** Fase 2 (server) + Task 13.1/14.1 (cliente). ✔
- **Progreso GET/PUT + realtime de cambios externos:** Fase 4 + emits en Fases 6/9 + Task 14.1. ✔
- **Intercambios en vivo + swap atómico (Serializable + FOR UPDATE):** Fase 6 + helpers Fase 3. ✔
- **Perfiles (handle inmutable), amigos, ofertas (swap), pendientes:** Fases 7/8/9. ✔
- **Desafíos (moderación ≥3 reportes, spoiler-gate, balls 1ª vez, ranking/stats):** Fase 10. ✔
- **Realtime WS (progreso/sala/presencia/broadcast), presence en memoria:** Fase 5 + clientes 14.3/14.4. ✔
- **DTOs snake_case (fidelidad con páginas):** Fase 12b. ✔
- **Migración por UUID, googleSub por email:** Fase 11 + AuthService. ✔
- **Docker (db+api, migrate deploy):** Fases 0/12. ✔
- **Cliente con exports idénticos, páginas intactas, supa.js shim:** Fases 13/14/15. ✔
- **Frontend en Pages + CORS + PUBLIC_API_URL:** Task 2.1 (CORS) + Task 15.1 (env). ✔

Sin placeholders. Nombres consistentes entre tasks (`salaDTO`, `perfilDTO`, `swapColeccion`, `rt.on/unir/salir/broadcast`, `apiGet/apiPost/apiPut/apiDelete`, `auth.loginGoogle/logout/user/onChange`).

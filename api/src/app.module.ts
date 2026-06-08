import { Module } from '@nestjs/common';
import { APP_GUARD } from '@nestjs/core';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { JwtAuthGuard } from './auth/jwt-auth.guard';
import { ProgresoModule } from './progreso/progreso.module';
import { RealtimeModule } from './realtime/realtime.module';
import { IntercambiosModule } from './intercambios/intercambios.module';
import { SocialModule } from './social/social.module';
import { DesafiosModule } from './desafios/desafios.module';
import { BatallaModule } from './batalla/batalla.module';
import { ErroresModule } from './errores/errores.module';

@Module({
  imports: [
    // rate-limit global por IP: 300 req / 60s (anti-spam/abuso al abrir al público). Generoso a propósito:
    // un grupo detrás de un NAT (varios usuarios, misma IP) entra cómodo; un bot a 5+/s se corta.
    // El ThrottlerGuard global lo aplica a TODAS las rutas HTTP (incluido el login, antes de autenticar).
    ThrottlerModule.forRoot([{ ttl: 60000, limit: 300 }]),
    PrismaModule, AuthModule, ProgresoModule, RealtimeModule, IntercambiosModule, SocialModule, DesafiosModule, BatallaModule, ErroresModule,
  ],
  providers: [
    { provide: APP_GUARD, useClass: ThrottlerGuard },
    { provide: APP_GUARD, useClass: JwtAuthGuard },
  ],
})
export class AppModule {}

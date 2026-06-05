import { Module } from '@nestjs/common';
import { APP_GUARD } from '@nestjs/core';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { JwtAuthGuard } from './auth/jwt-auth.guard';
import { ProgresoModule } from './progreso/progreso.module';
import { RealtimeModule } from './realtime/realtime.module';
import { IntercambiosModule } from './intercambios/intercambios.module';
import { SocialModule } from './social/social.module';
import { DesafiosModule } from './desafios/desafios.module';

@Module({
  imports: [PrismaModule, AuthModule, ProgresoModule, RealtimeModule, IntercambiosModule, SocialModule, DesafiosModule],
  providers: [{ provide: APP_GUARD, useClass: JwtAuthGuard }],
})
export class AppModule {}

import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module';
import { ProgresoModule } from '../progreso/progreso.module';
import { BatallaGateway } from './batalla.gateway';
import { SalasService } from './salas.service';

@Module({
  imports: [PrismaModule, ProgresoModule],
  providers: [BatallaGateway, SalasService],
})
export class BatallaModule {}

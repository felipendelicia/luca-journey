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

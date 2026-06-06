import { Controller, Get } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

// Ranking PvP (ELO). Para la escala actual (pocos usuarios) basta con escanear los blobs de
// progreso y leer col:pvp; a futuro se puede mover a una tabla dedicada.
@Controller()
export class BatallaController {
  constructor(private prisma: PrismaService) {}

  @Get('pvp/ranking')
  async ranking() {
    const progs = await this.prisma.progreso.findMany();
    const filas: { userId: string; rating: number; victorias: number; jugados: number; racha: number }[] = [];
    for (const p of progs) {
      let pvp: any = {};
      try { pvp = JSON.parse(((p.estado as any) || {})['col:pvp'] || '{}'); } catch { pvp = {}; }
      if (pvp && pvp.jugados) {
        filas.push({ userId: p.userId, rating: Number(pvp.rating) || 1000, victorias: pvp.victorias || 0, jugados: pvp.jugados || 0, racha: pvp.racha || 0 });
      }
    }
    filas.sort((a, b) => b.rating - a.rating || b.victorias - a.victorias);
    const top = filas.slice(0, 20);
    const perfiles = await this.prisma.perfil.findMany({ where: { userId: { in: top.map((f) => f.userId) } } });
    const m = new Map(perfiles.map((pf) => [pf.userId, pf]));
    return top.map((f, i) => ({
      pos: i + 1, rating: f.rating, victorias: f.victorias, jugados: f.jugados, racha: f.racha,
      handle: m.get(f.userId)?.handle || '', nombre: m.get(f.userId)?.nombre || '',
    }));
  }
}

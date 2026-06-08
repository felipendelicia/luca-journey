import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

// Acciones de moderación. Todas pasan por AdminGuard en el controller.
@Injectable()
export class AdminService {
  constructor(private prisma: PrismaService) {}

  async perfiles(limite = 60) {
    const rows = await this.prisma.perfil.findMany({
      orderBy: { actualizado: 'desc' }, take: limite,
      select: { userId: true, handle: true, nombre: true, descripcion: true },
    });
    // marcar baneados
    const users = await this.prisma.user.findMany({ where: { id: { in: rows.map((r) => r.userId) } }, select: { id: true, baneado: true } });
    const ban = new Map(users.map((u) => [u.id, u.baneado]));
    return rows.map((r) => ({ ...r, baneado: !!ban.get(r.userId) }));
  }

  async borrarPerfil(userId: string) {
    await this.prisma.perfil.deleteMany({ where: { userId } });
    return { ok: true };
  }

  async ban(userId: string, baneado: boolean) {
    await this.prisma.user.update({ where: { id: userId }, data: { baneado } as any });
    if (baneado) await this.prisma.perfil.deleteMany({ where: { userId } });   // banear también lo saca de lo público
    return { ok: true };
  }

  async desafios(limite = 60) {
    const rows = await this.prisma.desafio.findMany({
      orderBy: { creado: 'desc' }, take: limite,
      select: { id: true, autor: true, titulo: true, consigna: true, creado: true },
    });
    const perfiles = await this.prisma.perfil.findMany({ where: { userId: { in: rows.map((r) => r.autor) } }, select: { userId: true, handle: true } });
    const h = new Map(perfiles.map((p) => [p.userId, p.handle]));
    return rows.map((r) => ({ ...r, autor_handle: h.get(r.autor) || '' }));
  }

  async borrarDesafio(id: string) {
    await this.prisma.desafio.delete({ where: { id } }).catch(() => {});
    return { ok: true };
  }
}

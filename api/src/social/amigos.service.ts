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
    if (ya) return;
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

  async misRelaciones(uid: string) {
    const a = await this.prisma.amistad.findMany({ where: { OR: [{ deId: uid }, { aId: uid }] } });
    const otros = a.map((r) => ({ estado: r.estado, otro: r.deId === uid ? r.aId : r.deId }));
    const perfiles = await this.prisma.perfil.findMany({ where: { userId: { in: otros.map((o) => o.otro) } } });
    const m = new Map(perfiles.map((p) => [p.userId, p.handle]));
    return otros.filter((o) => m.has(o.otro)).map((o) => ({ handle: m.get(o.otro), estado: o.estado }));
  }
}

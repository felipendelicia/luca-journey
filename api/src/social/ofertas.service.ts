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

  async pendientes(uid: string) {
    const [am, of] = await this.prisma.$transaction([
      this.prisma.amistad.count({ where: { estado: 'pendiente', aId: uid } }),
      this.prisma.oferta.count({ where: { estado: 'pendiente', aId: uid } }),
    ]);
    return am + of;
  }
}

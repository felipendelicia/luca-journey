import { ForbiddenException, Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { RealtimeService } from '../realtime/realtime.service';
import { swapColeccion, Item } from '../coleccion/coleccion';
import { salaDTO } from '../common/dto';

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
    this.rt.sala(s.id, salaDTO(await this.leer(uid, s.id)));
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
    this.rt.sala(id, salaDTO(await this.prisma.intercambio.findUnique({ where: { id } })));
  }

  async ponerPedido(uid: string, id: string, pedido: Item[]) {
    const s = await this.leer(uid, id);
    if (s.estado !== 'abierta') throw new BadRequestException('la sala no está abierta');
    const data = uid === s.creadorId ? { creadorPedido: pedido as any } : { invitadoPedido: pedido as any };
    await this.prisma.intercambio.update({ where: { id }, data });
    this.rt.sala(id, salaDTO(await this.prisma.intercambio.findUnique({ where: { id } })));
  }

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
      this.rt.sala(id, salaDTO(await this.prisma.intercambio.findUnique({ where: { id } })));
    }
  }

  async confirmar(uid: string, id: string): Promise<'abierta' | 'completada'> {
    const s0 = await this.leer(uid, id);
    if (s0.estado !== 'abierta') throw new BadRequestException('la sala no está abierta');
    await this.prisma.intercambio.update({
      where: { id },
      data: uid === s0.creadorId ? { creadorOk: true } : { invitadoOk: true },
    });
    const s = await this.prisma.intercambio.findUnique({ where: { id } });
    if (!(s!.creadorOk && s!.invitadoOk)) {
      this.rt.sala(id, salaDTO(s));
      return 'abierta';
    }
    await this.ejecutar(s!);
    this.rt.sala(id, salaDTO(await this.prisma.intercambio.findUnique({ where: { id } })));
    return 'completada';
  }

  private async ejecutar(s: any) {
    const [ca, ia] = await this.prisma.$transaction(async (tx) => {
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
    this.rt.progreso(s.creadorId, ca);
    this.rt.progreso(s.invitadoId, ia);
  }
}

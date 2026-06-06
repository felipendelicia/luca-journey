import { BadRequestException, ForbiddenException, Injectable, UnauthorizedException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AmigosService } from './amigos.service';

const ALF = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const code6 = () => Array.from({ length: 6 }, () => ALF[Math.floor(Math.random() * ALF.length)]).join('');
const HANDLE_RE = /^[a-z0-9_]{3,20}$/;

@Injectable()
export class PerfilesService {
  constructor(private prisma: PrismaService, private amigos: AmigosService) {}

  // instancias del PC de un usuario EN VIVO (para ofertas async por instancia). Solo entre amigos.
  async pcDeUsuario(uid: string, otroId: string) {
    if (uid !== otroId && !(await this.amigos.sonAmigos(uid, otroId))) throw new ForbiddenException('solo entre amigos');
    const p = await this.prisma.progreso.findUnique({ where: { userId: otroId } });
    let pc: any[] = []; try { pc = JSON.parse(((p?.estado as any) || {})['col:pc'] || '[]'); } catch {}
    return { pc: pc.map((m) => ({ iid: m.iid, id: m.id, nivel: m.nivel, shiny: !!m.shiny, mote: m.mote || '' })) };
  }

  async mio(uid: string) {
    return this.prisma.perfil.findUnique({ where: { userId: uid } });
  }

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
    if (!existe) return;
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
    return this.prisma.perfil.findMany({
      where: { OR: [{ handle: { contains: t, mode: 'insensitive' } }, { nombre: { contains: t, mode: 'insensitive' } }] },
      orderBy: { handle: 'asc' }, take: 20,
      select: { handle: true, nombre: true, avatar: true },
    });
  }

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

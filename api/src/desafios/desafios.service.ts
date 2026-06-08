import { BadRequestException, ForbiddenException, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { contieneGroseria } from '../common/groserias';

const REGIONES = ['kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos', 'libre'];

@Injectable()
export class DesafiosService {
  constructor(private prisma: PrismaService) {}

  async crear(uid: string, d: any) {
    if (!String(d.titulo || '').trim()) throw new BadRequestException('falta el título');
    if (!String(d.func || '').trim()) throw new BadRequestException('falta el nombre de la función');
    if (!Array.isArray(d.casos) || d.casos.length === 0) throw new BadRequestException('faltan casos');
    if (contieneGroseria(d.titulo) || contieneGroseria(d.consigna)) throw new BadRequestException('el título/consigna tiene lenguaje no permitido');
    const row = await this.prisma.desafio.create({
      data: {
        autor: uid, titulo: d.titulo.trim(), consigna: d.consigna || '', func: d.func.trim(),
        starter: d.starter || '', casos: d.casos, dificultad: Math.max(1, Math.min(8, d.dificultad || 3)),
        region: REGIONES.includes(d.region) ? d.region : 'libre',
      },
    });
    return row.id;
  }

  async leer(id: string) {
    const d = await this.prisma.desafio.findUnique({ where: { id } });
    if (!d) throw new NotFoundException('no existe');
    return d;
  }

  async listar(uid: string, q: any) {
    const { orden = 'recientes', q: texto = '', region = 'todas', limite = 30, offset = 0 } = q;
    const desafios = await this.prisma.desafio.findMany();
    const conteoRes = new Map<string, number>();
    const conteoRep = new Map<string, number>();
    const resueltosMios = new Set<string>();
    for (const r of await this.prisma.resolucion.findMany()) {
      conteoRes.set(r.desafioId, (conteoRes.get(r.desafioId) || 0) + 1);
      if (r.userId === uid) resueltosMios.add(r.desafioId);
    }
    for (const r of await this.prisma.reporte.findMany())
      conteoRep.set(r.desafioId, (conteoRep.get(r.desafioId) || 0) + 1);
    const autores = await this.prisma.perfil.findMany();
    const handle = new Map(autores.map((p) => [p.userId, p.handle]));
    const t = String(texto).trim().toLowerCase();
    let rows = desafios.filter((d) => {
      if (region && region !== '' && region !== 'todas' && d.region !== region) return false;
      if (t && !(d.titulo.toLowerCase().includes(t) || d.consigna.toLowerCase().includes(t))) return false;
      if (d.autor !== uid && (conteoRep.get(d.id) || 0) >= 3) return false;
      return true;
    }).map((d) => ({
      id: d.id, titulo: d.titulo, consigna: d.consigna, dificultad: d.dificultad, region: d.region,
      autor_handle: handle.get(d.autor) || null, resoluciones: conteoRes.get(d.id) || 0,
      resuelto: resueltosMios.has(d.id), _creado: d.creado,
    }));
    if (orden === 'resueltos') rows.sort((a, b) => b.resoluciones - a.resoluciones || +b._creado - +a._creado);
    else if (orden === 'dificultad') rows.sort((a, b) => b.dificultad - a.dificultad || +b._creado - +a._creado);
    else rows.sort((a, b) => +b._creado - +a._creado);
    const lim = Math.max(1, Math.min(limite || 30, 60));
    return rows.slice(Math.max(0, offset || 0), Math.max(0, offset || 0) + lim).map(({ _creado, ...r }) => r);
  }

  async registrarResolucion(uid: string, desafioId: string, codigo: string): Promise<number> {
    const ya = await this.prisma.resolucion.findUnique({ where: { desafioId_userId: { desafioId, userId: uid } } });
    await this.prisma.resolucion.upsert({
      where: { desafioId_userId: { desafioId, userId: uid } },
      create: { desafioId, userId: uid, codigo: codigo || '' },
      update: { codigo: codigo || '', creado: new Date() },
    });
    if (ya) return 0;
    const d = await this.prisma.desafio.findUnique({ where: { id: desafioId } });
    const premio = 2 * (d?.dificultad || 3);
    const p = await this.prisma.progreso.findUnique({ where: { userId: uid } });
    const est = ((p?.estado as any) || {}) as Record<string, any>;
    // col:balls se guarda como STRING plana (espeja localStorage), no JSON-quoted.
    const balls = Number(est['col:balls'] || 0) + premio;
    est['col:balls'] = String(balls);
    await this.prisma.progreso.upsert({ where: { userId: uid }, create: { userId: uid, estado: est }, update: { estado: est } });
    return premio;
  }

  async solucionesDe(uid: string, desafioId: string) {
    const yo = await this.prisma.resolucion.findUnique({ where: { desafioId_userId: { desafioId, userId: uid } } });
    const d = await this.prisma.desafio.findUnique({ where: { id: desafioId } });
    if (!yo && d?.autor !== uid) return [];
    const res = await this.prisma.resolucion.findMany({ where: { desafioId } });
    const handle = new Map((await this.prisma.perfil.findMany({ where: { userId: { in: res.map((r) => r.userId) } } })).map((p) => [p.userId, p.handle]));
    const out = [];
    for (const r of res) {
      const votos = await this.prisma.voto.count({ where: { resolucionId: r.id } });
      const miVoto = !!(await this.prisma.voto.findUnique({ where: { resolucionId_userId: { resolucionId: r.id, userId: uid } } }));
      out.push({ id: r.id, codigo: r.codigo, autor_handle: handle.get(r.userId) || null, votos, mi_voto: miVoto, es_mia: r.userId === uid, _creado: r.creado });
    }
    out.sort((a, b) => b.votos - a.votos || +a._creado - +b._creado);
    return out.map(({ _creado, ...r }) => r);
  }

  async votar(uid: string, resolucionId: string, on: boolean) {
    if (on) await this.prisma.voto.upsert({ where: { resolucionId_userId: { resolucionId, userId: uid } }, create: { resolucionId, userId: uid }, update: {} });
    else await this.prisma.voto.deleteMany({ where: { resolucionId, userId: uid } });
  }

  async deUsuario(userId: string) {
    const creados = await this.prisma.desafio.findMany({ where: { autor: userId } });
    const resol = await this.prisma.resolucion.findMany({ where: { userId } });
    const dres = await this.prisma.desafio.findMany({ where: { id: { in: resol.map((r) => r.desafioId) } } });
    const rows = [
      ...creados.map((d) => ({ id: d.id, titulo: d.titulo, region: d.region, dificultad: d.dificultad, rol: 'creado' })),
      ...dres.map((d) => ({ id: d.id, titulo: d.titulo, region: d.region, dificultad: d.dificultad, rol: 'resuelto' })),
    ];
    rows.sort((a, b) => b.rol.localeCompare(a.rol) || a.titulo.localeCompare(b.titulo));
    return rows;
  }

  async ranking() {
    const perfiles = await this.prisma.perfil.findMany();
    const out = [];
    for (const p of perfiles) {
      const creados = await this.prisma.desafio.count({ where: { autor: p.userId } });
      const resueltos = await this.prisma.resolucion.count({ where: { userId: p.userId } });
      if (creados || resueltos) out.push({ handle: p.handle, avatar: p.avatar, creados, resueltos });
    }
    out.sort((a, b) => b.creados - a.creados || b.resueltos - a.resueltos);
    return out.slice(0, 20);
  }

  async stats(userId: string) {
    const [resueltos, creados] = await this.prisma.$transaction([
      this.prisma.resolucion.count({ where: { userId } }),
      this.prisma.desafio.count({ where: { autor: userId } }),
    ]);
    return { resueltos, creados };
  }

  async reportar(uid: string, desafioId: string, motivo: string) {
    await this.prisma.reporte.upsert({
      where: { desafioId_userId: { desafioId, userId: uid } },
      create: { desafioId, userId: uid, motivo: (motivo || '').slice(0, 200) },
      update: { motivo: (motivo || '').slice(0, 200), creado: new Date() },
    });
  }

  async borrar(uid: string, desafioId: string) {
    const d = await this.prisma.desafio.findUnique({ where: { id: desafioId } });
    if (!d) throw new NotFoundException('no existe');
    if (d.autor !== uid) throw new ForbiddenException('solo el autor puede borrarlo');
    await this.prisma.$transaction([
      this.prisma.voto.deleteMany({ where: { resolucionId: { in: (await this.prisma.resolucion.findMany({ where: { desafioId } })).map((r) => r.id) } } }),
      this.prisma.resolucion.deleteMany({ where: { desafioId } }),
      this.prisma.reporte.deleteMany({ where: { desafioId } }),
      this.prisma.desafio.delete({ where: { id: desafioId } }),
    ]);
  }
}

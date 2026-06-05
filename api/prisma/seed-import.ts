import 'dotenv/config';
import { PrismaClient } from '@prisma/client';
import { PrismaPg } from '@prisma/adapter-pg';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const prisma = new PrismaClient({ adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL }) });
const DIR = join(__dirname, 'dump');

function leerCsv(nombre: string): Record<string, string>[] {
  const path = join(DIR, nombre);
  if (!existsSync(path)) { console.log(`(skip) ${nombre} no existe`); return []; }
  const txt = readFileSync(path, 'utf8').trim();
  if (!txt) return [];
  const lineas = txt.split('\n');
  const cols = parseLinea(lineas[0]);
  return lineas.slice(1).map((l) => Object.fromEntries(parseLinea(l).map((v, i) => [cols[i], v])));
}
function parseLinea(l: string): string[] {
  const out: string[] = []; let cur = ''; let q = false;
  for (let i = 0; i < l.length; i++) {
    const c = l[i];
    if (q) { if (c === '"' && l[i + 1] === '"') { cur += '"'; i++; } else if (c === '"') q = false; else cur += c; }
    else { if (c === '"') q = true; else if (c === ',') { out.push(cur); cur = ''; } else cur += c; }
  }
  out.push(cur); return out;
}
const J = (s: string, def: any) => { try { return s ? JSON.parse(s) : def; } catch { return def; } };
const D = (s: string) => (s ? new Date(s) : undefined);

async function main() {
  for (const u of leerCsv('users.csv'))
    await prisma.user.upsert({ where: { id: u.id }, create: { id: u.id, email: u.email }, update: { email: u.email } });

  for (const r of leerCsv('progreso.csv'))
    await prisma.progreso.upsert({ where: { userId: r.user_id }, create: { userId: r.user_id, estado: J(r.estado, {}) }, update: { estado: J(r.estado, {}) } });

  for (const r of leerCsv('perfiles.csv'))
    await prisma.perfil.upsert({ where: { userId: r.user_id }, create: {
      userId: r.user_id, handle: r.handle, nombre: r.nombre || '', avatar: Number(r.avatar) || 0,
      codigoAmigo: r.codigo_amigo, publico: J(r.publico, {}), descripcion: r.descripcion || '',
    }, update: {} });

  for (const r of leerCsv('amistades.csv'))
    await prisma.amistad.upsert({ where: { id: r.id }, create: { id: r.id, deId: r.de_id, aId: r.a_id, estado: r.estado, creado: D(r.creado) }, update: {} });

  for (const r of leerCsv('ofertas.csv'))
    await prisma.oferta.upsert({ where: { id: r.id }, create: {
      id: r.id, deId: r.de_id, aId: r.a_id, doy: J(r.doy, []), pido: J(r.pido, []), estado: r.estado, creado: D(r.creado), resuelto: D(r.resuelto),
    }, update: {} });

  for (const r of leerCsv('intercambios.csv'))
    await prisma.intercambio.upsert({ where: { id: r.id }, create: {
      id: r.id, codigo: r.codigo, creadorId: r.creador_id, invitadoId: r.invitado_id || null,
      creadorNombre: r.creador_nombre || '', invitadoNombre: r.invitado_nombre || '',
      creadorLote: J(r.creador_lote, []), invitadoLote: J(r.invitado_lote, []),
      creadorPedido: J(r.creador_pedido, []), invitadoPedido: J(r.invitado_pedido, []),
      creadorOk: r.creador_ok === 't' || r.creador_ok === 'true', invitadoOk: r.invitado_ok === 't' || r.invitado_ok === 'true',
      estado: r.estado, creado: D(r.creado),
    }, update: {} });

  for (const r of leerCsv('desafios.csv'))
    await prisma.desafio.upsert({ where: { id: r.id }, create: {
      id: r.id, autor: r.autor, titulo: r.titulo, consigna: r.consigna || '', func: r.func, starter: r.starter || '',
      casos: J(r.casos, []), dificultad: Number(r.dificultad) || 3, region: r.region || 'libre', creado: D(r.creado),
    }, update: {} });

  for (const r of leerCsv('resoluciones.csv'))
    await prisma.resolucion.upsert({ where: { id: r.id }, create: { id: r.id, desafioId: r.desafio_id, userId: r.user_id, codigo: r.codigo || '', creado: D(r.creado) }, update: {} });

  for (const r of leerCsv('votos.csv'))
    await prisma.voto.upsert({ where: { resolucionId_userId: { resolucionId: r.resolucion_id, userId: r.user_id } }, create: { resolucionId: r.resolucion_id, userId: r.user_id }, update: {} });

  for (const r of leerCsv('reportes.csv'))
    await prisma.reporte.upsert({ where: { desafioId_userId: { desafioId: r.desafio_id, userId: r.user_id } }, create: { desafioId: r.desafio_id, userId: r.user_id, motivo: r.motivo || '', creado: D(r.creado) }, update: {} });

  console.log('import OK');
}
main().finally(() => prisma.$disconnect());

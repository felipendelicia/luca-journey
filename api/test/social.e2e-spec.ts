import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('social', () => {
  let app: INestApplication; let prisma: PrismaService; let http: any;
  const A = 'u-sa', B = 'u-sb';
  const blob = (atra: any) => ({ 'col:atrapados': JSON.stringify(atra), 'col:shiny': '[]' });
  beforeAll(async () => {
    app = await crearApp(); http = app.getHttpServer(); prisma = app.get(PrismaService);
    for (const [id, email, handle] of [[A, 'sa@test', 'usera'], [B, 'sb@test', 'userb']] as const) {
      await prisma.user.upsert({ where: { email }, create: { id, email }, update: {} });
      await prisma.perfil.upsert({ where: { userId: id }, create: { userId: id, handle, codigoAmigo: handle.toUpperCase().slice(0, 6) }, update: {} });
    }
  });
  beforeEach(async () => {
    await prisma.oferta.deleteMany({}); await prisma.amistad.deleteMany({});
    await prisma.progreso.upsert({ where: { userId: A }, create: { userId: A, estado: blob({ '25': 1 }) }, update: { estado: blob({ '25': 1 }) } });
    await prisma.progreso.upsert({ where: { userId: B }, create: { userId: B, estado: blob({ '7': 1 }) }, update: { estado: blob({ '7': 1 }) } });
  });
  afterAll(async () => { await app.close(); });

  it('amistad + oferta aceptada ejecuta swap', async () => {
    const tA = tokenDe(A, 'sa@test'), tB = tokenDe(B, 'sb@test');
    await request(http).post('/amigos/solicitar').set('Authorization', `Bearer ${tA}`).send({ handle: 'userb' }).expect(201);
    const sol = await request(http).get('/amigos/solicitudes').set('Authorization', `Bearer ${tB}`).expect(200);
    await request(http).post(`/amigos/${sol.body[0].id}/responder`).set('Authorization', `Bearer ${tB}`).send({ aceptar: true }).expect(201);
    const of = await request(http).post('/ofertas').set('Authorization', `Bearer ${tA}`).send({ aId: B, doy: [{ id: 25 }], pido: [{ id: 7 }] }).expect(201);
    const r = await request(http).post(`/ofertas/${of.body.id}/responder`).set('Authorization', `Bearer ${tB}`).send({ aceptar: true }).expect(201);
    expect(r.body.estado).toBe('aceptada');
    const pa = await prisma.progreso.findUnique({ where: { userId: A } });
    expect(JSON.parse((pa!.estado as any)['col:atrapados'])).toEqual({ '7': 1 });
  });
});

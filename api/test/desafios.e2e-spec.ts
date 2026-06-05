import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('desafios', () => {
  let app: INestApplication; let prisma: PrismaService; let http: any;
  const A = 'u-da', B = 'u-db';
  beforeAll(async () => {
    app = await crearApp(); http = app.getHttpServer(); prisma = app.get(PrismaService);
    for (const [id, email] of [[A, 'da@test'], [B, 'db@test']] as const)
      await prisma.user.upsert({ where: { email }, create: { id, email }, update: {} });
  });
  beforeEach(async () => {
    await prisma.voto.deleteMany({}); await prisma.resolucion.deleteMany({}); await prisma.desafio.deleteMany({});
    await prisma.progreso.upsert({ where: { userId: B }, create: { userId: B, estado: { 'col:balls': '0' } }, update: { estado: { 'col:balls': '0' } } });
  });
  afterAll(async () => { await app.close(); });

  it('soluciones gated + balls solo la primera vez', async () => {
    const tA = tokenDe(A, 'da@test'), tB = tokenDe(B, 'db@test');
    const d = await request(http).post('/desafios').set('Authorization', `Bearer ${tA}`)
      .send({ titulo: 'Suma', func: 'suma', casos: [{ args: [1, 2], esperado: '3' }], dificultad: 3 }).expect(201);
    const id = d.body.id;
    const g = await request(http).get(`/desafios/${id}/soluciones`).set('Authorization', `Bearer ${tB}`).expect(200);
    expect(g.body.length).toBe(0);
    const r1 = await request(http).post(`/desafios/${id}/resolver`).set('Authorization', `Bearer ${tB}`).send({ codigo: 'x' }).expect(201);
    expect(r1.body.balls).toBe(6);
    const r2 = await request(http).post(`/desafios/${id}/resolver`).set('Authorization', `Bearer ${tB}`).send({ codigo: 'y' }).expect(201);
    expect(r2.body.balls).toBe(0);
    const g2 = await request(http).get(`/desafios/${id}/soluciones`).set('Authorization', `Bearer ${tB}`).expect(200);
    expect(g2.body.length).toBe(1);
  });
});

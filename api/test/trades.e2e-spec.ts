import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('trades', () => {
  let app: INestApplication; let prisma: PrismaService; let http: any;
  const A = 'u-a', B = 'u-b';
  const tA = () => tokenDe(A, 'a@test'), tB = () => tokenDe(B, 'b@test');
  const blob = (atra: any, shiny: number[] = []) => ({ 'col:atrapados': JSON.stringify(atra), 'col:shiny': JSON.stringify(shiny) });

  beforeAll(async () => {
    app = await crearApp(); http = app.getHttpServer(); prisma = app.get(PrismaService);
    for (const [id, email] of [[A, 'a@test'], [B, 'b@test']] as const)
      await prisma.user.upsert({ where: { email }, create: { id, email }, update: {} });
  });
  beforeEach(async () => {
    await prisma.intercambio.deleteMany({});
    await prisma.progreso.upsert({ where: { userId: A }, create: { userId: A, estado: blob({ '25': 2 }) }, update: { estado: blob({ '25': 2 }) } });
    await prisma.progreso.upsert({ where: { userId: B }, create: { userId: B, estado: blob({ '7': 2 }) }, update: { estado: blob({ '7': 2 }) } });
  });
  afterAll(async () => { await prisma.intercambio.deleteMany({}); await prisma.progreso.deleteMany({ where: { userId: { in: [A, B] } } }); await app.close(); });

  it('crear→unirse→lotes→confirmar x2 ejecuta el swap', async () => {
    const c = await request(http).post('/trades').set('Authorization', `Bearer ${tA()}`).send({ nombre: 'A' }).expect(201);
    const id = c.body.id;
    await request(http).post('/trades/join').set('Authorization', `Bearer ${tB()}`).send({ codigo: c.body.codigo, nombre: 'B' }).expect(201);
    await request(http).post(`/trades/${id}/lote`).set('Authorization', `Bearer ${tA()}`).send({ lote: [{ id: 25 }] }).expect(201);
    await request(http).post(`/trades/${id}/lote`).set('Authorization', `Bearer ${tB()}`).send({ lote: [{ id: 7 }] }).expect(201);
    await request(http).post(`/trades/${id}/confirm`).set('Authorization', `Bearer ${tA()}`).expect(201);
    const fin = await request(http).post(`/trades/${id}/confirm`).set('Authorization', `Bearer ${tB()}`).expect(201);
    expect(fin.body.estado).toBe('completada');
    const pa = await prisma.progreso.findUnique({ where: { userId: A } });
    const pb = await prisma.progreso.findUnique({ where: { userId: B } });
    expect(JSON.parse((pa!.estado as any)['col:atrapados'])).toEqual({ '25': 1, '7': 1 });
    expect(JSON.parse((pb!.estado as any)['col:atrapados'])).toEqual({ '7': 1, '25': 1 });
  });
});

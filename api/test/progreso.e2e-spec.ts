import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';
import { PrismaService } from '../src/prisma/prisma.service';

describe('progreso', () => {
  let app: INestApplication; let prisma: PrismaService;
  beforeAll(async () => {
    app = await crearApp();
    prisma = app.get(PrismaService);
    await prisma.user.upsert({ where: { email: 'p@test' }, create: { id: 'u-prog', email: 'p@test' }, update: {} });
  });
  afterAll(async () => { await prisma.progreso.deleteMany({ where: { userId: 'u-prog' } }); await app.close(); });

  it('PUT luego GET devuelve el estado', async () => {
    const t = tokenDe('u-prog', 'p@test');
    await request(app.getHttpServer()).put('/progreso').set('Authorization', `Bearer ${t}`)
      .send({ estado: { 'col:balls': '5' } }).expect(200);
    const r = await request(app.getHttpServer()).get('/progreso').set('Authorization', `Bearer ${t}`).expect(200);
    expect(r.body.estado['col:balls']).toBe('5');
  });
});

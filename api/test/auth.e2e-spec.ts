import * as request from 'supertest';
import { INestApplication } from '@nestjs/common';
import { crearApp, tokenDe } from './util';

describe('auth', () => {
  let app: INestApplication;
  beforeAll(async () => { app = await crearApp(); });
  afterAll(async () => { await app.close(); });

  it('/auth/me sin token -> 401', async () => {
    await request(app.getHttpServer()).get('/auth/me').expect(401);
  });

  it('/auth/me con token -> userId', async () => {
    const t = tokenDe('user-1', 'a@test');
    const r = await request(app.getHttpServer()).get('/auth/me').set('Authorization', `Bearer ${t}`).expect(200);
    expect(r.body.id).toBe('user-1');
    expect(r.body.email).toBe('a@test');
  });
});

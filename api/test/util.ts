import { Test } from '@nestjs/testing';
import { JwtService } from '@nestjs/jwt';
import { INestApplication } from '@nestjs/common';
import { AppModule } from '../src/app.module';

export async function crearApp(): Promise<INestApplication> {
  // GoogleStrategy constructor requires a non-empty clientID; provide stubs for tests
  process.env.GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || 'test-client-id';
  process.env.GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || 'test-client-secret';
  process.env.GOOGLE_CALLBACK_URL = process.env.GOOGLE_CALLBACK_URL || 'http://localhost/auth/google/callback';

  const mod = await Test.createTestingModule({ imports: [AppModule] }).compile();
  const app = mod.createNestApplication();
  await app.init();
  return app;
}

export function tokenDe(userId: string, email = 'x@test'): string {
  const jwt = new JwtService({});
  return jwt.sign({ sub: userId, email }, { secret: process.env.JWT_SECRET || 'dev-secret', expiresIn: '1h' });
}

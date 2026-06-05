import 'dotenv/config';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  // Fail-fast: sin JWT_SECRET, las strategies caerían a un secreto público conocido
  // ('dev-secret') y cualquiera podría forjar un JWT e impersonar a otro usuario.
  if (!process.env.JWT_SECRET) {
    throw new Error('Falta JWT_SECRET (requerido para firmar/verificar tokens).');
  }
  const app = await NestFactory.create(AppModule);
  const origins = (process.env.CORS_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  app.enableCors({ origin: origins.length ? origins : true, credentials: true });
  await app.listen(Number(process.env.PORT) || 3000);
}
bootstrap();

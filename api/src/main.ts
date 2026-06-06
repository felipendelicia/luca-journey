import 'dotenv/config';
import { readFileSync, existsSync } from 'fs';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  // Fail-fast: sin JWT_SECRET, las strategies caerían a un secreto público conocido
  // ('dev-secret') y cualquiera podría forjar un JWT e impersonar a otro usuario.
  if (!process.env.JWT_SECRET) {
    throw new Error('Falta JWT_SECRET (requerido para firmar/verificar tokens).');
  }
  // TLS app-level: en deploy sin reverse proxy, si hay cert+key la API sirve HTTPS
  // directo (ej. en 443). En dev, sin TLS_CERT/TLS_KEY, sigue en HTTP.
  const cert = process.env.TLS_CERT;
  const key = process.env.TLS_KEY;
  const httpsOptions =
    cert && key && existsSync(cert) && existsSync(key)
      ? { cert: readFileSync(cert), key: readFileSync(key) }
      : undefined;
  const app = await NestFactory.create(AppModule, httpsOptions ? { httpsOptions } : {});
  const origins = (process.env.CORS_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  app.enableCors({ origin: origins.length ? origins : true, credentials: true });
  await app.listen(Number(process.env.PORT) || 3000);
}
bootstrap();

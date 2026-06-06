import { Body, Controller, Get, Logger, Post } from '@nestjs/common';
import { Public } from '../auth/public.decorator';

// Reportes de errores del cliente (JS roto en el navegador del alumno). Sin DB: se loguean
// (visibles con `docker compose logs api`) y se guardan los últimos 100 en memoria para revisar
// vía GET /errores (con sesión). Liviano y a prueba de spam (el cliente limita y deduplica).
const BUFFER: any[] = [];
const MAX = 100;
const corto = (v: any, n: number) => String(v ?? '').slice(0, n);

@Controller('errores')
export class ErroresController {
  private readonly log = new Logger('Cliente');

  @Public()
  @Post()
  registrar(@Body() b: any) {
    const e = {
      t: Date.now(),
      tipo: corto(b?.tipo || 'error', 20),
      mensaje: corto(b?.mensaje, 500),
      stack: corto(b?.stack, 2000),
      url: corto(b?.url, 300),
      ua: corto(b?.ua, 200),
      handle: corto(b?.handle, 30),
    };
    BUFFER.unshift(e);
    if (BUFFER.length > MAX) BUFFER.pop();
    this.log.warn(`[${e.tipo}] ${e.mensaje} @ ${e.url}${e.handle ? ' · @' + e.handle : ''}`);
    return { ok: true };
  }

  // últimos errores (requiere sesión — el guard global protege esta ruta)
  @Get()
  listar() {
    return BUFFER;
  }
}

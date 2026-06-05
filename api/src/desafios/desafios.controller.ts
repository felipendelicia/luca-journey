import { Body, Controller, Delete, Get, Param, Post, Query } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { DesafiosService } from './desafios.service';

@Controller()
export class DesafiosController {
  constructor(private svc: DesafiosService) {}

  @Post('desafios') crear(@CurrentUser() uid: string, @Body() b: any) {
    return this.svc.crear(uid, b).then((id) => ({ id }));
  }
  @Get('desafios/ranking') ranking() { return this.svc.ranking(); }
  @Get('desafios') listar(@CurrentUser() uid: string, @Query() q: any) { return this.svc.listar(uid, q); }
  @Get('desafios/:id') leer(@Param('id') id: string) { return this.svc.leer(id); }
  @Post('desafios/:id/resolver') resolver(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { codigo: string }) {
    return this.svc.registrarResolucion(uid, id, b.codigo).then((balls) => ({ balls }));
  }
  @Get('desafios/:id/soluciones') soluciones(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.solucionesDe(uid, id);
  }
  @Post('desafios/:id/reportar') reportar(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { motivo: string }) {
    return this.svc.reportar(uid, id, b.motivo).then(() => ({ ok: true }));
  }
  @Delete('desafios/:id') borrar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.borrar(uid, id).then(() => ({ ok: true }));
  }
  @Post('resoluciones/:id/votar') votar(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { on: boolean }) {
    return this.svc.votar(uid, id, !!b.on).then(() => ({ ok: true }));
  }
  @Get('usuarios/:id/desafios') deUsuario(@Param('id') id: string) { return this.svc.deUsuario(id); }
  @Get('usuarios/:id/stats') stats(@Param('id') id: string) { return this.svc.stats(id); }
}

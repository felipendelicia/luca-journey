import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { OfertasService } from './ofertas.service';

@Controller()
export class OfertasController {
  constructor(private svc: OfertasService) {}

  @Post('ofertas') crear(@CurrentUser() uid: string, @Body() b: { aId: string; doy: any[]; pido: any[] }) {
    return this.svc.crear(uid, b.aId, b.doy || [], b.pido || []).then((id) => ({ id }));
  }
  @Post('ofertas/:id/responder') responder(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { aceptar: boolean }) {
    return this.svc.responder(uid, id, !!b.aceptar).then((estado) => ({ estado }));
  }
  @Delete('ofertas/:id') cancelar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.cancelar(uid, id).then(() => ({ ok: true }));
  }
  @Get('ofertas') mias(@CurrentUser() uid: string) { return this.svc.mias(uid); }
  @Get('social/pendientes') pendientes(@CurrentUser() uid: string) {
    return this.svc.pendientes(uid).then((n) => ({ n }));
  }
}

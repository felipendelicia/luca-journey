import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { AmigosService } from './amigos.service';

@Controller('amigos')
export class AmigosController {
  constructor(private svc: AmigosService) {}

  @Post('solicitar') solicitar(@CurrentUser() uid: string, @Body() b: { handle?: string; codigo?: string }) {
    return this.svc.solicitar(uid, b.handle, b.codigo).then(() => ({ ok: true }));
  }
  @Post(':id/responder') responder(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { aceptar: boolean }) {
    return this.svc.responder(uid, id, !!b.aceptar).then(() => ({ ok: true }));
  }
  @Delete(':id') quitar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.quitar(uid, id).then(() => ({ ok: true }));
  }
  @Get() mis(@CurrentUser() uid: string) { return this.svc.misAmigos(uid); }
  @Get('solicitudes') solicitudes(@CurrentUser() uid: string) { return this.svc.solicitudes(uid); }
  @Get('relaciones') relaciones(@CurrentUser() uid: string) { return this.svc.misRelaciones(uid); }
  @Get('son/:otro') son(@CurrentUser() uid: string, @Param('otro') otro: string) {
    return this.svc.sonAmigos(uid, otro).then((v) => ({ son: v }));
  }
}

import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { IntercambiosService } from './intercambios.service';

@Controller('trades')
export class IntercambiosController {
  constructor(private svc: IntercambiosService) {}

  @Post()
  crear(@CurrentUser() uid: string, @Body() b: { nombre: string }) { return this.svc.crear(uid, b?.nombre || ''); }

  @Post('join')
  unirse(@CurrentUser() uid: string, @Body() b: { codigo: string; nombre: string }) {
    return this.svc.unirse(uid, b.codigo, b?.nombre || '').then((id) => ({ id }));
  }

  @Get(':id')
  leer(@CurrentUser() uid: string, @Param('id') id: string) { return this.svc.leer(uid, id); }

  @Get(':id/otro')
  otro(@CurrentUser() uid: string, @Param('id') id: string) { return this.svc.coleccionDelOtro(uid, id); }

  @Post(':id/lote')
  lote(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { lote: any[] }) {
    return this.svc.ponerLote(uid, id, b.lote || []).then(() => ({ ok: true }));
  }

  @Post(':id/pedido')
  pedido(@CurrentUser() uid: string, @Param('id') id: string, @Body() b: { pedido: any[] }) {
    return this.svc.ponerPedido(uid, id, b.pedido || []).then(() => ({ ok: true }));
  }

  @Post(':id/confirm')
  confirmar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.confirmar(uid, id).then((estado) => ({ estado }));
  }

  @Delete(':id')
  cancelar(@CurrentUser() uid: string, @Param('id') id: string) {
    return this.svc.cancelar(uid, id).then(() => ({ ok: true }));
  }
}

import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { PerfilesService } from './perfiles.service';

@Controller()
export class PerfilesController {
  constructor(private svc: PerfilesService) {}

  @Get('perfil/me') mio(@CurrentUser() uid: string) { return this.svc.mio(uid); }

  @Post('perfil') guardar(@CurrentUser() uid: string, @Body() b: any) { return this.svc.guardar(uid, b); }
  @Post('perfil/publico') publico(@CurrentUser() uid: string, @Body() b: { publico: any; avatar?: number }) {
    return this.svc.actualizarPublico(uid, b.publico, b.avatar).then(() => ({ ok: true }));
  }
  @Post('perfil/descripcion') desc(@CurrentUser() uid: string, @Body() b: { desc: string }) {
    return this.svc.actualizarDescripcion(uid, b.desc).then(() => ({ ok: true }));
  }
  @Get('perfiles') buscar(@Query('q') q: string) { return this.svc.buscar(q); }
  @Get('perfiles/listar') listar(@CurrentUser() uid: string, @Query('limite') l: string, @Query('offset') o: string) {
    return this.svc.listar(uid, Number(l), Number(o));
  }
  @Get('perfil/:handle') porHandle(@Param('handle') h: string) { return this.svc.porHandle(h); }
}

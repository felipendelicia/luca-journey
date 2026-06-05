import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { PerfilesService } from './perfiles.service';
import { perfilDTO } from '../common/dto';

@Controller()
export class PerfilesController {
  constructor(private svc: PerfilesService) {}

  @Get('perfil/me') async mio(@CurrentUser() uid: string) { return perfilDTO(await this.svc.mio(uid)); }

  @Post('perfil') async guardar(@CurrentUser() uid: string, @Body() b: any) { return perfilDTO(await this.svc.guardar(uid, b)); }
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
  @Get('perfil/:handle') async porHandle(@Param('handle') h: string) { return perfilDTO(await this.svc.porHandle(h)); }
}

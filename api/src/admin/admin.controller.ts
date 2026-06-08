import { Body, Controller, Delete, Get, Param, Post, UseGuards } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { AdminGuard, esAdmin } from './admin.guard';
import { AdminService } from './admin.service';

@Controller('admin')
export class AdminController {
  constructor(private svc: AdminService) {}

  // ¿soy admin? (el cliente lo usa para mostrar/ocultar el panel). No requiere AdminGuard.
  @Get('soy') soy(@CurrentUser() uid: string) { return { admin: esAdmin(uid) }; }

  @UseGuards(AdminGuard) @Get('perfiles') perfiles() { return this.svc.perfiles(); }
  @UseGuards(AdminGuard) @Delete('perfil/:userId') borrarPerfil(@Param('userId') id: string) { return this.svc.borrarPerfil(id); }
  @UseGuards(AdminGuard) @Post('ban/:userId') ban(@Param('userId') id: string, @Body() b: { baneado: boolean }) { return this.svc.ban(id, !!b.baneado); }
  @UseGuards(AdminGuard) @Get('desafios') desafios() { return this.svc.desafios(); }
  @UseGuards(AdminGuard) @Delete('desafio/:id') borrarDesafio(@Param('id') id: string) { return this.svc.borrarDesafio(id); }
}

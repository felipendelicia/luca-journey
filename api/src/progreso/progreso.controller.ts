import { Body, Controller, Get, Put } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { ProgresoService } from './progreso.service';

@Controller('progreso')
export class ProgresoController {
  constructor(private svc: ProgresoService) {}

  @Get()
  async get(@CurrentUser() userId: string) {
    return { estado: await this.svc.bajar(userId) };
  }

  @Put()
  async put(@CurrentUser() userId: string, @Body() body: { estado: Record<string, any> }) {
    return this.svc.subir(userId, body.estado || {});
  }
}

import { Module } from '@nestjs/common';
import { PerfilesService } from './perfiles.service';
import { PerfilesController } from './perfiles.controller';
import { AmigosService } from './amigos.service';
import { AmigosController } from './amigos.controller';
import { OfertasService } from './ofertas.service';
import { OfertasController } from './ofertas.controller';

@Module({
  controllers: [PerfilesController, AmigosController, OfertasController],
  providers: [PerfilesService, AmigosService, OfertasService],
})
export class SocialModule {}

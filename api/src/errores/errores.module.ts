import { Module } from '@nestjs/common';
import { ErroresController } from './errores.controller';

@Module({ controllers: [ErroresController] })
export class ErroresModule {}

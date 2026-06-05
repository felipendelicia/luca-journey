import { Injectable } from '@nestjs/common';
import { EventsGateway } from './events.gateway';

@Injectable()
export class RealtimeService {
  constructor(private gw: EventsGateway) {}
  progreso(uid: string, estado: Record<string, any>) { this.gw.emitirProgreso(uid, estado); }
  sala(id: string, row: any) { this.gw.emitirSala(id, row); }
}

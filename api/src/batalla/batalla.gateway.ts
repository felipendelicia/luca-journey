import {
  OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect, SubscribeMessage,
  WebSocketGateway, WebSocketServer, MessageBody, ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { JwtService } from '@nestjs/jwt';
import { SalasService } from './salas.service';

// Gateway PvP en su propio namespace /batalla (mirror de realtime/events.gateway: auth JWT en el
// handshake). Toda la lógica vive en SalasService; acá solo se rutean los eventos socket.
@WebSocketGateway({ namespace: 'batalla', cors: { origin: true } })
export class BatallaGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server: Server;
  private jwt = new JwtService({});

  constructor(private salas: SalasService) {}

  afterInit() { this.salas.server = this.server; }

  private uidDe(client: Socket): string | null {
    const token = (client.handshake.auth?.token || '') as string;
    try { return this.jwt.verify(token, { secret: process.env.JWT_SECRET || 'dev-secret' }).sub; } catch { return null; }
  }
  private uid(client: Socket): string { return (client.data as any)?.uid; }
  private nombre(client: Socket): string { return (client.data as any)?.nombre || 'Entrenador'; }

  handleConnection(client: Socket) {
    const uid = this.uidDe(client);
    if (!uid) { client.disconnect(true); return; }
    (client.data as any).uid = uid;
    (client.data as any).nombre = (client.handshake.auth?.nombre || '').toString().slice(0, 24) || 'Entrenador';
    client.join(`bu:${uid}`);
    this.salas.reconectar(client, uid);             // por si vuelve a una sala con gracia activa
  }

  handleDisconnect(client: Socket) {
    const uid = this.uid(client); if (uid) this.salas.marcarDesconexion(uid);
  }

  // ── matchmaking ──
  @SubscribeMessage('buscar')
  onBuscar(@ConnectedSocket() c: Socket) { this.salas.buscar(c, this.uid(c), this.nombre(c)); }
  @SubscribeMessage('cancelarCola')
  onCancelar(@ConnectedSocket() c: Socket) { this.salas.cancelarCola(this.uid(c)); }
  @SubscribeMessage('invitar')
  onInvitar(@ConnectedSocket() c: Socket, @MessageBody() rivalUid: string) { this.salas.invitar(c, this.uid(c), this.nombre(c), rivalUid); }
  @SubscribeMessage('aceptar')
  onAceptar(@ConnectedSocket() c: Socket, @MessageBody() roomId: string) { this.salas.aceptar(c, this.uid(c), this.nombre(c), roomId); }
  @SubscribeMessage('crearCodigo')
  onCrearCodigo(@ConnectedSocket() c: Socket) { this.salas.crearCodigo(c, this.uid(c), this.nombre(c)); }
  @SubscribeMessage('unirseCodigo')
  onUnirseCodigo(@ConnectedSocket() c: Socket, @MessageBody() code: string) { this.salas.unirseCodigo(c, this.uid(c), this.nombre(c), code); }

  // ── selección + combate (modelo SIMULTÁNEO) ──
  @SubscribeMessage('elegirEquipo')
  onElegir(@ConnectedSocket() c: Socket, @MessageBody() iids: string[]) { return this.salas.elegirEquipo(c, this.uid(c), iids); }
  // 'elegir' = elección de acción de la ronda (cliente manda el objeto Accion completo).
  @SubscribeMessage('elegir')
  onElegirAccion(@ConnectedSocket() c: Socket, @MessageBody() accion: any) { this.salas.elegir(c, this.uid(c), accion); }
  // atajos de conveniencia: arman el objeto Accion y delegan en 'elegir'.
  @SubscribeMessage('mover')
  onMover(@ConnectedSocket() c: Socket, @MessageBody() i: number) { this.salas.elegir(c, this.uid(c), { tipo: 'mover', i }); }
  @SubscribeMessage('cambiar')
  onCambiar(@ConnectedSocket() c: Socket, @MessageBody() idx: number) { this.salas.elegir(c, this.uid(c), { tipo: 'cambiar', idx }); }
  @SubscribeMessage('pocion')
  onPocion(@ConnectedSocket() c: Socket, @MessageBody() itemId: string) { this.salas.elegir(c, this.uid(c), { tipo: 'pocion', itemId }); }
  @SubscribeMessage('super')
  onSuper(@ConnectedSocket() c: Socket, @MessageBody() calidad: number) { this.salas.elegir(c, this.uid(c), { tipo: 'super', calidad }); }
  @SubscribeMessage('reemplazo')
  onReemplazo(@ConnectedSocket() c: Socket, @MessageBody() idx: number) { this.salas.elegir(c, this.uid(c), { tipo: 'reemplazo', idx }); }
  @SubscribeMessage('rendirse')
  onRendirse(@ConnectedSocket() c: Socket) { this.salas.elegir(c, this.uid(c), { tipo: 'rendirse' }); }
  // el cliente terminó de animar la resolución → cuando avisan los dos, el server arranca la próxima ronda.
  @SubscribeMessage('listoRonda')
  onListoRonda(@ConnectedSocket() c: Socket) { this.salas.ackRonda(this.uid(c)); }
}

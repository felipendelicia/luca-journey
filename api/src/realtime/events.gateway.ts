import {
  OnGatewayConnection, OnGatewayDisconnect, SubscribeMessage,
  WebSocketGateway, WebSocketServer, MessageBody, ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { JwtService } from '@nestjs/jwt';

// Topics: `progreso:<uid>`, `sala:<id>`, `presencia-global`.
@WebSocketGateway({ cors: { origin: true } })
export class EventsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server: Server;
  private jwt = new JwtService({});

  // presencia: topic -> Set<userId>
  private presentes = new Map<string, Set<string>>();

  private uidDe(client: Socket): string | null {
    const token = (client.handshake.auth?.token || '') as string;
    try {
      const p: any = this.jwt.verify(token, { secret: process.env.JWT_SECRET || 'dev-secret' });
      return p.sub;
    } catch { return null; }
  }

  handleConnection(client: Socket) {
    const uid = this.uidDe(client);
    if (!uid) { client.disconnect(true); return; }
    (client.data as any).uid = uid;
    client.join(`progreso:${uid}`); // recibe cambios externos de su propia colección
  }

  handleDisconnect(client: Socket) {
    const uid = (client.data as any)?.uid;
    for (const [topic, set] of this.presentes) {
      if (uid && set.delete(uid)) this.emitirPresencia(topic);
    }
  }

  @SubscribeMessage('join')
  onJoin(@ConnectedSocket() client: Socket, @MessageBody() topic: string) {
    const uid = (client.data as any)?.uid;
    client.join(topic);
    if (!this.presentes.has(topic)) this.presentes.set(topic, new Set());
    this.presentes.get(topic)!.add(uid);
    this.emitirPresencia(topic);
  }

  @SubscribeMessage('leave')
  onLeave(@ConnectedSocket() client: Socket, @MessageBody() topic: string) {
    const uid = (client.data as any)?.uid;
    client.leave(topic);
    this.presentes.get(topic)?.delete(uid);
    this.emitirPresencia(topic);
  }

  @SubscribeMessage('broadcast')
  onBroadcast(@MessageBody() msg: { topic: string; payload: any }) {
    this.server.to(msg.topic).emit('broadcast', msg.payload);
  }

  private emitirPresencia(topic: string) {
    const ids = Array.from(this.presentes.get(topic) || []);
    this.server.to(topic).emit('presencia', { topic, ids });
  }

  emitirProgreso(uid: string, estado: Record<string, any>) {
    this.server.to(`progreso:${uid}`).emit('progreso', estado);
  }
  emitirSala(id: string, row: any) {
    this.server.to(`sala:${id}`).emit('sala', row);
  }
}

export function salaDTO(s: any) {
  if (!s) return s;
  return {
    id: s.id, codigo: s.codigo, estado: s.estado,
    creador_id: s.creadorId, invitado_id: s.invitadoId,
    creador_nombre: s.creadorNombre, invitado_nombre: s.invitadoNombre,
    creador_lote: s.creadorLote, invitado_lote: s.invitadoLote,
    creador_pedido: s.creadorPedido, invitado_pedido: s.invitadoPedido,
    creador_ok: s.creadorOk, invitado_ok: s.invitadoOk,
  };
}
export function perfilDTO(p: any) {
  if (!p) return p;
  return {
    user_id: p.userId, handle: p.handle, nombre: p.nombre, avatar: p.avatar,
    codigo_amigo: p.codigoAmigo, publico: p.publico, descripcion: p.descripcion,
  };
}

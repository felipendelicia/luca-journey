import { CanActivate, ExecutionContext, ForbiddenException, Injectable } from '@nestjs/common';

// admins por user_id (default: felipo). Override con ADMIN_UIDS="uid1,uid2" en el .env.
export const ADMIN_UIDS = (process.env.ADMIN_UIDS || '39560479-e110-474e-9566-3718bd479a5a')
  .split(',').map((s) => s.trim()).filter(Boolean);

export function esAdmin(uid?: string): boolean {
  return !!uid && ADMIN_UIDS.includes(uid);
}

@Injectable()
export class AdminGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest();
    if (!esAdmin(req.user?.userId)) throw new ForbiddenException('solo admin');
    return true;
  }
}

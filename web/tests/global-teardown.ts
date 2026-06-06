import { execFileSync } from 'node:child_process';
import path from 'node:path';

// restaura web/.env al terminar la corrida e2e (lo había blanqueado el comando del webServer)
export default function globalTeardown() {
  try { execFileSync('node', [path.join('tests', 'e2e-env.mjs'), 'on'], { stdio: 'inherit' }); } catch {}
}

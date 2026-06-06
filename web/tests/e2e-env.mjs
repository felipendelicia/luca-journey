// e2e-env.mjs — apaga/restaura el gate de login para los tests e2e blanqueando web/.env.
//   node tests/e2e-env.mjs off  → respalda .env y deja PUBLIC_API_URL vacío (modo solo-localStorage)
//   node tests/e2e-env.mjs on   → restaura el .env original
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ENV = path.resolve(HERE, '..', '.env');
const BAK = path.resolve(HERE, '..', '.env.e2ebak');
const modo = process.argv[2];

if (modo === 'off') {
  if (fs.existsSync(ENV) && !fs.existsSync(BAK)) fs.copyFileSync(ENV, BAK);
  fs.writeFileSync(ENV, '# e2e: gate de login apagado (lo restaura `e2e-env.mjs on`)\nPUBLIC_API_URL=\n');
  console.log('[e2e] gate OFF');
} else if (modo === 'on') {
  if (fs.existsSync(BAK)) { fs.copyFileSync(BAK, ENV); fs.rmSync(BAK); console.log('[e2e] .env restaurado'); }
  else console.log('[e2e] no había backup; .env sin cambios');
}

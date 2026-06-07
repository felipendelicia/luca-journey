// sync-batalla-data.mjs — copia los datos de combate del front (web/src/data) a api/src/batalla/data.
// El motor del server (api/src/batalla/motor.ts) necesita su PROPIA copia: el Docker build usa solo
// ./api como contexto, así que web/ no está en la imagen. Correr cuando cambien los datos del front:
//   node scripts/sync-batalla-data.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(HERE, '..', '..', 'web', 'src', 'data');
const DST = path.resolve(HERE, '..', 'src', 'batalla', 'data');
const FILES = ['tipos.json', 'movimientos.json', 'learnsets.json', 'pokemon.json', 'evoluciones.json', 'estadisticas.json', 'habilidades.json', 'yields.json'];

fs.mkdirSync(DST, { recursive: true });
for (const f of FILES) {
  fs.copyFileSync(path.join(SRC, f), path.join(DST, f));
  console.log('✓', f);
}
console.log('Datos de combate sincronizados →', path.relative(process.cwd(), DST));

// motor COMPARTIDO: el core puro vive en web/src/lib/combate-core.ts (fuente de verdad). Copiamos
// una réplica a api/src/batalla/ para que motor.ts la importe (Docker buildea solo ./api).
const CORE_SRC = path.resolve(HERE, '..', '..', 'web', 'src', 'lib', 'combate-core.ts');
const CORE_DST = path.resolve(HERE, '..', 'src', 'batalla', 'combate-core.ts');
const aviso = '// ⚠️ GENERADO: copia de web/src/lib/combate-core.ts. NO EDITAR acá — editá el original y\n'
  + '// corré `node scripts/sync-batalla-data.mjs`.\n';
fs.writeFileSync(CORE_DST, aviso + fs.readFileSync(CORE_SRC, 'utf8'));
console.log('✓ combate-core.ts (motor compartido) →', path.relative(process.cwd(), CORE_DST));

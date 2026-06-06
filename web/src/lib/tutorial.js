// tutorial.js — tour de onboarding (primer uso). Modal por pasos centrado (robusto en mobile/desktop).
// Se muestra una vez (flag localStorage 'tuto:visto'); relanzable con iniciarTutorial(true).
const PASOS = [
  { ico: '👋', t: '¡Bienvenido!', d: 'Esta es la plataforma del curso: aprendés <b>Python</b> jugando con Pokémon. Te muestro el recorrido en 30 segundos.' },
  { ico: '📖', t: '1. El Libro', d: 'Toda la <b>teoría</b> del curso, con ejemplos que podés ejecutar ahí mismo. Empezá leyendo.' },
  { ico: '🏋️', t: '2. Ejercicios', d: 'Resolvé ejercicios con <b>tests reales</b> en el navegador. Cada uno te da <b>🔴 Pokébolas</b>.' },
  { ico: '🎒', t: '3. Safari', d: 'Gastá tus Pokébolas para <b>atrapar Pokémon</b> salvajes (¡con su nivel y rareza!).' },
  { ico: '📕', t: '4. Pokédex', d: 'Tu colección: subí de <b>nivel</b> con caramelos, <b>evolucioná</b> (¡con animación!) y armá tu equipo.' },
  { ico: '⚔️', t: '5. Batalla', d: 'Peleá por turnos (vs CPU o <b>en vivo</b>). El <b>⚡ Súper</b> se desata resolviendo un reto de código.' },
  { ico: '🔥', t: '¡Volvé cada día!', d: 'Tenés <b>racha diaria</b> (bonus de Pokébolas), <b>logros</b> y la <b>Liga</b> con medallas. ¡A aprender!' },
];

export function iniciarTutorial(forzar = false) {
  if (!forzar && localStorage.getItem('tuto:visto') === '1') return;
  if (document.getElementById('tuto-overlay')) return;   // ya abierto
  let i = 0;
  const ov = document.createElement('div');
  ov.id = 'tuto-overlay'; ov.className = 'tuto-overlay';
  const cerrar = () => { localStorage.setItem('tuto:visto', '1'); ov.remove(); };
  const pintar = () => {
    const p = PASOS[i];
    const dots = PASOS.map((_, k) => '<span class="tuto-dot' + (k === i ? ' on' : '') + '"></span>').join('');
    const ultimo = i === PASOS.length - 1;
    ov.innerHTML =
      '<div class="tuto-card">' +
        '<button class="tuto-x" id="tuto-x" aria-label="Cerrar">✕</button>' +
        '<div class="tuto-ico">' + p.ico + '</div>' +
        '<h2 class="tuto-t">' + p.t + '</h2>' +
        '<p class="tuto-d">' + p.d + '</p>' +
        '<div class="tuto-dots">' + dots + '</div>' +
        '<div class="tuto-nav">' +
          '<button class="tuto-skip" id="tuto-skip">' + (ultimo ? '' : 'Saltar') + '</button>' +
          (i > 0 ? '<button class="tuto-prev" id="tuto-prev">← Atrás</button>' : '') +
          '<button class="tuto-next" id="tuto-next">' + (ultimo ? '¡A jugar! 🚀' : 'Siguiente →') + '</button>' +
        '</div>' +
      '</div>';
    ov.querySelector('#tuto-x').onclick = cerrar;
    ov.querySelector('#tuto-skip').onclick = cerrar;
    const prev = ov.querySelector('#tuto-prev'); if (prev) prev.onclick = () => { i--; pintar(); };
    ov.querySelector('#tuto-next').onclick = () => { if (ultimo) cerrar(); else { i++; pintar(); } };
  };
  pintar();
  ov.addEventListener('click', (e) => { if (e.target === ov) cerrar(); });
  document.body.appendChild(ov);
}

// Agrupa los capítulos del libro en secciones desplegables.
export const GRUPOS = [
  { nombre: 'Introducción', icono: '🎒', slugs: ['introduccion'] },
  { nombre: 'Linux', icono: '🐧', slugs: ['linux-fundamentos', 'linux-intermedio'] },
  {
    nombre: 'Python',
    icono: '🐍',
    slugs: [
      'python-introduccion', 'control-de-flujo', 'funciones',
      'listas-y-colecciones', 'cadenas-y-archivos',
    ],
  },
  { nombre: 'Git', icono: '🔀', slugs: ['git'] },
  {
    nombre: 'Python avanzado',
    icono: '🔥',
    slugs: ['poo-introduccion', 'poo-avanzado', 'modulos-y-pip'],
  },
  { nombre: 'Ayuda', icono: '❓', slugs: ['ayuda'] },
];

// caps: array YA ordenado por 'order'. Devuelve grupos con sus capítulos + nº global.
export function agrupar(caps) {
  const pos = new Map(caps.map((c, i) => [c.slug, i]));
  return GRUPOS
    .map((g) => ({
      nombre: g.nombre,
      icono: g.icono,
      items: g.slugs.filter((s) => pos.has(s)).map((s) => ({ cap: caps[pos.get(s)], n: pos.get(s) })),
    }))
    .filter((g) => g.items.length);
}

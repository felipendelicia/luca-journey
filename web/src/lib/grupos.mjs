// Agrupa los capítulos del libro en secciones desplegables.
export const GRUPOS = [
  { nombre: 'Introducción', icono: '🎒', slugs: ['introduccion'] },
  { nombre: 'Linux', icono: '🐧', slugs: ['linux-fundamentos', 'linux-intermedio'] },
  {
    nombre: 'Fundamentos',
    icono: '🐍',
    slugs: [
      'python-introduccion', 'control-de-flujo', 'funciones',
      'listas-y-colecciones', 'cadenas-y-archivos',
      'poo-introduccion', 'poo-avanzado', 'modulos-y-pip',
    ],
  },
  {
    nombre: 'Análisis de datos',
    icono: '📊',
    slugs: [
      'numpy-arrays', 'numpy-calculo', 'pandas-series-dataframe', 'pandas-seleccion',
      'pandas-limpieza', 'pandas-groupby', 'matplotlib', 'analisis-integrador',
    ],
  },
  {
    nombre: 'APIs',
    icono: '🛰️',
    slugs: [
      'api-http-json', 'flask-primera-app', 'flask-json', 'flask-parametros',
      'flask-post', 'flask-rest-crud', 'consumir-api', 'pokedex-api',
    ],
  },
  {
    nombre: 'Bases de datos',
    icono: '🗄️',
    slugs: [
      'sql-intro', 'sql-crear', 'sql-select', 'sql-agregaciones',
      'sql-update-delete', 'sql-join', 'sqlite-python', 'proyecto-db',
    ],
  },
  { nombre: 'Git', icono: '🔀', slugs: ['git'] },
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

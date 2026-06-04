// rehype-callouts.mjs — Convierte los blockquotes del markdown en "cajas de aviso"
// del libro, eligiendo el tipo según el emoji inicial (⚠️ cuidado, 💡 tip, etc.).
// Sin dependencias externas: recorre el árbol HAST a mano.

function texto(node) {
  if (node.type === 'text') return node.value;
  if (node.children) return node.children.map(texto).join('');
  return '';
}

export default function rehypeCallouts() {
  return (tree) => {
    const visitar = (node) => {
      if (node.children) node.children.forEach(visitar);
      if (node.type === 'element' && node.tagName === 'blockquote') {
        const t = texto(node);
        let tipo = 'nota', etiqueta = 'NOTA';
        if (/⚠/.test(t)) { tipo = 'cuidado'; etiqueta = 'CUIDADO'; }
        else if (/💡/.test(t)) { tipo = 'tip'; etiqueta = 'TIP'; }
        else if (/🎯/.test(t)) { tipo = 'nota'; etiqueta = 'META'; }
        else if (/⚡/.test(t)) { tipo = 'tip'; etiqueta = 'ÁNIMO'; }
        node.tagName = 'div';
        node.properties = node.properties || {};
        node.properties.className = ['callout', tipo];
        node.children.unshift({
          type: 'element',
          tagName: 'span',
          properties: { className: ['et'] },
          children: [{ type: 'text', value: etiqueta }],
        });
      }
    };
    visitar(tree);
  };
}

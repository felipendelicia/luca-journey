// rehype-base-links.mjs — prefija los links/imagenes internos del markdown ("/...")
// con el base path del sitio (process.env.DEPLOY_BASE). En dev queda igual ('/...').
export default function rehypeBaseLinks() {
  const base = (process.env.DEPLOY_BASE || '').replace(/\/$/, '');
  if (!base) return () => {};
  const fix = (node, attr) => {
    const v = node.properties && node.properties[attr];
    if (typeof v === 'string' && v.startsWith('/') && !v.startsWith('//')) {
      node.properties[attr] = base + v;
    }
  };
  const walk = (node) => {
    if (node.type === 'element') {
      if (node.tagName === 'a') fix(node, 'href');
      if (node.tagName === 'img') fix(node, 'src');
    }
    if (node.children) node.children.forEach(walk);
  };
  return (tree) => walk(tree);
}

import { defineConfig } from 'astro/config';
import rehypeCallouts from './src/lib/rehype-callouts.mjs';
import rehypeBaseLinks from './src/lib/rehype-base-links.mjs';

// Plataforma web del curso "Python con Pokémon".
// En dev: base '/'. En build de producción: DEPLOY_BASE=/luca-journey (GitHub Pages).
// La salida va a ../docs para que GitHub Pages la sirva (source: /docs).
const base = process.env.DEPLOY_BASE || undefined;

export default defineConfig({
  site: 'https://felipendelicia.github.io',
  base,
  outDir: '../docs',
  markdown: {
    shikiConfig: {
      theme: 'one-dark-pro',
      wrap: false,
      transformers: [{ pre(node) { node.properties['data-language'] = this.options.lang; } }],
    },
    rehypePlugins: [rehypeCallouts, rehypeBaseLinks],
  },
});

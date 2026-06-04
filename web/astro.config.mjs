import { defineConfig } from 'astro/config';
import rehypeCallouts from './src/lib/rehype-callouts.mjs';

// Plataforma web del curso "Python con Pokémon".
// 'site' y 'base' se ajustan cuando hagamos el deploy a GitHub Pages.
export default defineConfig({
  site: 'https://felipendelicia.github.io',
  // base: '/luca-journey',   // se activa al desplegar en /docs
  markdown: {
    // Resaltado de código en tiempo de build (tema oscuro tipo one-dark).
    shikiConfig: {
      theme: 'one-dark-pro',
      wrap: false,
      // Guardamos el lenguaje en data-language para el botón ▶ ejecutar.
      transformers: [
        {
          pre(node) {
            node.properties['data-language'] = this.options.lang;
          },
        },
      ],
    },
    // Cajas de aviso desde los blockquotes.
    rehypePlugins: [rehypeCallouts],
  },
});

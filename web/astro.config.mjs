import { defineConfig } from 'astro/config';

// Plataforma web del curso "Python con Pokémon".
// 'site' y 'base' se ajustan cuando hagamos el deploy a GitHub Pages.
export default defineConfig({
  site: 'https://felipendelicia.github.io',
  // base: '/luca-journey',   // se activa al desplegar en /docs
});

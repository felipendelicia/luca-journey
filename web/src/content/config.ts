import { defineCollection, z } from 'astro:content';

// El "libro": cada capítulo es un .md en src/content/libro/ con título y orden.
// Esta es la ÚNICA fuente del contenido teórico (se edita acá, en el proyecto web).
const libro = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    order: z.number(),
  }),
});

export const collections = { libro };

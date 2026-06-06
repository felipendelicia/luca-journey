import type { Page } from '@playwright/test';

// siembra claves de localStorage ANTES de que corran los scripts de la página (cada navegación).
export async function seed(page: Page, data: Record<string, unknown>) {
  await page.addInitScript((d) => {
    for (const [k, v] of Object.entries(d)) {
      localStorage.setItem(k, typeof v === 'string' ? (v as string) : JSON.stringify(v));
    }
  }, data);
}

export const EEVEE = { iid: 'e1', id: 133, nivel: 30, exp: 0, shiny: false, movs: [], creado: 1 };

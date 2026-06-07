import { test, expect } from '@playwright/test';
import { seed } from './helpers';

test('batalla práctica: elegir equipo y un ataque resuelve el turno', async ({ page }) => {
  test.setTimeout(60000);
  await seed(page, {
    'col:pc': [
      { iid: 'a', id: 4, nivel: 20, exp: 0, shiny: false, movs: [], creado: 1 },
      { iid: 'b', id: 7, nivel: 20, exp: 0, shiny: false, movs: [], creado: 2 },
    ],
  });
  await page.goto('/batalla');
  await page.locator('#bt-modo .bt-modo-b[data-modo="practica"]').click();
  await page.locator('#bt-sel .bt-pick').first().click();
  await page.locator('#bt-go').click();
  await expect(page.locator('#bt-combate')).toBeVisible();
  const move = page.locator('#bt-moves .bt-move[data-i]').first();
  await expect(move).toBeVisible();
  await move.click();
  // tras el turno, la barra de Súper sube de 0%
  await expect(page.locator('#bt-carga-txt')).not.toHaveText('Súper: 0%', { timeout: 35000 });
});

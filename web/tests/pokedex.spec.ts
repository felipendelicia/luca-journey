import { test, expect } from '@playwright/test';
import { seed, EEVEE } from './helpers';

const SEED = { 'col:pc': [EEVEE], 'col:items': { piedraagua: 1 }, 'col:caramelos': { 133: 5 }, 'col:vistos': [133] };

test('modal: stats + chooser muestra TODAS las ramas; evo-scene oculta en reposo', async ({ page }) => {
  await seed(page, SEED);
  await page.goto('/pokedex');
  // regresión: la escena de evolución NO debe tapar la página en reposo
  await expect(page.locator('#evo-scene')).toBeHidden();
  await page.locator('#tab-pc').click();                           // pestaña "Mi PC"
  await page.locator('[data-iid="e1"]').click();
  await expect(page.locator('.st-lista')).toBeVisible();           // panel de estadísticas
  await page.locator('#pm-evo-toggle').click();
  await expect(page.locator('.pm-evo-pick, .pm-evo-locked')).toHaveCount(8);   // Eevee = 8 formas
});

test('Mi PC: limpiador de repetidos agrupa por línea evolutiva y conserva el mejor', async ({ page }) => {
  await seed(page, {
    'col:pc': [
      { iid: 'a', id: 16, nivel: 5, exp: 0, shiny: false, movs: [], creado: 1 },
      { iid: 'b', id: 16, nivel: 12, exp: 0, shiny: false, movs: [], creado: 2 },
      { iid: 'c', id: 17, nivel: 20, exp: 0, shiny: false, movs: [], creado: 3 },
    ],
    'col:vistos': [16, 17],
  });
  await page.goto('/pokedex');
  await page.locator('#pc-dup').click();
  await expect(page.locator('#dup-modal')).toBeVisible();
  await expect(page.locator('.dup-grupo')).toHaveCount(1);   // una familia (Pidgey)
  await expect(page.locator('.dup-lib')).toHaveCount(3);     // TODOS liberables (vos elegís)
  await expect(page.locator('.dup-free')).toHaveCount(3);    // cada uno con botón Liberar
  await expect(page.locator('.dup-lib.best')).toHaveCount(1); // 1 sugerido (⭐, igual liberable)
});

test('evolución: Eevee→Vaporeon con piedra (animación + reveal concreta el cambio)', async ({ page }) => {
  test.setTimeout(60000);
  await seed(page, SEED);
  await page.goto('/pokedex');
  await page.locator('#tab-pc').click();
  await page.locator('[data-iid="e1"]').click();
  await page.locator('#pm-evo-toggle').click();
  await page.locator('.pm-evo-pick').first().click();   // Vaporeon (única habilitada con Piedra Agua)
  await expect(page.locator('#evo-done')).toBeVisible({ timeout: 25000 });
  const pcId = await page.evaluate(() => JSON.parse(localStorage.getItem('col:pc') || '[]')[0]?.id);
  expect(pcId).toBe(134);   // ahora es Vaporeon
});

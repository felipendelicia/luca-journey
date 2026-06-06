import { test, expect } from '@playwright/test';

test('ejercicios: tabs de región muestran una región a la vez', async ({ page }) => {
  await page.goto('/ejercicios/');
  await expect(page.locator('.reg-tabs')).toBeVisible();
  await expect(page.locator('.region-panel:not([hidden])')).toHaveCount(1);   // solo una visible
  await page.locator('.reg-tab[data-region="galar"]').click();
  await expect(page.locator('.region-panel[data-region="galar"]')).toBeVisible();
  await expect(page.locator('.region-panel[data-region="kanto"]')).toBeHidden();
});

test('ejercicios: el buscador filtra temas de todas las regiones', async ({ page }) => {
  await page.goto('/ejercicios/');
  await page.locator('#ej-buscar').fill('recursión');
  await expect(page.locator('.tema-card[data-slug="algo-recursion"]')).toBeVisible();   // tema de Paldea
  await expect(page.locator('body')).toHaveClass(/ej-buscando/);                          // líderes ocultos
});

// el código corre en un worker con timeout: un bucle infinito NO congela la pestaña
test('ejercicios: bucle infinito muestra timeout (no se cuelga)', async ({ page }) => {
  test.setTimeout(90000);
  await page.goto('/ejercicios/python-introduccion/saludo');
  await page.locator('.cm-content').click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type('while True:\n    pass');
  await page.locator('#ejecutar').click();
  await expect(page.locator('#result')).toContainText(/tardó demasiado|bucle infinito/i, { timeout: 75000 });
});

import { test, expect } from '@playwright/test';

test('home carga, sin gate de login (modo local)', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Python con Pokémon');
  await expect(page.locator('text=Entrá para jugar')).toBeHidden();
});

// regresión: la racha diaria no aparecía (se usaba el evento equivocado)
test('home: la racha diaria aparece', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#racha-chip')).toBeVisible();
  await expect(page.locator('#racha-chip')).toContainText('racha');
});

test('nav: links principales presentes', async ({ page }) => {
  await page.goto('/');
  for (const t of ['Libro', 'Ejercicios', 'Liga', 'Safari']) {
    await expect(page.locator('.cards').getByText(t, { exact: false }).first()).toBeVisible();
  }
});

import { test, expect } from '@playwright/test';
import { seed } from './helpers';

test('safari: con Pokébolas, tirar atrapa un Pokémon', async ({ page }) => {
  test.setTimeout(60000);
  await seed(page, { 'col:balls': 30 });
  await page.goto('/safari');
  await expect(page.locator('#tirar')).toBeEnabled();
  await page.locator('#tirar').click();
  await expect(page.locator('.captura-txt')).toBeVisible({ timeout: 20000 });   // resultado de captura
});

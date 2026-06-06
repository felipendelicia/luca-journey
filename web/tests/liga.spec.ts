import { test, expect } from '@playwright/test';

test('liga: tabs muestran una sección a la vez (Logros + regiones)', async ({ page }) => {
  await page.goto('/liga');
  await expect(page.locator('#liga-tabs')).toBeVisible();
  await expect(page.locator('.liga-panel:not([hidden])')).toHaveCount(1);
  await page.locator('.reg-tab[data-tab="logros"]').click();
  await expect(page.locator('.liga-panel[data-tab="logros"]')).toBeVisible();
  await page.locator('.reg-tab[data-tab="paldea"]').click();
  await expect(page.locator('.liga-panel[data-tab="paldea"]')).toBeVisible();
  await expect(page.locator('.liga-panel[data-tab="logros"]')).toBeHidden();
});

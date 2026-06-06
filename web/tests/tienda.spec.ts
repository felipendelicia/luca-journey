import { test, expect } from '@playwright/test';

test('tienda: piedras tipadas a 40, Disco a 50, Revivir, y sprites SVG (no emoji)', async ({ page }) => {
  await page.goto('/tienda');
  await expect(page.locator('[data-id="piedrafuego"]')).toBeVisible();
  await expect(page.locator('[data-id="piedrafuego"]')).toHaveAttribute('data-precio', '40');
  await expect(page.locator('[data-id="discoenlace"]')).toHaveAttribute('data-precio', '50');
  await expect(page.locator('[data-id="revivir"]')).toBeVisible();
  // los items de Pokémon usan sprite SVG, no emoji
  await expect(page.locator('[data-id="piedrafuego"] svg').first()).toBeVisible();
  await expect(page.locator('[data-id="revivir"] svg').first()).toBeVisible();
});

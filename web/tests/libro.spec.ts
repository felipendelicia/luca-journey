import { test, expect } from '@playwright/test';

// guarda contra la regresión: Shiki marca el bloque ```quiz como 'plaintext', así que el quiz
// se detecta por contenido ("P:"). Verificamos que rendericen interactivos (viejos y nuevos).
test('libro: los quizzes renderizan interactivos', async ({ page }) => {
  await page.goto('/libro/algo-busqueda');
  await expect(page.locator('.quiz').first()).toBeVisible();
  await expect(page.locator('.quiz')).toHaveCount(2);
  await expect(page.locator('.quiz-op').first()).toBeVisible();
});

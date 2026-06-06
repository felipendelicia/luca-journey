import { test, expect } from '@playwright/test';

// guarda contra la regresión: Shiki marca el bloque ```quiz como 'plaintext', así que el quiz
// se detecta por contenido ("P:"). Verificamos que rendericen interactivos (viejos y nuevos).
test('libro: los quizzes renderizan interactivos', async ({ page }) => {
  await page.goto('/libro/algo-busqueda');
  await expect(page.locator('.quiz').first()).toBeVisible();
  await expect(page.locator('.quiz')).toHaveCount(2);
  await expect(page.locator('.quiz-op').first()).toBeVisible();
});

// el ▶ del libro (sin input) corre en un worker con streaming + timeout
test('libro ▶: salida en vivo por worker', async ({ page }) => {
  test.setTimeout(90000);
  await page.goto('/libro/funciones');
  await page.locator('.cw .cm-content').first().click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type('print("hola worker")');
  await page.locator('.cw-run').first().click();
  await expect(page.locator('.cw-out').first()).toContainText('hola worker', { timeout: 75000 });
});

test('libro ▶: bucle infinito muestra timeout (no se cuelga)', async ({ page }) => {
  test.setTimeout(90000);
  await page.goto('/libro/funciones');
  await page.locator('.cw .cm-content').first().click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type('while True:\n    pass');
  await page.locator('.cw-run').first().click();
  await expect(page.locator('.cw-out').first()).toContainText(/tardó demasiado|bucle infinito/i, { timeout: 75000 });
});

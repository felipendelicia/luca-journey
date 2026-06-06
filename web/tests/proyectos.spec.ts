import { test, expect } from '@playwright/test';

// los proyectos (líderes de gimnasio) corren en el worker con timeout: un bucle infinito NO congela
test('proyectos ▶: bucle infinito muestra timeout (no se cuelga)', async ({ page }) => {
  test.setTimeout(90000);
  await page.goto('/proyectos/algo-busqueda');
  await page.locator('.cm-content').first().click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type('while True:\n    pass');
  await page.locator('#run-indice').click();
  await expect(page.locator('#res-indice')).toContainText(/tardó demasiado|bucle infinito/i, { timeout: 75000 });
});

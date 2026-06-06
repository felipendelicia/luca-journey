import { defineConfig } from '@playwright/test';

// e2e contra el dev server con el gate de login APAGADO (el webServer blanquea web/.env vía
// e2e-env.mjs; global-teardown lo restaura). Modo solo-localStorage. Usa el Chrome del sistema
// (channel: 'chrome'), sin bajar chromium.
export default defineConfig({
  testDir: './tests',
  timeout: 45000,
  expect: { timeout: 8000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [['list']],
  globalTeardown: './tests/global-teardown.ts',
  use: {
    baseURL: 'http://localhost:4321',
    channel: 'chrome',
    headless: true,
    viewport: { width: 920, height: 1040 },
  },
  webServer: {
    command: 'node tests/e2e-env.mjs off && npm run prep && npx astro dev --port 4321',
    url: 'http://localhost:4321',
    reuseExistingServer: false,
    timeout: 120000,
  },
});

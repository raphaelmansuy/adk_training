import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright E2E Test Configuration
 * Tests the Docusaurus blog for the Interactions API article
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 60000,
  
  use: {
    baseURL: 'http://localhost:3000/adk_training',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  /* Run local dev server before starting tests */
  webServer: {
    command: 'npm run start -- --port 3000',
    url: 'http://localhost:3000/adk_training',
    reuseExistingServer: true,
    timeout: 120 * 1000,
  },
});

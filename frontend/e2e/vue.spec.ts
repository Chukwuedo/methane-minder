import { test, expect } from '@playwright/test';

test.describe('Dashboard E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173/');
  });

  test('shows the Risk Assessment section', async ({ page }) => {
    const header = page.locator('h3.card-title', { hasText: 'Risk Assessment' });
    await expect(header).toBeVisible();
  });

  test('renders circle markers on the map', async ({ page }) => {
    // Wait for at least one Leaflet marker
    await page.waitForSelector('.leaflet-interactive', { timeout: 10000 });
    const markers = await page.$$('.leaflet-interactive');
    expect(markers.length).toBeGreaterThan(0);
  });
});

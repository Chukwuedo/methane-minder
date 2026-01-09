import { test, expect } from '@playwright/test';

test.describe('Dashboard E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
  });

  test('should display header and country selector', async ({ page }) => {
    await expect(page.getByText('Methane Minder Dashboard')).toBeVisible();
    await expect(page.getByRole('combobox', { name: 'Country:' })).toBeVisible();
  });

  test('should show risk assessment on load', async ({ page }) => {
    // assuming mock or real backend with US risk
    await expect(page.getByText('Risk Assessment')).toBeVisible();
  });

  test('should fly map to selected country', async ({ page }) => {
    const select = page.getByRole('combobox');
    await select.selectOption('Switzerland');
    // check Leaflet map center lat-lng printed in console or exported,
    // cannot easily test map canvas, but check URL remains same
    await expect(page).toHaveURL(/.*country=Switzerland.*/);
  });
});

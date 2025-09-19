import { test, expect } from "@playwright/test";

test("homepage loads and shows title", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("h1")).toHaveText("QR Ticket Scanner");
});

test("upload ticket and get result", async ({ page }) => {
  await page.goto("/");

  const fileInput = page.locator('input[type="file"]');
  const [response] = await Promise.all([
  page.waitForResponse(resp =>
    resp.url().includes("/decode") && resp.status() === 200
  ),
  fileInput.setInputFiles("tests/fixtures/ticket2.jpg"),
]);

await expect(page.locator("h2")).toBeVisible();
});

test("camera UI opens", async ({ page }) => {
  await page.goto("/");
  await page.click("text=Open Camera");
  await expect(page.locator("button", { hasText: "Capture & Scan" })).toBeVisible();
  await expect(page.locator("button", { hasText: "Close Camera" })).toBeVisible();
});

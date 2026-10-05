const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const context = await browser.newContext({ bypassCSP: true });
  const page = await context.newPage();
  await page.route('**/*', route => route.continue());
  const logs = [];
  page.on('pageerror', err => logs.push('[PAGEERROR] ' + err.message));
  page.on('console', msg => { if (msg.type() === 'error') logs.push('[console] ' + msg.text()); });
  const resp = await page.goto('http://localhost:8080/exams?free_attempt=1&start=professional', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(4000);
  const diag = await page.evaluate(() => {
    const app = document.getElementById('app');
    return {
      status: 'ok',
      childCount: app ? app.childElementCount : -1,
      text: (app && app.innerText || '').slice(0, 400),
      body: (document.body.innerText || '').slice(0, 400),
    };
  });
  await page.screenshot({ path: 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_blank_debug.png', fullPage: true });
  console.log('NAV', resp.status());
  console.log('LOGS', logs.join('\n') || '(none)');
  console.log('DIAG', JSON.stringify(diag));
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });

const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage();
  const logs = [];
  page.on('console', msg => logs.push(`[${msg.type()}] ${msg.text()}`));
  page.on('pageerror', err => logs.push(`[PAGEERROR] ${err.message}\n${err.stack||''}`));
  page.on('requestfailed', req => logs.push(`[REQFAIL] ${req.url()} ${req.failure()?.errorText}`));
  const url = 'http://localhost:8080/exams?free_attempt=1&start=professional';
  const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  logs.push(`[NAV] status=${resp?.status()}`);
  await page.waitForTimeout(4000);
  const html = await page.content();
  let appText = '';
  try { appText = await page.locator('#app').innerText({ timeout: 2000 }); } catch { appText = '(empty/missing)'; }
  const bodyText = await page.evaluate(() => document.body ? document.body.innerText : '');
  await page.screenshot({ path: 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_blank_debug.png', fullPage: true });
  // Also evaluate React root / inertia
  const diag = await page.evaluate(() => {
    const app = document.getElementById('app');
    const pageEl = document.querySelector('script[data-page="app"]');
    let pageJsonOk = false, qCount = 0, incomplete = false;
    try {
      const raw = pageEl ? pageEl.textContent : '';
      incomplete = raw.includes('Incomplete_Class');
      const data = JSON.parse(raw);
      qCount = (data.props && data.props.questions) ? data.props.questions.length : -1;
      pageJsonOk = true;
    } catch (e) { return { parseError: String(e), appHtml: app ? app.innerHTML.slice(0,200) : null }; }
    return {
      pageJsonOk, qCount, incomplete,
      appChildCount: app ? app.childElementCount : -1,
      appHTML: app ? app.innerHTML.slice(0,300) : null,
      title: document.title,
    };
  });
  console.log('LOGS_START');
  logs.forEach(l => console.log(l));
  console.log('LOGS_END');
  console.log('DIAG=' + JSON.stringify(diag));
  console.log('APP_TEXT=' + JSON.stringify((appText||'').slice(0,500)));
  console.log('BODY_TEXT=' + JSON.stringify((bodyText||'').slice(0,800)));
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });

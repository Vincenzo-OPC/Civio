const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const p = await b.newPage();
  await p.goto('http://localhost:8080/exams?free_attempt=1&start=professional&v=noshield', { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(3500);
  // skip demographic questions to a sample one if needed - click next a few times
  for (let i = 0; i < 25; i++) {
    const text = await p.locator('body').innerText();
    if (text.includes('Sample Q') || text.includes('Which option is correct')) break;
    const next = p.getByRole('button', { name: /next|→|>/i }).first();
    if (await next.count()) await next.click().catch(()=>{});
    else {
      // keyboard
      await p.keyboard.press('ArrowRight').catch(()=>{});
    }
    await p.waitForTimeout(200);
  }
  const info = await p.evaluate(() => {
    const body = document.body.innerText;
    const buttons = [...document.querySelectorAll('button')].map(b => b.innerText.trim()).filter(Boolean).slice(0, 40);
    const options = [...document.querySelectorAll('[class*="option"], [data-option], button')].map(el => el.innerText.trim()).filter(t => /^[A-D]\b|Option /.test(t)).slice(0, 20);
    const q = (document.body.innerText.match(/Question[\s\S]{0,400}/)||[])[0];
    return { q, options, buttons, hasOptionA: body.includes('Option A'), hasABCD: /\nA\n|\nA\s/.test(body) };
  });
  await p.screenshot({ path: 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_options_debug.png', fullPage: false });
  console.log(JSON.stringify(info, null, 2));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });

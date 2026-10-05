const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ channel: 'chrome', headless: true });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('http://localhost:8080/exams?free_attempt=1&start=professional&v=noshield', { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2500);
  // Jump via palette to a later question that is sample (after demographics ~20)
  for (let i = 0; i < 30; i++) {
    await p.keyboard.press('ArrowRight');
    await p.waitForTimeout(100);
  }
  const text = await p.locator('body').innerText();
  console.log('AROUND_Q=', JSON.stringify(text.slice(text.indexOf('Question '), text.indexOf('Question ')+600)));
  // Count visible choice rows
  const choices = await p.evaluate(() => {
    const nodes = [...document.querySelectorAll('button, div, label')];
    return nodes
      .filter(n => /^[A-E]\s*$/.test((n.innerText||'').trim()) || /Option [A-D]/.test(n.innerText||'') || (n.innerText||'').includes('Public /'))
      .map(n => ({ tag: n.tagName, text: (n.innerText||'').trim().slice(0,80), cls: (n.className||'').toString().slice(0,80) }))
      .slice(0, 30);
  });
  console.log('CHOICES', JSON.stringify(choices, null, 2));
  await p.screenshot({ path: 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_sample_q.png' });
  // Also check active question from React if exposed - read from inertia page after build pool is hard
  // Check computed style of option area
  const styles = await p.evaluate(() => {
    const stem = [...document.querySelectorAll('p,div,h1,h2,h3')].find(el => (el.innerText||'').includes('Which option is correct') || (el.innerText||'').includes('Sample Q') || (el.innerText||'').includes('graduate from'));
    if (!stem) return { foundStem: false };
    let el = stem.parentElement;
    for (let i=0;i<5 && el;i++) {
      const btns = [...el.querySelectorAll('button')].map(b => ({t:b.innerText.trim().slice(0,60), display:getComputedStyle(b).display, visibility:getComputedStyle(b).visibility, opacity:getComputedStyle(b).opacity, h:b.getBoundingClientRect().height}));
      if (btns.length >= 4) return { foundStem: true, btns };
      el = el.parentElement;
    }
    return { foundStem: true, btns: 'none nearby' };
  });
  console.log('STYLES', JSON.stringify(styles, null, 2));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });

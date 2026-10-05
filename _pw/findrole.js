const fs = require('fs');
const p = 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_pw/app-built.js';
let t = fs.readFileSync(p, 'utf8');
const needles = ['Begin Exam', 'can_download_pdf'];
for (const n of needles) {
  let idx = 0, c = 0;
  while ((idx = t.indexOf(n, idx)) >= 0 && c < 5) {
    console.log('---', n, idx);
    console.log(JSON.stringify(t.slice(Math.max(0, idx - 150), idx + n.length + 100)));
    idx += n.length; c++;
  }
}
let m, count = 0;
const re = /\.user\.role/g;
while ((m = re.exec(t)) && count < 15) {
  console.log('user.role@', m.index, JSON.stringify(t.slice(m.index - 40, m.index + 60)));
  count++;
}

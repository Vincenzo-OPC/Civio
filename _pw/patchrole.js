const fs = require('fs');
const src = 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_pw/app-built.js';
let t = fs.readFileSync(src, 'utf8');
const before = (t.match(/f\.user\.role/g) || []).length;
t = t.split('f.user.role').join('f.user?.role');
// avoid double optional
t = t.split('f.user?.?.role').join('f.user?.role');
const after = (t.match(/f\.user\.role/g) || []).length;
const opt = (t.match(/f\.user\?\.role/g) || []).length;
fs.writeFileSync(src, t);
console.log({before, after, opt, size: t.length});
console.log('sample', JSON.stringify(t.slice(2895600, 2895800)));

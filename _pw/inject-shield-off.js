const fs = require('fs');
const p = 'C:/Users/GT/Desktop/Grok/Hiraya-Review/_pw/app-fixed.js';
let t = fs.readFileSync(p, 'utf8');
const start = 'function SZ(e={}){let{onCopyAttempt:t,onShieldActivate:n,contentLabel:r=`Exam`}=e,';
const inject = 'function SZ(e={}){if(typeof window!==`undefined`&&(location.hostname===`localhost`||location.hostname===`127.0.0.1`)){let R=(0,Y.useRef)(null);return{isShielded:!1,isResumeLocked:!1,dismissShield:()=>{},styleBlock:``,contentRef:R,wrapperProps:{onCopy:()=>{},onContextMenu:()=>{},onMouseDown:()=>{},onDragStart:()=>{}}}}let{onCopyAttempt:t,onShieldActivate:n,contentLabel:r=`Exam`}=e,';
if (!t.includes(start)) {
  console.log('START_NOT_FOUND');
  const i = t.indexOf('function SZ(e={})');
  console.log(JSON.stringify(t.slice(i, i+120)));
  process.exit(1);
}
if (t.includes('location.hostname===`localhost`')) {
  console.log('already injected');
} else {
  t = t.replace(start, inject);
  fs.writeFileSync(p, t);
  console.log('injected', t.length);
}

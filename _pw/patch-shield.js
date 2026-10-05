const fs = require('fs');
const p = 'C:/Users/GT/Desktop/Grok/Hiraya-Review/resources/js/pages/user/exams/hooks/use-content-shield.ts';
let t = fs.readFileSync(p, 'utf8');
if (t.includes('LOCAL_SHIELD_OFF')) {
  console.log('already patched');
  process.exit(0);
}
const re = /export function useContentShield\(\s*options: UseContentShieldOptions = \{\},\s*\): UseContentShieldReturn \{\s*const \{ onCopyAttempt, onShieldActivate, contentLabel = 'Exam' \} = options;/;
const insert = `export function useContentShield(
    options: UseContentShieldOptions = {},
): UseContentShieldReturn {
    // LOCAL_SHIELD_OFF — allow screenshots/study on Docker localhost
    const isLocalHost =
        typeof window !== 'undefined' &&
        (window.location.hostname === 'localhost' ||
            window.location.hostname === '127.0.0.1');
    const localContentRef = useRef<HTMLDivElement | null>(null);
    if (isLocalHost) {
        return {
            isShielded: false,
            isResumeLocked: false,
            dismissShield: () => {},
            styleBlock: '',
            contentRef: localContentRef,
            wrapperProps: {
                onCopy: () => {},
                onContextMenu: () => {},
                onMouseDown: () => {},
                onDragStart: () => {},
            },
        };
    }
    const { onCopyAttempt, onShieldActivate, contentLabel = 'Exam' } = options;`;
if (!re.test(t)) {
  console.log('pattern not found');
  const idx = t.indexOf('export function useContentShield');
  console.log(JSON.stringify(t.slice(idx, idx + 200)));
  process.exit(1);
}
t = t.replace(re, insert);
fs.writeFileSync(p, t);
console.log('patched ok');

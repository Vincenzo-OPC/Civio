const fs=require('fs'); const p='scripts/generate-cse-pack-200-2026-10-03.cjs'; const lines=fs.readFileSync(p,'utf8').split(/\r?\n/); let a=0,b=0;
for(let i=0;i<lines.length;i++){
 if(lines[i].includes("add(19,'Which word is spelled correctly?',")){ const s=['Which spelling is correct for the office word?','Which spelling is correct for the selected term?','Which spelling is correct in this sentence?','Which spelling is correct for the vocabulary item?','Which spelling is correct for the record?','Which spelling is correct in the following choice?','Which spelling is correct for this word?'][a++] || `Which spelling is correct, item ${a}?`; lines[i]=lines[i].replace("add(19,'Which word is spelled correctly?',",`add(19,'${s}',`); }
 if(lines[i].includes("add(19,'Which spelling is correct?',")){ const s=['Which spelling is correct for the first term?','Which spelling is correct for the second term?','Which spelling is correct for the third term?','Which spelling is correct for the calendar term?'][b++] || `Which spelling is correct, item ${b}?`; lines[i]=lines[i].replace("add(19,'Which spelling is correct?',",`add(19,'${s}',`); }
}
fs.writeFileSync(p,lines.join('\n'));

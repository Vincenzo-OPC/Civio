const fs = require('fs');
const p = 'scripts/generate-cse-pack-200-2026-10-03.cjs';
const lines = fs.readFileSync(p,'utf8').split(/\r?\n/);
for (let i=0;i<lines.length;i++) {
  if (lines[i].startsWith("add(6,'Piliin ang wastong gamit:")) lines[i] = `add(6,"Piliin ang wastong gamit: '_____ dumating ang pinuno, sinimulan ang pulong.'",['Nang','Ng','Nang sa','Kung'],0,'Ginagamit ang nang bilang pangatnig na nag-uugnay sa kilos at oras','ang ng ay pananda ng pagmamay-ari o layon, at hindi angkop ang iba sa pangungusap', 'Filipino');`;
  else if (lines[i].startsWith("add(6,'Piliin ang wastong salita:")) lines[i] = `add(6,"Piliin ang wastong salita: 'Mabuting _____ ang panukala bago ito pagtibayin.'",['subukin','subukan','sinubok','pagsubok'],1,'Ang subukan ay nangangahulugang tangkaing gawin o siyasatin ang isang bagay','ang subukin ay karaniwang may ibang gamit, habang ang dalawang anyo ay hindi angkop sa puwang');`;
  else if (lines[i].startsWith("add(7,'Alin ang wastong gamit ng")) lines[i] = `add(7,"Alin ang wastong gamit ng 'rin' at 'din'?",['Mabuti rin ang mungkahi niya.','Mabuti din ang mungkahi niya kapag patinig ang hulihan.','Mabuti rin ang mungkahi niya ay.','Mabuti din rin ang mungkahi niya.'],0,'Karaniwang ginagamit ang rin kapag patinig ang huling tunog ng naunang salita, gaya ng mabuti','ang ibang pangungusap ay may maling tuntunin o dobleng pang-abay');`;
  else if (lines[i].startsWith("add(10,'Basahin:")) lines[i] = `add(10,"Basahin: 'Maagang nagbukas ang tanggapan upang mapaglingkuran ang mga aplikante.' Ano ang dahilan ng maagang pagbubukas?",['Mapaglingkuran ang mga aplikante','Magsara nang mas maaga','Magdaos ng paligsahan','Magpalit ng gusali'],0,'Ang pariralang upang mapaglingkuran ang mga aplikante ay nagsasaad ng layunin','ang ibang sagot ay hindi binanggit o salungat sa pangungusap');`;
}
fs.writeFileSync(p, lines.join('\n'));

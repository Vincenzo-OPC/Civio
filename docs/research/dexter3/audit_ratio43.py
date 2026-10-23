#!/usr/bin/env python3
"""Exact-rational audit of 29 share questions and 14 mixed ratio/proportion items."""
import collections,gzip,json,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
STATE=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
def fnum(s):return F(s.replace(',',''))
def ratios(s):
 m=re.search(r'(?:ratio(?: of)?\s*)?([\d,]+)\s*(?::|-to-|\bto\b)\s*([\d,]+)(?:\s*(?::|\bto\b)\s*([\d,]+))?',s,re.I)
 if not m:return None
 return [int(m[i].replace(',','')) for i in range(1,4) if m[i]]
def solve(fam,s):
 r=ratios(s)
 if not r:
  direct=re.search(r'uses (\d+) cups of syrup for every (\d+) cups of water',s,re.I)
  if direct:r=[int(direct[1]),int(direct[2])]
  else:return None
 if fam=='two-share-total-candidate':
  m=re.search(r'₱\s*([\d,]+)',s)
  if not m:return None
  total=fnum(m[1]);parts=sum(r);return total*F(r[1],parts),'two-person-share-of-total',{'total':str(total),'parts':r,'selected_part':2}
 # Three-part allocation from a known total, usually asking for one labeled share.
 if len(r)==3:
  m=re.search(r'([\d,]+)\s+seedlings',s,re.I)
  if not m:m=re.search(r'₱\s*([\d,]+)',s)
  if not m:m=re.search(r'(?:It has|has|pack)\s*([\d,]+)',s,re.I)
  if not m:m=re.search(r'(\d+) (?:kits|bags)\b',s,re.I)
  if m:
   total=fnum(m[1]);which=3 if re.search(r'(?:largest|third area|third share)',s,re.I) else 2
   if re.search(r'middle share',s,re.I):which=2
   if 'volunteers pack' in s.lower():which=2
   return total*F(r[which-1],sum(r)),'three-part-total-allocation',{'total':str(total),'parts':r,'selected_part':which}
  # Same ratio can allocate outputs in proportion to hours.
  m=re.search(r'(\d+) volunteers? pack (\d+) .*? in the ratio',s,re.I)
  if m:
   total=fnum(m[2]);which=2
   return total*F(r[which-1],sum(r)),'output-allocated-by-ratio',{'total':str(total),'parts':r,'selected_part':which}
 # Ratio parts and known quantity for a named component.
 if 'women' in s.lower() and re.search(r'men to women',s,re.I):
  m=re.search(r'(\d+) women',s,re.I)
  if m:return F(int(m[1])*r[0],r[1]),'known-second-part-to-first',{'ratio':r,'known_second':int(m[1])}
 if len(r)==2 and 'coffee sacks' in s.lower():
  m=re.search(r'(\d+) coffee sacks',s,re.I)
  if m:return F(int(m[1])*r[1],r[0]),'known-first-part-to-second',{'ratio':r,'known_first':int(m[1])}
 if len(r)==2 and 'nurses to midwives' in s.lower():
  m=re.search(r'(\d+) nurses',s,re.I)
  if m:return F(int(m[1])*r[1],r[0]),'known-first-part-to-second',{'ratio':r,'known_first':int(m[1])}
 m=re.search(r'(?:ratio of|ratio between)\s+([\w ]+?)\s+(?:and|to)\s+([\w ]+?)(?:\s+is|\s+are|\s+in|\s*,|\.)',s,re.I)
 if m:
  left,right=m[1].strip().lower(),m[2].strip().lower()
  nums=list(re.finditer(r'(?<!\w)(\d+)\s+([a-z][a-z -]+)',s,re.I))
  for n in nums:
   phrase=n[2].strip().lower().rstrip('s')
   if phrase in left or left.rstrip('s') in phrase:
    return F(int(n[1]))*F(r[1],r[0]),'known-first-part-to-second',{'ratio':r,'known_first':int(n[1])}
   if phrase in right or right.rstrip('s') in phrase:
    return F(int(n[1]))*F(r[0],r[1]),'known-second-part-to-first',{'ratio':r,'known_second':int(n[1])}
 # Raise the smaller of two total parts to equal the larger.
 if len(r)==2 and re.search(r'added to the smaller team to match',s,re.I):
  m=re.search(r'together they have (\d+)',s,re.I)
  if m:return F(int(m[1])*abs(r[1]-r[0]),sum(r)),'difference-to-equalize-ratio-groups',{'ratio':r,'total':int(m[1])}
 # Difference fixes the scale, for explicitly described two-part groups.
 m=re.search(r'are (\d+) years? older|is (\d+) years? more|received (\d+) more',s,re.I)
 if not m:m=re.search(r'(\d+) more (?:letters|crates)',s,re.I)
 if m and len(r)==2:
  diff=int(next(x for x in m.groups() if x));scale=F(diff,abs(r[0]-r[1]));
  if 'older' in s.lower():idx=0
  elif 'letters' in s.lower() and 'first office' in s.lower():idx=0
  elif 'crates' in s.lower():return scale*abs(r[0]-r[1]),'difference-to-equalize-ratio-groups',{'ratio':r,'difference':diff}
  else:idx=0
  return scale*r[idx],'known-difference-between-ratio-parts',{'ratio':r,'difference':diff,'selected_part':idx+1}
 # A stated older-younger age gap sets the scale of a two-part ratio.
 if len(r)==2 and re.search(r'older one is (\d+) years older',s,re.I):
  m=re.search(r'older one is (\d+) years older',s,re.I)
  if m:return F(int(m[1])*r[0],r[0]-r[1]),'age-ratio-from-difference',{'ratio':r,'age_difference':int(m[1]),'selected_part':1}
 # Direct scale between two quantities where one component count is known.
 if 'water' in s.lower() and 'syrup' in s.lower():
  matches=re.findall(r'(\d+) cups of water',s,re.I)
  if matches:
   known=int(matches[-1]);return F(known*r[0],r[1]),'direct-proportion-known-second-part',{'ratio':r,'known_second':known}
 # Total of two ratio shares, target smaller/larger specified.
 # Total divided between two categories, including non-currency totals.
 m=re.search(r'(\d+) (?:stools|crates|letters|bags|kits) in all|Together they have (\d+) (?:crates)',s,re.I)
 if m and len(r)==2:
  total=int(next(x for x in m.groups() if x));idx=0 if re.search(r'(?:smaller|smallest|first office)',s,re.I) else 1
  return F(total*r[idx],sum(r)),'two-part-total-allocation',{'total':total,'ratio':r,'selected_part':idx+1}
 # Two-part money or amount shares in the smaller ratio-only review pool.
 if len(r)==2:
  m=re.search(r'₱\s*([\d,]+)',s)
  if m:
   total=fnum(m[1]);idx=min(range(2),key=lambda i:r[i]) if re.search(r'smaller share',s,re.I) else 1
   return total*F(r[idx],sum(r)),'two-part-total-allocation',{'total':str(total),'ratio':r,'selected_part':idx+1}
 # Syrup/water and count-known generic phrasing.
 m=re.search(r'(\d+) (cups|sacks|kits|women|nurses|coffee sacks|letters|volunteers)',s,re.I)
 if m and len(r)==2:
  value=int(m[1]);unit=m[2].lower()
  if 'water' in s.lower(): return F(value*r[0],r[1]),'direct-proportion-known-second-part',{'ratio':r,'known_second':value}
  if 'coffee' in s.lower() or 'men to women' in s.lower() or 'nurses to midwives' in s.lower():return F(value*r[1],r[0]),'direct-proportion-known-first-part',{'ratio':r,'known_first':value}
 return None
def optval(s):
 m=re.search(r'₱\s*([\d,]+(?:\.\d+)?)',s)
 if not m:m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',s)
 if not m:raise ValueError(s)
 return F((m[1] if m.lastindex else m.group()).replace(',',''))
def main():
 cache={};rows=[]
 for fam in ('two-share-total-candidate','NUM-WP-RATIO'):
  for r in [x for x in STATE['records'] if x['work_family']==fam]:
   if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
   q=cache[r['source_file']][r['question_id']];res=solve(fam,q['stem']);opts={o['option_id']:o['text'] for o in q['options']}
   if res is None:calc=method=params=None;matches=[]
   else:calc,method,params=res;matches=[i for i,t in opts.items() if optval(t)==calc]
   key=q['answer_option_id'];sig=(method,json.dumps(params,sort_keys=True)) if res else None
   rows.append({'question_id':q['id'],'status':q['status'],'source_file':r['source_file'],'source_record_sha256':r['source_record_sha256'],'family':fam,'stem':q['stem'],'method':method,'parameters':params,'calculated_answer':str(calc) if calc is not None else None,'key_option_id':key,'key_text':opts.get(key),'matching_options':matches,'key_matches':bool(calc is not None and matches==[key]),'wrong_choice_feedback_present':all(o['option_id']==key or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'duplicate_signature':json.dumps(sig,sort_keys=True) if sig else None,'manual_review':None if calc is not None else 'No supported exact ratio parser; manual solution required'})
 groups=collections.defaultdict(list)
 for x in rows:
  if x['duplicate_signature']:groups[x['duplicate_signature']].append(x['question_id'])
 repeated=[{'question_ids':v,'parameters':json.loads(k)} for k,v in groups.items() if len(v)>1]
 pilot=json.loads((D/'pilot-v0.1.json').read_text());overlay=json.loads((D/'math25-v0.1.json').read_text());covered={b['question_id'] for b in pilot['bindings']}|{b['question_id'] for b in overlay['bindings']}
 for x in rows:x['existing_tutoring_binding']=x['question_id'] in covered
 summary={'record_count':len(rows),'statuses':dict(collections.Counter(x['status'] for x in rows)),'families':dict(collections.Counter(x['family'] for x in rows)),'methods':dict(collections.Counter(x['method'] or 'manual' for x in rows)),'exact_calculations':sum(x['calculated_answer'] is not None for x in rows),'key_matches':sum(x['key_matches'] for x in rows),'key_conflicts':sum(x['calculated_answer'] is not None and not x['key_matches'] for x in rows),'manual_required':sum(x['calculated_answer'] is None for x in rows),'missing_wrong_choice_feedback':sum(not x['wrong_choice_feedback_present'] for x in rows),'approved_already_bound':sum(x['status']=='approved' and x['existing_tutoring_binding'] for x in rows),'approved_unbound':sum(x['status']=='approved' and not x['existing_tutoring_binding'] for x in rows),'parameter_repeat_groups':repeated,'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
 artifact={'schema_version':'dexter-ratio43-audit-v0.1','baseline_commit':'32db7861a2d89435c4019a3a7a66b41dd4fd604a','method':'Exact rational parts-total, known-part and known-difference calculations; source pilot and math overlays reconciled to avoid duplicate tutoring bindings. Unsupported forms remain manual.','summary':summary,'items':rows}
 (D/'ratio43-audit-v0.1.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()

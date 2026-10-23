#!/usr/bin/env python3
"""Exact arithmetic audit of fraction, decimal, percent and basic-operation records."""
import collections,gzip,json,math,re
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent
S=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
FAMILIES={'NUM-FRAC-DEC','NUM-OPS-FRAC-DEC','NUM-PCT-BASIC','NUM-DECIMAL','NUM-PROPERTY'}
def val(t):
 t=t.strip().replace(',','').replace('−','-').replace('₱','')
 m=re.fullmatch(r'(-?)(\d+)\s+(\d+)/(\d+)(?:\s+.*)?',t)
 if m:
  sign=-1 if m[1] else 1;return sign*(F(int(m[2]))+F(int(m[3]),int(m[4])))
 m=re.match(r'(-?\d+\s*/\s*\d+|-?\d+(?:\.\d+)?)',t)
 if not m:raise ValueError(t)
 return F(m[1].replace(' ',''))
def nums(s):return [F(int(a),int(b)) for a,b in re.findall(r'(\d+)\s*/\s*(\d+)',s)]
def solve(s):
 # sequential fractions of the remaining stock
 p=re.search(r'had ([\d,]+) [^.]+\. In the morning (?:she )?(?:checks|scans) (\d+/\d+) of them, and in the afternoon (?:she )?(?:encodes|labels) (\d+/\d+) of the remaining',s,re.I)
 if p:return F(p[1].replace(',',''))*(1-val(p[2]))*(1-val(p[3])),'sequential-fractions-of-remaining'
 p=re.search(r'used (\d+/\d+) of a ([\d,]+)-sheet ream on Monday and (\d+/\d+) of the same ream on Tuesday',s,re.I)
 if p:return F(p[2].replace(',',''))*(1-val(p[1])-val(p[3])),'fractions-of-the-same-whole-remaining'
 p=re.search(r'had ([\d,]+) [^.]+\. It gave out (\d+/\d+) of them.*? and (\d+/\d+) of the remaining',s,re.I)
 if p:
  total=F(p[1].replace(',',''));a,b=nums(p[2]+' '+p[3]);return total*(1-a)*(1-b),'successive-fractions-of-remaining'
 p=re.search(r'pour(?:s|ed) (\d+\s+\d+/\d+|\d+/\d+) liter.*? (\d+\s+\d+/\d+|\d+/\d+) liter.*?(?:in all|total)',s,re.I)
 if p:return val(p[1])+val(p[2]),'add-fractions-with-common-unit'
 p=re.search(r'was (\d+\s+\d+/\d+|\d+/\d+) meters? deep.*?lowered.*?by (\d+\s+\d+/\d+|\d+/\d+)',s,re.I)
 if p:return val(p[1])-val(p[2]),'subtract-measurement-fractions'
 p=re.search(r'of (\d+) seats.*?(\d+/\d+) are reserved',s,re.I)
 if p:return F(int(p[1]))*val(p[2]),'fraction-of-a-whole-count'
 p=re.search(r'fraction in simplest form is equal to (0\.\d+)',s,re.I)
 if p:
  d=p[1];return F(d),'decimal-to-fraction-equivalence'
 p=re.search(r'represents the same distance',s,re.I)
 if p:
  m=re.search(r'(\d+)\s+(\d+)/(\d+)',s);return F(int(m[1])*int(m[3])+int(m[2]),int(m[3])),'mixed-to-improper-fraction'
 p=re.search(r'(\d+) blankets.*?held (\d+/\d+) of all the blankets',s,re.I)
 if p:return F(int(p[1]))/val(p[2]),'recover-whole-from-fractional-part'
 p=re.search(r'(\d+\s+\d+/\d+|\d+/\d+) liters?.*?Each serving is (\d+/\d+) liter',s,re.I)
 if p:return val(p[1])/val(p[2]),'divide-quantity-by-unit-fraction'
 p=re.search(r'collected (\d+\s+\d+/\d+) kilograms?.*?and (\d+\s+\d+/\d+) kilograms?.*?combined',s,re.I)
 if p:return val(p[1])+val(p[2]),'add-mixed-numbers'
 p=re.search(r'finished (\d+/\d+) of a shoreline.*?another (\d+/\d+).*?What fraction remains',s,re.I)
 if p:return 1-val(p[1])-val(p[2]),'remaining-fraction-after-two-parts'
 p=re.search(r'(\d+) seedlings\. Two thirds are native trees, and (\d+/\d+) of those native trees',s,re.I)
 if p:return F(int(p[1]))*F(2,3)*val(p[2]),'fraction-of-a-fraction'
 p=re.search(r'long\. Surveyors have measured (\d+/\d+) of it',s,re.I)
 if p:
  whole=re.search(r'long',s);length=re.search(r'(\d+)\s+(?:2/3|\d+/\d+) kilometers?',s,re.I)
  mixed=re.search(r'(\d+)\s+(\d+)/(\d+) kilometers?',s,re.I)
  return F(int(mixed[1])*int(mixed[3])+int(mixed[2]),int(mixed[3]))*val(p[1]),'fraction-of-measured-length'
 p=re.search(r'had (\d+\s+\d+/\d+) kilograms? of rice and cooked (\d+\s+\d+/\d+)',s,re.I)
 if p:return val(p[1])-val(p[2]),'subtract-mixed-numbers'
 p=re.search(r'of (\d+) employees, (\d+/\d+) ride',s,re.I)
 if p:return F(int(p[1]))*val(p[2]),'fraction-of-a-whole-count'
 p=re.search(r'(\d+)[ -]meter roll.*?strips, each (\d+/\d+) meter',s,re.I)
 if p:return F(int(p[1]))/val(p[2]),'divide-length-by-strip-length'
 p=re.search(r'spent ₱([\d,]+).*?which is (\d+/\d+) of its .*?budget',s,re.I)
 if p:return F(p[1].replace(',',''))/val(p[2]),'recover-whole-budget-from-fraction'
 p=re.search(r'(\d+) of (\d+).*?What percentage',s,re.I)
 if p:return F(int(p[1]),int(p[2]))*100,'part-over-whole-as-percent'
 p=re.search(r'percentage of all attendees completed a survey',s,re.I)
 if p:
  ns=list(map(int,re.findall(r'(\d+)% of (\d+)',s)[0]));n2=list(map(int,re.findall(r'(\d+)% of (\d+)',s)[1]));return F(ns[0]*ns[1]+n2[0]*n2[1],ns[1]+n2[1]),'weighted-group-percentages'
 p=re.search(r'gave vitamins to (\d+)% of (\d+).*?reached (\d+)% of (\d+).*?How many more',s,re.I)
 if p:
  a,b,c,d=map(int,p.groups());return F(c*d-a*b,100),'compare-percentages-with-different-wholes'
 p=re.search(r'(?:received|budget of|sets aside) (?:₱)?([\d,]+)(?: thousand pesos)?(?:.*?)(\d+(?:\.\d+)?)% (?:for|of)',s,re.I)
 if p:return F(p[1].replace(',',''))*F(p[2])/100,'percentage-of-given-base'
 p=re.search(r'(\d+(?:\.\d+)?)% commission on ₱([\d,]+)',s,re.I)
 if p:return F(p[1])*F(p[2].replace(',',''))/100,'percent-of-a-money-base'
 p=re.search(r'After a (\d+)% raise.*? is ₱([\d,]+)',s,re.I)
 if p:return F(p[2].replace(',',''))/(1+F(p[1])/100),'reverse-percentage-after-increase'
 p=re.search(r'ratio (\d+)\s*:\s*(\d+).*?fraction of all the items are',s,re.I)
 if p:return F(int(p[1]),int(p[1])+int(p[2])),'ratio-part-over-total-parts'
 p=re.search(r'(?:had|has) ([\d,]+) [^.]+\. In the morning (?:she |it )?(?:checks|scans) (\d+/\d+) of them, and in the afternoon (?:she |it )?(?:encodes|labels) (\d+/\d+) of the remaining',s,re.I)
 if p:return F(p[1].replace(',',''))*(1-val(p[2]))*(1-val(p[3])),'sequential-fractions-of-remaining'
 p=re.search(r'(\d+(?:\.\d+)?) out of (\d+).*?What percentage',s,re.I)
 if p:return F(p[1])/F(p[2])*100,'part-over-whole-as-percent'
 p=re.search(r'(\d+) documents, which is (\d+(?:\.\d+)?)% of the assigned',s,re.I)
 if p:return F(int(p[1]))/(F(p[2])/100),'recover-whole-from-percent'
 p=re.search(r'(\d+\s+\d+/\d+|\d+/\d+)\s*×\s*(\d+/\d+)',s)
 if p:return val(p[1])*val(p[2]),'fraction-multiplication'
 p=re.search(r'(\d+/\d+)\s*\+\s*(\d+/\d+)',s)
 if p:return val(p[1])+val(p[2]),'fraction-addition'
 p=re.search(r'one (\d+/\d+) meter long and one (\d+/\d+) meter long',s,re.I)
 if p:return val(p[1])+val(p[2]),'add-board-lengths'
 p=re.search(r'(\d+(?:\.\d+)?) kilograms? of flour for (\d+/\d+)-kilogram sample bags',s,re.I)
 if p:return F(p[1])/val(p[2]),'divide-total-by-unit-fraction'
 p=re.search(r'filled four identical containers to (.*?) of their capacity',s,re.I)
 if p:
  fs=nums(p[1]);return max(fs),'compare-fractions'
 p=re.search(r'Which number is the greatest\? (.*)',s,re.I)
 if p:
  opts=[F(x) for x in re.findall(r'\d+/\d+|\d+\.\d+',p[1])];return max(opts),'compare-fractions-and-decimals'
 p=re.search(r'(\d+) as a fraction in lowest terms',s,re.I)
 if p:
  d=str(int(p[1]));return F('0.'+d),'decimal-to-fraction'
 p=re.search(r'Evaluate (\d+)⁽?(\d+)⁾?',s)
 if p:return F(int(p[1])**int(p[2])),'integer-power'
 p=re.search(r'Evaluate (\d+)⁵',s)
 if p:return F(int(p[1])**5),'integer-power'
 p=re.search(r'(\d+(?:\.\d+)?)\s*×\s*(\d+(?:\.\d+)?)',s)
 if p:return F(p[1])*F(p[2]),'decimal-multiplication'
 p=re.search(r'(\d+(?:\.\d+)?)\s*÷\s*(\d+(?:\.\d+)?)',s)
 if p:return F(p[1])/F(p[2]),'decimal-division'
 p=re.search(r'(\d+)\s*\+\s*(\d+)',s)
 if p:return F(int(p[1])+int(p[2])),'addition'
 p=re.search(r'(\d+)\s*−\s*(\d+)',s)
 if p:return F(int(p[1])-int(p[2])),'subtraction'
 p=re.search(r'(\d+)\s*×\s*(\d+)',s)
 if p:return F(int(p[1])*int(p[2])),'multiplication'
 p=re.search(r'(\d+)\s*÷\s*(\d+)',s)
 if p:return F(int(p[1]),int(p[2])),'division'
 p=re.search(r'(\d+)\s*\^\s*(\d+)',s)
 if p:return F(int(p[1])**int(p[2])),'integer-power'
 p=re.search(r'LCM\) of (\d+) and (\d+)',s,re.I)
 if p:return F(math.lcm(int(p[1]),int(p[2]))),'least-common-multiple'
 p=re.search(r'GCF\) of (\d+) and (\d+)',s,re.I)
 if p:return F(math.gcd(int(p[1]),int(p[2]))),'greatest-common-factor'
 p=re.search(r'multiplied by itself, gives (\d+)',s,re.I)
 if p:
  n=math.isqrt(int(p[1]));return F(n),'perfect-square-root' if n*n==int(p[1]) else None
 p=re.search(r'What is (\d+(?:\.\d+)?) × (\d+(?:\.\d+)?)',s)
 if p:return F(p[1])*F(p[2]),'decimal-times-integer'
 # A fractional part of the remaining starting quantity.
 return None,None

def answer(t):
 t=t.strip().replace(',','').replace('₱','')
 m=re.fullmatch(r'(\d+)\s+(\d+)/(\d+)(?:\s+.*)?',t)
 if m:return F(int(m[1])*int(m[3])+int(m[2]),int(m[3]))
 m=re.match(r'(-?\d+\s*/\s*\d+|-?\d+(?:\.\d+)?)',t)
 if not m:raise ValueError(t)
 return F(m[1].replace(' ',''))

def main():
 cache={};out=[]
 for r in S['records']:
  if r['work_family'] not in FAMILIES:continue
  if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
  q=cache[r['source_file']][r['question_id']];calc,method=solve(q['stem']);opts={o['option_id']:answer(o['text']) for o in q['options']};key=opts[q['answer_option_id']];matches=[i for i,v in opts.items() if v==calc] if calc is not None else []
  out.append({'question_id':q['id'],'source_record_sha256':r['source_record_sha256'],'source_status':r['bank_status'],'work_family':r['work_family'],'stem':q['stem'],'method':method,'calculation':str(calc) if calc is not None else None,'key_value':str(key),'key_matches':matches==[q['answer_option_id']],'matching_options':matches,'wrong_choice_explanation_coverage':all(o['option_id']==q['answer_option_id'] or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'manual_review':None if calc is not None else 'No exact parser method matched; manual solution required'})
 summ={'records':len(out),'groups':dict(collections.Counter(r['work_family'] for r in out)),'statuses':dict(collections.Counter(r['source_status'] for r in out)),'deterministic_calculations':sum(r['calculation'] is not None for r in out),'keys_matching':sum(r['key_matches'] for r in out),'key_conflicts':sum(r['calculation'] is not None and not r['key_matches'] for r in out),'manual_solution_required':sum(r['calculation'] is None for r in out),'wrong_choice_rationales_missing':sum(not r['wrong_choice_explanation_coverage'] for r in out),'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
 (D/'foundation65-audit-v0.1.json').write_text(json.dumps({'schema_version':'dexter-foundation73-audit-v0.1','baseline_commit':'d215839e34884296e61bdce7c16961df02f0a74a','method':'Exact rational arithmetic on recognized stem templates; no guessed results for unsupported forms.','summary':summ,'items':out},ensure_ascii=False,indent=2)+'\n');print(json.dumps(summ))
if __name__=='__main__':main()

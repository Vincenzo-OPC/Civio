#!/usr/bin/env python3
"""Exact template-based audit of average, geometry and elementary word-algebra pools."""
import gzip,json,re,hashlib,collections
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent
STATE=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
def number_options(q):return {o['option_id']:F(re.sub(r'[^0-9./-]','',o['text'].split()[0])) for o in q['options']}
def check(key_id,opts,val):return [i for i,v in opts.items() if v==val]==[key_id]
def calc_average(s):
 m=re.search(r'average (?:age|years of service) of the (\d+) .*? is (\d+).*?\. .*?(?:who is|with) (\d+)',s,re.I)
 if m:return ((int(m[1])*int(m[2])+int(m[3]))/F(int(m[1])+1),'new-member-average')
 m=re.search(r'average cost per kilogram of the mixture',s,re.I)
 if m:
  a=re.search(r'blends (\d+) kilograms.*?₱([\d,]+) per kilogram with (\d+) kilograms costing ₱([\d,]+) per kilogram',s,re.I)
  if a:return (F(int(a[1])*int(a[2].replace(',',''))+int(a[3])*int(a[4].replace(',','')),int(a[1])+int(a[3])),'weighted-mixture-average')
 m=re.search(r'What score does he need .*? average (\d+)',s,re.I)
 if m:
  vals=list(map(int,re.findall(r'\d+',re.search(r'scored (.*?) on three quizzes',s,re.I)[1])))
  return (F(4*int(m[1])-sum(vals)),'unknown-value-for-target-average')
 m=re.search(r'How many must it serve on the fifth day to average (\d+)',s,re.I)
 if m:
  vals=list(map(int,re.findall(r'\d+',s.split('served ',1)[1].split(' patients',1)[0])));return (F(5*int(m[1])-sum(vals)),'unknown-value-for-target-average')
 return None

def calc_geometry(s):
 p=re.search(r'(\d+) m long and (\d+) m wide',s,re.I)
 if p:
  l,w=map(int,p.groups());cost=re.search(r'costs? ₱([\d,]+) per meter',s,re.I)
  if cost and re.search(r'cost to put .*? around the whole',s,re.I):return (F(2*(l+w)*int(cost[1].replace(',',''))),'perimeter-times-cost-per-meter')
  if re.search(r'how many meters of fence',s,re.I):return (F(2*(l+w)),'rectangular-perimeter')
 p=re.search(r'(?:a )?straight (?:fence|path) (\d+) ?m(?:eter)? long gets? (?:a )?(?:post|tree) every (\d+) ?m',s,re.I)
 if not p:p=re.search(r'Along a (\d+)[ -]meter straight path.*?plants a tree every (\d+) meters',s,re.I)
 if p:
  length,gap=map(int,p.groups());return (F(length,gap)+1,'intervals-plus-one-including-both-ends')
 return None

def calc_algebra(s):
 word_num={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
 # Age relationship: older is r times younger; apply future multiplier after t years.
 ratio={'twice':2,'three times':3,'four times':4}
 p=re.search(r'is (\d+) times as old.*?In (\d+) years?, .*? (twice|three times|four times) as old',s,re.I)
 if p:
  r,t,q=int(p[1]),int(p[2]),ratio[p[3].lower()];younger=F(t*(q-1),r-q);return (younger*r,'age-ratio-forward-time')
 p=re.search(r'mother is (\d+) years older than her son\. (\w+) years ago, the mother was (\w+) times as old as her son',s,re.I)
 if p:
  gap,t=int(p[1]),word_num.get(p[2].lower(),int(p[2]) if p[2].isdigit() else 0);mult=ratio.get(p[3].lower()+' times',2 if p[3].lower()=='four' else None)
  if p[3].lower()=='four':mult=4
  return (F(gap+(mult-1)*t,mult-1),'age-difference-relation-past')
 p=re.search(r'Two cousins are (\d+) years apart\. (\w+) years from now their ages will total (\d+)',s,re.I)
 if p:
  gap=int(p[1]);t=word_num.get(p[2].lower(),int(p[2]) if p[2].isdigit() else 0);total=int(p[3]);return (F(total-2*t-gap,2),'age-difference-and-future-sum')
 p=re.search(r'(?:multiplies it by|multiplied by) (\d+).*?subtracts? (\d+).*?(?:gets|result is) (\d+)',s,re.I)
 if p:
  a,b,c=map(int,p.groups());return (F(c+b,a),'linear-inverse-operation')
 p=re.search(r'delivery contained (\d+) folders more than the morning count\. The delivery count was (\d+)',s,re.I)
 if p:return (F(int(p[2])-int(p[1])),'unknown-start-after-increase')
 p=re.search(r'(?:three|3) identical bundles\. Each bundle contains some beads and (\w+) spacers\. Across the three bundles there are (\d+) pieces',s,re.I)
 if p:
  spword,total=p.groups();sp={'four':4,'three':3,'two':2,'one':1}.get(spword.lower());sp=sp if sp is not None else int(spword) if spword.isdigit() else 0;return (F(int(total),3)-sp,'repeated-equal-groups')
 p=re.search(r'Two (?:delivery )?routes cover (\d+) kilometers in total\. One route is (\d+) kilometers longer',s,re.I)
 if p:
  total,d=map(int,p.groups());return (F(total+d,2),'sum-and-difference-larger-value')
 p=re.search(r'Two consecutive even apartment numbers add up to (\d+)',s,re.I)
 if p:return (F(int(p[1]),2)+1,'consecutive-even-number-pair')
 p=re.search(r'charges ₱(\d+) to set up.*?₱(\d+) per booklet\. .*?paid ₱(\d+)',s,re.I)
 if p:
  setup,unit,total=map(int,p.groups());return (F(total-setup,unit),'fixed-fee-plus-unit-cost')
 p=re.search(r'sold (\d+) kilograms.*?remaining stock was (\d+) kilograms more than half the starting stock',s,re.I)
 if p:
  sold,b=map(int,p.groups());return (F(sold+b)*2,'remaining-equals-half-start-plus-offset')
 p=re.search(r'two trays with x beads and (\d+) labels in each tray, plus a third bag with x beads only\. Altogether there are (\d+) pieces',s,re.I)
 if p:
  labels,total=map(int,p.groups());return (F(total-2*labels,3),'collect-like-terms')
 p=re.search(r'(?:adds up to|is) (\d+)\. What is the largest of the three\?',s,re.I)
 if p:return (F(int(p[1]),3)+2,'three-consecutive-odd-integers')
 p=re.search(r'Four consecutive whole numbers add up to (\d+)',s,re.I)
 if p:return (F(int(p[1])-6,4),'four-consecutive-integers')
 p=re.search(r'Two numbers add up to (\d+), and one is (\d+) times the other\. What is the smaller',s,re.I)
 if p:
  total,mul=map(int,p.groups());return (F(total,mul+1),'sum-and-multiple')
 p=re.search(r'classrooms in all\. The new building has (\d+) times as many classrooms as the old one',s,re.I)
 if p:
  mul=int(p[1]);total=int(re.search(r'have (\d+) classrooms in all',s,re.I)[1]);return (F(total,mul+1),'part-to-whole-multiplicative-relation')
 p=re.search(r'Two numbers add up to (\d+), and one is (\d+) more than the other\. What is the larger',s,re.I)
 if p:
  total,d=map(int,p.groups());return (F(total+d,2),'sum-and-difference-larger-value')
 p=re.search(r'Solve for x: (\d+)x ([+-]) (\d+) = (\d+)',s,re.I)
 if p:
  a,op,b,c=int(p[1]),p[2],int(p[3]),int(p[4]);return (F(c-b if op=='+' else c+b,a),'one-step-linear-equation')
 p=re.search(r'fare as (\d+)x \+ (\d+) = (\d+)',s,re.I)
 if p:
  a,b,c=map(int,p.groups());return (F(c-b,a),'linear-fare-model')
 p=re.search(r'tripled and (\d+) is subtracted, the result is (\d+)',s,re.I)
 if p:return (F(int(p[2])+int(p[1]),3),'inverse-order-of-operations')
 p=re.search(r'3 identical sets of forms\. Each set has x forms after (\d+) damaged forms are removed\. If the three sets contain (\d+) usable forms',s,re.I)
 if p:
  damaged,total=map(int,p.groups());return (F(total,3)+damaged,'equation-within-equal-groups')
 p=re.search(r'has ₱([\d,]+) for refreshments\. It buys (\d+) sandwiches at ₱([\d,]+) each and (\d+) water bottles at ₱([\d,]+) each',s,re.I)
 if p:
  budget,n1,c1,n2,c2=(int(x.replace(',','')) for x in p.groups());return (F(budget-n1*c1-n2*c2),'budget-minus-item-costs')
 return None

def loadq(r,cache):
 if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
 return cache[r['source_file']][r['question_id']]
def main():
 cache={};rows=[]
 for fam,fn in [('NUM-WP-AVERAGE',calc_average),('NUM-WP-GEOM',calc_geometry),('NUM-WP-ALGEBRA',calc_algebra)]:
  for r in [x for x in STATE['records'] if x['work_family']==fam]:
   q=loadq(r,cache);calc=fn(q['stem']);opts=number_options(q);key=opts[q['answer_option_id']]
   rows.append({'question_id':q['id'],'source_record_sha256':r['source_record_sha256'],'status':r['bank_status'],'family':fam,'stem':q['stem'],'key':str(key),'calculation':str(calc[0]) if calc else None,'method':calc[1] if calc else None,'key_matches':bool(calc and calc[0]==key and check(q['answer_option_id'],opts,calc[0])),'single_matching_option':bool(calc and check(q['answer_option_id'],opts,calc[0])),'all_distractor_rationales_present':all(o['option_id']==q['answer_option_id'] or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'manual_review':None if calc else 'No supported deterministic stem template; manual solution required'})
 duplicate=collections.defaultdict(list)
 for x in rows:
  # Remove personal names, organizations and numeric values to expose repeated template frames.
  sig=re.sub(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b','NAME',x['stem']);sig=re.sub(r'\d+','N',sig);duplicate[(x['family'],sig)].append(x['question_id'])
 result={'schema_version':'dexter-word-math87-audit-v0.1','baseline_commit':'c2f003c6746573e82d8d07ec1206b9ad22aad3ef','summary':{'record_count':len(rows),'by_family':dict(collections.Counter(x['family'] for x in rows)),'bank_statuses':dict(collections.Counter(x['status'] for x in rows)),'supported_calculation_checks':sum(x['calculation'] is not None for x in rows),'key_matches':sum(x['key_matches'] for x in rows),'key_conflicts':sum(x['calculation'] is not None and not x['key_matches'] for x in rows),'manual_solution_required':sum(x['calculation'] is None for x in rows),'missing_wrong_choice_explanations':sum(not x['all_distractor_rationales_present'] for x in rows),'repeated_template_frames':sum(len(ids)>1 for ids in duplicate.values()),'status':'draft_audit_only','human_review':None,'runtime_eligible':False},'items':rows,'template_frequency':[{'family':fam,'count':len(ids),'examples':ids[:3]} for (fam,_),ids in duplicate.items() if len(ids)>1]}
 (D/'word-math87-audit-v0.1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result['summary']))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Exact-rational audit of price-change, sale-price and simple-interest records."""
import collections,gzip,json,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
STATE=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
def solve(fam,s):
    if fam=='successive-price':
        p=re.search(r'₱([\d,]+).*?(?:raised the price by|increased the price by) (\d+)%.*?(?:lowered|cut|reduced) the new price by (\d+)%',s,re.I)
        if not p:return None
        base,up,down=int(p[1].replace(',','')),int(p[2]),int(p[3]);a=F(base)*F(100+up,100);v=a*F(100-down,100)
        return v,'successive-price-change',{'starting_price':base,'increase_percent':up,'intermediate_price':str(a),'decrease_percent':down}
    if fam=='sale-price':
        p=re.search(r'priced at ₱([\d,]+).*?(?:sold at|on sale for) (\d+)% off',s,re.I)
        if not p:return None
        base,off=int(p[1].replace(',','')),int(p[2]);return F(base)*F(100-off,100),'sale-price-from-original-base',{'original_price':base,'discount_percent':off,'discounted_fraction':str(F(100-off,100))}
    if fam=='simple-interest':
        p=re.search(r'borrows ₱([\d,]+) at (\d+)% simple interest per year.*?(\d+) years?(?: and (\d+) months?)?',s,re.I)
        if not p:return None
        principal,rate,years,months=int(p[1].replace(',','')),int(p[2]),int(p[3]),int(p[4] or 0);time=F(years)+F(months,12)
        return F(principal)*F(rate,100)*time,'simple-interest-principal-rate-time',{'principal':principal,'annual_rate_percent':rate,'years':str(time)}
    return None
def option_value(s):
    m=re.search(r'₱\s*([\d,]+(?:\.\d+)?)',s)
    if not m:m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',s)
    if not m:raise ValueError(f'no numeric option {s}')
    return F(m.group(1).replace(',',''))
def main():
    cache={};rows=[]
    for fam in ('successive-price','sale-price','simple-interest'):
      for r in [x for x in STATE['records'] if x['work_family']==fam]:
        if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
        q=cache[r['source_file']][r['question_id']];res=solve(fam,q['stem']);opts={o['option_id']:o['text'] for o in q['options']}
        if res is None:calc=method=params=None;matches=[]
        else:
            calc,method,params=res;matches=[oid for oid,text in opts.items() if option_value(text)==calc]
        key=q['answer_option_id'];sig=(method,json.dumps(params,sort_keys=True)) if res else None
        rows.append({'question_id':q['id'],'status':q['status'],'source_file':r['source_file'],'source_record_sha256':r['source_record_sha256'],'source_family':fam,'stem':q['stem'],'method':method,'parameters':params,'calculated_answer':str(calc) if calc is not None else None,'key_option_id':key,'key_text':opts.get(key),'matching_options':matches,'key_matches':bool(calc is not None and matches==[key]),'wrong_choice_feedback_present':all(o['option_id']==key or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'duplicate_signature':json.dumps(sig,sort_keys=True) if sig else None,'manual_review':None if calc is not None else 'No supported exact solver template; manual audit required','interpretation_note':'Starting-price wording should explicitly distinguish original, intermediate and final price.' if fam=='successive-price' else None})
    # Reconcile against existing approved-source tutoring, without regenerating covered bindings.
    pilot=json.loads((D/'pilot-v0.1.json').read_text());overlay=json.loads((D/'math25-v0.1.json').read_text())
    covered={b['question_id'] for b in pilot['bindings']}|{b['question_id'] for b in overlay['bindings']}
    for row in rows:row['existing_tutoring_binding']=row['question_id'] in covered
    groups=collections.defaultdict(list)
    for x in rows:
      if x['duplicate_signature']:groups[x['duplicate_signature']].append(x['question_id'])
    repeated=[{'question_ids':v,'same_solution_parameters':json.loads(k)} for k,v in groups.items() if len(v)>1]
    summary={'record_count':len(rows),'by_family':dict(collections.Counter(x['source_family'] for x in rows)),'status_counts':dict(collections.Counter(x['status'] for x in rows)),'exact_calculations':sum(x['calculated_answer'] is not None for x in rows),'key_matches':sum(x['key_matches'] for x in rows),'key_conflicts':sum(x['calculated_answer'] is not None and not x['key_matches'] for x in rows),'manual_required':sum(x['calculated_answer'] is None for x in rows),'missing_wrong_choice_feedback':sum(not x['wrong_choice_feedback_present'] for x in rows),'approved_records_missing_existing_tutoring':sum(x['status']=='approved' and not x['existing_tutoring_binding'] for x in rows),'approved_records_already_tutored':sum(x['status']=='approved' and x['existing_tutoring_binding'] for x in rows),'same-parameter-groups':repeated,'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
    artifact={'schema_version':'dexter-price38-audit-v0.1','baseline_commit':'2e1127feee2a8e67afe0dc248cf21728053f984d','method':'Exact rational successive percentage multipliers, sale-price complements and simple interest P×r×t. Canonical records are reconciled with existing pilot and math overlays; none are regenerated by this audit. Key checks are not editorial approval.','summary':summary,'items':rows}
    (D/'price38-audit-v0.1.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()

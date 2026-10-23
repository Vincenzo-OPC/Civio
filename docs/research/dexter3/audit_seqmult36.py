#!/usr/bin/env python3
"""Exact screening audit for the 36 NUM-SEQ-MULT queued records."""
import collections, gzip, json, re
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
STATE=json.loads(gzip.decompress((OUT/'bulk-state.json.gz').read_bytes()))

def options(q):
    result={}
    for o in q['options']:
        m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',o['text'])
        if not m: raise ValueError(f"Non-numeric option {o['text']!r}")
        result[o['option_id']]=F(m.group().replace(',',''))
    return result

def candidates(s):
    # Avoid unrelated numbers in prose; select the final consecutive list with at least four terms.
    runs=re.findall(r'(?<!\d)(?:\d[\d,]*(?:\.\d+)?\s*,\s*){3,}\d[\d,]*(?:\.\d+)?',s)
    if not runs: raise ValueError('Could not locate a four-term sequence')
    run=runs[-1]
    terms=[F(x) for x in re.findall(r'\d+(?:\.\d+)?',run)]
    if len(terms)>6: terms=terms[-5:]
    out=[]
    def add(rule,nxt):
        if (rule,nxt) not in out: out.append((rule,nxt))
    dif=[b-a for a,b in zip(terms,terms[1:])]
    if len(set(dif))==1: add('constant-additive-difference',terms[-1]+dif[-1])
    if len(terms)>=3:
        dd=[b-a for a,b in zip(dif,dif[1:])]
        if dd and len(set(dd))==1: add('constant-second-difference',terms[-1]+dif[-1]+dd[-1])
        # t(n+1) = a*t(n)+b, solved from the first three terms and verified against all terms.
        if dif[0] != 0:
            a=(terms[2]-terms[1])/dif[0]; b=terms[1]-a*terms[0]
            if all(terms[i+1]==a*terms[i]+b for i in range(1,len(terms)-1)):
                add('affine-multiplicative-recurrence',a*terms[-1]+b)
    if terms[0]!=0:
        ratio=terms[1]/terms[0]
        if all(y==x*ratio for x,y in zip(terms,terms[1:])): add('constant-ratio',terms[-1]*ratio)
    # Named families are checked exactly, without floating-point square tests.
    for start in range(0,100):
        sq=[F(i*i) for i in range(start,start+len(terms))]
        if sq==terms: add('consecutive-squares',F((start+len(terms))**2)); break
    for start in range(0,30):
        cb=[F(i**3) for i in range(start,start+len(terms))]
        if cb==terms: add('consecutive-cubes',F((start+len(terms))**3)); break
    if terms==[F(1),F(2),F(6),F(24)]: add('factorial-growth',F(120))
    return terms,out

def main():
    cache={};rows=[]
    for r in [x for x in STATE['records'] if x['work_family']=='NUM-SEQ-MULT']:
        if r['source_file'] not in cache:
            cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
        q=cache[r['source_file']][r['question_id']]; terms,rules=candidates(q['stem']); opts=options(q); key=q['answer_option_id']
        supported={v for _,v in rules}; matching=[oid for oid,v in opts.items() if v in supported]
        key_value=opts[key]; key_hits=[fam for fam,v in rules if v==key_value]
        conflict=(len({opts[x] for x in matching})>1)
        rows.append({'question_id':q['id'],'status':q['status'],'source_file':r['source_file'],'source_record_sha256':r['source_record_sha256'],'stem':q['stem'],'sequence':[str(x) for x in terms],'candidate_rules':[{'family':f,'next':str(v)} for f,v in rules],'key_option_id':key,'key_value':str(key_value),'key_matches_supported_rule':bool(key_hits and not conflict and len(matching)==1 and matching[0]==key),'matching_options':matching,'competing_offered_rule':conflict,'distractor_feedback_present':all(o['option_id']==key or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'manual_review':None if key_hits and not conflict and len(matching)==1 and matching[0]==key else 'Inspect sequence rule ambiguity or key/options manually'})
    exact=collections.defaultdict(list); overlaps=[]
    for row in rows:
        vals=tuple(row['sequence']); exact[vals].append(row['question_id'])
    for i,a in enumerate(rows):
        av=list(map(F,a['sequence']))
        for b in rows[i+1:]:
            bv=list(map(F,b['sequence']))
            overlap=max((k for k in range(4,min(len(av),len(bv))+1) if any(av[x:x+k]==bv[y:y+k] for x in range(len(av)-k+1) for y in range(len(bv)-k+1))),default=0)
            if overlap>=4: overlaps.append({'question_ids':[a['question_id'],b['question_id']],'shared_consecutive_terms':overlap,'pattern_concern':'same run/pattern; editorial review required'})
    summary={'record_count':len(rows),'statuses':dict(collections.Counter(x['status'] for x in rows)),'supported_exact_rule_checks':sum(bool(x['candidate_rules']) for x in rows),'key_matches':sum(x['key_matches_supported_rule'] for x in rows),'key_conflicts_or_manual':sum(not x['key_matches_supported_rule'] for x in rows),'missing_wrong_choice_feedback':sum(not x['distractor_feedback_present'] for x in rows),'same_or_overlapping_runs':overlaps,'rule_families':dict(collections.Counter(x['candidate_rules'][0]['family'] if x['candidate_rules'] else 'unresolved' for x in rows)),'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
    artifact={'schema_version':'dexter-seqmult36-audit-v0.1','baseline_commit':'cb0312813f23c83b7789cd0d08dbf4b23e4d1e97','method':'Exact rational candidate recognition for constant differences, constant second differences, affine multiplier-plus-offset recurrence, constant ratio, squares, cubes and the explicit factorial sequence. Matching the stored key is a screening check; it does not establish a unique intended pattern pedagogically.','summary':summary,'items':rows}
    (OUT/'seqmult36-audit-v0.1.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()

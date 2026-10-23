#!/usr/bin/env python3
"""Deterministic check of percentage/price/interest answers and incremental bindings."""
import gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
state=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()));audit=json.loads((D/'price38-audit-v0.1.json').read_text());side=json.loads((D/'price38-guide-draft-v0.1.json').read_text())
def sha(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
rows={x['question_id']:x for x in state['records'] if x['work_family'] in ('successive-price','sale-price','simple-interest')}
assert len(audit['items'])==38 and len(rows)==38 and len({x['question_id'] for x in audit['items']})==38
assert all(x['key_matches'] and x['calculated_answer'] is not None and len(x['matching_options'])==1 for x in audit['items'])
pilot=json.loads((D/'pilot-v0.1.json').read_text());overlay=json.loads((D/'math25-v0.1.json').read_text());covered={b['question_id'] for b in pilot['bindings']}|{b['question_id'] for b in overlay['bindings']}
expected={x['question_id'] for x in audit['items'] if x['status']=='approved' and x['question_id'] not in covered}
bindings={x['question_id']:x for x in side['bindings']};assert len(expected)==17 and set(bindings)==expected
assert len(side['already_covered_ids'])==20 and len(side['excluded_nonapproved_ids'])==1
for a in audit['items']:
    qid=a['question_id'];r=rows[qid]
    if qid not in expected:continue
    q=next(q for q in json.loads((ROOT/r['source_file']).read_text())['items'] if q['id']==qid)
    b=bindings[qid];p=a['parameters'];ans=F(a['calculated_answer'])
    if a['source_family']=='successive-price':expected_ans=F(p['starting_price'])*F(100+p['increase_percent'],100)*F(100-p['decrease_percent'],100)
    elif a['source_family']=='sale-price':expected_ans=F(p['original_price'])*F(100-p['discount_percent'],100)
    else:expected_ans=F(p['principal'])*F(p['annual_rate_percent'],100)*F(p['years'])
    assert ans==expected_ans==F(b['verified_answer']['value'])
    assert b['source_record_sha256']==a['source_record_sha256']==sha(q)
    assert b['status']=='draft' and b['runtime_eligible'] is False and b['editorial_review'] is None
    assert b['transfer']['approved_question_id'] is None
assert side['runtime_eligible'] is False and side['independent_review'] is None
report={'status':'passed','audit_records':38,'exact_calculations_and_key_matches':38,'key_conflicts':0,'manual_exceptions':0,'approved_sources_already_tutored':20,'incremental_approved_source_drafts':17,'nonapproved_excluded':1,'human_reviews':0,'runtime_approved':0}
(D/'price38-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

#!/usr/bin/env python3
"""Recompute ratio/proportion answers and enforce incremental binding boundaries."""
import gzip,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
S=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()));A=json.loads((D/'ratio43-audit-v0.1.json').read_text());G=json.loads((D/'ratio43-guide-draft-v0.1.json').read_text())
def sha(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ov(text):
 m=re.search(r'₱\s*([\d,]+(?:\.\d+)?)',text)
 if not m:m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',text)
 assert m
 return F((m[1] if m.lastindex else m.group()).replace(',',''))
def recalc(m,p):
 if m=='two-person-share-of-total':return F(p['total'])*F(p['parts'][1],sum(p['parts']))
 if m in ('three-part-total-allocation','output-allocated-by-ratio'):return F(p['total'])*F(p['parts'][p['selected_part']-1],sum(p['parts']))
 if m=='two-part-total-allocation':return F(p['total'])*F(p['ratio'][p['selected_part']-1],sum(p['ratio']))
 if m=='known-first-part-to-second':return F(p['known_first']*p['ratio'][1],p['ratio'][0])
 if m=='known-second-part-to-first':return F(p['known_second']*p['ratio'][0],p['ratio'][1])
 if m=='direct-proportion-known-second-part':return F(p['known_second']*p['ratio'][0],p['ratio'][1])
 if m=='difference-to-equalize-ratio-groups':return F(p['total']*abs(p['ratio'][1]-p['ratio'][0]),sum(p['ratio']))
 if m=='age-ratio-from-difference':return F(p['age_difference']*p['ratio'][0],p['ratio'][0]-p['ratio'][1])
 if m=='known-difference-between-ratio-parts':return F(p['difference']*p['ratio'][p['selected_part']-1],abs(p['ratio'][0]-p['ratio'][1]))
 raise AssertionError(m)
records={r['question_id']:r for r in S['records'] if r['work_family'] in ('NUM-WP-RATIO','two-share-total-candidate')};assert len(records)==43
assert len(A['items'])==43 and len({x['question_id'] for x in A['items']})==43
assert all(x['calculated_answer'] is not None and x['key_matches'] for x in A['items'])
pilot=json.loads((D/'pilot-v0.1.json').read_text());overlay=json.loads((D/'math25-v0.1.json').read_text());covered={b['question_id'] for b in pilot['bindings']}|{b['question_id'] for b in overlay['bindings']}
expected={x['question_id'] for x in A['items'] if x['status']=='approved' and x['question_id'] not in covered};bindings={b['question_id']:b for b in G['bindings']}
assert len(expected)==9 and set(bindings)==expected and len(G['already_covered_ids'])==20 and len(G['excluded_nonapproved_ids'])==14
for a in A['items']:
 qid=a['question_id'];r=records[qid];q=next(q for q in json.loads((ROOT/r['source_file']).read_text())['items'] if q['id']==qid)
 options={o['option_id']:ov(o['text']) for o in q['options']};key=q['answer_option_id'];val=F(a['calculated_answer'])
 assert a['key_option_id']==key and options[key]==val and [i for i,v in options.items() if v==val]==[key]
 if qid not in expected:continue
 b=bindings[qid];assert val==recalc(a['method'],a['parameters'])==F(b['verified_answer']['value'])
 assert b['source_record_sha256']==a['source_record_sha256']==sha(q)
 assert b['status']=='draft' and b['runtime_eligible'] is False and b['editorial_review'] is None and b['transfer']['approved_question_id'] is None
assert G['runtime_eligible'] is False and G['independent_review'] is None
report={'status':'passed','audited_records':43,'unique_records':43,'exact_answer_and_option_checks':43,'key_conflicts':0,'manual_exceptions':0,'approved_sources_already_bound':20,'new_approved_source_drafts':9,'reviewed_or_draft_excluded':14,'duplicate_parameter_groups':len(A['summary']['parameter_repeat_groups']),'human_reviews':0,'runtime_approved':0}
(D/'ratio43-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

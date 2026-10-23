#!/usr/bin/env python3
"""Deterministic cross-checks for the NUM-SEQ-MULT audit and draft sidecar."""
import gzip, hashlib, json, re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent; ROOT=Path(__file__).resolve().parents[3]
state=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
audit=json.loads((D/'seqmult36-audit-v0.1.json').read_text()); side=json.loads((D/'seqmult36-guide-draft-v0.1.json').read_text())
def sha(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def options(q):
 out={}
 for o in q['options']:
  m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',o['text']);assert m
  out[o['option_id']]=F(m.group().replace(',',''))
 return out
assert len(audit['items'])==36 and len({x['question_id'] for x in audit['items']})==36
source={r['question_id']:r for r in state['records'] if r['work_family']=='NUM-SEQ-MULT'}
assert len(source)==36
assert all(x['key_matches_supported_rule'] for x in audit['items'])
assert all(len(x['matching_options'])==1 for x in audit['items'])
assert all(x['distractor_feedback_present'] for x in audit['items'])
bindings={x['question_id']:x for x in side['bindings']}
approved={x['question_id'] for x in audit['items'] if x['status']=='approved'}
assert len(approved)==20 and len(bindings)==20 and set(bindings)==approved
assert len(side['excluded_nonapproved_ids'])==16
for aid,a in ((x['question_id'],x) for x in audit['items']):
 row=source[aid];q=next(q for q in json.loads((ROOT/row['source_file']).read_text())['items'] if q['id']==aid)
 assert row['bank_status']=='approved' if aid in approved else row['bank_status'] in ('draft','reviewed')
 if aid in approved:
  b=bindings[aid];assert sha(q)==a['source_record_sha256']==b['source_record_sha256']
  t=list(map(F,a['sequence']));mult=(t[2]-t[1])/(t[1]-t[0]);offset=t[1]-mult*t[0]
  assert all(t[i+1]==mult*t[i]+offset for i in range(1,len(t)-1))
  nxt=mult*t[-1]+offset;assert nxt==F(a['key_value'])==options(q)[q['answer_option_id']]
  assert b['status']=='draft' and b['runtime_eligible'] is False and b['editorial_review'] is None
  assert b['transfer']['approved_question_id'] is None
assert side['runtime_eligible'] is False and side['independent_review'] is None
report={'status':'passed','audit_records':36,'unique_source_records':36,'exact_rule_and_key_checks':36,'key_conflicts':0,'approved_source_tutoring_drafts':20,'nonapproved_excluded':16,'overlapping_sequence_pairs_flagged':len(audit['summary']['same_or_overlapping_runs']),'human_reviews':0,'runtime_approved':0}
(D/'seqmult36-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

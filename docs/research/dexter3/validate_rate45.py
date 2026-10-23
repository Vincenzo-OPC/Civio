#!/usr/bin/env python3
"""Cross-check rate/time audit and draft tutoring-source boundaries."""
import gzip,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
state=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()));audit=json.loads((D/'rate45-audit-v0.1.json').read_text());side=json.loads((D/'rate45-guide-draft-v0.1.json').read_text())
def sha(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
records={x['question_id']:x for x in state['records'] if x['work_family']=='NUM-WP-RATE'}
assert len(audit['items'])==45 and len(records)==45 and len({x['question_id'] for x in audit['items']})==45
assert all(x['key_matches'] for x in audit['items']) and all(x['calculated_answer'] is not None for x in audit['items'])
assert all(len(x['matching_options'])==1 for x in audit['items'])
assert all(x['distractor_feedback_present'] for x in audit['items'])
bindings={x['question_id']:x for x in side['bindings']}
eligible={x['question_id'] for x in audit['items'] if x['status']=='approved' and x['method']=='two-workers-combined-rate'}
assert len(eligible)==27 and set(bindings)==eligible
assert len(side['excluded_nonapproved_ids'])==18
for x in audit['items']:
    if x['question_id'] not in eligible:continue
    rid=x['question_id'];r=records[rid]
    q=next(q for q in json.loads((ROOT/r['source_file']).read_text())['items'] if q['id']==rid)
    b=bindings[rid];a,bh=map(F,x['parameters']['hours']);ans=F(a*bh,a+bh)
    assert ans==F(x['calculated_answer'])==F(b['verified_answer']['value_hours'])
    assert b['source_record_sha256']==x['source_record_sha256']==sha(q)
    assert b['status']=='draft' and b['runtime_eligible'] is False and b['editorial_review'] is None
    assert b['transfer']['approved_question_id'] is None
assert side['runtime_eligible'] is False and side['independent_review'] is None
report={'status':'passed','audit_records':45,'exact_calculations_and_key_matches':45,'key_conflicts':0,'manual_exceptions':0,'approved_source_tutoring_drafts':27,'nonapproved_sources_excluded':18,'same_parameter_groups':len(audit['summary']['same-parameter-question-groups']),'human_reviews':0,'runtime_approved':0}
(D/'rate45-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

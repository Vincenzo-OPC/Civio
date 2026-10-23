#!/usr/bin/env python3
"""Confirm exact answers and source status for the two final numerical queue records."""
import gzip,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
S=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()));A=json.loads((D/'numeric-tail2-audit-v0.1.json').read_text())
rows={r['question_id']:r for r in S['records'] if r['work_family'] in ('NUM-SEQ-ALT','NUM-UNIT')};assert len(rows)==2 and len(A['items'])==2
for a in A['items']:
 r=rows[a['question_id']];assert r['bank_status']=='draft' and a['status']=='draft'
 q=next(q for q in json.loads((ROOT/r['source_file']).read_text())['items'] if q['id']==a['question_id'])
 opts={o['option_id']:F(re.search(r'-?\d+(?:\.\d+)?',o['text']).group()) for o in q['options']}
 assert a['key_option_id']==q['answer_option_id'] and opts[q['answer_option_id']]==F(a['calculated_answer'])
 assert [i for i,v in opts.items() if v==F(a['calculated_answer'])]==[q['answer_option_id']]
 assert a['key_matches'] is True and a['runtime_eligible'] is False
report={'status':'passed','records':2,'exact_key_checks':2,'draft_sources_excluded':2,'tutoring_bindings':0,'human_review':0,'runtime_approved':0}
(D/'numeric-tail2-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

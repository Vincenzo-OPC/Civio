#!/usr/bin/env python3
"""Deterministic checks for the 133-record English spelling screen."""
import json, subprocess, sys
from pathlib import Path
D=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(D/'audit_spell133.py')],check=True,capture_output=True,text=True)
a=json.loads((D/'spell133-audit-v0.1.json').read_text()); s=a['summary']; ids=[x['question_id'] for x in a['items']]
assert len(ids)==133 and len(set(ids))==133
assert s['by_family']=={'CLR-SPELL-WRONG':63,'CLR-SPELL-RIGHT':50,'CLR-SPELLING':20}
assert s['status_counts']=={'approved':113,'draft':20}
assert (s['single-key-rule_matches'],s['spell-rule-exceptions'],s['context-resolved-lexical-alternatives'],s['unresolved_single-answer_review'])==(131,2,1,1)
assert s['wrong_option_feedback_missing']==0 and s['already_bound_in_pilot']==20
assert s['human_reviews']==0 and s['runtime_eligible'] is False
for x in a['items']:
 assert x['source_record_sha256']
 if x['question_id']=='CIVIO-CLR-SPELL-RIGHT-000900': assert not x['key_agrees_with_item_context']
 if x['question_id']=='CIVIO-CLR-20261013-0034': assert x['key_agrees_with_item_context']
(D/'spell133-validation.json').write_text(json.dumps({'schema_version':'dexter-spell133-validation-v0.1','record_count':133,'unique_ids':True,'result':'PASS','scope':'lexical/key screen; no approval or runtime eligibility'},indent=2)+'\n')
print('PASS: 133 unique references; 131 lexical key matches; one context-resolved alternative; one unresolved ambiguity; all remain non-runtime.')

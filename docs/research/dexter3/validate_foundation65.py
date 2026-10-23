#!/usr/bin/env python3
"""Recompute and validate the 65-item exact foundation audit and approved-only drafts."""
import json,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def run():
 subprocess.run([sys.executable,str(D/'audit_foundation65.py')],cwd=ROOT,check=True,capture_output=True,text=True)
 a=json.loads((D/'foundation65-audit-v0.1.json').read_text());d=json.loads((D/'foundation65-guide-draft-v0.1.json').read_text())
 assert len(a['items'])==65 and a['summary']['deterministic_calculations']==65
 assert a['summary']['keys_matching']==65 and a['summary']['key_conflicts']==0 and a['summary']['manual_solution_required']==0
 assert a['summary']['wrong_choice_rationales_missing']==0
 by={x['question_id']:x for x in a['items']};assert len(d['bindings'])==25 and len(d['excluded_nonapproved_ids'])==40
 assert len({x['question_id'] for x in d['bindings']})==25
 for b in d['bindings']:
  x=by[b['question_id']]
  assert x['source_status']=='approved' and b['bank_status_at_authoring']=='approved'
  assert x['source_record_sha256']==b['source_record_sha256']
  assert x['key_matches'] and b['verified_answer']['exact_check_passed']
  c=b['diagnostic']['choices'];assert len(c)==4 and len({z['id'] for z in c})==4
  assert sum(z['role']=='correct-rule' for z in c)==1 and sum(z['role']=='uncertain' for z in c)==1
  assert all(z['feedback'] for z in c)
  assert b['transfer']['approved_question_id'] is None and not b['runtime_eligible'] and b['status']=='draft' and b['editorial_review'] is None
  assert b['assistance_contract']['diagnostic_does_not_establish_mastery'] and b['assistance_contract']['uncertain_or_misclick_assigns_no_hypothesis']
 return {'status':'passed','audit_records':65,'exact_key_checks':65,'conflicts':0,'manual_exceptions':0,'approved_source_tutoring_drafts':25,'excluded_nonapproved_sources':40,'runtime_approved':0,'human_approved':0}
if __name__=='__main__':
 r=run();(D/'foundation65-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

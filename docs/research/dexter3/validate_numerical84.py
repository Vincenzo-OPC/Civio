#!/usr/bin/env python3
"""Recheck the draft 84-item arithmetic/sequence audit and 59 source-approved bindings."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent

def run():
 subprocess.run([sys.executable,str(D/'audit_numerical84.py')],cwd=ROOT,check=True,capture_output=True,text=True)
 audit=json.loads((D/'numerical84-audit-v0.1.json').read_text());draft=json.loads((D/'numerical84-guide-draft-v0.1.json').read_text())
 assert audit['summary']['records']==84 and audit['summary']['exact_key_passes']==84
 assert audit['summary']['uncovered_explanations']==audit['summary']['uncovered_codes']==0
 assert all(x['key_matches'] and not x['needs_manual_review'] for x in audit['items'])
 byid={x['question_id']:x for x in audit['items']}
 assert len(draft['bindings'])==59 and len(draft['excluded_nonapproved_ids'])==25
 assert len({b['question_id'] for b in draft['bindings']})==59
 for bind in draft['bindings']:
  a=byid[bind['question_id']]
  assert a['bank_status']=='approved' and bind['bank_status_at_authoring']=='approved'
  assert bind['source_record_sha256']==a['source_hash']
  assert bind['verified_answer']['value']==a['exact_answer']
  assert bind['verified_answer']['option_id']==a['key_option_id']
  assert bind['diagnostic_template'] in draft['templates']
  choices=bind['diagnostic']['choices']
  assert len(choices)==4 and len({c['id'] for c in choices})==4
  assert sum(c['role'] in ('correct_rule','correct-rule') for c in choices)==1
  assert sum(c['role']=='uncertain' for c in choices)==1
  assert all(c.get('feedback') for c in choices)
  assert bind['transfer']['approved_question_id'] is None
  assert bind['outcome_contract']['diagnostic_is_assisted'] is True
  assert bind['outcome_contract']['uncertain_or_misclick_assigns_hypothesis'] is False
  assert bind['outcome_contract']['correct_diagnostic_is_not_mastery'] is True
  assert bind['status']=='draft' and not bind['runtime_eligible'] and bind['editorial_review'] is None
 assert draft['human_adjudication'] if 'human_adjudication' in draft else True
 return {'status':'passed','audit_records':84,'exact_key_checks':84,'draft_bindings_source_approved':59,'nonapproved_excluded':25,'duplicate_sequence_pairs':len(audit['summary']['repeated_term_sequences']),'unmapped_transfer_approved':59,'runtime_approved':0,'human_review_decisions':0}
if __name__=='__main__':
 r=run();(D/'numerical84-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

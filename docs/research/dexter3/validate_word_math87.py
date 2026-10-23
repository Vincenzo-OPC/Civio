#!/usr/bin/env python3
"""Re-run exact checks and validate approved-only draft tutoring bindings."""
import json,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def run():
 subprocess.run([sys.executable,str(D/'audit_word_math87.py')],cwd=ROOT,check=True,capture_output=True,text=True)
 a=json.loads((D/'word-math87-audit-v0.1.json').read_text());d=json.loads((D/'word-math87-guide-draft-v0.1.json').read_text())
 assert len(a['items'])==87 and a['summary']['supported_calculation_checks']==87 and a['summary']['key_matches']==87
 assert a['summary']['key_conflicts']==0 and a['summary']['missing_wrong_choice_explanations']==0
 byid={r['question_id']:r for r in a['items']}
 assert len(d['bindings'])==60 and len(d['excluded_nonapproved_ids'])==27
 assert len({x['question_id'] for x in d['bindings']})==60
 for b in d['bindings']:
  source=byid[b['question_id']]
  assert source['status']=='approved' and b['bank_status_at_authoring']=='approved'
  assert b['source_record_sha256']==source['source_record_sha256']
  assert b['verified_answer']['value']==source['calculation'] and b['verified_answer']['exact_calculation_matches_stored_key']
  c=b['diagnostic']['choices']
  assert len(c)==4 and len({x['id'] for x in c})==4
  assert sum(x['role']=='correct-rule' for x in c)==1 and sum(x['role']=='uncertain' for x in c)==1
  assert all(x.get('feedback') for x in c)
  assert b['transfer']['approved_question_id'] is None
  assert b['status']=='draft' and not b['runtime_eligible'] and b['editorial_review'] is None
  assert b['assistance_contract']['diagnostic_does_not_establish_mastery']
  assert b['assistance_contract']['uncertain_or_misclick_assigns_no_hypothesis']
 return {'status':'passed','source_records_audited':87,'exact_answer_checks':87,'key_conflicts':0,'approved_source_bindings':60,'nonapproved_sources_excluded':27,'duplicate_template_frames':a['summary']['repeated_template_frames'],'transfer_mappings_approved':0,'human_reviews':0,'runtime_approved':0}
if __name__=='__main__':
 r=run();(D/'word-math87-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

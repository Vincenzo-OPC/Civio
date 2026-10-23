#!/usr/bin/env python3
"""Create neutral evidence and a blank reviewer template, never review decisions.
Also check four explicitly scoped, non-approved foundation candidates.
Run from repo root. No application, database, model or approval operations.
"""
import copy
import csv
import hashlib
import json
import re
import subprocess
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
BASE='9584106042bdd8d57eaa054f98fb4a1b73470cb0'
PACKET=ROOT/'docs/research/dexter2/pilot/dexter-rescue-pilot-packet-2026-10-22.csv'
IDS=['CIVIO-NUM-PCT-BASIC-926013','CIVIO-NUM-PCT-BASIC-926014','CIVIO-NUM-PCT-BASIC-926015','CIVIO-B3-NUM-PCT-BASIC-0265']
CRITERIA=['interpretation_correct','diagnostic_tests_comprehension','feedback_distinct_and_appropriate','hypothesis_supported_without_overclaim','hints_progress_without_early_solution','worked_solution_and_shortcut_correct','original_intermediate_final_distinguished','accessible_to_percentage_beginner','natural_tutor_voice','safe_to_reuse_with_validated_parameters']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fingerprint(q):return hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def read(path):return json.loads(path.read_text())
def write(name,obj):
    p=OUT/name;text=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
    if p.exists() and p.read_text()!=text:raise RuntimeError('Existing artifact differs; inspect and version explicitly: '+name)
    if not p.exists():p.write_text(text)

def number(text):
    x=re.match(r'(\d+(?:\.\d+)?)(?:\s+(\d+/\d+))?',text)
    assert x,text
    return F(x[1])+(F(x[2]) if x[2] else 0)

def source_record(row):
    d=read(ROOT/row['source_file']);items=d['items'] if isinstance(d,dict) else d
    found=[q for q in items if q['id']==row['id']];assert len(found)==1
    return found[0]

def excerpt(q):
    return {k:copy.deepcopy(q[k]) for k in ['id','track','archetype','stem','options','answer_option_id','reveal','distractor_reasoning','source','status']}

def foundation_review(q,row):
    suffix=q['id'].split('-')[-1]
    if suffix=='926013':
        a=F(360)*F(15,100);b=F(360,10)+F(360,20)
        role='known_whole_and_rate_find_part';methods=['360 × 15/100 = 54 notebooks.','10% is 36 and 5% is 18; 36 + 18 = 54.']
        interpretation='360 is the full donation; 15% is the fraction set aside; the unknown is a notebook count.'
        wrong={'o2':F(360)*F(20,100),'o3':F(360,10),'o4':F(360,15)}
        concerns=[{'option_id':'o4','canonical_code':'NUM-WRONG-BASE','proposed_local_hypothesis':'percent_operator_misread','note':'360 ÷ 15 uses the right whole but the wrong percent operation. It does not alone prove that another base was selected.'}]
        prompts=['Which amount represents the full donation?','Does 15% name a number of notebooks or a fraction of the full donation?']
        transfer='Potential approved prerequisite assessment after review/approval; different context from sale-price tasks, but only direct percentage amount.'
    elif suffix=='926014':
        a=F(18,60)*100;b=F(18,6)*10
        role='known_part_and_whole_find_rate';methods=['18 ÷ 60 × 100 = 30%.','Simplify 18/60 to 3/10, then scale to 30/100 = 30%.']
        interpretation='18 is the cycling part and 60 is the whole group of invitees; the unknown is a percentage.'
        wrong={'o1':F(60,18),'o3':F(18),'o4':100-a}
        concerns=[{'option_id':'o1','canonical_code':'NUM-OP-SWAP','proposed_local_hypothesis':'whole_divided_by_part_then_mislabeled_percent','note':'60/18 = 3 1/3 is a ratio, not 3 1/3%. The foil requires inversion plus a missing percent conversion. Avoid describing it as a pure single-operation error.'},{'option_id':'o4','canonical_code':'NUM-OTHER-SHARE','proposed_local_hypothesis':'complement_group_selected','note':'70% is the non-cycling group. This is a target-group distinction; no ratio-sharing problem is involved.'}]
        prompts=['Which group is the whole when the question says percentage of invitees?','Does the question ask how many people cycled or what percentage cycled?']
        transfer='Potential part/whole-to-rate application after approval; cannot assess reverse markup by itself.'
    elif suffix=='926015':
        a=F(72)/F(25,100);b=F(72)*4
        role='known_part_and_rate_find_whole';methods=['72 ÷ 0.25 = 288 files.','25% is one quarter. Four quarters contain 4 × 72 = 288 files.']
        interpretation='72 is the encoded quarter, not the original total or the unencoded remainder.'
        wrong={'o1':F(72)*F(25,100),'o2':F(72),'o4':F(72)/F(75,100)}
        concerns=[{'option_id':'o1','canonical_code':'NUM-WRONG-BASE','proposed_local_hypothesis':'part_mistaken_for_whole','note':'Ask what 72 represents before claiming the learner selected a wrong base.'},{'option_id':'o4','canonical_code':'NUM-WRONG-BASE','proposed_local_hypothesis':'given_part_mistaken_for_remaining_part','note':'72/0.75 assumes 72 is the 75% remainder. Confirm that interpretation; the code alone loses the distinction.'}]
        prompts=['Does 72 represent all assigned files, the completed part, or the remaining part?','If 72 is one quarter, how many such equal quarters form the whole?']
        transfer='Useful inverse-percent prerequisite after approval. It recovers a whole from a 25% part; it is a different relation from reversing a 25% markup, where the given final is 125%.'
    else:
        assert suffix=='0265'
        a=F(180)/F(120,100);b=F(180,12)*10
        role='known_final_after_raise_find_original';methods=['Original × 1.20 = 180, so original = 180 ÷ 1.20 = ₱150.','120% = ₱180, so 10% = ₱15 and 100% = ₱150.']
        interpretation='₱180 is already after the raise; the unknown original is 100% and the given final is 120%.'
        wrong={'n1':F(180)*F(80,100),'n3':F(180)-20,'n4':F(180)*F(120,100)}
        concerns=[{'option_id':'n3','canonical_code':'NUM-OP-SWAP','proposed_local_hypothesis':'percent_as_fixed_pesos','note':'180 − 20 treats 20% as ₱20. Separate unit interpretation from reversing a multiplication.'}]
        prompts=['Has the 20% raise already happened when the allowance is ₱180?','Is ₱180 the original 100%, or the new 120% of the original?']
        transfer='Closest existing reverse-raise near practice for the ₱640 contrast after approval. A 20% allowance raise is the same inverse-multiplier family as a 25% price markup, so it is not full unfamiliar-family transfer.'
    assert a==b
    hits=[o['option_id'] for o in q['options'] if number(o['text'])==a]
    assert hits==[q['answer_option_id']]
    for o in q['options']:
        if o['option_id']!=q['answer_option_id']:assert number(o['text'])==wrong[o['option_id']]
    # Check the relationship in the original direction as a third consistency check.
    if suffix=='926013':assert a/F(360)==F(15,100)
    elif suffix=='926014':assert F(60)*a/100==18
    elif suffix=='926015':assert a/4==72
    else:assert a+a/5==180
    return dict(question_id=q['id'],source_file=row['source_file'],source_question_hash=row['content_sha256'],source_record_sha256=fingerprint(q),status_observed=q['status'],eligible_for_runtime=False,family=role,interpretation=interpretation,mathematical_verification={'status':'passed','result':str(a),'unit':'percent' if suffix=='926014' else 'notebooks' if suffix=='926013' else 'files' if suffix=='926015' else 'pesos','methods':methods,'wrong_options_recomputed':3,'exactly_one_correct_option':True},editorial_observations=concerns,draft_diagnostic_prompts=prompts,transfer_limit=transfer,independent_reviewer=None,adjudication=None,canonical_change=None)

def main():
    overlay=read(OUT/'price15-v0.2.json')
    manifest={m['id']:m for m in read(ROOT/'docs/research/bank/civio-flat-2100-manifest-2026-10-22.json')['items']}
    original_rows=list(csv.DictReader(PACKET.open()))
    # No re-inventory, no regeneration, no current author verdicts in the review evidence.
    evidence=[];review_items=[]
    for b in overlay['bindings']:
        q=source_record(manifest[b['question_id']]);assert fingerprint(q)==b['source_record_sha256']
        rows=[r for r in original_rows if r['item_id']==q['id']];assert len(rows)==3
        evidence.append({'question_id':q['id'],'source_file':b['source_file'],'source_record_sha256':b['source_record_sha256'],'source_question_hash':b['source_question_hash'],'source':excerpt(q),'binding':{k:copy.deepcopy(v) for k,v in b.items() if k!='finding_ids'},'original_distractor_rows':[{k:r[k] for k in ('item_id','correct_option','distractor_option','distractor_code','why_wrong','why_correct')} for r in rows]})
        review_items.append({'question_id':q['id'],'own_solution':None,'criteria':{k:None for k in CRITERIA},'distractors':[], 'item_family_distinct':None,'notes':None})
        review_items[-1]['distractors']=[{'option_id':r['distractor_option'].split(':')[0],'code_matches_error':None,'why_wrong_accurate':None,'notes':None} for r in rows]
    foundation=[];candidates=[];rejected_fixtures=0
    for qid in IDS:
        row=manifest[qid];q=source_record(row);assert q['status'] in ('reviewed','draft')
        foundation.append(foundation_review(q,row));candidates.append({'question_id':qid,'source_file':row['source_file'],'source_record_sha256':fingerprint(q),'source':excerpt(q)})
        # Each candidate must reject a wrong key and a second numerically correct option.
        for mutation in ('wrong_key','duplicate_correct_value'):
            bad=copy.deepcopy(q)
            wrong=next(o for o in bad['options'] if o['option_id']!=q['answer_option_id'])
            if mutation=='wrong_key':bad['answer_option_id']=wrong['option_id']
            else:wrong['text']=next(o['text'] for o in q['options'] if o['option_id']==q['answer_option_id'])
            try:foundation_review(bad,row)
            except AssertionError:rejected_fixtures+=1
            else:raise AssertionError('Bad candidate accepted: '+qid+' '+mutation)
    audit={'schema_version':'dexter-foundation-candidate-audit-v0.1','baseline_commit':BASE,'status':'author_review_only','question_count':4,'records':foundation,'approval_status':'pending','learner_results':None}
    write('foundation4-audit-v0.1.json',audit)
    packet={'schema_version':'dexter-price15-review-packet-v0.1','baseline_commit':BASE,'status':'awaiting_independent_review','overlay_file':'price15-v0.2.json','overlay_sha256':sha(OUT/'price15-v0.2.json'),'original_packet_sha256':sha(PACKET),'criteria':CRITERIA,'rating_values':['yes','no','unclear'],'instructions':['Solve each source item before consulting its stored key. A key in this packet is reference evidence, not an instruction to agree.','Review independently; do not inspect another reviewer\'s completed form before submitting your own.','Compare diagnosis with the actual response evidence. Unknown/self-report/assisted checks must not become knowledge or permanent diagnoses.','Mark exact failures and affected node/response IDs. Do not copy the author second-pass verdict as your own.','Foundation candidates remain unapproved even when your mathematics is correct. Bank signing and runtime activation are separate gates.'],'price_items':evidence,'flows':overlay['flows'],'contrast':overlay['contrast'],'candidate_sources':candidates,'review_form_template':{'packet_sha256':'COMPUTE_SHA256_OF_PACKET_BYTES_WHEN_CREATING_SEPARATE_REVIEW_COPY','reviewer_identity':None,'reviewer_kind':None,'reviewed_at':None,'independence_declaration':None,'price_items':review_items,'contrast':{'meaning_first':None,'forward_reverse_distinct':None,'wrong_inverse_demonstrated':None,'new_example_correct':None,'no_false_independent_outcome':None,'notes':None},'foundation_candidates':[{'question_id':qid,'own_solution':None,'key_correct':None,'wording_clear':None,'rationales_correct':None,'codes_precise':None,'transfer_role':None,'notes':None} for qid in IDS],'overall_recommendation':None},'adjudication':{'review_1_record':None,'review_2_record':None,'adjudicator':None,'adjudicated_at':None,'decision':None}}
    write('price15-review-packet-v0.1.json',packet)
    assert len(evidence)==15 and sum(len(r['original_distractor_rows']) for r in evidence)==45
    assert len(foundation)==4 and sum(r['mathematical_verification']['wrong_options_recomputed'] for r in foundation)==12
    assert rejected_fixtures==8
    assert all(r['independent_reviewer'] is None and r['adjudication'] is None for r in foundation)
    assert 'editorial_review' not in packet and 'finding_ids' not in json.dumps(packet)
    assert all(all(value is None for value in item['criteria'].values()) and all(r['code_matches_error'] is None and r['why_wrong_accurate'] is None for r in item['distractors']) for item in packet['review_form_template']['price_items'])
    for name in ['pilot-v0.1.json','coverage-v0.1.json','price15-v0.2.json','price15-check-results.json']:
        assert (OUT/name).read_bytes()==subprocess.check_output(['git','show',BASE+':docs/research/dexter3/'+name],cwd=ROOT)
    assert PACKET.read_bytes()==subprocess.check_output(['git','show',BASE+':'+str(PACKET.relative_to(ROOT))],cwd=ROOT)
    report={'baseline_commit':BASE,'packet_sha256':sha(OUT/'price15-review-packet-v0.1.json'),'foundation_audit_sha256':sha(OUT/'foundation4-audit-v0.1.json'),'price_items_in_review_packet':15,'distractor_rows_in_review_packet':45,'foundation_keys_checked':4,'foundation_distractor_values_checked':12,'invalid_candidate_fixtures_rejected':rejected_fixtures,'foundation_statuses':{'reviewed':3,'draft':1},'independent_reviews_recorded':0,'approved_candidates_added':0,'prior_artifacts_byte_identical':True,'original_reviewer_csv_byte_identical':True,'bank_items_changed':0,'runtime_changes':0}
    write('price15-review-preparation-results.json',report)
    print('PASS: neutral 15-item/45-distractor review packet; 4 non-approved candidate keys and 12 wrong-option values checked; prior artifacts intact; reviewer fields pending.')

if __name__=='__main__':main()

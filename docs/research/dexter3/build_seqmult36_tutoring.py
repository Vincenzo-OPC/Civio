#!/usr/bin/env python3
"""Prepare draft rule-recognition tutoring bindings for approved sequence items."""
import gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
STATE=json.loads(gzip.decompress((OUT/'bulk-state.json.gz').read_bytes()))

def sha(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def main():
    audit=json.loads((OUT/'seqmult36-audit-v0.1.json').read_text());cache={};bindings=[]
    for a in audit['items']:
        if a['status']!='approved': continue
        row=next(r for r in STATE['records'] if r['question_id']==a['question_id'])
        if row['source_file'] not in cache: cache[row['source_file']]={q['id']:q for q in json.loads((ROOT/row['source_file']).read_text())['items']}
        q=cache[row['source_file']][a['question_id']]
        if sha(q)!=a['source_record_sha256']: raise ValueError(f"Changed source: {q['id']}")
        terms=list(map(F,a['sequence'])); mult=(terms[2]-terms[1])/(terms[1]-terms[0]); offset=terms[1]-mult*terms[0]
        assert all(terms[i+1]==mult*terms[i]+offset for i in range(1,len(terms)-1))
        mtxt=str(mult.numerator) if mult.denominator==1 else str(mult); otxt=str(abs(offset.numerator)) if offset.denominator==1 else str(abs(offset))
        relation=f"multiply the previous term by {mtxt}, then {'add' if offset>=0 else 'subtract'} {otxt}"
        choices=[
          {'id':'affine-rule','text':'Multiply the previous term by a fixed number, then make the same fixed adjustment.','role':'correct-rule','feedback':'That two-part rule is the pattern to test. Check it against every listed transition before extending it.'},
          {'id':'constant-gap','text':'Add the same amount to the previous term each time.','role':'common-error','feedback':'Compare the differences. They do not stay equal here, so a fixed addition alone does not explain all transitions.'},
          {'id':'constant-ratio','text':'Multiply the previous term by the same factor, with no extra adjustment.','role':'common-error','feedback':'Compare the ratios. A constant multiplier alone does not account for the same additional change at each step.'},
          {'id':'unsure','text':'I am unsure, guessed, or used another approach.','role':'uncertain','feedback':'No cause is established. First compare neighboring differences; if they change, test a multiplier and a repeated adjustment.'}]
        diffs=[terms[i+1]-terms[i] for i in range(len(terms)-1)]
        steps=[f"Neighboring differences are {', '.join(map(str,diffs))}; they are not a constant gap.",f"A rule that fits every listed transition is: {relation}.",f"Check the final given transition: {terms[-2]} × {mtxt} {'+' if offset>=0 else '−'} {otxt} = {terms[-1]}.",f"Continue once: {terms[-1]} × {mtxt} {'+' if offset>=0 else '−'} {otxt} = {a['key_value']}."]
        bindings.append({'question_id':q['id'],'source_file':row['source_file'],'source_record_sha256':a['source_record_sha256'],'bank_status_at_authoring':'approved','difficulty':q.get('difficulty'),'language':q.get('language'),'concept_family':'affine-multiplicative-recurrence','diagnostic_template':'multiply-then-fixed-adjustment','diagnostic':{'prompt':'Before finding the next number, which kind of rule should you test against every pair of neighboring terms?','choices':choices,'confirmation':'Was that your original way of reading the sequence, a method you chose after seeing these choices, a guess, or a misclick? A selection alone does not confirm a misconception.'},'verified_answer':{'option_id':q['answer_option_id'],'value':a['key_value'],'method':relation,'checks':['exact recurrence verified across all transitions','calculated next term matches stored answer','single matching option under audited candidate rules']},'worked_solution':{'steps':steps,'hint_levels':['Compare the differences between neighboring terms.','If those differences change, test a fixed multiplier and then check whether the same adjustment remains.','Substitute the rule into each listed transition before extending it.'],'shortcut':'Once a two-part rule is confirmed across all given terms, apply it once to the final term. Do not assume a rule from only one transition.'},'transfer':{'approved_question_id':None,'reason':'No distinct-family approved transfer item has been verified. Overlapping sequences in this family are flagged for editorial review, not treated as independent transfer.'},'outcome_contract':{'diagnostic_is_assisted':True,'misconception_is_hypothesis_only':True,'confirmation_required_for_persistent_hypothesis':True,'uncertain_or_misclick_assigns_hypothesis':False,'diagnostic_correctness_is_not_mastery':True,'independent_transfer_required_for_mastery':True},'status':'draft','editorial_review':None,'runtime_eligible':False})
    artifact={'schema_version':'dexter-seqmult36-guide-draft-v0.1','baseline_commit':'cb0312813f23c83b7789cd0d08dbf4b23e4d1e97','status':'draft','runtime_eligible':False,'independent_review':None,'learner_evidence':None,'bindings':bindings,'excluded_nonapproved_ids':[a['question_id'] for a in audit['items'] if a['status']!='approved'],'notes':['Draft scaffolding only; no source item, answer, option or approval status changed.','All approved items in this batch share the same affine multiplier-plus-offset family; 20 question bindings therefore do not represent 20 distinct learning families.','Transfer mapping remains unresolved pending approved, unfamiliar questions.']}
    (OUT/'seqmult36-guide-draft-v0.1.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n'); print('draft bindings',len(bindings),'excluded',len(artifact['excluded_nonapproved_ids']))
if __name__=='__main__': main()

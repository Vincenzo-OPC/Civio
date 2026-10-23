#!/usr/bin/env python3
"""Draft rate-combination guides for approved two-worker items in the 45-item audit."""
import gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
STATE=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
def sha(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def main():
    audit=json.loads((D/'rate45-audit-v0.1.json').read_text());cache={};bindings=[]
    for a in audit['items']:
        if a['status']!='approved' or a['method']!='two-workers-combined-rate':continue
        row=next(x for x in STATE['records'] if x['question_id']==a['question_id'])
        if row['source_file'] not in cache:cache[row['source_file']]={q['id']:q for q in json.loads((ROOT/row['source_file']).read_text())['items']}
        q=cache[row['source_file']][a['question_id']]
        assert sha(q)==a['source_record_sha256']
        x,y=map(int,a['parameters']['hours']);time=F(x*y,x+y);rate=F(1,x)+F(1,y)
        assert time==F(a['calculated_answer'])
        def frac(v):return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
        choices=[
          {'id':'combine-rates','text':'Add the fractions of the job each person completes in one hour, then take the reciprocal.','role':'correct-rule','feedback':'Right. Work rates add because both people contribute during the same hour. The combined rate is jobs per hour; its reciprocal gives hours per job.'},
          {'id':'add-times','text':'Add the two completion times.','role':'time-rate-confusion','feedback':'Those are the times each person would need alone. To combine simultaneous workers, add the amount of the job each completes per hour.'},
          {'id':'average-times','text':'Average the two completion times.','role':'average-time-error','feedback':'The mean time does not account for how much work each person contributes in the same hour. Convert each time to a rate first.'},
          {'id':'faster-alone','text':'Use only the faster person’s completion time.','role':'ignore-second-contribution','feedback':'The faster person works at that rate, but the second person adds more work during each hour. Combine both rates.'},
          {'id':'unsure','text':'I am unsure, guessed, or used another approach.','role':'uncertain','feedback':'No cause is established. Ask: what fraction of the job does each person finish in one hour?'}]
        bindings.append({'question_id':q['id'],'source_file':row['source_file'],'source_record_sha256':a['source_record_sha256'],'bank_status_at_authoring':'approved','difficulty':q.get('difficulty'),'language':q.get('language'),'concept_family':'simultaneous-constant-work-rates','diagnostic_template':'add-unit-work-rates-then-reciprocal','diagnostic':{'prompt':'Before calculating together-time, what should you combine?','choices':choices,'confirmation':'Was that the reasoning you used before answering, did you choose it after seeing these choices, did you guess, or did you misclick? A selected option is only a hypothesis.'},'verified_answer':{'option_id':q['answer_option_id'],'value_hours':frac(time),'combined_rate_jobs_per_hour':frac(rate),'method':'reciprocal of the sum of individual unit-work rates','checks':['exact reciprocal verified','calculation matches stored key','one offered option matches exact answer']},'worked_solution':{'steps':[f'In one hour, the first worker completes 1/{x} of the job.',f'In one hour, the second worker completes 1/{y} of the job.',f'Together they complete 1/{x} + 1/{y} = {frac(rate)} of the job per hour.',f'Time = 1 ÷ {frac(rate)} = {frac(time)} hours.'], 'hints':['A completion time is not the same as a work rate.','Find the fraction of the whole job each person completes in one hour.','Add those hourly fractions, then ask how many hours are needed for one whole job.'],'shortcut':'For two constant-rate workers completing the same job together: time = (first time × second time) ÷ (first time + second time). Check that the result is shorter than either solo time.'},'transfer':{'approved_question_id':None,'reason':'No approved, unfamiliar transfer item from a distinct rate context has been verified; repetitions within two-worker work-together questions are retrieval only.'},'outcome_contract':{'diagnostic_is_assisted':True,'misconception_is_hypothesis_only':True,'confirmation_required_for_persistent_hypothesis':True,'uncertain_or_misclick_assigns_hypothesis':False,'diagnostic_correctness_is_not_mastery':True,'independent_transfer_required_for_mastery':True},'status':'draft','editorial_review':None,'runtime_eligible':False})
    side={'schema_version':'dexter-rate45-guide-draft-v0.1','baseline_commit':'ac59a961f3136c88a81219bb3d5f920ba7a7fae2','status':'draft','runtime_eligible':False,'independent_review':None,'learner_evidence':None,'bindings':bindings,'excluded_nonapproved_ids':[x['question_id'] for x in audit['items'] if x['status']!='approved'],'notes':['Only 27 approved-source questions share this same simultaneous-work archetype; they are one learning family, not 27 distinct skills.','All 18 reviewed/draft source records are excluded from tutoring bindings, although their answer calculations were audited.','No distinct-family approved transfer is linked; no question status or canonical record was changed.']}
    (D/'rate45-guide-draft-v0.1.json').write_text(json.dumps(side,ensure_ascii=False,indent=2)+'\n');print('draft bindings',len(bindings),'excluded',len(side['excluded_nonapproved_ids']))
if __name__=='__main__':main()

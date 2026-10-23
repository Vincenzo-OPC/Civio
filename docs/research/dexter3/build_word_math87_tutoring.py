#!/usr/bin/env python3
"""Draft parameter-bound Guide Me templates for source-approved word-math records."""
import json,re,gzip,hashlib
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent
STATE=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))

def flow_choice(i,text,role,fb):return {'id':i,'text':text,'role':role,'feedback':fb}
def answers(q):return {o['option_id']:o['text'] for o in q['options']}
def main():
 audit=json.loads((D/'word-math87-audit-v0.1.json').read_text());cache={};bindings=[]
 for a in audit['items']:
  if a['status']!='approved':continue
  row=next(r for r in STATE['records'] if r['question_id']==a['question_id'])
  if row['source_file'] not in cache:cache[row['source_file']]={q['id']:q for q in json.loads((ROOT/row['source_file']).read_text())['items']}
  q=cache[row['source_file']][a['question_id']];s=q['stem'];params={};steps=[]
  if a['family']=='NUM-WP-AVERAGE':
   p=re.search(r'average (?:age|years of service) of the (\d+) .*? is (\d+).*?\. .*?(?:who is|with) (\d+)',s,re.I)
   assert p;params={'count':int(p[1]),'old_average':int(p[2]),'new_value':int(p[3])};n,mu,v=params.values();val=F(n*mu+v,n+1)
   diag={'prompt':'What does the stated average tell you about the original group?','choices':[flow_choice('old-total','Its total is its average multiplied by its number of members.','correct-rule','Yes. Average × count recovers the original total. Then include the new member and divide by the new count.'),flow_choice('add-first','Add the new member to the average, then divide by the new count.','common-error','The average is not the original total. First recover the old total by multiplying average by the old count.'),flow_choice('divide-old','Divide the old average by the new count, then add the new member.','common-error','The old average describes the old group. Recover that group’s total before including the newcomer.'),flow_choice('unsure','I am unsure, guessed, or selected by mistake.','uncertain','No cause is established. Let’s separate the group’s average from its total first.')],'confirmation':'Was that your original method, or did you choose it after seeing the options?'}
   steps=[f'Original total: {n} × {mu} = {n*mu}.',f'Add the new member: {n*mu} + {v} = {n*mu+v}.',f'Divide by the new count {n+1}: {n*mu+v} ÷ {n+1} = {val}.']
   method='new-member-average';transfer=None;hints=['Average × number of members gives the original total.','Add the new member, then divide by one more member.'];shortcut='New average = old average + (new member’s value − old average) ÷ new group size.'
  elif a['family']=='NUM-WP-GEOM':
   p=re.search(r'(\d+) m long and (\d+) m wide',s,re.I);assert p
   length,width=map(int,p.groups());cost=re.search(r'costs? ₱([\d,]+) per meter',s,re.I)
   if cost:rate=F(cost[1].replace(',',''));val=F(2*(length+width))*rate;params={'length_m':length,'width_m':width,'cost_per_m':str(rate)};steps=[f'Perimeter = 2 × ({length} + {width}) = {2*(length+width)} m.',f'Multiply fence length by cost per meter: {2*(length+width)} × ₱{rate} = ₱{val}.'];method='rectangular-perimeter-times-unit-rate'
   else:val=F(2*(length+width));params={'length_m':length,'width_m':width};steps=[f'Perimeter = 2 × ({length} + {width}) = {val} m.'];method='rectangular-perimeter'
   diag={'prompt':'The question asks about fencing the whole boundary. Which quantity should you find before using a per-meter cost?','choices':[flow_choice('perimeter','The total distance around the rectangle.','correct-rule','Correct. A per-meter charge applies to the boundary length, not the area.'),flow_choice('area','The length multiplied by the width.','common-error','That is the area inside the rectangle. Fencing the boundary requires the distance around it.'),flow_choice('one-side','Only the length plus the width once.','common-error','A rectangle has two lengths and two widths around its boundary.'),flow_choice('unsure','I am unsure, guessed, or selected by mistake.','uncertain','No cause is established. Trace all four sides of the rectangle.')],'confirmation':'Was that the quantity you used before answering, or did you choose it after seeing the options?'}
   hints=['A rectangle has two lengths and two widths.','Find the perimeter first; multiply it by the rate only if the question asks for cost.'];shortcut='Double the sum of length and width, then apply the cost per meter if requested.';transfer=None
  else:
   p=re.search(r'is (\d+) times as old.*?In (\d+) years?, .*? (twice|three times|four times) as old',s,re.I);assert p
   r,t,qw=int(p[1]),int(p[2]),p[3].lower();future={'twice':2,'three times':3,'four times':4}[qw];young=F(t*(future-1),r-future);older=r*young;val=older
   params={'present_ratio':r,'years':t,'future_ratio':future,'younger_now':str(young),'older_now':str(older)}
   diag={'prompt':f'Let the younger person’s present age be x. Which equation represents the ages {t} years from now?','choices':[flow_choice('both-advance',f'{r}x + {t} = {future}(x + {t})','correct-rule','Yes. Both people age by the same number of years. The future ratio applies to their future ages.'),flow_choice('only-younger-advances',f'{r}x = {future}(x + {t})','common-error','This advances the younger person but leaves the older person at the present age. Add the same time to both.'),flow_choice('only-older-advances',f'{r}x + {t} = {future}x','common-error','This advances the older person but leaves the younger person at the present age. Add the same time to both.'),flow_choice('unsure','I am unsure, guessed, or selected by mistake.','uncertain','No cause is established. Track each person’s present age and future age separately.')],'confirmation':'Was that how you set up the original problem, or did you choose it after seeing the options?'}
   steps=[f'Let the younger person’s present age be x. The older person is {r}x now.',f'After {t} years: {r}x + {t} = {future}(x + {t}).',f'Solve: x = {young}; the older person’s present age is {r} × {young} = {older}.',f'Check: now {older}:{young} = {r}:1; in {t} years, {older+t}:{young+t} = {future}:1.']
   hints=['Choose x for the younger person’s age now; express the older person’s current age with the given ratio.','After t years, add t to both ages before applying the future ratio.'];shortcut='The younger age is t × (future ratio − 1) ÷ (present ratio − future ratio); multiply by the present ratio if asked for the older person.';method='age-ratio-forward-time';transfer=None
  key=answers(q)[q['answer_option_id']]
  assert F(re.sub(r'[^0-9./-]','',key.split()[0]))==val
  bindings.append({'question_id':q['id'],'source_file':row['source_file'],'source_record_sha256':row['source_record_sha256'],'bank_status_at_authoring':'approved','difficulty':q.get('difficulty'),'parameters':params,'method':method,'diagnostic':diag,'hints':hints,'worked_solution':steps,'mental_shortcut':shortcut,'verified_answer':{'option_id':q['answer_option_id'],'value':str(val),'exact_calculation_matches_stored_key':True},'existing_explanation_reference':q['reveal'].get('why_correct'),'transfer':{'approved_question_id':transfer,'status':'gap_unresolved'},'assistance_contract':{'diagnostic_and_all_retries_assisted':True,'diagnostic_does_not_establish_mastery':True,'uncertain_or_misclick_assigns_no_hypothesis':True,'confirmation_is_self_report_not_independent_proof':True},'status':'draft','editorial_review':None,'runtime_eligible':False})
 doc={'schema_version':'dexter-word-math87-guide-draft-v0.1','baseline_commit':'c2f003c6746573e82d8d07ec1206b9ad22aad3ef','status':'draft','runtime_eligible':False,'human_review':None,'learner_evidence':None,'bindings':bindings,'excluded_nonapproved_ids':[a['question_id'] for a in audit['items'] if a['status']!='approved'],'notes':['Exact calculations are checked; wording, diagnostic quality, and feedback still require editorial review.','Three separate method families use one reusable interaction shape each.','No unrelated approved transfer candidate is asserted.','No canonical question, option, key, status or source reference was changed.']}
 (D/'word-math87-guide-draft-v0.1.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n');print('draft bindings',len(bindings),'excluded',len(doc['excluded_nonapproved_ids']))
if __name__=='__main__':main()

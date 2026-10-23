#!/usr/bin/env python3
"""Scoped draft overlays for 5 interest and 20 ratio bindings; no bank writes."""
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
BASE='70586e4e15455a9e071255ca1bb52656006d107c'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(q):return hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def money(n):return f'₱{float(F(n)):,.2f}'.removesuffix('.00')
def o(i,t,f,n,e='unknown',h=None):return dict(id=i,text=t,feedback=f,next=n,evidence=e,hypothesis=h)
def n(prompt,options,kind='comprehension'):return dict(kind=kind,prompt=prompt,options=options)

def interest_flow():
    nodes={
      'target':n('What amount does the question ask you to find?',[
        o('interest','The interest charge alone','Keep the borrowed money separate from the extra charge. Next identify the base amount.','principal','consistent'),
        o('repayment','The borrowed money plus interest','Which quantity were you trying to report when you chose your answer?','confirm_target','possible','interest-versus-repayment'),
        o('unknown','I am not sure','Interest is the extra borrowing charge. The question asks for that charge alone.','principal')]),
      'confirm_target':n('Which describes your first approach?',[
        o('total','I thought the question wanted the total repayment','That supports a target-quantity mix-up in this attempt. Calculate the extra interest but do not add the principal to the requested answer.','principal','supports_prior_repayment','interest-versus-repayment'),
        o('extra','I knew it wanted interest, but added the principal anyway','That may be an extra step rather than a misunderstanding of the words. Stop when the interest has been found.','principal','self_report_only'),
        o('other','I do not remember, used another method, or selected by mistake','We do not know the cause yet. Separate principal and interest before calculating.','principal')],kind='self_report'),
      'principal':n('In this question, what does {principal} represent?',[
        o('borrowed','The amount originally borrowed','Yes. This is the principal used to calculate simple interest.','rate','consistent'),
        o('charge','The interest already owed','The wording says this amount was borrowed. It is the principal, not a calculated charge.','rate','possible','principal-versus-interest'),
        o('unknown','I am not sure','The principal is the starting loan amount. Here it is {principal}.','rate')]),
      'rate':n('What does {rate}% per year mean here?',[
        o('original','{rate} out of every 100 of the original principal for each full year','Yes. Under this simple-interest model the base stays the original principal.','time','consistent'),
        o('growing','{rate}% of a new balance that includes earlier interest each year','Which base did you use for later years?','confirm_base','possible','simple-versus-compound'),
        o('fixed','Exactly ₱{rate} for the whole loan each year','Did you treat the rate numeral as a fixed peso charge?','confirm_rate','possible','percent-as-fixed-pesos'),
        o('unknown','I am not sure','Percent means out of 100. The annual charge is that fraction of the principal.','hint_1')]),
      'confirm_base':n('Which matches your calculation?',[
        o('compound','I added earlier interest to the base before calculating the next year','That describes compounding. This question specifies simple interest, so use the original principal each year.','time','supports_prior_growing','simple-versus-compound'),
        o('original','I used the original principal but chose the wrong description','Then the selected description does not establish compounding. We can check the duration next.','time','self_report_only'),
        o('unknown','I am not sure or used another method','The cause remains unknown. Use the original principal for this simple-interest model.','time')],kind='self_report'),
      'confirm_rate':n('How did you use the number {rate}?',[
        o('pesos','I used it as a fixed peso amount','That supports a percent-unit interpretation in this attempt. The amount changes with the principal; {rate}% means {rate}/100 of it per year.','hint_1','supports_prior_fixed','percent-as-fixed-pesos'),
        o('fraction','I intended a fraction of the principal','Then we should not label the method from the selected description alone. Check the duration next.','time','self_report_only'),
        o('unknown','I do not remember or used another method','We do not have enough evidence for a cause. A percent reminder may help.','hint_1')],kind='self_report'),
      'time':n('Which duration matches the question, using years to match the annual rate?',[
        o('duration','{duration}','Use that duration with the annual charge.','method','consistent'),
        o('wrong','{wrong_duration}','Which interpretation led to that duration?','confirm_time','possible','duration-conversion'),
        o('unknown','I am not sure','The rate is per year. Extra months are divided by 12, not written as decimal digits after the whole years.','time_help')]),
      'confirm_time':n('Which describes how you handled the time?',[
        o('digits','I wrote the month count directly after the decimal point','Months are twelfths of a year. Six months is 6/12 = one half, not six tenths.','time_help','supports_only_if_months_present','months-as-decimal-digits'),
        o('one','I calculated only one year and did not include the full duration','That may be an unfinished time step. Include every stated year and any extra months.','time_help','self_report_only'),
        o('other','Another method, a mistaken selection, or I do not remember','The reason remains unknown. Match the duration to the annual rate.','time_help')],kind='self_report'),
      'time_help':{'kind':'hint','level':1,'text':'A year has 12 months. Six months is half a year. For a whole-year duration, keep all the stated years.','next':'method','requires':'learner_requests_next_hint'},
      'method':n('Once the interest for one year is known, how do you find the interest for the whole duration?',[
        o('multiply','Multiply the annual interest by the duration in years','Yes. Keep that interest result separate from the original loan.','retry','consistent'),
        o('principal','Add the principal to the annual interest','That gives a different quantity and may also leave out years. The target here is interest alone for the full duration.','hint_1','possible','target-or-duration'),
        o('unknown','I am not sure','Simple interest uses the same annual charge for equal years. Count all years and the stated fraction of a year.','hint_1')]),
      'hint_1':{'kind':'hint','level':1,'text':'Find 1% of the principal by dividing by 100; multiply by the annual rate numeral. This gives one year’s interest.','next':'hint_2','requires':'learner_requests_next_hint'},
      'hint_2':{'kind':'hint','level':2,'text':'Multiply that annual interest by the full years. For six extra months, add half of one year’s interest.','next':'retry','requires':'learner_requests_next_hint'},
      'retry':{'kind':'action','action':'return_to_original_mcq','assisted':True,'next':'explain','requires':'learner_requests_authorized_reveal'},
      'explain':{'kind':'action','action':'authorized_binding_worked_solution','next':'transfer','requires':'server_reveal_authorized'},
      'transfer':{'kind':'terminal','action':'eligible_transfer_or_truthful_gap','full_target_transfer_id':None}}
    return dict(entry='target',node_budget=17,nodes=nodes,exits=['stop','authorized_reveal'],evidence_contract_ref='price15_v0.3_evidence_context_contract')

def ratio_flow():
    return dict(entry='whole',node_budget=17,exits=['stop','authorized_reveal'],evidence_contract_ref='price15_v0.3_evidence_context_contract',nodes={
      'whole':n('What does the given {total} represent?',[
        o('combined','The combined fund for both named recipients','Yes. The ratio describes how to split that whole fund.','order','consistent'),
        o('second','Only the second recipient’s share','Which meaning did you give that amount when solving?','confirm_whole','possible','whole-versus-share'),
        o('unknown','I am not sure','The wording says the amount is shared or divided. It names the whole fund before the shares are found.','order')]),
      'confirm_whole':n('Which describes your approach?',[
        o('share','I treated the given amount as one recipient’s share','That supports a whole-versus-share interpretation in this attempt. Here the amount is both shares combined.','order','supports_prior_second','whole-versus-share'),
        o('total','I knew it was the whole but selected the other description','Then the selection does not establish that misconception. We can check ratio order next.','order','self_report_only'),
        o('unknown','I do not remember or used another method','The cause remains unknown. Keep the full fund separate from either share.','order')],kind='self_report'),
      'order':n('In {first_parts}:{second_parts}, which number belongs to the second named recipient?',[
        o('second','{second_parts} parts','Yes. Keep that recipient attached to those parts.','denominator','consistent'),
        o('first','{first_parts} parts','Did you reverse the recipient order, or was that a mistaken selection?','confirm_order','possible','recipient-order'),
        o('unknown','I am not sure','Match the first recipient to the first ratio number and the second recipient to the second number.','denominator')]),
      'confirm_order':n('Which matches your first calculation?',[
        o('reversed','I assigned the first ratio number to the second recipient','That supports an order mix-up here. Ratio order follows recipient order in the wording.','denominator','supports_prior_first','recipient-order'),
        o('misclick','I intended the second ratio number but selected the first','Then do not infer an order misconception. Check the total number of parts next.','denominator','self_report_only'),
        o('unknown','I used another method or cannot explain yet','We do not know the cause. Label each recipient before counting all parts.','denominator')],kind='self_report'),
      'denominator':n('How many equal parts does the entire fund contain?',[
        o('sum','{sum_parts} parts: {first_parts} + {second_parts}','Yes. One part is the whole fund divided by all those equal parts.','one_part','consistent'),
        o('target','Only {second_parts} parts','Which rule did you use to divide the whole fund?','confirm_parts','possible','target-only-denominator'),
        o('two','Two equal parts because there are two recipients','Two recipients do not necessarily get equal shares. The ratio counts how many equal-sized units each receives.','hint_1','possible','equal-sharing'),
        o('unknown','I am not sure','Count all the ratio parts, not only the parts for the recipient being asked about.','hint_1')]),
      'confirm_parts':n('Which describes your division step?',[
        o('target','I divided the whole fund by the requested recipient’s ratio number','That supports a denominator mix-up. To find one equal part, divide by the sum of both ratio numbers.','hint_1','supports_prior_target','target-only-denominator'),
        o('sum','I used the sum but chose the wrong description','Then we should not label your denominator from that selection. Check what one part means.','one_part','self_report_only'),
        o('unknown','I cannot remember, guessed, or used another method','The cause remains unknown. We can rebuild the equal-part interpretation.','hint_1')],kind='self_report'),
      'one_part':n('After dividing {total} by {sum_parts}, what have you found?',[
        o('unit','The value of one equal ratio part','Yes. The requested recipient receives several such parts.','target','consistent'),
        o('answer','The requested recipient’s complete share','Did you stop at one part because you thought that was the whole requested share?','confirm_unit','possible','one-part-versus-share'),
        o('unknown','I am not sure','That division finds one equal-sized unit. Multiply it by the requested recipient’s number of units.','hint_2')]),
      'confirm_unit':n('Which best describes why you stopped there?',[
        o('meaning','I thought one part was the recipient’s entire share','That supports a part-versus-share mix-up in this attempt. The requested recipient gets {second_parts} of those equal parts.','hint_2','supports_prior_answer','one-part-versus-share'),
        o('unfinished','I knew I still had to multiply but did not finish','That may be incomplete work rather than a conceptual mistake. Include the requested number of parts.','hint_2','self_report_only'),
        o('unknown','I do not know or selected the description by mistake','No specific cause is established. Keep one part separate from the full share.','hint_2')],kind='self_report'),
      'target':n('Which final quantity should you report?',[
        o('second','The second named recipient’s share','Yes. Use {second_parts} parts, then check both shares add to {total}.','retry','consistent'),
        o('first','The first named recipient’s share','That is a different share. Reread whose amount is requested before multiplying.','hint_2','possible','other-recipient'),
        o('unknown','I am not sure','The question asks for the second named recipient. Keep that name beside {second_parts} parts.','hint_2')]),
      'hint_1':{'kind':'hint','level':1,'text':'Add the two ratio numbers. That sum counts all the equal parts in the combined fund.','next':'hint_2','requires':'learner_requests_next_hint'},
      'hint_2':{'kind':'hint','level':2,'text':'Divide the total fund by all parts, then multiply one part by the requested recipient’s parts.','next':'retry','requires':'learner_requests_next_hint'},
      'retry':{'kind':'action','action':'return_to_original_mcq','assisted':True,'next':'explain','requires':'learner_requests_authorized_reveal'},
      'explain':{'kind':'action','action':'authorized_binding_worked_solution','next':'transfer','requires':'server_reveal_authorized'},
      'transfer':{'kind':'terminal','action':'eligible_transfer_or_truthful_gap','full_target_transfer_id':None}})

def main():
    base=json.loads((OUT/'pilot-v0.1.json').read_text());selected=[b for b in base['bindings'] if b['recipe_id'] in ('simple-interest','two-share-total')]
    bindings=[]
    for old in selected:
        b={k:copy.deepcopy(old[k]) for k in ('question_id','source_file','source_question_hash','source_record_sha256')}
        q=next(q for q in json.loads((ROOT/b['source_file']).read_text())['items'] if q['id']==b['question_id']);assert fingerprint(q)==b['source_record_sha256']
        p=old['math_verification']['parameters'];b.update(status='draft',base_binding_sha256=fingerprint(old),review={'human_reviewer_1':None,'human_reviewer_2':None,'adjudication':None},family=old['recipe_id'],visibility={'meanings_and_solution':'authorized_explanation_only','flow':'one_current_node_only'},source_codes_preserved=True)
        if b['family']=='simple-interest':
            principal=F(p['principal']);rate=p['annual_rate_percent'];years=p['years'];months=p['months'];annual=principal*rate/100;answer=annual*years+annual*F(months,12)
            duration=f'{years} years'+(' plus half a year (6 months)' if months==6 else '')
            wrong=f'{years}.6 years' if months==6 else 'One year only'
            b.update(parameters={'principal':money(principal),'rate':str(rate),'duration':duration,'wrong_duration':wrong},worked_solution=[f'1% of {money(principal)} is {money(principal/100)}.',f'{rate}% for one year is {money(annual)}.',f'Full years contribute {money(annual*years)}.' ]+([f'Six months contributes half an annual charge: {money(annual/2)}.'] if months else [])+[f'Interest alone: {money(answer)}. Do not add the loan amount.',f'Check: {money(principal)} × {rate}/100 × ({years} + {months}/12) = {money(answer)}.'],mental_method='Find 1%, multiply by the rate numeral, then use whole annual charges and half an annual charge for six months.',prerequisites=['percent-as-hundredths','annual-rate-units','year-as-12-months','principal-versus-interest'],local_hypotheses={'NUM-PARTIAL':'duration-omitted-or-stopped-early','NUM-UNIT':'months-as-decimal-digits','NUM-EXTRA-STEP':'interest-versus-repayment','NUM-DECIMAL':'rate-scale-possible'},transfer={'full_target_distinct_family_id':None,'same_family_practice_candidates':['CIVIO-NUM-WP-PCT-CHANGE-000013'],'related_component_candidate':'CIVIO-NUM-WP-PCT-CHANGE-000121','component_limit':'Sale-price application checks percentage amount and target quantity; it does not test annual rate or duration.','approved_for_transfer':False})
        else:
            total=F(p['total']);a=p['first_parts'];z=p['second_parts'];unit=total/(a+z);answer=unit*z
            b.update(parameters={'total':money(total),'first_parts':str(a),'second_parts':str(z),'sum_parts':str(a+z)},worked_solution=[f'The whole fund has {a} + {z} = {a+z} equal parts.',f'One part is {money(total)} ÷ {a+z} = {money(unit)}.',f'The second recipient gets {z} × {money(unit)} = {money(answer)}.',f'Check: the first share is {money(unit*a)}; both add to {money(total)}, with ratio {a}:{z}.'],mental_method='Find one equal part first. Keep the requested recipient’s name attached to its ratio number; check both shares reconstruct the fund.',prerequisites=['whole-versus-part','ordered-ratio-meaning','division','multiplication'],local_hypotheses={'NUM-PARTIAL':'one-part-versus-share','NUM-WRONG-BASE':'target-only-denominator','NUM-OTHER-SHARE':'other-recipient'},transfer={'full_target_distinct_family_id':None,'same_family_practice_candidates':['CIVIO-NUM-WP-RATIO-000021'],'related_component_candidate':None,'component_limit':'The approved ratio family repeats second-share-from-total. Combined work-rate items add rate/fraction prerequisites and are not automatic transfer for this beginner skill.','approved_for_transfer':False})
        bindings.append(b)
    data={'schema_version':'dexter-math25-overlay-v0.1','baseline_commit':BASE,'status':'draft','runtime_eligible':False,'base_sidecar_sha256':digest(OUT/'pilot-v0.1.json'),'evidence_contract_source':'price15-v0.3-patch.json:evidence_context_contract operation','evidence_contract_sha256':digest(OUT/'price15-v0.3-patch.json'),'policy':{'tutor_nodes_update_knowledge':False,'uncertainty_assigns_hypothesis':False,'hypotheses':'Local proposals only. Confirm a candidate from compatible pre-correction responses; no diagnosis from an answer alone.','assistance':'Record help before serving tutoring; preserve the first independent answer, but all later retries on this item stay assisted.','display':'Server controls response shuffle and keeps stable authoring IDs distinct from opaque client response IDs.','fallback':'Unreviewed/stale metadata uses ordinary authorized explanation. Missing approved transfer means a truthful gap.','strict':'No tutor payload during an active Strict Mock.'},'flows':{'simple-interest':interest_flow(),'two-share-total':ratio_flow()},'bindings':bindings,'independent_ai_review':None,'human_adjudication':None,'learner_evidence':None}
    target=OUT/'math25-v0.1.json';text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    if target.exists():assert target.read_text()==text,'Version changed draft explicitly; never overwrite silently.'
    else:target.write_text(text)
    print('Prepared 5 interest and 20 ratio draft bindings, reusing two authored flows. Source questions and original sidecars unchanged.')

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Author a separate, draft-only overlay. Never regenerate pilot-v0.1.json.
This is an author second pass, not an independent human review.
"""
import collections
import hashlib
import json
import re
from pathlib import Path
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BASE = '4934bc2c4551ee6f9823db99f3f8dcf9926e01de'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def fullhash(q): return hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def money(n): return f'₱{float(F(n)):,.2f}'.removesuffix('.00')
def amount(s): return F(re.search(r'₱([\d,.]+)',s)[1].replace(',',''))
def save(name,obj):
    path=OUT/name; text=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
    if path.exists() and path.read_text()==text: return
    if path.exists(): raise RuntimeError('Existing authored overlay differs; revise explicitly in a new version, never overwrite silently.')
    path.write_text(text)

def opt(oid,text,feedback,next_id,evidence='unknown',hypothesis=None):
    return dict(id=oid,text=text,feedback=feedback,next=next_id,evidence=evidence,hypothesis=hypothesis)
def node(prompt,options,kind='comprehension',**extra):
    return dict(prompt=prompt,options=options,kind=kind,**extra)

def flow(successive):
    change='raise' if successive else 'discount'
    nodes={
      'interpret':node('What does {original} represent in the question?',[
        opt('before',f'The price before the {change}',f'You placed it before the {change}. Now choose what happens to that starting price.','direction','consistent'),
        opt('after',f'The price after the {change}','Let us check which wording led you there before changing your method.','confirm','possible','given-stage'),
        opt('unknown','I am not sure','Let us locate the given price and the action that follows it.','wording_help')]),
      'confirm':node('Which best describes why you placed the given price after the change?',[
        opt('assumption','I assumed a stated price already includes the change','That helps locate the issue: the given price comes before the stated action. We will label the stages before calculating.','direction','supports_if_prior_after','given-stage'),
        opt('misread','I overlooked the words describing the change','That sounds like a reading slip in this attempt. Reread the action, then choose the operation.','direction','self_report_only'),
        opt('guess','I guessed or cannot explain yet','We do not yet know the cause. Use the wording reminder and try the next step.','wording_help')],kind='self_report'),
      'wording_help':node(f'The price is given first; the {change} is then applied. Which label belongs to the given amount?',[
        opt('before','Before the change','Yes. This is a supported retry after help, not new independent evidence.','direction','assisted_check'),
        opt('after','After the change','Keep the given amount at the start of the timeline. You can open the worked explanation if that remains unclear.','hint_1','assisted_check'),
        opt('unknown','Still unsure','We can take this in smaller steps or use the worked explanation.','hint_1')],kind='assisted_check'),
      'direction':node(f'The given amount is before the {change}. Which action comes next?',[
        opt('forward','Add a percentage of it' if successive else 'Subtract a percentage of it','That follows the direction stated in the question.','base' if successive else 'percent_meaning','consistent'),
        opt('reverse','Divide to recover an earlier price','Division would recover an earlier value if the changed price were given. Here we start before the change.','hint_1','possible','forward-reverse'),
        opt('unknown','I am not sure','Name the action first: a raise adds; a discount takes away.','hint_1')]),
      'percent_meaning':node('In this question, {rate}% means what?',[
        opt('fraction','{rate} out of every 100 parts of the stated base','Right. It is a proportion of a price, not a fixed number of pesos.','target','consistent'),
        opt('pesos','Exactly {rate} pesos, whatever the price','Is that how you treated the percentage when choosing your answer?','confirm_units','possible','percent-as-pesos'),
        opt('unknown','I am not sure','Percent means out of 100. We can use 10%, half, or a quarter as a starting point.','hint_1')]),
      'confirm_units':node('When you first answered, how did you use the number {rate}?',[
        opt('fixed','I treated it as a fixed peso amount','Then the unit is the part to correct: {rate}% changes with the base price. We still have not tested your arithmetic.','hint_1','supports_if_prior_pesos','percent-as-pesos'),
        opt('proportion','I meant a proportion but selected the wrong description','We should not label this as percent-as-pesos from that selection. Check the requested amount next.','target','self_report_only'),
        opt('unknown','I do not remember','The cause remains unknown. Use a small percent reminder before trying again.','hint_1')],kind='self_report'),
      'target':node('Which amount must your final answer name?',[
        opt('paid','The price the buyer pays after all stated changes','Yes. A change amount can be calculated correctly and still answer the wrong question.','arithmetic_check','consistent'),
        opt('saved','Only the amount taken off','Did you stop at the amount taken off because you thought that was being asked?','confirm_target','possible','change-versus-result'),
        opt('unknown','I am not sure','Look at “final price” or “how much does a buyer pay.” It asks for what remains to be paid.','hint_1')]),
      'confirm_target':node('Which matches your first approach?',[
        opt('stopped','I thought the amount taken off was the requested answer','That supports a target-quantity mix-up in this attempt. Keep “amount saved” separate from “amount paid.”','hint_1','supports_if_prior_saved','change-versus-result'),
        opt('slip','I knew it asked for the price but stopped early','That may be an unfinished solution, not a misunderstanding of the words.','hint_1','self_report_only'),
        opt('unknown','I am not sure','No specific cause is established. Label the final amount before choosing.','hint_1')],kind='self_report'),
      'arithmetic_check':node('A small calculation check: what is 10% of ₱200?',[
        opt('20','₱20','That calculation is correct. If the original answer is still wrong, check the stage, base and target rather than assuming all percentage arithmetic is weak.','retry','arithmetic_sample_correct'),
        opt('2','₱2','₱2 is 1% of ₱200. For 10%, divide by 10: ₱20. This one response does not establish a lasting arithmetic difficulty.','hint_1','possible','percent-scale'),
        opt('10','₱10','The 10 is a percentage, not a fixed peso amount. Ten out of every hundred is ₱20 out of ₱200.','hint_1','possible','percent-as-pesos'),
        opt('unknown','I am not sure','10% is one tenth. Divide ₱200 into ten equal parts.','hint_1')],kind='arithmetic_sample',skip_rule='Skip only if an equivalent pre-help arithmetic response is actually recorded; never infer ability from the original MCQ key alone.'),
      'hint_1':dict(kind='hint',level=1,text='Write the labels first: before the change, after the change, and the amount asked for.',next='hint_2',requires='learner_requests_next_hint'),
      'hint_2':dict(kind='hint',level=2,text='Percent means out of 100. The base is the price at the moment this change happens.',next='hint_3',requires='learner_requests_next_hint'),
      'hint_3':dict(kind='hint',level=3,text='Find the increase from the starting price. Then find the discount from the raised price and take it off.' if successive else 'Find {rate}/100 of the starting price. That is the saving; subtract it to find the amount paid.',next='retry',requires='learner_requests_next_hint'),
      'retry':dict(kind='action',action='return_to_original_mcq',assisted=True,next='explain',requires='learner_requests_authorized_reveal'),
      'explain':dict(kind='action',action='authorized_existing_worked_solution',next='transfer',requires='server_reveal_authorized'),
      'transfer':dict(kind='terminal',action='eligible_approved_transfer_or_truthful_gap')}
    if successive:
        nodes['base']=node('For the later discount, which amount is the base?',[
          opt('intermediate','The price after the raise','Yes. The discount uses the intermediate price.','percent_meaning','consistent'),
          opt('original','The price before the raise','Before we change that, which rule were you using for the two percentages?','confirm_base','possible','base-stays-original'),
          opt('unknown','I am not sure','The words “new price” identify the price after the raise. We can work from those stages.','hint_1')])
        nodes['confirm_base']=node('Which describes your approach?',[
          opt('same','I used the first price for both percentages','That supports a same-base approach in this attempt. Each change instead uses the price just before it.','hint_1','supports_if_prior_original','base-stays-original'),
          opt('net','I subtracted the percent rates first','That supports combining rates before applying them. These changes use different bases, so that shortcut does not apply.','hint_1','self_report_only','net-rates'),
          opt('unknown','I selected without a rule','A wrong selection alone does not establish a misconception. We will label the two bases.','hint_1')],kind='self_report')
    return dict(entry='interpret',nodes=nodes,exits=['stop','authorized_reveal'],node_budget=16,diagnosis_policy='Only combine a prior relevant selection with a matching pre-correction self-report. Call it supported for this attempt, never proven or a permanent learner trait. Post-teaching answers are assisted checks, not independent confirmation.')

def contrast():
    # Authored instructional checks only. They are not bank additions or mastery evidence.
    nodes={
      'meaning':node('The problem calls ₱640 the original price. What does ₱640 represent?',[
        opt('original','The price before the markup','Correct. We can build forward from that starting value.','forward','consistent'),
        opt('marked','The price after markup','Before calculating, what made you place it after the markup?','reason','possible','given-stage'),
        opt('unknown','I am not sure','Original names the value before the stated changes. Let us check the direction next.','forward')]),
      'reason':node('Which best describes your interpretation?',[
        opt('assumed','I took ₱640 to mean an already marked-up price','That explains why you wanted to reverse it. In this problem, “original” places ₱640 before the markup. Your calculation of 25% can still be correct.','forward','supports_if_prior_marked','given-stage'),
        opt('slip','I missed the word original','That points to a reading slip, not proof of weak percentage arithmetic.','forward','self_report_only'),
        opt('unknown','I cannot tell yet','The cause is still uncertain. Place ₱640 before the action because the wording says original.','forward')],kind='self_report'),
      'forward':node('Using the already-correct result 25% of ₱640 = ₱160, what happens next?',[
        opt('add','Add ₱160 to ₱640','Yes. The markup is added to the original, giving ₱800.','discount_base','consistent'),
        opt('divide','Divide ₱640 by 1.25','That would answer a different problem where ₱640 was the marked-up price. Here the original is already given.','discount_base','possible','forward-reverse'),
        opt('unknown','I am not sure','A markup increases the starting value. ₱640 + ₱160 gives ₱800.','discount_base')]),
      'discount_base':node('After the markup gives ₱800, which value supplies the 20% discount?',[
        opt('new','₱800','Yes. 20% of ₱800 is ₱160, so the final price is ₱640.','reverse_meaning','consistent'),
        opt('old','₱640','The discount follows the markup, so it uses ₱800. Taking 20% off that gives ₱640.','reverse_meaning','possible','base-stays-original'),
        opt('unknown','I am not sure','Use the price at the moment of the discount: ₱800. The discount is ₱160 and the final price is ₱640.','reverse_meaning')]),
      'reverse_meaning':node('Now change the wording: ₱640 is the price AFTER a 25% markup. What percentage of the unknown original is ₱640?',[
        opt('125','125%','Right. The final price contains the original 100% plus 25%.','reverse_operation','consistent'),
        opt('100','100%','The given amount now includes the markup. It is 125% of the original.','reverse_operation','possible','final-base'),
        opt('unknown','I am not sure','Call the original 100%. With a further 25%, the given final amount is 125%.','reverse_operation')]),
      'reverse_operation':node('Which operation undoes multiplication by 1.25?',[
        opt('divide','Divide by 1.25','Yes. ₱640 ÷ 1.25 = ₱512. A check gives ₱512 + ₱128 = ₱640.','different_example','consistent'),
        opt('subtract','Subtract 25% of ₱640','That takes a quarter of the larger final amount. It gives ₱480, whose 25% markup reaches only ₱600. Divide by 1.25 instead: ₱512.','different_example','possible','subtract-to-reverse'),
        opt('unknown','I am not sure','If original × 1.25 = final, divide the final by 1.25 to recover the original. Here that gives ₱512.','different_example')]),
      'different_example':node('A bag costs ₱900 AFTER a 25% markup. Which statement identifies the unknown correctly?',[
        opt('base','The original is unknown; ₱900 is 125% of it','Yes. Now try the calculation without another hint.','different_calculation','assisted_check'),
        opt('start','₱900 is the original, so the markup must still be added','“After” means the increase is already included. This example is reverse, not forward.','different_calculation','assisted_check'),
        opt('unknown','I am not sure','The final price is given; the earlier price is the unknown.','different_calculation')],kind='assisted_check'),
      'different_calculation':node('What was the bag’s original price?',[
        opt('720','₱720','Check: 25% of ₱720 is ₱180; adding gives ₱900. This is a supported learning check, not an independent mastery result.','fresh','assisted_check'),
        opt('675','₱675','That subtracts 25% of the final price. ₱675 × 1.25 = ₱843.75, so it fails the forward check.','fresh','assisted_check'),
        opt('1125','₱1,125','That applies another markup to the final price. The original should be smaller than ₱900.','fresh','assisted_check'),
        opt('unknown','I am not sure','Use 900 ÷ 1.25, or 900 × 4/5. Continue with guided practice if needed.','fresh')],kind='assisted_check'),
      'fresh':dict(kind='terminal',action='request_approved_unassisted_item',full_target_transfer_id=None,missing_type='reverse percentage or a distinct successive-change application',fallback='No approved full-target transfer was found. Offer a clearly labeled cross-context percentage-base task if eligible; otherwise stop without claiming mastery.')}
    return dict(id='original-versus-marked-up-640-v0.2',status='draft',bank_question_id=None,entry='meaning',nodes=nodes,arithmetic_evidence='The owner supplied that 25% of ₱640 = ₱160 was already understood. Do not generalize that observation to other learners.',requires='authorized_explanation_context',independent_review=None,runtime_approved=False,checks={'forward':640,'reverse':512,'new_reverse':720,'wrong_reverse_forward':600,'new_wrong_reverse_forward':'843.75'})

def main():
    base=json.loads((OUT/'pilot-v0.1.json').read_text())
    selected=[b for b in base['bindings'] if b['recipe_id'] in ('successive-price','sale-price')]
    manifest=json.loads((ROOT/'docs/research/bank/civio-flat-2100-manifest-2026-10-22.json').read_text())['items']
    cache={}
    def source(m):
        if m['source_file'] not in cache:
            d=json.loads((ROOT/m['source_file']).read_text());cache[m['source_file']]=d['items'] if isinstance(d,dict) else d
        return next(q for q in cache[m['source_file']] if q['id']==m['id'])
    # Targeted transfer search, not a repeat inventory or semantic audit of other bank items.
    numerical=[m for m in manifest if m['domain']=='numerical']
    hits=[]
    for m in numerical:
        q=source(m)
        if not re.search(r'%|percent|markup|mark.up|discount|profit|loss|interest',q['stem'],re.I):continue
        family='simple-interest' if 'simple interest' in q['stem'] else 'successive-price' if 'raised' in q['stem'] else 'sale-price' if re.search(r'\b\d+%\s+off\b',q['stem']) else 'other_percentage_or_profit'
        hits.append(dict(question_id=q['id'],status=q['status'],source_file=m['source_file'],source_hash=m['content_sha256'],stem=q['stem'],family=family))
    references={}
    for suffix in ('000013','000124','000121'):
        qid='CIVIO-NUM-WP-PCT-CHANGE-'+suffix;m=next(m for m in manifest if m['id']==qid);q=source(m)
        references[qid]=dict(source_file=m['source_file'],source_question_hash=m['content_sha256'],source_record_sha256=fullhash(q),status=q['status'],track=q['track'],answer_option_id=q['answer_option_id'],answer_text=next(o['text'] for o in q['options'] if o['option_id']==q['answer_option_id']),role={'000013':'different_context_percent_base_only','000124':'sale_to_changed_base_extension','000121':'same_family_sale_practice_only'}[suffix],reviewer=None,usable_at_runtime=False)
    reviews=[]; bindings=[]
    for b in selected:
        qid=b['question_id'];succ=b['recipe_id']=='successive-price';p=b['math_verification']['parameters'];original=F(p['original']);rate=p['increase_percent'] if succ else p['discount_percent']
        issues=['F01','F02','F03','F04','F05','F06']
        if not succ:issues.append('F07')
        if succ and p['decrease_percent']==50:issues.append('F08')
        if succ and p['increase_percent']==p['decrease_percent']:issues.append('F09')
        candidates=['CIVIO-NUM-WP-PCT-CHANGE-000013'] if succ else ['CIVIO-NUM-WP-PCT-CHANGE-000124','CIVIO-NUM-WP-PCT-CHANGE-000013']
        sibling=[x['question_id'] for x in selected if x['recipe_id']==b['recipe_id'] and x['question_id']!=qid]
        evaluations={
          'interpretation':'Correct; given is pre-change and target is final amount paid.',
          'comprehension_diagnostic':'Correct topic, but one binary choice does not test reasoning or arithmetic separately.',
          'branch_feedback':'Revise: generic correct feedback; wrong and unsure duplicate one another.',
          'misconception_evidence':'Revise: retain candidate only until compatible pre-teaching self-report; no permanent diagnosis.',
          'hint_progression':'Conceptually ordered, but no visibility/request contract; given_meanings would spoil the first diagnostic if shown first.',
          'solution_and_shortcut':'Exact calculations correct. Retain solution; add a practical mental method.',
          'stage_distinction':'Revise: test original/intermediate/target in separate turns; do not show stage meanings before interpret.',
          'foundational_access':'Revise: percent-as-hundredths check and optional benchmark arithmetic; decimal multiplication is not a mandatory prerequisite.',
          'tutor_voice':'Revise generic praise and duplicated feedback; use brief response-specific statements.',
          'safe_reuse':'Two semantic templates only; allowlisted parameters, family validation and source hashes; do not bind by broad archetype alone.'}
        evaluations['coincidence_warning']='Discount amount equals final amount; require the target-quantity response.' if 'F08' in issues else 'No 50%-discount coincidence in this item.'
        reviews.append(dict(question_id=qid,criteria=evaluations,finding_ids=issues,author_second_pass=True,independent_reviewer=None,adjudication=None))
        def mental(r):
            return {10:'Find 10% by dividing by 10.',15:'Find 10%, then half of that for 5%; add them.',20:'Find one fifth by dividing by 5.',25:'Find one quarter by dividing by 4.',30:'Find 10% and multiply it by 3.',40:'Find 10% and multiply it by 4.',50:'Take half.'}[r]
        mental_steps=[mental(rate)]
        if succ:mental_steps+=['Add that increase to the starting price.',mental(p['decrease_percent'])+' Use the raised price this time.','Subtract that discount from the raised price.']
        else:mental_steps+=['Subtract the saving from the starting price.']
        bindings.append(dict(question_id=qid,source_question_hash=b['source_question_hash'],source_record_sha256=b['source_record_sha256'],source_file=b['source_file'],base_binding_sha256=fullhash(b),status='draft',review={'reviewer_1':None,'reviewer_2':None,'adjudication':None},family=b['recipe_id'],flow_id=b['recipe_id'],parameters={'original':money(original),'rate':str(rate)},inherited_fields=['worked_solution','math_verification','distractor_evidence'],visibility={'given_meanings':'after_initial_response_only','worked_solution':'server_authorized_reveal_only','flow':'one_current_node_only'},mental_method=mental_steps,prerequisites={'required':['understand_percent_as_hundredths','identify_stage','add_subtract'], 'optional_methods':['fraction_benchmarks','decimal_multipliers'], 'missing_approved_assessment':'NUM-PCT-BASIC'},transfer={'candidate_ids':candidates,'full_target_distinct_family_id':None,'same_family_pilot_siblings':sibling,'runtime_exposure':'unknown','independent_transfer_approved':False},finding_ids=issues))
    result=dict(schema_version='dexter-guide-price-overlay-v0.2',status='draft',runtime_eligible=False,baseline_commit=BASE,base_sidecar='pilot-v0.1.json',base_sidecar_sha256=sha(OUT/'pilot-v0.1.json'),base_coverage_sha256=sha(OUT/'coverage-v0.1.json'),original_packet_sha256=sha(ROOT/'docs/research/dexter2/pilot/dexter-rescue-pilot-packet-2026-10-22.csv'),scope_count=15,flows={'successive-price':flow(True),'sale-price':flow(False)},contrast=contrast(),bindings=bindings,editorial_review=reviews,transfer_candidates=references,transfer_search={'scope':'Manifest numerical records only; keyword retrieval followed by manual classification. No recount of whole bank or audit of nonmatching answers.', 'screened_ids':[m['id'] for m in numerical],'keyword_expression':r'%|percent|markup|mark.up|discount|profit|loss|interest','hits':hits,'limitation':'Non-numerical misclassification and non-manifest records not exhausted; absent matches are a scoped gap, not proof of global absence.'},outcome_policy={'diagnostic':'Assistance event, never a scored bank answer. Unknown stays unknown. Compatible pre-feedback responses support an attempt-level hypothesis only.','history':'Preserve first independent answer recorded before help. Later success on this item is assisted.','transfer':'New ID alone is insufficient. Record same-family practice separately from different-family transfer; future learner exposure must be checked.','mastery':'No mastery assertion or fabricated learner result.','fallback':'Ordinary authorized Reveal when draft/stale/missing; no specific diagnosis. No transfer pool means a truthful gap.'})
    result['response_order_policy']='Stable option IDs are semantic identities, not display positions. Server may shuffle displayed responses, stores the mapping, and never sends correctness, branch rules or hypotheses with the prompt.'
    result['misconception_refinements']=[
      {'question_id':b['question_id'],'option_id':e['option_id'],'canonical_code_preserved':e['stored_code'],'proposed_local_hypothesis':'percent-as-pesos','reason':'The option subtracts the percentage numeral as a fixed peso amount. This is a percent-unit interpretation, not evidence that the learner chose the wrong percentage base.','required_confirmation_node':'confirm_units','reviewer':None}
      for b in selected if b['recipe_id']=='sale-price' for e in b['distractor_evidence'] if e['stored_code']=='NUM-WRONG-BASE']
    save('price15-v0.2.json',result)
    print('Wrote draft overlay for 15 bindings and one contrast. Original 60-item sidecar untouched.')

if __name__=='__main__':main()

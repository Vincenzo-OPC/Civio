#!/usr/bin/env python3
"""Offline authoring/checkpoint tool; never writes canonical bank or runtime files.
Run from repo root: python3 docs/research/dexter3/build_pilot.py
Generated prose is DRAFT. Passing checks is not independent educational approval.
"""
import collections
import csv
import hashlib
import json
import pathlib
import re
import sys
from fractions import Fraction as F

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/research/dexter3'
sys.path.insert(0, str(ROOT / 'scripts/batches/qa'))
from flat_2100_manifest_2026_10_22 import content_hash

MANIFEST = 'docs/research/bank/civio-flat-2100-manifest-2026-10-22.json'
PACKET = 'docs/research/dexter2/pilot/dexter-rescue-pilot-packet-2026-10-22.csv'
BASELINE = '78df5c26b07b5c94b53482c2f6200ab4a49a1551'

def read(path):
    return json.loads((ROOT / path).read_text())

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def save(name, value):
    path = OUT / name
    content = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if path.exists() and path.read_text() == content:
        return
    if name == 'pilot-v0.1.json' and path.exists():
        prior = json.loads(path.read_text())
        assert all(not any(b['review'].values()) for b in prior['bindings']), 'Never overwrite reviewed sidecars; create a new version.'
    path.write_text(content)

def money(value):
    n = F(value)
    return f'₱{int(n):,}' if n.denominator == 1 else f'₱{float(n):,.2f}'

def amount(text):
    return F(re.search(r'₱([\d,]+(?:\.\d+)?)', text)[1].replace(',', ''))

def diagnostic(stem, correct, wrong, feedback, hypothesis):
    return {'prompt': stem, 'options': [
        {'id': 'meaning', 'text': correct, 'correct': True, 'feedback': 'Yes. Use that meaning to decide which operation comes next.', 'hypothesis': None},
        {'id': 'alternative', 'text': wrong, 'correct': False, 'feedback': feedback, 'hypothesis': hypothesis},
        {'id': 'unsure', 'text': 'I am not sure yet.', 'correct': False, 'feedback': feedback, 'hypothesis': None}],
        'inference_policy': 'One response supports a possible interpretation error only. Uncertainty is not a diagnosis; do not update mastery from this scaffold.'}

RECIPES = {
    'successive-price': {'prerequisites': ['percent-as-hundredths', 'identify-current-base', 'multiply-decimals'], 'asking': 'Find the price after both changes, not the raise or the intermediate price.', 'mistakes': ['Treat the starting price as already marked up', 'Apply both percentages to the original base', 'Cancel equal increases and decreases', 'Stop after the increase'], 'hints': ['Label the starting, raised and final prices.', 'The second percentage uses the raised price.', 'First add the raise; then subtract the discount from that new amount.'], 'fast_method': 'Multiply original × (1 + increase/100) × (1 − decrease/100). This is a forward method; if the final value is given, divide by the known multipliers in reverse order.'},
    'sale-price': {'prerequisites': ['percent-as-hundredths', 'part-versus-whole'], 'asking': 'Find the amount paid, not the amount saved.', 'mistakes': ['Return only the discount', 'Subtract the percent number as pesos', 'Add instead of subtract'], 'hints': ['Identify the price before the sale.', 'Find the discount as a fraction of that price.', 'Subtract the discount, or calculate the fraction of the price still paid.'], 'fast_method': 'Multiply the original price by (100 − discount percent)/100. To recover an original price from a sale price, divide by this factor instead.'},
    'simple-interest': {'prerequisites': ['percent-as-hundredths', 'months-to-years', 'interest-versus-balance'], 'asking': 'Find the interest charge only; do not add the borrowed principal.', 'mistakes': ['Return principal plus interest', 'Count only one year', 'Read six months as 0.6 years', 'Use compound interest although simple interest is specified'], 'hints': ['Identify principal, annual rate and duration.', 'Convert extra months to months/12 years.', 'Find one year’s interest and multiply by the duration.'], 'fast_method': 'Use I = P × (r/100) × t, with t in years. Simple interest uses the same principal each year.'},
    'two-share-total': {'prerequisites': ['equal-parts', 'ratio-order', 'division-multiplication'], 'asking': 'Find the second named recipient’s share of the whole fund.', 'mistakes': ['Treat the total as one person’s share', 'Divide by only the requested ratio number', 'Give the first recipient’s share', 'Report the value of one part'], 'hints': ['Match each recipient to a ratio number in the order given.', 'Add both ratio numbers to count all equal parts.', 'Divide the total by all parts, then multiply by the requested recipient’s parts.'], 'fast_method': 'For a:b and total T, the second share is T × b/(a+b). Check that both shares sum to T.'},
    'spelling-task-direction': {'prerequisites': ['read-negative-instruction', 'word-specific-orthography'], 'asking': 'Select the incorrectly spelled word, rather than a word that merely looks unfamiliar.', 'mistakes': ['Select a correctly spelled but unfamiliar foil', 'Reverse the task and choose a correct spelling', 'Apply an unreliable general spelling rule'], 'hints': ['Reread whether the task asks for correct or incorrect spelling.', 'Inspect each word in letter groups; unfamiliarity alone is not an error.', 'Use a reviewed word-specific spelling contrast, not a universal rhyme.'], 'fast_method': 'Read the task direction first, then inspect each option once. There is no reliable universal spelling shortcut.'}
}

def make_binding(q, m, packet_rows):
    s = q['stem']; skill = q['archetype']; math = None
    meanings = []; steps = []; flags = []
    if skill == 'NUM-WP-RATIO':
        recipe = 'two-share-total'; total = amount(s)
        a, b = map(int, re.search(r'ratio (\d+)\s*:\s*(\d+)', s).groups())
        result = total * b / (a+b); unit = total / (a+b)
        # Independent relation check: shares sum to total and have given ratio.
        other = total-result
        assert other/result == F(a,b) and other+result == total
        params = {'total': str(total), 'first_parts': a, 'second_parts': b}
        meanings = [f'{money(total)} is both shares together.', f'{a}:{b} assigns {a} parts to the first recipient and {b} to the second.']
        diag = diagnostic(f'In this question, what does {money(total)} represent?', 'The combined fund for both recipients', 'Only the second recipient’s share', 'The wording says the fund is shared or divided. It names the whole before either share is found.', 'total-mistaken-for-share')
        steps = [f'Total parts: {a} + {b} = {a+b}.', f'One part: {money(total)} ÷ {a+b} = {money(unit)}.', f'Second share: {b} × {money(unit)} = {money(result)}.', f'Check: the other share is {money(other)}; together they equal {money(total)} and their ratio is {a}:{b}.']
    elif skill == 'NUM-WP-PCT-CHANGE':
        base = amount(s)
        rates = [int(x) for x in re.findall(r'(\d+)%', s)]
        if 'simple interest' in s:
            recipe = 'simple-interest'; rate = rates[0]
            years = int(re.search(r'after (\d+) year', s)[1]); mm = re.search(r'and (\d+) months', s); months = int(mm[1]) if mm else 0
            t = F(years) + F(months,12); annual = base*rate/100; result = annual*t
            assert result == base*rate*(years*12+months)/1200
            params = {'principal': str(base), 'annual_rate_percent': rate, 'years': years, 'months': months}
            meanings = [f'{money(base)} is the borrowed principal, not the interest.', f'{rate}% applies per year to that principal.', f'Time is {years} + {months}/12 = {t} years.']
            diag = diagnostic('What amount does the question ask you to report?', 'Interest alone', 'The loan plus interest', 'It asks how much interest is due. The borrowed money is the base for calculating that charge, not part of the requested answer.', 'interest-mistaken-for-balance')
            steps = [f'One year’s interest: {money(base)} × {rate}/100 = {money(annual)}.', f'Time: {years} + {months}/12 = {t} years.', f'Interest: {money(annual)} × {t} = {money(result)}.', 'Check with total months: principal × annual rate × months/12. Do not add the principal.']
        elif 'off' in s:
            recipe = 'sale-price'; rate = rates[0]; discount = base*rate/100; result = base-discount
            assert result == base*F(100-rate,100)
            params = {'original': str(base), 'discount_percent': rate}
            meanings = [f'{money(base)} is the price before the discount.', f'{rate}% is the fraction removed, not the amount still paid.']
            diag = diagnostic(f'Is {money(base)} the price before or after the stated discount?', 'Before the discount', 'After the discount', 'The item is priced at that amount and then sold at a discount. Start with that price and take the discount off.', 'starting-value-mistaken-for-final')
            steps = [f'Discount: {money(base)} × {rate}/100 = {money(discount)}.', f'Pay: {money(base)} − {money(discount)} = {money(result)}.', f'Check: {100-rate}% remains; {money(base)} × {100-rate}/100 = {money(result)}.']
        else:
            recipe = 'successive-price'; up, down = rates
            raised = base*(100+up)/100; result = raised*(100-down)/100
            raise_amount = base*up/100; cut = (base+raise_amount)*down/100
            assert result == base+raise_amount-cut
            params = {'original': str(base), 'increase_percent': up, 'decrease_percent': down}
            meanings = [f'{money(base)} is the price before the raise.', f'{up}% applies to {money(base)}.', f'{down}% applies to the new price after the raise.']
            diag = diagnostic(f'When the question gives {money(base)}, has the {up}% raise already been applied?', 'No; it is the price before the raise', 'Yes; it is already the raised price', 'The stated price comes before “raised the price.” First increase that amount. Dividing would answer a different question where the raised price was given.', 'starting-value-mistaken-for-final')
            steps = [f'Raise: {money(base)} × {up}/100 = {money(raise_amount)}.', f'Raised price: {money(base)} + {money(raise_amount)} = {money(raised)}.', f'Cut: {money(raised)} × {down}/100 = {money(cut)}.', f'Final price: {money(raised)} − {money(cut)} = {money(result)}.', f'Check by multipliers: {money(base)} × {100+up}/100 × {100-down}/100 = {money(result)}.']
        # The second method above uses additive/unit reasoning, not the stored explanation.
    else:
        recipe = 'spelling-task-direction'
        diag = diagnostic('What kind of word should you select?', 'A word with a spelling error', 'A correctly spelled word', 'The question asks for a word that is spelled wrong. A correct-looking or familiar word is not automatically the target.', 'task-direction-reversed')
        meanings = ['“Misspelled” means the letter sequence is not the intended standard spelling.', 'A familiar sound does not establish the written spelling.']
        steps = [q['reveal']['why_correct']]
        flags = ['Dictionary and language-variety check pending for all four options.', 'Stored spelling explanation retained as evidence, not newly certified.', 'A chosen correct foil does not identify the learner’s spelling rule.']
        if '000090' in q['id']:
            flags += ['basicly → basically inserts al (two letters). Stored singular “drops a letter” is imprecise.']
    if skill.startswith('NUM-'):
        hits = [o['option_id'] for o in q['options'] if amount(o['text']) == result]
        assert hits == [q['answer_option_id']], (q['id'], hits, result)
        math = {'model': recipe, 'parameters': params, 'result_rational_pesos': str(result), 'checks': ['exact_fraction_calculation', 'second_additive_or_relation_method', 'exactly_one_matching_option', 'stored_key_agrees'], 'status': 'passed'}
    return {'question_id': q['id'], 'source_file': m['source_file'], 'source_question_hash': m['content_sha256'], 'source_record_sha256': hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(), 'canonical_status_observed': q['status'], 'recipe_id': recipe, 'status': 'draft', 'review': {'reviewer_1': None, 'reviewer_2': None, 'adjudication': None}, 'what_is_asked': RECIPES[recipe]['asking'], 'given_meanings': meanings, 'initial_diagnostic': diag, 'distractor_evidence': [{'option_id': r['distractor_option'].split(':')[0], 'stored_code': r['distractor_code'], 'stored_feedback': r['why_wrong'], 'diagnosis_status': 'hypothesis_only_pending_review'} for r in packet_rows], 'worked_solution': steps, 'math_verification': math, 'transfer': {'approved_question_id': None, 'status': 'not_selected', 'reason': 'Require a distinct instructional family and reviewer-confirmed target-skill match. Different wording/numbers alone is insufficient. Runtime must additionally check all exposure and approval state.'}, 'manual_review': flags, 'outcome_contract': 'outcomes-v0.1'}

def main():
    manifest = read(MANIFEST); records = {}; cache = {}
    counts = collections.defaultdict(collections.Counter); topics = collections.defaultdict(collections.Counter); fields = collections.defaultdict(collections.Counter)
    for m in manifest['items']:
        path = m['source_file']
        if path not in cache:
            d = read(path); cache[path] = d['items'] if isinstance(d,dict) else d
        matches = [q for q in cache[path] if q.get('id') == m['id']]
        assert len(matches)==1, m['id']
        q = matches[0]; assert content_hash(q)==m['content_sha256'] and q['status']==m['status']
        assert q['id'] not in records
        records[q['id']] = (q,m)
        counts[m['domain']][m['status']] += 1; topics[q['archetype']][m['status']] += 1
        wrong = [o['option_id'] for o in q['options'] if o['option_id']!=q['answer_option_id']]
        f = fields[m['status']]; f['records']+=1
        for key,value in {'why_correct':q.get('reveal',{}).get('why_correct'), 'terms':q.get('reveal',{}).get('terms'), 'shortcut':q.get('shortcut') or q.get('reveal',{}).get('shortcut'), 'complete_wrong_rationales': all(q.get('reveal',{}).get('why_wrong',{}).get(o) for o in wrong), 'complete_distractor_codes':all(q.get('distractor_reasoning',{}).get(o) for o in wrong)}.items():
            f[key] += bool(value)
    packet = list(csv.DictReader((ROOT/PACKET).open())); by_id = collections.defaultdict(list)
    for r in packet: by_id[r['item_id']].append(r)
    bindings = []
    for qid, rows in by_id.items():
        q,m = records[qid]; assert q['status']=='approved' and len(rows)==3
        assert q['track'] in ('both','subprofessional','sub')
        for r in rows:
            oid = r['distractor_option'].split(':')[0]
            assert r['stem']==q['stem'] and r['correct_option'].split(':')[0]==q['answer_option_id']
            assert q['distractor_reasoning'][oid]==r['distractor_code'] and q['reveal']['why_wrong'][oid]==r['why_wrong']
        bindings.append(make_binding(q,m,rows))
    assert len(bindings)==60 and len(records)==2100
    contrast = {'id':'original-versus-marked-up-640', 'status':'draft', 'bank_question_id':None, 'purpose':'Authored instructional contrast, not a new scored bank item or independent transfer test.', 'forward': {'given_meaning':'₱640 is the original price before a 25% markup and then a 20% discount.', 'diagnostic':diagnostic('The wording identifies ₱640 as the original price. Has the markup already been added?', 'No, ₱640 is the starting value', 'Yes, ₱640 includes the markup', 'Original means before the stated changes. Your percentage calculation may be sound; first attach the amount to the correct stage.', 'starting-value-mistaken-for-final'), 'next_diagnostic':diagnostic('After the markup, which price supplies the base for the 20% discount?', 'The newly marked-up price', 'The original ₱640', 'The discount happens after the markup, so its base is the new price at that moment.', 'discount-base-stays-original'), 'worked_solution':['25% of ₱640 is ₱160.','Add: ₱640 + ₱160 = ₱800.','20% of ₱800 is ₱160.','Subtract: ₱800 − ₱160 = ₱640.'], 'fast_method':'640 × 125/100 × 80/100 = 640. Equal peso changes here do not mean equal percent changes cancel generally.'}, 'reverse': {'given_meaning':'In a different problem, ₱640 is the price AFTER a 25% markup; find the original.', 'diagnostic':diagnostic('What fraction of the original is the given ₱640?', '125% of the original', '100% of the original', 'After a 25% markup, the final price contains all of the original plus another quarter of it.', 'final-mistaken-for-original'), 'worked_solution':['Let the original be x. Then 1.25x = 640.','Divide: x = 640 ÷ 1.25 = ₱512.','Check: 25% of ₱512 is ₱128; ₱512 + ₱128 = ₱640.'], 'wrong_operation_feedback':'640 − 25% of 640 = 480 uses the final price as the base. Its forward check gives 480 × 1.25 = 600, not 640.', 'fast_method':'Divide the final value by 1.25. A 25% markup is reversed by division by 1.25, not by subtracting 25%.'}, 'transfer_question_id':None, 'independent_review':'pending'}
    assert F(640)*F(125,100)*F(80,100)==640 and F(640)/F(125,100)==512
    sidecar = {'schema_version':'dexter-guide-v0.1', 'status':'draft', 'runtime_eligible':False, 'baseline_commit':BASELINE, 'manifest_sha256':digest(MANIFEST), 'packet_sha256':digest(PACKET), 'recipes':RECIPES, 'contrast_examples':[contrast], 'outcomes-v0.1': {'assisted': 'Any diagnostic feedback, hint, explanation or worked step viewed makes subsequent success on that item assisted.', 'independent': 'Only a separate approved item with no prior exposure or family contamination and no help is a candidate for independent evidence.', 'omitted': 'Record separately; not evidence of a specific misconception.', 'repeated': 'Retention/practice evidence; never a new first response.', 'mastery': 'No diagnostic option or one correct response establishes mastery.', 'learner_results':None}, 'bindings':bindings}
    save('pilot-v0.1.json',sidecar)
    save('coverage-v0.1.json', {'baseline_commit':BASELINE,'manifest_sha256':digest(MANIFEST),'source_files':{p:digest(p) for p in sorted(cache)},'candidate_records':len(records),'approved_subprofessional_eligible':sum(q['status']=='approved' and q['track'] in ('both','subprofessional','sub') for q,m in records.values()),'by_domain_status':counts,'by_archetype_status':topics,'metadata_presence_by_status':fields,'pilot_items':60,'pilot_distractor_rows':len(packet),'pilot_adjudicated_rows':sum(bool(r['adjudication']) for r in packet),'pilot_recipe_counts':collections.Counter(b['recipe_id'] for b in bindings),'math_items_checked':sum(b['math_verification'] is not None for b in bindings),'spelling_items_needing_dictionary_review':20,'selected_approved_distinct_family_transfers':0,'independently_approved_sidecars':0,'source_items_changed':0,'limitations':['Mechanical metadata presence is not semantic correctness.','Approved labels are not proof of signed active import.','No live database or learner records accessed.','All 60 require independent editorial review; no reviewer cells filled.']})
    print('PASS: 2100 source references/hashes; 60 pilot bindings; 180 source distractor bindings; 40 two-method exact math/key checks. All content remains draft.')

if __name__ == '__main__':
    main()

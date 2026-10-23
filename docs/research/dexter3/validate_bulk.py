#!/usr/bin/env python3
"""Offline regression checks for the resumable queue and draft math overlay.
No runtime, database, approval or network writes. Run from the repository root.
"""
import copy
import json
import re
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
import bulk_pipeline as b


def validate():
    state, summary, execution = b.run(False)
    records = state['records']
    assert len(records) == len({r['question_id'] for r in records}) == 2100
    queued = [i for job in state['family_jobs'] for i in job['question_ids']]
    assert Counter(queued) == Counter(r['question_id'] for r in records)
    assert len(state['family_jobs']) == 73
    assert execution == {'reused_records': 2100, 'new_or_changed_records': 0}
    assert summary['mechanical_problem_records'] == 0
    assert all(not r['runtime_eligible'] and r['tutoring_status'] == 'draft' for r in records)
    assert all(j['human_review'] is None for j in state['family_jobs'])
    registry = b.read(b.OUT/'family-recipes-luna-v0.1.json')
    assert registry['author_provenance'] == {'model': 'gpt-6-luna', 'effort': 'medium'}
    recipes = registry['recipes']
    assert Counter(r['family'] for r in recipes) == Counter(j['family'] for j in state['family_jobs'])
    assert sum(r['candidate_count'] for r in recipes) == 2100
    assert all(r['status']=='draft' and not r['runtime_eligible'] and not r['independently_reviewed'] for r in recipes)
    # A full-record-only change must invalidate exactly one cached record.
    original_read = b.read
    selected = records[0]
    def changed_read(path):
        data = original_read(path)
        if path == b.ROOT/selected['source_file']:
            data = copy.deepcopy(data)
            source = data['items'] if isinstance(data, dict) else data
            next(q for q in source if q['id']==selected['question_id'])['_test_only_note'] = 'changed'
        return data
    b.read = changed_read
    try:
        _, _, delta = b.run(False)
        assert delta == {'reused_records': 2099, 'new_or_changed_records': 1}
    finally:
        b.read = original_read
    # Changing one recipe must invalidate only the records using that work group.
    family = recipes[0]['family']
    count = sum(r['work_family']==family for r in records)
    def recipe_read(path):
        data = original_read(path)
        if path == b.OUT/'family-recipes-luna-v0.1.json':
            data = copy.deepcopy(data)
            next(r for r in data['recipes'] if r['family']==family)['test_only_note']='changed'
        return data
    b.read = recipe_read
    try:
        _, _, delta = b.run(False)
        assert delta == {'reused_records': 2100-count, 'new_or_changed_records': count}
    finally:
        b.read = original_read
    overlay = b.read(b.OUT/'math25-v0.1.json')
    pilot = b.read(b.OUT/'pilot-v0.1.json')
    old = {x['question_id']:x for x in pilot['bindings']}
    assert overlay['base_sidecar_sha256']==b.filehash(b.OUT/'pilot-v0.1.json')
    assert overlay['status']=='draft' and not overlay['runtime_eligible']
    assert overlay['independent_ai_review'] is None and overlay['human_adjudication'] is None
    assert len(overlay['bindings'])==25
    keys = distractors = 0
    for binding in overlay['bindings']:
        prior = old[binding['question_id']]
        source = b.read(b.ROOT/binding['source_file'])['items']
        q = next(q for q in source if q['id']==binding['question_id'])
        assert b.h(q)==binding['source_record_sha256']==prior['source_record_sha256']
        assert b.content_hash(q)==binding['source_question_hash']
        assert all(v is None for v in binding['review'].values())
        assert binding['status']=='draft' and binding['transfer']['approved_for_transfer'] is False
        p = prior['math_verification']['parameters']
        if binding['family']=='simple-interest':
            principal=F(p['principal']); rate=F(p['annual_rate_percent']); y=p['years']; m=p['months']
            answer=principal*rate/100*(F(y)+F(m,12))
            assert answer==principal*rate*(12*y+m)/1200
            wrong={'NUM-EXTRA-STEP':principal+answer,'NUM-PARTIAL':principal*rate/100*(y if m else 1),'NUM-UNIT':principal*rate/100*(F(y)+F(m,10)), 'NUM-DECIMAL':answer*10}
        else:
            total=F(p['total']); a=p['first_parts']; z=p['second_parts']
            answer=total*z/(a+z)
            assert answer+total*a/(a+z)==total
            wrong={'NUM-PARTIAL':total/(a+z),'NUM-WRONG-BASE':total/z,'NUM-OTHER-SHARE':total*a/(a+z)}
        match=[]
        for option in q['options']:
            value=F(option['text'].replace('₱','').replace(',',''))
            if value==answer:match.append(option['option_id'])
            else:
                code=q['distractor_reasoning'][option['option_id']]
                expected=wrong[code]
                # Currency options may round to the nearest cent.
                rounded=F((Decimal(expected.numerator)/Decimal(expected.denominator)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
                assert value==rounded,(q['id'],code,value,rounded)
                distractors+=1
        assert match==[q['answer_option_id']]
        keys+=1
        flow=overlay['flows'][binding['family']]
        nodes=flow['nodes']; visited=set()
        def visit(key, path):
            assert key in nodes and key not in path
            visited.add(key); node=nodes[key]
            if 'options' in node:
                assert len({o['id'] for o in node['options']})==len(node['options'])
                assert len({o['text'].format(**binding['parameters']) for o in node['options']})==len(node['options'])
            for option in node.get('options',[]):
                option['text'].format(**binding['parameters']);option['feedback'].format(**binding['parameters'])
                if option['id'] in ('unknown','other'):assert option['hypothesis'] is None
                visit(option['next'],path+[key])
            for field in ('prompt','text'):
                if field in node:node[field].format(**binding['parameters'])
            if 'next' in node:visit(node['next'],path+[key])
            assert len(path)+1<=flow['node_budget']
        visit(flow['entry'],[])
        assert visited==set(nodes)
    assert (keys,distractors)==(25,75)
    return {'status':'passed','candidate_queue':2100,'work_groups':73,'warm_cache_hits':2100,'single_source_change_recomputed':1,'recipe_change_scope':'only dependent group','overlay_keys_checked':keys,'overlay_distractor_amounts_checked':distractors,'all_overlay_flows':'references, reachability, acyclic paths, rendered parameters and budgets passed','semantic_split_groups':sum(r['recipe']['semantic_status']=='needs_semantic_split' for r in recipes),'runtime_approvals':0,'limits':['Structural checks are not semantic or human approval.','Only 38 supported bank stems have fresh automated math checks in the bulk ledger.','25 overlay calculations separately checked; 5 overlap those 38, so do not add counts blindly.','Interest whole-year bindings still contain a month-specific response; editorial pruning pending.','Luna registry is a family draft scaffold, not 2100 completed tutoring bindings.']}

if __name__=='__main__':
    result=validate()
    b.save(b.OUT/'bulk-validation.json',result)
    print(json.dumps(result))

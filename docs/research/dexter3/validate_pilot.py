#!/usr/bin/env python3
"""Independent deterministic contract/key checks, not independent human review.
Run from repo root. No dependencies; does not write files or call a model.
"""
import copy
import json
from fractions import Fraction as F
from build_pilot import ROOT, OUT, MANIFEST, PACKET, amount, content_hash, digest

def validate(p):
    assert p['schema_version']=='dexter-guide-v0.1'
    assert p['status']=='draft' and p['runtime_eligible'] is False
    assert p['outcomes-v0.1']['learner_results'] is None
    assert p['manifest_sha256']==digest(MANIFEST) and p['packet_sha256']==digest(PACKET)
    manifest = {r['id']:r for r in json.loads((ROOT/MANIFEST).read_text())['items']}
    ids = set(); math_count = 0
    for b in p['bindings']:
        required = {'question_id','source_file','source_question_hash','source_record_sha256','canonical_status_observed','recipe_id','status','review','what_is_asked','given_meanings','initial_diagnostic','distractor_evidence','worked_solution','math_verification','transfer','manual_review','outcome_contract'}
        assert set(b)==required
        qid=b['question_id']; assert qid not in ids; ids.add(qid)
        assert b['status']=='draft' and all(v is None for v in b['review'].values())
        m=manifest[qid]; assert m['status']=='approved' and b['source_file']==m['source_file']
        d=json.loads((ROOT/m['source_file']).read_text()); q=next(q for q in d['items'] if q['id']==qid)
        assert b['source_question_hash']==content_hash(q)==m['content_sha256']
        import hashlib
        assert b['source_record_sha256']==hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        recipe=p['recipes'][b['recipe_id']]
        for k in ('prerequisites','mistakes','hints'): assert isinstance(recipe[k],list) and len(recipe[k])>=2
        assert isinstance(recipe['fast_method'],str) and recipe['fast_method']
        assert b['what_is_asked'] and b['given_meanings'] and b['worked_solution']
        diag=b['initial_diagnostic']; options=diag['options']
        assert len(options)==3 and len({o['id'] for o in options})==3
        assert sum(o['correct'] is True for o in options)==1
        assert all(isinstance(o['correct'],bool) and o['feedback'] and o['text'] for o in options)
        assert options[-1]['hypothesis'] is None
        wrong={o['option_id'] for o in q['options'] if o['option_id']!=q['answer_option_id']}
        assert {r['option_id'] for r in b['distractor_evidence']}==wrong
        for r in b['distractor_evidence']:
            assert q['distractor_reasoning'][r['option_id']]==r['stored_code']
            assert q['reveal']['why_wrong'][r['option_id']]==r['stored_feedback']
        assert b['transfer']['approved_question_id'] is None  # v0.1 has no validated transfer mapping
        v=b['math_verification']
        if v:
            x=v['parameters']; model=v['model']
            if model=='successive-price':
                original=F(x['original']); raised=original+original*F(x['increase_percent'],100)
                answer=raised-raised*F(x['decrease_percent'],100)
            elif model=='sale-price':
                original=F(x['original']); answer=original-original*F(x['discount_percent'],100)
            elif model=='simple-interest':
                monthly=F(x['principal'])*F(x['annual_rate_percent'],1200)
                answer=monthly*(12*x['years']+x['months'])
            elif model=='two-share-total':
                # Solve A/B=a/b and A+B=T by substituting A=(a/b)B.
                answer=F(x['total'])/(1+F(x['first_parts'],x['second_parts']))
            else: raise AssertionError(model)
            assert answer==F(v['result_rational_pesos'])
            assert [o['option_id'] for o in q['options'] if amount(o['text'])==answer]==[q['answer_option_id']]
            math_count+=1
    assert len(ids)==60 and math_count==40
    contrast=p['contrast_examples'][0]
    assert contrast['status']=='draft' and contrast['bank_question_id'] is None and contrast['transfer_question_id'] is None
    assert F(640)+F(640,4)==800 and F(800)-F(800,5)==640
    assert F(512)+F(512,4)==640 and F(480)*F(5,4)==600
    return math_count

def main():
    p=json.loads((OUT/'pilot-v0.1.json').read_text()); validate(p)
    mutations=[lambda x:x['bindings'][0].update(source_question_hash='bad'), lambda x:x['bindings'][0]['math_verification'].update(result_rational_pesos='999'), lambda x:x['bindings'][0]['review'].update(adjudication='validated'), lambda x:x['bindings'][0]['initial_diagnostic']['options'][1].update(correct=True), lambda x:x.update(runtime_eligible=True)]
    for mutate in mutations:
        broken=copy.deepcopy(p); mutate(broken)
        try: validate(broken)
        except AssertionError: pass
        else: raise AssertionError('Mutation wrongly accepted')
    print('PASS: 60 sidecar contracts/references; 40 independent exact recalculations; forward/reverse contrast; 5 invalid-fixture rejections. Human review remains pending.')

if __name__=='__main__': main()

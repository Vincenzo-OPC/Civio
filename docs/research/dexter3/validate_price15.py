#!/usr/bin/env python3
"""Read-only scoped checks plus an explicitly requested results file.
No runtime tutor is implemented here; flow traversal tests authored data only.
Run: python3 docs/research/dexter3/validate_price15.py --write-report
"""
import copy
import csv
import json
import re
import subprocess
import sys
from fractions import Fraction as F
from build_price15 import ROOT, OUT, BASE, sha, fullhash, amount, money

def validate(data):
    assert data['schema_version']=='dexter-guide-price-overlay-v0.2'
    assert data['status']=='draft' and data['runtime_eligible'] is False
    assert data['baseline_commit']==BASE
    assert data['base_sidecar_sha256']==sha(OUT/'pilot-v0.1.json')
    assert data['base_coverage_sha256']==sha(OUT/'coverage-v0.1.json')
    packet=ROOT/'docs/research/dexter2/pilot/dexter-rescue-pilot-packet-2026-10-22.csv'
    assert data['original_packet_sha256']==sha(packet)
    base=json.loads((OUT/'pilot-v0.1.json').read_text())
    original={b['question_id']:b for b in base['bindings'] if b['recipe_id'] in ('successive-price','sale-price')}
    assert len(data['bindings'])==len(original)==15
    assert {b['question_id'] for b in data['bindings']}==set(original)
    assert len(data['editorial_review'])==15
    checked=[]
    for b in data['bindings']:
        old=original[b['question_id']]
        assert b['base_binding_sha256']==fullhash(old)
        for key in ('question_id','source_file','source_question_hash','source_record_sha256'):assert b[key]==old[key]
        assert b['status']=='draft' and all(x is None for x in b['review'].values())
        q=next(q for q in json.loads((ROOT/b['source_file']).read_text())['items'] if q['id']==b['question_id'])
        assert fullhash(q)==b['source_record_sha256'] and q['status']=='approved'
        numbers=[F(x.replace(',','')) for x in re.findall(r'\d[\d,]*(?:\.\d+)?',q['stem'])]
        # Reparse source stem, not the generated sidecar arithmetic parameters.
        original_price=amount(q['stem']);rates=[int(x) for x in re.findall(r'(\d+)%',q['stem'])]
        if b['family']=='successive-price':
            assert len(rates)==2;u,d=rates
            intermediate=original_price+original_price*u/100
            expected=intermediate-intermediate*d/100
            alternate=original_price*F(100+u,100)*F(100-d,100)
            wrong_values={'NUM-PARTIAL':intermediate,'NUM-PCT-ADD':original_price*(1+F(u-d,100)),'NUM-EXTRA-STEP':expected*(1+F(u,100))}
        else:
            assert b['family']=='sale-price' and len(rates)==1;d=rates[0]
            expected=original_price-original_price*d/100;alternate=original_price*F(100-d,100)
            wrong_values={'NUM-PARTIAL':original_price*d/100,'NUM-WRONG-BASE':original_price-d,'NUM-OP-SWAP':original_price*(1+F(d,100))}
        assert expected==alternate==F(old['math_verification']['result_rational_pesos'])
        assert [o['option_id'] for o in q['options'] if amount(o['text'])==expected]==[q['answer_option_id']]
        for o in q['options']:
            if o['option_id']!=q['answer_option_id']:
                assert amount(o['text'])==wrong_values[q['distractor_reasoning'][o['option_id']]]
        assert b['transfer']['full_target_distinct_family_id'] is None and not b['transfer']['independent_transfer_approved']
        assert all(cid in data['transfer_candidates'] for cid in b['transfer']['candidate_ids'])
        assert b['visibility']['given_meanings']=='after_initial_response_only'
        checked.append(dict(question_id=b['question_id'],result=str(expected),key=q['answer_option_id'],distractors_checked=3))
    for row in data['editorial_review']:
        assert row['author_second_pass'] is True and row['independent_reviewer'] is None and row['adjudication'] is None
        assert len(row['criteria'])==11 # ten requested criteria plus numerical coincidence note
    for fid,flow in data['flows'].items():
        nodes=flow['nodes'];assert flow['entry'] in nodes
        for nid,n in nodes.items():
            options=n.get('options',[])
            assert not options or len({o['id'] for o in options})==len(options)
            assert not options or len({o['feedback'] for o in options})==len(options)
            for o in options:
                assert o['next'] in nodes
                if o['id'] in ('unknown','guess'):assert o['hypothesis'] is None and o['evidence']=='unknown'
            if 'next' in n:assert n['next'] in nodes
            if n['kind']=='hint':assert n['requires']=='learner_requests_next_hint'
        # All nodes must be reachable, acyclic and within the authored turn budget.
        visited=set()
        def walk(nid,path):
            assert nid not in path
            path=path+[nid];assert len(path)<=flow['node_budget'];visited.add(nid)
            n=nodes[nid];targets=[o['next'] for o in n.get('options',[])]+([n['next']] if 'next' in n else [])
            for target in targets:walk(target,path)
        walk(flow['entry'],[]);assert visited==set(nodes)
        # No final price appears in any pre-Reveal prompt/hint for these 15 bound items.
        for b in data['bindings']:
            if b['flow_id']!=fid:continue
            for n in nodes.values():
                for t in [n.get('prompt',''),n.get('text','')]+[s for o in n.get('options',[]) for s in (o['text'],o['feedback'])]:
                    rendered=t.format(**b['parameters'])
                    final=money(original[b['question_id']]['math_verification']['result_rational_pesos'])
                    assert final not in rendered, 'Final amount leaked into a pre-Reveal prompt or feedback'
        assert nodes['interpret']['options'][1]['next']=='confirm'
        assert nodes['interpret']['options'][2]['next']=='wording_help'
    # Explicit data-path regression fixtures, not an application test.
    f=data['flows']['successive-price']['nodes']
    def route(nid,choice):return next(o for o in f[nid]['options'] if o['id']==choice)
    assert route('interpret','after')['next']=='confirm'
    assert route('confirm','assumption')['evidence']=='supports_if_prior_after'
    assert route('confirm','guess')['hypothesis'] is None
    assert route('target','paid')['next']=='arithmetic_check'
    assert route('arithmetic_check','20')['evidence']=='arithmetic_sample_correct'
    assert route('arithmetic_check','2')['evidence']=='possible'
    c=data['contrast'];assert c['bank_question_id'] is None and c['independent_review'] is None and not c['runtime_approved']
    assert c['checks']=={'forward':640,'reverse':512,'new_reverse':720,'wrong_reverse_forward':600,'new_wrong_reverse_forward':'843.75'}
    assert F(640)*F(5,4)*F(4,5)==640 and F(640)*F(4,5)==512
    assert F(900)*F(4,5)==720 and F(640)*F(3,4)*F(5,4)==600 and F(900)*F(3,4)*F(5,4)==F('843.75')
    for n in c['nodes'].values():
        for o in n.get('options',[]):assert o['next'] in c['nodes']
    expected_transfers={'000013':F(20000)*F(6,100)*F(30,12),'000124':F(250)*F(120,100)*F(75,100),'000121':F(2400)*F(75,100)}
    for qid,r in data['transfer_candidates'].items():
        q=next(q for q in json.loads((ROOT/r['source_file']).read_text())['items'] if q['id']==qid)
        assert q['status']=='approved' and q['track'] in ('both','subprofessional') and fullhash(q)==r['source_record_sha256']
        assert r['reviewer'] is None and r['usable_at_runtime'] is False
        expected=expected_transfers[qid[-6:]]
        assert [o['option_id'] for o in q['options'] if amount(o['text'])==expected]==[q['answer_option_id']]
    return checked

def main():
    path=OUT/'price15-v0.2.json';data=json.loads(path.read_text());checked=validate(data)
    mutations=[('source drift',lambda d:d['bindings'][0].update(source_record_sha256='bad')),
      ('runtime promotion',lambda d:d.update(runtime_eligible=True)),
      ('invented reviewer',lambda d:d['bindings'][0]['review'].update(reviewer_1='AI as human')),
      ('unknown becomes diagnosis',lambda d:d['flows']['successive-price']['nodes']['interpret']['options'][2].update(hypothesis='given-stage')),
      ('broken edge',lambda d:d['flows']['sale-price']['nodes']['interpret']['options'][0].update(next='missing')),
      ('duplicate response feedback',lambda d:d['flows']['sale-price']['nodes']['interpret']['options'][2].update(feedback=d['flows']['sale-price']['nodes']['interpret']['options'][1]['feedback'])),
      ('false transfer approval',lambda d:d['bindings'][0]['transfer'].update(independent_transfer_approved=True)),
      ('wrong contrast result',lambda d:d['contrast']['checks'].update(reverse=480))]
    for name,mutate in mutations:
        broken=copy.deepcopy(data);mutate(broken)
        try:validate(broken)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('Invalid fixture accepted: '+name)
    # Prove prior deliverables and the original reviewer packet were not rewritten.
    protected=['pilot-v0.1.json','coverage-v0.1.json','build_pilot.py','validate_pilot.py']
    for name in protected:
        prior=subprocess.check_output(['git','show',BASE+':docs/research/dexter3/'+name],cwd=ROOT)
        assert prior==(OUT/name).read_bytes()
    report={'baseline_commit':BASE,'overlay_sha256':sha(path),'bindings_evaluated':15,'contrast_evaluated':1,'math_checks':checked,'canonical_distractor_values_checked':45,'candidate_calculations':{k:v['answer_text'] for k,v in data['transfer_candidates'].items()},'flow_contracts_passed':2,'invalid_fixtures_rejected':[n for n,_ in mutations],'prior_files_byte_identical':protected,'mathematical_errors_found':0,'editorial_status':'author_second_pass_plausible_pending_independent_review','independent_human_reviews':0,'runtime_approvals':0,'runtime_tests_run':False}
    if '--write-report' in sys.argv:(OUT/'price15-check-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 15 price items, 45 distractor values, 3 approved-source candidate keys, 2 flow contracts, contrast calculations, 8 invalid-fixture rejections; prior sidecars intact.')

if __name__=='__main__':main()

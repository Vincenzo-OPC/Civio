#!/usr/bin/env python3
"""Validate/apply the authored v0.3 patch in memory only; no runtime integration.
Run: python3 docs/research/dexter3/validate_price_patch.py --write-report
"""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
BASE='d405fed2faa08270f48e266e90f0afe52009cf42'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def materialize(patch):
    assert patch['schema_version']=='dexter-guide-price-patch-v0.3'
    assert patch['status']=='draft' and patch['runtime_eligible'] is False
    assert patch['base_file']=='price15-v0.2.json' and patch['base_sha256']==sha(OUT/patch['base_file'])
    assert all(patch['review'][key] is None for key in ('human_reviewer_1','human_reviewer_2','adjudication'))
    assert patch['review']['independent_ai_pass']=='reviews/ai-review-01.json'
    assessment=json.loads((OUT/patch['review']['independent_ai_pass']).read_text())
    assert assessment['reviewer_kind']=='AI' and assessment['runtime_approved'] is False
    assert assessment['human_adjudication']=='pending' and assessment['learner_evidence'] is None
    assert assessment['packet_sha256']==sha(OUT/'price15-review-packet-v0.1.json')
    assert len(assessment['price_items'])==15 and sum(len(i['distractors']) for i in assessment['price_items'])==45
    assert len(assessment['foundation_candidates'])==4 and len(assessment['findings'])==7
    candidates={r['question_id']:r for r in json.loads((OUT/'foundation4-audit-v0.1.json').read_text())['records']}
    assert len(patch['foundation_proposals'])==2
    for proposed in patch['foundation_proposals']:
        assert proposed['source_record_sha256']==candidates[proposed['question_id']]['source_record_sha256']
        assert proposed['runtime_eligible'] is False and proposed['independent_reviewer'] is None
        assert not any(key in proposed for key in ('options','answer_option_id','review_status','approved'))
    original=json.loads((OUT/patch['base_file']).read_text());result=copy.deepcopy(original)
    for op in patch['operations']:
        assert op['op'] in ('add','replace') and set(op)=={'op','path','value'}
        path=op['path'];assert path.startswith(('/flows/','/contrast/nodes/','/bindings/')) or path in ('/schema_version','/evidence_context_contract','/contrast/evidence_contract_ref','/contrast/node_budget')
        if path.startswith('/bindings/'):assert path.endswith('/visibility/given_meanings')
        parts=[p.replace('~1','/').replace('~0','~') for p in path.lstrip('/').split('/')]
        parent=result
        for part in parts[:-1]:parent=parent[int(part)] if isinstance(parent,list) else parent[part]
        leaf=parts[-1];value=copy.deepcopy(op['value'])
        if isinstance(parent,list):
            if op['op']=='replace':parent[int(leaf)]=value
            elif leaf=='-':parent.append(value)
            else:parent.insert(int(leaf),value)
        else:
            if op['op']=='replace':assert leaf in parent
            else:assert leaf not in parent
            parent[leaf]=value
    assert result['schema_version']=='dexter-guide-price-overlay-v0.3'
    assert result['status']=='draft' and result['runtime_eligible'] is False
    assert len(result['bindings'])==15
    for b,old in zip(result['bindings'],original['bindings']):
        changed=copy.deepcopy(b);changed['visibility']=copy.deepcopy(old['visibility'])
        assert changed==old, 'Only visibility may change on a source binding'
        assert b['visibility']['given_meanings']=='authorized_explanation_only'
        assert all(v is None for v in b['review'].values())
    return result

def validate(patch):
    d=materialize(patch);flow_results={}
    assert d['evidence_context_contract']['knowledge_updates_from_tutor_nodes'] is False
    assert d['evidence_context_contract']['learner_records_created'] is None
    assert 'target_was_taught_before_response' in d['evidence_context_contract']['required_provenance']
    for fid,flow in d['flows'].items():
        nodes=flow['nodes'];seen=set();max_depth=0;terminals=set()
        assert flow['evidence_contract_ref']=='evidence_context_contract'
        def walk(nid,path):
            nonlocal max_depth
            assert nid in nodes and nid not in path
            path=path+[nid];seen.add(nid);max_depth=max(max_depth,len(path))
            assert len(path)<=flow['node_budget']
            n=nodes[nid];options=n.get('options',[])
            assert not options or len({o['id'] for o in options})==len(options)
            assert not options or len({o['feedback'] for o in options})==len(options)
            for o in options:
                assert o['next'] in nodes
                if o['id'] in ('unknown','guess'):assert o['hypothesis'] is None and o['evidence']=='unknown'
                walk(o['next'],path)
            if 'next' in n:walk(n['next'],path)
            if n['kind']=='terminal':terminals.add(nid)
            if n['kind']=='hint':assert n['requires']=='learner_requests_next_hint'
        walk(flow['entry'],[]);assert seen==set(nodes)
        assert nodes['arithmetic_check']['options'][0]['next']=='retry'
        assert all(o['next']=='percent_help' for o in nodes['arithmetic_check']['options'][1:])
        assert nodes['percent_help']['next']=='percent_check'
        assert nodes['percent_check']['options'][0]['next']=='retry'
        assert all(o['next']=='arithmetic_exit' for o in nodes['percent_check']['options'][1:])
        assert nodes['arithmetic_exit']['approved_prerequisite_id'] is None
        flow_results[fid]={'nodes':len(nodes),'max_path_nodes':max_depth,'terminals':sorted(terminals)}
    n=d['flows']['successive-price']['nodes']
    assert 'starting price, price after the raise, and final price after the discount' in n['hint_1']['text']
    assert n['target']['options'][-1]['id']=='raised' and n['target']['options'][-1]['next']=='confirm_intermediate'
    assert n['confirm_intermediate']['options'][0]['evidence']=='supports_if_prior_raised'
    assert n['confirm_base']['options'][-1]['id']=='misclick' and n['confirm_base']['options'][-1]['hypothesis'] is None
    assert n['confirm_base']['options'][2]['hypothesis'] is None and 'another approach' in n['confirm_base']['options'][2]['text']
    c=d['contrast']['nodes']
    assert c['different_calculation']['options'][0]['next']=='transfer_choice'
    assert all(o['next']=='reverse_remedy' for o in c['different_calculation']['options'][1:])
    assert all(o['next']=='remedial_exit' for o in c['reverse_remedy']['options'])
    assert c['remedial_exit']['transfer_automatically_requested'] is False
    assert [o['next'] for o in c['transfer_choice']['options']]==['fresh','reverse_remedy','done']
    seen=set()
    def contrast_walk(nid,path):
        assert nid in c and nid not in path
        assert len(path)+1<=d['contrast']['node_budget']
        seen.add(nid)
        for o in c[nid].get('options',[]):contrast_walk(o['next'],path+[nid])
    contrast_walk(d['contrast']['entry'],[]);assert seen==set(c)
    assert d['contrast']['checks']==json.loads((OUT/'price15-v0.2.json').read_text())['contrast']['checks']
    assert d['contrast']['runtime_approved'] is False and d['contrast']['independent_review'] is None
    assert d['contrast']['evidence_contract_ref']=='evidence_context_contract'
    for nid in ('forward','discount_base','reverse_meaning','reverse_operation'):
        assert c[nid]['kind']=='assisted_check'
        assert all(o['evidence']!='consistent' for o in c[nid]['options'])
    # The diagnostic mini-check is authored teaching; exactly one of these amounts is 10% of 300.
    from fractions import Fraction as F
    assert F(300,10)==30 and F(300,100)==3
    return flow_results

def main():
    path=OUT/'price15-v0.3-patch.json';patch=json.loads(path.read_text());flows=validate(patch)
    followup_path=OUT/'reviews/ai-review-01-followup.json'
    followup=json.loads(followup_path.read_text())
    assert followup['patch_sha256']==sha(path)
    assert followup['frozen_assessment_sha256']==sha(OUT/'reviews/ai-review-01.json')
    assert followup['reviewer_kind']=='AI' and followup['runtime_approved'] is False
    assert followup['human_adjudication']=='pending' and followup['new_blocking_issues']==[]
    assert {r['finding_id'] for r in followup['finding_dispositions']}=={'AI01-F01','AI01-F02','AI01-F03','AI01-F04','AI01-F05'}
    bads=[('base drift',lambda p:p.update(base_sha256='bad')),
          ('fake human decision',lambda p:p['review'].update(adjudication='approved')),
          ('runtime activation',lambda p:p.update(runtime_eligible=True)),
          ('alter source identity',lambda p:p['operations'].append({'op':'replace','path':'/bindings/0/question_id','value':'other'})),
          ('wrong answer advances to transfer',lambda p:p['operations'].append({'op':'replace','path':'/contrast/nodes/different_calculation/options/1/next','value':'fresh'})),
          ('arithmetic error gets generic hint',lambda p:p['operations'].append({'op':'replace','path':'/flows/sale-price/nodes/arithmetic_check/options/1/next','value':'hint_1'})),
          ('intermediate target removed',lambda p:p['operations'].append({'op':'replace','path':'/flows/successive-price/nodes/target/options/3/next','value':'retry'})),
          ('meanings shown before diagnosis',lambda p:p['operations'].append({'op':'replace','path':'/bindings/0/visibility/given_meanings','value':'after_initial_response_only'})),
          ('tutor nodes become knowledge',lambda p:p['operations'].append({'op':'replace','path':'/evidence_context_contract/knowledge_updates_from_tutor_nodes','value':True})),
          ('foundation proposal activated',lambda p:p['foundation_proposals'][0].update(runtime_eligible=True)),
          ('timeline collapsed',lambda p:p['operations'].append({'op':'replace','path':'/flows/successive-price/nodes/hint_1/text','value':'Before and after the change'})),
          ('untraceable AI assessment',lambda p:p['review'].update(independent_ai_pass='another.json'))]
    for name,mutate in bads:
        p=copy.deepcopy(patch);mutate(p)
        try:validate(p)
        except (AssertionError,KeyError,ValueError):pass
        else:raise AssertionError('Invalid patch accepted: '+name)
    protected=['pilot-v0.1.json','coverage-v0.1.json','price15-v0.2.json','price15-review-packet-v0.1.json','foundation4-audit-v0.1.json']
    for name in protected:
        assert (OUT/name).read_bytes()==subprocess.check_output(['git','show',BASE+':docs/research/dexter3/'+name],cwd=ROOT)
    report={'baseline_commit':BASE,'patch_sha256':sha(path),'separate_ai_review_sha256':sha(OUT/'reviews/ai-review-01.json'),'separate_ai_followup_sha256':sha(followup_path),'separate_ai_review_kind':'AI_with_limited_blinding','binding_references_preserved':15,'source_keys_or_options_changed':0,'flow_checks':flows,'contrast_node_count':len(materialize(patch)['contrast']['nodes']),'foundation_proposals_pending_review':2,'invalid_fixtures_rejected':[name for name,_ in bads],'protected_snapshots_byte_identical':protected,'human_review_decisions_recorded':0,'runtime_approved':False,'runtime_tests_run':False}
    if '--write-report' in sys.argv:(OUT/'price15-v0.3-check-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 15 source bindings preserved; targeted arithmetic/target/reverse branches; 12 invalid patches rejected; AI review traced; prior snapshots intact. Draft only.')

if __name__=='__main__':main()

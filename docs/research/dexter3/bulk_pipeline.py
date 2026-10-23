#!/usr/bin/env python3
"""Resumable offline bank-to-tutoring work queue. No AI/network/runtime writes.
Run from repo root: python3 docs/research/dexter3/bulk_pipeline.py --write
The queue accounts for every candidate; missing lessons never count as finished.
"""
import argparse
import collections
import hashlib
import gzip
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
MANIFEST=ROOT/'docs/research/bank/civio-flat-2100-manifest-2026-10-22.json'
POLICY='dexter-bulk-offline-v1'
sys.path.insert(0,str(ROOT/'scripts/batches/qa'))
from flat_2100_manifest_2026_10_22 import content_hash

def h(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def filehash(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_text())
def save(path,data):
    text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    if path.suffix=='.gz':
        payload=gzip.compress(text.encode(),mtime=0)
        if not path.exists() or path.read_bytes()!=payload:path.write_bytes(payload)
    elif not path.exists() or path.read_text()!=text:path.write_text(text)

def method_family(q):
    s=q['stem'];a=q.get('archetype','UNKNOWN')
    if a=='NUM-WP-PCT-CHANGE':
        if re.search(r'\bsimple interest\b',s,re.I):return 'simple-interest'
        if re.search(r'\d+%\s+off\b',s,re.I):return 'sale-price'
        if len(re.findall(r'\d+%',s))==2 and re.search(r'raised|raise',s,re.I):return 'successive-price'
        return 'NUM-WP-PCT-CHANGE:needs-semantic-split'
    if a=='NUM-WP-RATIO' and re.search(r'ratio \d+\s*:\s*\d+',s) and re.search(r'will share|divided between|split.*between',s):return 'two-share-total-candidate'
    return a

def exact_math(q,family):
    """Abstain outside explicitly supported stem contracts; never eval prose."""
    s=q['stem'];m=re.search(r'₱([\d,]+(?:\.\d+)?)',s)
    if not m:return None
    base=F(m[1].replace(',',''));rates=[int(x) for x in re.findall(r'(\d+)%',s)]
    value=None
    if family=='simple-interest':
        t=re.search(r'after (\d+) years?(?: and (\d+) months?)?',s)
        if t and len(rates)==1 and 'per year' in s:
            years=int(t[1]);months=int(t[2] or 0)
            if months>=12:return None
            annual=base*rates[0]/100
            value=annual*years+annual*F(months,12)
            assert value==base*F(rates[0],1200)*(12*years+months)
    elif family=='sale-price' and len(rates)==1 and 'How much does a buyer pay?' in s:
        value=base-base*rates[0]/100
        assert value==base*F(100-rates[0],100)
    elif family=='successive-price' and len(rates)==2 and 'final price' in s:
        up,down=rates;raised=base+base*up/100;value=raised-raised*down/100
        assert value==base*F(100+up,100)*F(100-down,100)
    # Ratio parameters alone do not establish who is asked or what the total means.
    # Only the existing individually checked 20 pilot records are reused below.
    if value is None:return None
    matching=[]
    for option in q['options']:
        amount=re.fullmatch(r'₱([\d,]+(?:\.\d+)?)',option['text'])
        if amount and F(amount[1].replace(',',''))==value:matching.append(option['option_id'])
    return {'result_rational':str(value),'key_matches':matching==[q['answer_option_id']],'matching_options':matching,'method':'exact fractions plus additive/multiplier check','independent_review':False}

def run(write=False):
    manifest=read(MANIFEST);rows=manifest['items'];assert len(rows)==2100 and len({r['id'] for r in rows})==2100
    prior_path=OUT/'bulk-state.json.gz';prior=read(prior_path) if prior_path.exists() else {'records':[]}
    previous={r['question_id']:r for r in prior['records']}
    pilot=read(OUT/'pilot-v0.1.json');pilot_by_id={b['question_id']:b for b in pilot['bindings']}
    price=read(OUT/'price15-v0.2.json');price_ids={b['question_id'] for b in price['bindings']}
    math_path=OUT/'math25-v0.1.json';math=read(math_path) if math_path.exists() else {'bindings':[]}
    math_ids={b['question_id'] for b in math['bindings']}
    registry_path=OUT/'family-recipes-luna-v0.1.json'
    registry=read(registry_path) if registry_path.exists() else {}
    entries=registry if isinstance(registry,list) else registry.get('recipes',registry.get('families',[]))
    family_recipes={r.get('family',r.get('work_family')):r for r in entries}
    dependency_hashes={p:filehash(OUT/p) for p in ('pilot-v0.1.json','price15-v0.2.json','price15-v0.3-patch.json')}
    if math_path.exists():dependency_hashes['math25-v0.1.json']=filehash(math_path)
    recipe_sources={
      'successive-price':'price15-v0.2.json + price15-v0.3-patch.json',
      'sale-price':'price15-v0.2.json + price15-v0.3-patch.json',
      'simple-interest':'math25-v0.1.json',
      'two-share-total-candidate':'math25-v0.1.json'}
    cache={};records=[];hits=0;changed=0
    implementation_hash=filehash(Path(__file__))
    taxonomy=set(re.findall(r"'([A-Z][A-Z0-9-]+)' => \['domain'",(ROOT/'config/dexter_misconceptions.php').read_text()))
    taxonomy_hash=filehash(ROOT/'config/dexter_misconceptions.php')
    for row in rows:
        path=row['source_file']
        if path not in cache:
            d=read(ROOT/path);items=d['items'] if isinstance(d,dict) else d
            cache[path]={q['id']:q for q in items}
        q=cache[path][row['id']];full_hash=h(q);family=method_family(q)
        relevant={}
        if q['id'] in price_ids or family in ('sale-price','successive-price'):
            relevant={p:v for p,v in dependency_hashes.items() if p.startswith('price15-')}
        elif q['id'] in math_ids or family in ('simple-interest','two-share-total-candidate'):
            relevant={p:v for p,v in dependency_hashes.items() if p=='math25-v0.1.json'}
        elif q['id'] in pilot_by_id:relevant={'pilot-v0.1.json':dependency_hashes['pilot-v0.1.json']}
        if family in family_recipes:relevant['family_recipe_entry']=h(family_recipes[family])
        fingerprint=h({'source_record':full_hash,'manifest_row':row,'policy':POLICY,'implementation':implementation_hash,'taxonomy':taxonomy_hash,'relevant_recipe_dependencies':relevant})
        old=previous.get(q['id'])
        if old and old['work_fingerprint']==fingerprint:
            records.append(old);hits+=1;continue
        changed+=1;problems=[];review=q.get('reveal',{});options=q.get('options',[])
        ids=[o.get('option_id') for o in options];wrong=[o for o in ids if o!=q.get('answer_option_id')]
        if len(options)!=4 or len(set(ids))!=4 or q.get('answer_option_id') not in ids:problems.append('invalid_option_key_contract')
        if content_hash(q)!=row['content_sha256']:problems.append('manifest_content_hash_drift')
        if q.get('status')!=row['status']:problems.append('status_drift')
        if not review.get('why_correct'):problems.append('missing_correct_explanation')
        if not all(review.get('why_wrong',{}).get(o) for o in wrong):problems.append('missing_distractor_feedback')
        if not all(q.get('distractor_reasoning',{}).get(o) for o in wrong):problems.append('missing_distractor_code')
        unrecognized=sorted({q.get('distractor_reasoning',{}).get(o) for o in wrong}-{None}-taxonomy)
        checks=exact_math(q,family)
        if checks and not checks['key_matches']:problems.append('deterministic_key_conflict')
        support='recipe_not_authored';binding=None
        if q['id'] in price_ids:support='refined_draft_separate_ai_pass';binding='price15-v0.2.json + price15-v0.3-patch.json'
        elif q['id'] in math_ids:support='author_draft_pending_flow_qa';binding='math25-v0.1.json'
        elif q['id'] in pilot_by_id:support='original_draft_needs_refinement';binding='pilot-v0.1.json'
        elif family in recipe_sources and (family!='two-share-total-candidate' or 'ratio' in q.get('concept','').lower()):support='family_recipe_candidate_needs_binding_review'
        elif family in family_recipes:support='family_draft_authored_needs_binding_review'
        remaining=['independent_editorial_review','approved_distinct_family_transfer','runtime_content_authorization']
        if support=='recipe_not_authored':remaining.insert(0,'author_family_recipe_and_diagnostic')
        elif support in ('family_recipe_candidate_needs_binding_review','family_draft_authored_needs_binding_review'):remaining.insert(0,'verify_semantic_match_before_template_binding')
        elif support in ('author_draft_pending_flow_qa','original_draft_needs_refinement'):remaining.insert(0,'validate_or_refine_family_flow')
        if family_recipes.get(family,{}).get('recipe',{}).get('semantic_status')=='needs_semantic_split':remaining.insert(0,'split_mixed_semantics_before_binding')
        if row['status']!='approved':remaining.append('bank_approval_workflow')
        records.append({'question_id':q['id'],'source_file':path,'source_record_sha256':full_hash,'work_fingerprint':fingerprint,'domain':row['domain'],'archetype':q.get('archetype'),'work_family':family,'bank_status':row['status'],'tutoring_status':'draft','runtime_eligible':False,'content_support':support,'binding_source':binding,'mechanical_problems':problems,'unmapped_codes':unrecognized,'math_check':checks,'remaining_actions':remaining})
    groups=collections.defaultdict(list)
    for r in records:groups[r['work_family']].append(r)
    jobs=[]
    for family,items in sorted(groups.items()):
        signature=h({'policy':POLICY,'family':family,'inputs':sorted((r['question_id'],r['work_fingerprint']) for r in items)})
        domain=items[0]['domain'];approved=sum(r['bank_status']=='approved' for r in items)
        priority=0 if any(r['mechanical_problems'] for r in items) else 1 if domain=='numerical' else 2 if domain=='clerical' else 3 if domain in ('verbal_en','verbal_fil') else 4
        jobs.append({'job_id':'FAMILY-'+hashlib.sha256(family.encode()).hexdigest()[:12],'family':family,'signature':signature,'domain':domain,'candidate_count':len(items),'approved_label_count':approved,'priority':priority,'question_ids':[r['question_id'] for r in items],'recipe_source':recipe_sources.get(family) or ('family-recipes-luna-v0.1.json' if family in family_recipes else None),'stage':'needs_exception_resolution' if priority==0 else 'content_review_pending','required_output':['semantic_subfamilies_if_needed','shared_diagnostic_and_feedback','per_item_binding_exceptions','exact_math_or_primary_source_checks','transfer_roles_and_gaps'],'human_review':None,'runtime_eligible':False})
    state={'schema_version':POLICY,'manifest_sha256':filehash(MANIFEST),'recipe_dependency_hashes':dependency_hashes,'candidate_count':len(records),'records':records,'family_jobs':sorted(jobs,key=lambda j:(j['priority'],-j['approved_label_count'],j['family'])),'approval_policy':'Authoring can continue automatically. No human review or bank/runtime approval is fabricated; missing evidence remains explicit.'}
    summary={'candidate_records_accounted_for':len(records),'archetype_labels':len({r['archetype'] for r in records}),'work_groups_not_verified_semantic_families':len(jobs),'by_content_support':dict(collections.Counter(r['content_support'] for r in records)),'bank_statuses':dict(collections.Counter(r['bank_status'] for r in records)),'mechanical_problem_records':sum(bool(r['mechanical_problems']) for r in records),'semantic_split_records':sum('split_mixed_semantics_before_binding' in r['remaining_actions'] for r in records),'exact_math_checks':sum(r['math_check'] is not None for r in records),'unmapped_code_records':sum(bool(r['unmapped_codes']) for r in records),'all_tutoring_authoring_complete':False,'runtime_approved_records':0,'next_work':'Process family_jobs by priority, splitting mixed methods; author once per method, verify each binding, review exceptions, checkpoint and continue without asking after each small slice.'}
    if write:save(prior_path,state);save(OUT/'bulk-summary.json',summary)
    return state,summary,{'reused_records':hits,'new_or_changed_records':changed}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    _,summary,execution=run(args.write);print(json.dumps({'summary':summary,'execution':execution},ensure_ascii=False))

if __name__=='__main__':main()

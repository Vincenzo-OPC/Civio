#!/usr/bin/env python3
"""Independent exact audit of two queued numerical groups; writes QA only."""
import ast, collections, gzip, json, re
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
STATE=json.loads(gzip.decompress((OUT/'bulk-state.json.gz').read_bytes()))

def evaluate(expression):
    expression=expression.replace('×','*').replace('÷','/').replace('−','-').replace('–','-')
    tree=ast.parse(expression,mode='eval')
    def go(n):
        if isinstance(n,ast.Expression):return go(n.body)
        if isinstance(n,ast.Constant) and type(n.value) is int:return Fraction(n.value)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
            v=go(n.operand);return -v if isinstance(n.op,ast.USub) else v
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
            a,c=go(n.left),go(n.right)
            if isinstance(n.op,ast.Add):return a+c
            if isinstance(n.op,ast.Sub):return a-c
            if isinstance(n.op,ast.Mult):return a*c
            return a/c
        raise ValueError('unsupported expression')
    return go(tree)

def predict(seq):
    candidates=[]
    d=[b-a for a,b in zip(seq,seq[1:])]
    if len(set(d))==1:candidates.append(('arithmetic-sequence',seq[-1]+d[-1]))
    if len(d)>=2 and len(set(b-a for a,b in zip(d,d[1:])))==1:
        dd=d[-1]-d[-2];candidates.append(('arithmetic-first-differences',seq[-1]+d[-1]+dd))
    if len(d)>=2 and all(x>=0 for x in d):
        roots=[int(x**Fraction(1,2)) for x in []]
        if all(int(x**0.5)**2==x for x in d): candidates.append(('square-number-differences',seq[-1]+(int(d[-1]**0.5)+1)**2))
    if len(seq)>=3 and all(seq[i]==seq[i-1]+seq[i-2] for i in range(2,len(seq))):candidates.append(('sum-previous-two',seq[-1]+seq[-2]))
    if len(seq)>=3:
        roots=[int(x**Fraction(1,2)) for x in []] # exact check below, avoids float inference
        squares=[]
        for start in range(0,30):
            if [i*i for i in range(start,start+len(seq))]==seq:squares.append(start+len(seq))
        if squares:candidates.append(('consecutive-squares',squares[0]**2))
        cubes=[]
        for start in range(0,15):
            if [i**3 for i in range(start,start+len(seq))]==seq:cubes.append(start+len(seq))
        if cubes:candidates.append(('consecutive-cubes',cubes[0]**3))
    def prime(n):return n>1 and all(n%d for d in range(2,int(n**.5)+1))
    if len(seq)>=3 and all(prime(x) for x in seq):
        n=seq[-1]+1
        while not prime(n):n+=1
        candidates.append(('consecutive-primes',n))
    if len(seq)>=3 and seq[0]>0 and all(Fraction(b,a)==Fraction(seq[1],seq[0]) for a,b in zip(seq,seq[1:])):
        candidates.append(('geometric-sequence',Fraction(seq[-1]*seq[1],seq[0])))
    # Rule-label priority favors a recognizable conventional form over finite differences.
    priority={'consecutive-squares':0,'consecutive-cubes':0,'sum-previous-two':0,'consecutive-primes':0,'arithmetic-sequence':1,'geometric-sequence':1,'arithmetic-first-differences':2,'constant-third-differences':3}
    candidates.sort(key=lambda x:priority.get(x[0],9))
    unique=[]
    for fam,val in candidates:
        if (fam,val) not in unique:unique.append((fam,val))
    return unique

def load_question(row,cache):
    p=row['source_file']
    if p not in cache:
        data=json.loads((ROOT/p).read_text());cache[p]={x['id']:x for x in data['items']}
    return cache[p][row['question_id']]

def main():
    cache={};out=[]
    for family in ('NUM-OPS-ORDER','NUM-SEQ-DIFF'):
      for row in [r for r in STATE['records'] if r['work_family']==family]:
        q=load_question(row,cache);options={o['option_id']:o['text'] for o in q['options']};key=options[q['answer_option_id']]
        base={'question_id':q['id'],'bank_status':q['status'],'difficulty':q.get('difficulty'),'language':q.get('language'),'source_hash':row['source_record_sha256'],'archetype':family,'stem':q['stem'],'key_option_id':q['answer_option_id'],'key_text':key,'distractor_feedback_coverage':all(o['option_id']==q['answer_option_id'] or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'distractor_code_coverage':all(o['option_id']==q['answer_option_id'] or q.get('distractor_reasoning',{}).get(o['option_id']) for o in q['options'])}
        if family=='NUM-OPS-ORDER':
            expr=q['stem'].split('value of',1)[1].strip().rstrip('?').strip()
            try:
                value=evaluate(expr);matches=[i for i,t in options.items() if Fraction(t)==value]
                base.update(concept_family='order-of-operations',parsed_expression=expr.strip(),exact_answer=str(value),key_matches=(matches==[q['answer_option_id']]),matching_options=matches,independent_method='restricted AST exact-rational evaluation',needs_manual_review=False)
            except Exception as e:base.update(exact_answer=None,key_matches=False,manual_reason=str(e),needs_manual_review=True)
        else:
            m=re.search(r'((?:\d+\s*,\s*){3,}\d+)\s*,?\s*_+',q['stem'])
            if not m:m=re.search(r'((?:\d+\s*,\s*){3,}\d+)(?:\s*,?\s*(?:_+|\?)|$)',q['stem'])
            if not m:base.update(concept_family='unparsed-sequence',needs_manual_review=True,manual_reason='Sequence parser could not isolate terms')
            else:
                seq=[int(x.strip()) for x in m.group(1).split(',')];candidates=predict(seq)
                candidate_values={v for _,v in candidates};matches=[i for i,t in options.items() if Fraction(t) in candidate_values]
                key_value=Fraction(key);selected=[(f,str(v)) for f,v in candidates if v==key_value]
                primary=next(((f,str(v)) for f,v in candidates if f not in ('arithmetic-sequence','geometric-sequence','square-number-differences') and v==key_value),None) or next(((f,str(v)) for f,v in candidates if v==key_value),None)
                matching_rules=[(f,v) for f,v in candidates if any(Fraction(t)==v for t in options.values())]
                offered_values={v for _,v in matching_rules}
                key_pass=(key_value in offered_values and len(matches)==1 and matches[0]==q['answer_option_id'])
                base.update(sequence=seq,first_differences=[b-a for a,b in zip(seq,seq[1:])],candidate_rules=[{'family':f,'next':str(v)} for f,v in candidates],concept_family=primary[0] if primary else ('conflicting_conventional_rules' if candidates else 'unresolved-pattern'),exact_answer=str(key_value) if key_pass else None,key_matches=key_pass,matching_candidate_options=matches,alternatives_not_offered=sorted(str(v) for v in candidate_values-offered_values),needs_manual_review=(not key_pass or not primary))
                if not key_pass:base['manual_reason']='More than one conventional candidate is represented or stored key conflicts with supported option'

        out.append(base)
    duplicate=collections.defaultdict(list)
    for x in out:
        if 'sequence' in x:duplicate[tuple(x['sequence'])].append(x['question_id'])
    repeats=[{'terms':list(k),'question_ids':v} for k,v in duplicate.items() if len(v)>1]
    summary={'groups_audited':{'NUM-OPS-ORDER':sum(x['archetype']=='NUM-OPS-ORDER' for x in out),'NUM-SEQ-DIFF':sum(x['archetype']=='NUM-SEQ-DIFF' for x in out)},'records':len(out),'exact_key_passes':sum(x.get('key_matches') is True for x in out),'key_conflicts_or_manual_exceptions':sum(x.get('key_matches') is False or x.get('needs_manual_review') for x in out),'uncovered_explanations':sum(not x['distractor_feedback_coverage'] for x in out),'uncovered_codes':sum(not x['distractor_code_coverage'] for x in out),'repeated_term_sequences':repeats,'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
    artifact={'schema_version':'dexter-numerical84-audit-v0.1','baseline_commit':'8b69fffbba83fc663e6a2389bdae880a325314d8','method':'Restricted exact-expression evaluation; conventional sequence rule candidates plus exact options/key reconciliation. Results are screening, not pedagogical approval.','summary':summary,'items':out}
    (OUT/'numerical84-audit-v0.1.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()

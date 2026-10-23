#!/usr/bin/env python3
"""Exact rational audit of the queued 45-item rate, time and proportionality pool."""
import collections,gzip,json,math,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
STATE=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
WORDS={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12}
def count(s):
    return int(s) if s.isdigit() else WORDS[s.lower()]

def solve(s):
    m=re.search(r'(?:can|could) .{1,100}? in (\d+) hours?.{0,100}?(?:can|could) .{1,100}? in (\d+) hours?.{0,100}?(?:work together|working together|both work|at the same time)',s,re.I)
    if m:
        a,b=map(int,m.groups());return F(a*b,a+b),'two-workers-combined-rate',{'hours':sorted([a,b])}
    m=re.search(r'from (\d{1,2}:\d{2})\s*([ap])\.m\. to (\d{1,2}:\d{2})\s*([ap])\.m\.',s,re.I)
    if m:
        def mins(t,ap):
            h,mi=map(int,t.split(':'));h%=12;return h*60+mi+(720 if ap.lower()=='p' else 0)
        start=mins(m[1],m[2]);end=mins(m[3],m[4]);duration=end-start
        breaks=sum(map(int,re.findall(r'(\d+)[- ]minute (?:lunch|snack|break)',s,re.I)))
        return F(duration-breaks,60),'elapsed-time-minus-breaks',{'duration_minutes':duration,'break_minutes':breaks}
    m=re.search(r'(\d+) meters? of .*? for ₱([\d,]+).*?same price per meter.*?(\d+) meters?',s,re.I)
    if m:
        a,c,b=int(m[1]),int(m[2].replace(',','')),int(m[3]);return F(c*b,a),'unit-rate-proportion',{'base_quantity':a,'base_cost':c,'target_quantity':b}
    m=re.search(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) trained packers?.*? in (\d+) hours?.*?(\d+) equally fast packers?.*?(?:how many|take)',s,re.I)
    if m:
        w,h,n=count(m[1]),int(m[2]),int(m[3]);return F(w*h,n),'inverse-workers-time',{'workers_start':w,'hours_start':h,'workers_target':n}
    m=re.search(r'every 1 centimeter represents (\d+) kilometers?.*?(\d+(?: \d+/\d+)?|\d+\.\d+) centimeters?',s,re.I)
    if m:
        scale=F(m[1]);v=number(m[2]);return scale*v,'map-scale',{'km_per_cm':str(scale),'map_cm':str(v)}
    m=re.search(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) equally fast volunteers? pack (\d+) .*? in (\d+) hours?.*?(\d+) volunteers?.*? (\d+) hours?',s,re.I)
    if m:
        w,n,h,w2,h2=count(m[1]),int(m[2]),int(m[3]),int(m[4]),int(m[5]);return F(n*w2*h2,w*h),'workers-hours-output',{'workers':w,'output':n,'hours':h,'target_workers':w2,'target_hours':h2}
    m=re.search(r'One pump .*? in (\d+) hours?.*?Another pump .*? in (\d+) hours?.*?(?:both|together)',s,re.I)
    if m:
        a,b=map(int,m.groups());return F(a*b,a+b),'two-pumps-combined-rate',{'hours':sorted([a,b])}
    m=re.search(r'One hose fills .*? in (\d+) hours?.*?a second hose fills .*? in (\d+) hours?.*?both',s,re.I)
    if m:
        a,b=map(int,m.groups());return F(a*b,a+b),'two-hoses-combined-rate',{'hours':sorted([a,b])}
    m=re.search(r'covers (\d+) kilometers? in (\d+(?: \d+/\d+)?|\d+\.\d+) hours?.*?how many hours?.*?(\d+) kilometers?',s,re.I)
    if m:
        d,t,d2=int(m[1]),number(m[2]),int(m[3]);return F(d2,d)*t,'constant-speed-time',{'distance_km':d,'time_h':str(t),'target_distance_km':d2}
    m=re.search(r'travels (\d+) kilometers? at (\d+) km/h, then another (\d+) kilometers? at (\d+) km/h.*?average speed',s,re.I)
    if m:
        d1,s1,d2,s2=map(int,m.groups());return F(d1+d2,F(d1,s1)+F(d2,s2)),'average-speed-total-distance-over-total-time',{'legs':[[d1,s1],[d2,s2]]}
    m=re.search(r'(\d+) prepaid study cards? for ₱(\d+) each\. Each card costs the kiosk ₱(\d+).*?total profit',s,re.I)
    if m:
        n,p,c=map(int,m.groups());return F(n*(p-c)),'total-profit-per-unit-margin',{'quantity':n,'selling_price':p,'unit_cost':c}
    m=re.search(r'covers (\d+) km at an average of (\d+) km/h.*?how long',s,re.I)
    if m:
        d,v=map(int,m.groups());return F(d,v),'distance-over-speed',{'distance_km':d,'speed_kmh':v}
    m=re.search(r'(\d+) envelopes?.*?packs of (\d+).*?how many packs',s,re.I)
    if m:
        need,pack=map(int,m.groups());return F(math.ceil(need/pack)),'whole-packs-ceiling',{'needed':need,'per_pack':pack}
    m=re.search(r'puts away (\d+) folders? each hour.*?(\d+)-hour shift',s,re.I)
    if m:
        rate,h=map(int,m.groups());return F(rate*h),'unit-rate-times-time',{'per_hour':rate,'hours':h}
    m=re.search(r'(?:bought|buys) (\d+) ballpens? at ₱(\d+) each and (\d+) folders? at ₱(\d+) each\. She pays with a ₱(\d+)',s,re.I)
    if not m:m=re.search(r'buys (\d+) bottles of water at ₱(\d+) each and (\d+) boxes of pandesal at ₱(\d+) each, paying with a ₱(\d+)',s,re.I)
    if m:
        n1,c1,n2,c2,pay=map(int,m.groups());return F(pay-n1*c1-n2*c2),'purchase-change',{'counts_prices':[[n1,c1],[n2,c2]],'paid':pay}
    m=re.search(r'starts work at (\d{1,2}:\d{2})\s*([ap])\.m\. and stops at (\d{1,2}:\d{2})\s*([ap])\.m\., taking a (\d+)-minute lunch',s,re.I)
    if m:
        def mins(t,ap):
            h,mi=map(int,t.split(':'));h%=12;return h*60+mi+(720 if ap.lower()=='p' else 0)
        start=mins(m[1],m[2]);end=mins(m[3],m[4]);return F(end-start-int(m[5]),60),'elapsed-work-time',{'elapsed_minutes':end-start,'break_minutes':int(m[5])}
    return None

def number(s):
    m=re.search(r'(\d+)\s+(\d+)\s*/\s*(\d+)',s)
    if m:return F(int(m[1]))+F(int(m[2]),int(m[3]))
    m=re.search(r'\d+\s*/\s*\d+',s)
    if m:return F(m.group())
    m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',s)
    if not m:raise ValueError('No numeric option')
    return F(m.group().replace(',',''))

def option_value(text,method):
    if method in ('elapsed-time-minus-breaks','elapsed-work-time','distance-over-speed','constant-speed-time'):
        if 'hour' in text.lower() and 'minute' in text.lower():
            m=re.search(r'(\d+)\s*hours?\s*(\d+)\s*minutes?',text,re.I)
            if m:return F(60*int(m[1])+int(m[2]),60)
        return number(text)
    if method=='whole-packs-ceiling':return number(text)
    return number(text)

def main():
    cache={};rows=[]
    for r in [x for x in STATE['records'] if x['work_family']=='NUM-WP-RATE']:
        if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
        q=cache[r['source_file']][r['question_id']];res=solve(q['stem']);opts={o['option_id']:o['text'] for o in q['options']}
        if res is None:calc=method=params=None;matches=[]
        else:
            calc,method,params=res;matches=[oid for oid,t in opts.items() if option_value(t,method)==calc]
        key=q['answer_option_id'];sig=(method,json.dumps(params,sort_keys=True)) if res else None
        rows.append({'question_id':q['id'],'status':q['status'],'source_file':r['source_file'],'source_record_sha256':r['source_record_sha256'],'stem':q['stem'],'method':method,'parameters':params,'calculated_answer':str(calc) if calc is not None else None,'key_option_id':key,'key_text':opts.get(key),'matching_options':matches,'key_matches':bool(calc is not None and matches==[key]),'distractor_feedback_present':all(o['option_id']==key or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'duplicate_signature':json.dumps(sig,sort_keys=True) if sig else None,'manual_review':None if calc is not None else 'No supported exact solver template; manual audit required'})
    groups=collections.defaultdict(list)
    for x in rows:
        if x['duplicate_signature']:groups[x['duplicate_signature']].append(x['question_id'])
    repeated=[{'question_ids':v,'same_solution_parameters':json.loads(k)} for k,v in groups.items() if len(v)>1]
    summary={'record_count':len(rows),'status_counts':dict(collections.Counter(x['status'] for x in rows)),'methods':dict(collections.Counter(x['method'] or 'manual' for x in rows)),'exact_calculations':sum(x['calculated_answer'] is not None for x in rows),'key_matches':sum(x['key_matches'] for x in rows),'key_conflicts':sum(x['calculated_answer'] is not None and not x['key_matches'] for x in rows),'manual_required':sum(x['calculated_answer'] is None for x in rows),'missing_wrong_choice_feedback':sum(not x['distractor_feedback_present'] for x in rows),'same-parameter-question-groups':repeated,'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
    artifact={'schema_version':'dexter-rate45-audit-v0.1','baseline_commit':'ac59a961f3136c88a81219bb3d5f920ba7a7fae2','method':'Explicit exact-rational solvers for rate/work, proportionality, constant speed, elapsed time, unit pricing, output, money and pack-ceiling forms. Any unsupported stem is retained as a manual exception. Stored-key agreement is not editorial approval.','summary':summary,'items':rows}
    (D/'rate45-audit-v0.1.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()

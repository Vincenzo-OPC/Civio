#!/usr/bin/env python3
"""Close the two unprocessed single-item numerical families in the queue."""
import gzip,json,re
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3];S=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
def main():
 rows=[];cache={}
 for fam in ('NUM-SEQ-ALT','NUM-UNIT'):
  for r in [x for x in S['records'] if x['work_family']==fam]:
   if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
   q=cache[r['source_file']][r['question_id']];stem=q['stem']
   if fam=='NUM-SEQ-ALT':
    seq=list(map(int,re.findall(r'\d+',stem.split('___')[0])))[-6:];calc=F(seq[-2]+(seq[-2]-seq[-4]));method='two-interleaved-arithmetic-sequences'
    # Even positions 6, 9, 12 rise by 3; odd positions 30, 27, 24 fall by 3.
   else:
    m=re.search(r'(\d+(?:\.\d+)?) hours?',stem,re.I);calc=F(m[1])*60;method='hours-times-60-minutes-per-hour'
   opts={o['option_id']:F(re.search(r'-?\d+(?:\.\d+)?',o['text']).group()) for o in q['options']};matches=[i for i,v in opts.items() if v==calc];key=q['answer_option_id']
   rows.append({'question_id':q['id'],'status':q['status'],'source_record_sha256':r['source_record_sha256'],'stem':stem,'method':method,'calculated_answer':str(calc),'key_option_id':key,'matching_options':matches,'key_matches':matches==[key],'manual_review':'Sequence continuation remains an editorial judgment; alternating rule and options support the stored result.' if fam=='NUM-SEQ-ALT' else None,'runtime_eligible':False})
 summary={'record_count':len(rows),'by_family':{f:sum(x['question_id'].startswith('CIVIO-D1022-NUMSEQ') if f=='NUM-SEQ-ALT' else x['question_id'].startswith('CIVIO-B3-NUM-UNIT') for x in rows) for f in ('NUM-SEQ-ALT','NUM-UNIT')},'all_records_draft':all(x['status']=='draft' for x in rows),'key_matches':sum(x['key_matches'] for x in rows),'key_conflicts':sum(not x['key_matches'] for x in rows),'tutoring_bindings_added':0,'status':'draft_audit_only','human_review':None,'runtime_eligible':False}
 out={'schema_version':'dexter-numeric-tail2-audit-v0.1','baseline_commit':'8ec91ef1386a7755e59c0e47ef9e0ac1d6c6c4f7','method':'Direct exact arithmetic. The sequence item uses alternating increasing and decreasing subsequences; the duration conversion uses 60 minutes per hour.','summary':summary,'items':rows}
 (D/'numeric-tail2-audit-v0.1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main()

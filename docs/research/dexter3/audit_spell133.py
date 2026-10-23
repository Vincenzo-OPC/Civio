#!/usr/bin/env python3
"""Spell-check screening of 133 queued clerical spelling items using system Hunspell."""
import collections,ctypes,gzip,hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3];S=json.loads(gzip.decompress((D/'bulk-state.json.gz').read_bytes()))
AFF=b'/usr/share/hunspell/en_US.aff';DIC=b'/usr/share/hunspell/en_US.dic'
class Spell:
 def __init__(self):
  try:self.lib=ctypes.CDLL('libhunspell-1.7.so.0')
  except OSError as e:raise RuntimeError('This audit requires libhunspell-1.7 and the hunspell-en-us dictionary.') from e
  self.buf=ctypes.create_string_buffer(1024);self.ptr=ctypes.cast(self.buf,ctypes.c_void_p)
  self.ctor=self.lib._ZN8HunspellC1EPKcS1_S1_;self.ctor.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p];self.ctor(self.ptr,AFF,DIC,None)
  self.check=self.lib._ZN8Hunspell5spellEPKcPiPPc;self.check.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p];self.check.restype=ctypes.c_int
  self.dtor=self.lib._ZN8HunspellD1Ev;self.dtor.argtypes=[ctypes.c_void_p]
 def valid(self,w):return bool(self.check(self.ptr,w.encode('utf-8'),None,None))
 def close(self):self.dtor(self.ptr)
def main():
 sp=Spell();cache={};rows=[]
 try:
  for fam in ('CLR-SPELL-WRONG','CLR-SPELL-RIGHT','CLR-SPELLING'):
   for r in [x for x in S['records'] if x['work_family']==fam]:
    if r['source_file'] not in cache:cache[r['source_file']]={q['id']:q for q in json.loads((ROOT/r['source_file']).read_text())['items']}
    q=cache[r['source_file']][r['question_id']];vals=[{'option_id':o['option_id'],'text':o['text'],'hunspell_accepts_en_us':sp.valid(o['text'].strip())} for o in q['options']]
    accepted=[v['option_id'] for v in vals if v['hunspell_accepts_en_us']];key=q['answer_option_id']
    if fam=='CLR-SPELL-WRONG':rule_ok=(key not in accepted and len(accepted)==3)
    else:rule_ok=(key in accepted and len(accepted)==1)
    row={'question_id':q['id'],'family':fam,'status':q['status'],'source_file':r['source_file'],'source_record_sha256':r['source_record_sha256'],'stem':q['stem'],'options':vals,'key_option_id':key,'accepted_spellings':accepted,'key_agrees_with_spell_rule':rule_ok,'wrong_option_feedback_present':all(o['option_id']==key or q.get('reveal',{}).get('why_wrong',{}).get(o['option_id']) for o in q['options']),'manual_review':None if rule_ok else 'Dictionary result does not establish a single defensible answer; check lexical variants, regional forms, meaning and target variety.'}
    if q['id']=='CIVIO-CLR-20261013-0034':
     row['editorial_resolution']='The key is contextually defensible: the stem specifies “a schedule of dates.” “Calender” is also a correctly spelled but different word for a roller process or machine. Preserve the meaning cue.'
     row['manual_review']=None;row['key_agrees_with_item_context']=True
    elif q['id']=='CIVIO-CLR-SPELL-RIGHT-000900':
     row['editorial_resolution']='Unresolved ambiguity: “yeld” is a real regional/dialect word, while “yield” is the common target. The stem gives no meaning or variety restriction, so the question does not ensure a single defensible spelling answer.'
     row['key_agrees_with_item_context']=False
    else:row['key_agrees_with_item_context']=rule_ok
    rows.append(row)
 finally:sp.close()
 # Preserve pre-existing question-specific tutoring; do not duplicate it.
 pilot=json.loads((D/'pilot-v0.1.json').read_text());covered={x['question_id'] for x in pilot['bindings']}
 for row in rows:row['existing_tutoring_binding']=row['question_id'] in covered
 statuses=collections.Counter(x['status'] for x in rows);fam=collections.Counter(x['family'] for x in rows)
 art={'schema_version':'dexter-spell133-audit-v0.1','baseline_commit':'e40b6b965de422ab4f8e5cd7462bbac5425ed291','method':'Hunspell English (United States), package hunspell-en-us 1:2020.12.07-2, checked through libhunspell 1.7 with its affix rules. This is an automated lexical screen, not a substitute for editorial review of regional, archaic, proper-name or meaning-specific alternatives.','summary':{'record_count':len(rows),'by_family':dict(fam),'status_counts':dict(statuses),'single-key-rule_matches':sum(x['key_agrees_with_spell_rule'] for x in rows),'spell-rule-exceptions':sum(not x['key_agrees_with_spell_rule'] for x in rows),'context-resolved-lexical-alternatives':sum(x.get('key_agrees_with_item_context') and not x['key_agrees_with_spell_rule'] for x in rows),'unresolved_single-answer_review':sum(not x.get('key_agrees_with_item_context',False) for x in rows),'wrong_option_feedback_missing':sum(not x['wrong_option_feedback_present'] for x in rows),'already_bound_in_pilot':sum(x['existing_tutoring_binding'] for x in rows),'human_reviews':0,'status':'draft_audit_only','runtime_eligible':False},'items':rows,'known_lexical_review':'CIVIO-CLR-SPELL-RIGHT-000900 offers “yield” and “yeld.” Collins records yeld as a Scottish/Northern English dialect adjective; absent a definition or locale cue, this is a second valid word and should be replaced or contextualized. CIVIO-CLR-20261013-0034 offers “calendar” and “calender”; the stem supplies the meaning “a schedule of dates,” which distinguishes the intended answer. See SPELLING_REVIEW.md.'}
 (D/'spell133-audit-v0.1.json').write_text(json.dumps(art,ensure_ascii=False,indent=2)+'\n');print(json.dumps(art['summary'],ensure_ascii=False))
if __name__=='__main__':main()

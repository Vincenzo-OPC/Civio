#!/usr/bin/env python3
"""Build the Dexter Rescue editorial validation packet (ADR-0003, Issue #22).

Read-only over approved bank items. Picks 20 approved items per pilot skill
(NUM-WP-PCT-CHANGE, NUM-WP-RATIO, CLR-SPELL-WRONG), one per rough stem family,
with a fixed seed. One row per WRONG option, so reviewers judge each
code-to-distractor match. Reviewer columns are left blank: agents never fill
or approve them.

Run from repo root:
    python3 docs/research/dexter2/pilot/build_pilot_packet.py
"""
import csv, json, random, re, sys, pathlib, hashlib

ROOT = pathlib.Path('.')
OUT = ROOT / 'docs/research/dexter2/pilot'
sys.path.insert(0, str(ROOT / 'docs/research/dexter2'))
import bank_metadata_audit as audit  # noqa: E402  (module runs its audit on import; output discarded)

SKILLS = ['NUM-WP-PCT-CHANGE', 'NUM-WP-RATIO', 'CLR-SPELL-WRONG']
PER_SKILL = 20
SEED = 20261022
REVIEW_COLS = [
    'r1_code_matches_error', 'r1_why_wrong_accurate', 'r1_item_family_distinct', 'r1_notes',
    'r2_code_matches_error', 'r2_why_wrong_accurate', 'r2_item_family_distinct', 'r2_notes',
    'agreement', 'disagreement_note', 'ambiguity_note', 'adjudication', 'adjudicator', 'adjudicated_at',
]

rows = list(csv.DictReader(audit.MANIFEST.open()))
by_skill = {s: {} for s in SKILLS}
for r in rows:
    if r['status'] != 'approved':
        continue
    rec = audit.load(r['source_file']).get(r['id'])
    arch = audit.archetype_of(r['id'], rec)
    if arch in by_skill and rec:
        by_skill[arch].setdefault(audit.stem_family(rec.get('stem')), []).append(rec)

rng = random.Random(SEED)
out_rows, summary = [], {}
for skill in SKILLS:
    fams = sorted(by_skill[skill].items())
    picks = []
    for fam, recs in fams:
        recs = sorted(recs, key=lambda x: x['id'])
        picks.append((fam, rng.choice(recs)))
    rng.shuffle(picks)
    picks = sorted(picks[:PER_SKILL], key=lambda p: p[1]['id'])
    summary[skill] = {'families_available': len(fams), 'picked': len(picks)}
    for fam, rec in picks:
        opts = {o['option_id']: o['text'] for o in rec['options']}
        key = rec['answer_option_id']
        for oid, text in opts.items():
            if oid == key:
                continue
            code = (rec.get('distractor_reasoning') or {}).get(oid, '')
            out_rows.append({
                'item_id': rec['id'], 'skill': skill, 'stem_family': fam, 'language': rec.get('language', ''),
                'stem': rec['stem'], 'correct_option': f"{key}: {opts[key]}",
                'distractor_option': f"{oid}: {text}", 'distractor_code': code,
                'code_in_dexter_taxonomy': 'yes' if code in audit.TAXONOMY else 'no',
                'subreason': str((rec.get('distractor_subreason') or {}).get(oid, '')),
                'why_wrong': (rec.get('reveal') or {}).get('why_wrong', {}).get(oid, ''),
                'why_correct': (rec.get('reveal') or {}).get('why_correct', ''),
                **{c: '' for c in REVIEW_COLS},
            })

with (OUT / 'dexter-rescue-pilot-packet-2026-10-22.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    w.writerows(out_rows)

json.dump({'seed': SEED, 'items': sum(v['picked'] for v in summary.values()), 'distractor_rows': len(out_rows),
           'per_skill': summary, 'sha256_csv': hashlib.sha256((OUT / 'dexter-rescue-pilot-packet-2026-10-22.csv').read_bytes()).hexdigest()},
          (OUT / 'pilot-packet-summary.json').open('w'), indent=1)
print(json.dumps(summary))

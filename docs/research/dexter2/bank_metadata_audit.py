#!/usr/bin/env python3
"""Read-only Dexter metadata audit of the flat 2,100 manifest (Issue #22).

Counts, per item, whether the source record has what Dexter Rescue needs.
It never writes bank files. Run from the repo root:
    python3 docs/research/dexter2/bank_metadata_audit.py > docs/research/dexter2/bank_metadata_audit.json
"""
import csv, json, re, sys, collections, pathlib, hashlib

ROOT = pathlib.Path('.')
MANIFEST = ROOT / 'docs/research/bank/civio-flat-2100-manifest-2026-10-22.csv'
TAXONOMY = set(re.findall(r"'([A-Z]{2,3}-[A-Z0-9-]+)' => \['domain'", (ROOT / 'config/dexter_misconceptions.php').read_text()))
GRAPH = set(re.findall(r"'([A-Z]{3}-[A-Z0-9-]+)' => \['label'", (ROOT / 'config/dexter_skill_graph.php').read_text()))
PRIORITY = ['NUM-PCT-BASIC', 'NUM-WP-PCT-CHANGE', 'NUM-FRAC-DEC', 'NUM-WP-RATIO', 'NUM-WP-RATE', 'NUM-WP-ALGEBRA', 'NUM-OPS-ORDER', 'CLR-SPELL-RIGHT', 'CLR-SPELL-WRONG', 'CLR-FILE-POSITION']

_cache = {}
def load(path):
    if path not in _cache:
        try:
            data = json.loads((ROOT / path).read_text())
        except Exception:
            data = None
        idx = {}
        def walk(x):
            if isinstance(x, dict):
                if isinstance(x.get('id'), str) and x['id'].startswith('CIVIO-') and 'stem' in x:
                    idx[x['id']] = x
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(data)
        _cache[path] = idx
    return _cache[path]

def archetype_of(item_id, rec):
    a = rec.get('archetype') if rec else None
    if isinstance(a, str) and a:
        return a
    m = re.match(r'CIVIO-(.+)-\d{6}$', item_id)
    return m.group(1) if m else None

def option_ids(rec):
    out = []
    for o in rec.get('options') or []:
        if isinstance(o, dict):
            out.append(o.get('option_id'))
        else:
            out.append(None)
    return out

def stem_family(stem):
    s = re.sub(r'\d+([.,]\d+)?', '#', (stem or '').lower())
    s = re.sub(r'\b[A-Z][a-z]+\b', 'N', s)
    return hashlib.sha1(re.sub(r'\s+', ' ', s)[:80].encode()).hexdigest()[:10]

rows = list(csv.DictReader(MANIFEST.open()))
tot = collections.Counter()
by_arch = collections.defaultdict(collections.Counter)
families = collections.defaultdict(set)
missing_source = 0
for r in rows:
    status = r['status']
    rec = load(r['source_file']).get(r['id'])
    if rec is None:
        missing_source += 1
    arch = archetype_of(r['id'], rec)
    key = arch or 'UNKNOWN'
    c = by_arch[key]
    c['items'] += 1
    c[status] += 1
    tot[status] += 1
    if status != 'approved' or rec is None:
        continue
    oids = option_ids(rec)
    ans = rec.get('answer_option_id')
    wrong = [o for o in oids if o and o != ans]
    reveal = rec.get('reveal') or {}
    why_wrong = reveal.get('why_wrong') or {}
    dr = rec.get('distractor_reasoning') or {}
    checks = {
        'answer_key_resolvable': bool(ans) and ans in oids and len(oids) == 4,
        'why_wrong_complete': bool(wrong) and all(isinstance(why_wrong.get(o), str) and why_wrong.get(o).strip() for o in wrong),
        'distractor_codes_complete': bool(wrong) and all(isinstance(dr.get(o), str) and dr.get(o) for o in wrong),
        'distractor_codes_in_taxonomy': bool(wrong) and all(dr.get(o) in TAXONOMY for o in wrong),
        'has_source': bool(str(rec.get('source') or '').strip()),
        'review_passed': rec.get('review_status') == 'passed',
        'archetype_in_graph': arch in GRAPH,
        'subpro_eligible': r['track'] in ('sub', 'both'),
    }
    checks['rescue_ready'] = all(checks[k] for k in ['answer_key_resolvable', 'why_wrong_complete', 'distractor_codes_in_taxonomy', 'archetype_in_graph'])
    for k, v in checks.items():
        if v:
            c['approved_' + k] += 1
            tot['approved_' + k] += 1
    families[key].add(stem_family(rec.get('stem')))

out = {
    'generated_from': str(MANIFEST), 'manifest_rows': len(rows), 'source_records_not_found': missing_source,
    'taxonomy_codes': len(TAXONOMY), 'graph_skills': len(GRAPH),
    'totals': dict(tot),
    'priority_archetypes': {a: dict(by_arch[a], approved_stem_families=len(families[a])) for a in PRIORITY},
    'all_archetypes': {a: dict(c, approved_stem_families=len(families[a])) for a, c in sorted(by_arch.items())},
    'notes': [
        'Read-only. Counts come from bank source JSON named by the manifest, not from a runtime DB.',
        'archetype falls back to the id prefix when the record has no archetype field.',
        'rescue_ready = resolvable key + why_wrong for every wrong option + every distractor code in the Dexter taxonomy + archetype in the skill graph.',
        'approved_stem_families is a rough template-clone detector (numbers and names masked); it is not a human judgement.',
        'Nothing here verifies that a code is the RIGHT diagnosis; that needs editorial review (Issue #22 pilot).',
    ],
}
json.dump(out, sys.stdout, indent=1, sort_keys=True)

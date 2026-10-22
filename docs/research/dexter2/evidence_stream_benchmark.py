#!/usr/bin/env python3
"""Offline benchmark for ADR-0001 as decided: fixed BKT vs rolling independent
accuracy, fed ONLY the knowledge stream (first answer to each distinct
question; blanks and repeats removed), on the synthetic fixtures from
mastery_simulation.py. No real learner data. Pure Python, fixed seeds.

Run: python3 docs/research/dexter2/evidence_stream_benchmark.py > docs/research/dexter2/evidence_stream_benchmark_results.json
"""
import json, random, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import mastery_simulation as ms

def knowledge_stream(events):
    seen, out = set(), []
    for e in events:
        if e['skipped'] or e['item'] in seen:
            continue
        seen.add(e['item'])
        out.append(e)
    return out

def run():
    res = {'note': 'Synthetic only. Fixed BKT parameters are not calibrated; this does not pick a model.', 'results': {}}
    for gname, gen in ms.GENERATORS.items():
        agg = {}
        for seed in ms.SEEDS:
            data = gen(random.Random(seed))
            preds = {'bkt_fixed': [], 'rolling10': []}
            for ev in data:
                models = {'bkt_fixed': ms.BKT(), 'rolling10': ms.Rolling()}
                for e in knowledge_stream(ev):
                    for k, m in models.items():
                        preds[k].append((m.predict(e['item']), 1 if e['correct'] else 0, e['p_true']))
                        m.update(e['item'], e['correct'], False)
            for k, p in preds.items():
                for mk, mv in ms.metrics(p).items():
                    agg.setdefault(k, {}).setdefault(mk, []).append(mv)
        res['results'][gname] = {k: {mk: (None if any(v is None for v in vs) else round(sum(vs) / len(vs), 4)) for mk, vs in m.items()} for k, m in agg.items()}
    return res

if __name__ == '__main__':
    print(json.dumps(run(), indent=1))

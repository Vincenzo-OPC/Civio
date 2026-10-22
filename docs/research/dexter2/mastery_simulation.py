#!/usr/bin/env python3
"""Offline synthetic comparison of mastery estimators for Issue #20.

Pure Python 3 (no packages), fixed seeds, no network, no real learner data.
Compares next-answer prediction of:
  bkt_fixed      Civio SkillMasteryEstimator parameters (pInit .2, learn .1, slip .1, guess .25)
  bkt_skip_wrong same, but a skipped item is fed as a wrong answer (current LearningInsightsService behaviour)
  rolling10      Laplace-smoothed accuracy over the last 10 independent answers
  elo            learner-skill rating + item difficulty learned across the population (K = 0.4 / (1 + 0.05 n))
on four generators:
  bkt_hetero     true BKT with per-learner parameters drawn around Civio defaults
  irt_drift      logistic ability x item difficulty, ability grows slowly with practice
  repeats        irt_drift where 30% of exposures repeat a seen item (memorization boost +0.25)
  skips          irt_drift with 15% of items left blank (blank is not an observed wrong answer)
Metrics on answered items only: Brier, log loss, ECE (10 bins), and the false
"ready" rate: share of estimates >= 0.85 where the true P(correct) < 0.7.

Run:  python3 docs/research/dexter2/mastery_simulation.py > docs/research/dexter2/mastery_simulation_results.json
"""
import json, math, random

SEEDS = [11, 23, 37]
N_LEARNERS = 300
N_ITEMS = 120
N_STEPS = 40
GUESS = 0.25

def sig(x):
    return 1 / (1 + math.exp(-x))

def clamp(p):
    return min(max(p, 1e-4), 1 - 1e-4)

# ---------- generators: yield per learner a list of events ----------
def gen_bkt_hetero(rng):
    learners = []
    for _ in range(N_LEARNERS):
        p0 = min(max(rng.gauss(0.2, 0.1), 0.01), 0.8)
        pl = min(max(rng.gauss(0.1, 0.06), 0.01), 0.5)
        sl = min(max(rng.gauss(0.1, 0.05), 0.01), 0.3)
        gu = min(max(rng.gauss(0.25, 0.07), 0.05), 0.45)
        known = rng.random() < p0
        ev = []
        for _ in range(N_STEPS):
            ptrue = (1 - sl) if known else gu
            item = rng.randrange(N_ITEMS)
            ev.append({'item': item, 'p_true': ptrue, 'correct': rng.random() < ptrue, 'skipped': False})
            if not known and rng.random() < pl:
                known = True
        learners.append(ev)
    return learners

def gen_irt(rng, repeat_rate=0.0, skip_rate=0.0):
    diffs = [rng.gauss(0, 1) for _ in range(N_ITEMS)]
    learners = []
    for _ in range(N_LEARNERS):
        theta = rng.gauss(-0.5, 1)
        growth = abs(rng.gauss(0.04, 0.03))
        seen = []
        ev = []
        for _ in range(N_STEPS):
            if seen and rng.random() < repeat_rate:
                item = rng.choice(seen)
                boost = 0.25
            else:
                item = rng.randrange(N_ITEMS)
                boost = 0.0
            p = GUESS + (1 - GUESS) * sig(theta - diffs[item])
            p = min(p + boost, 0.99)
            skipped = rng.random() < skip_rate
            ev.append({'item': item, 'p_true': p, 'correct': (not skipped) and rng.random() < p, 'skipped': skipped})
            if not skipped:
                theta += growth
                seen.append(item)
        learners.append(ev)
    return learners

GENERATORS = {
    'bkt_hetero': gen_bkt_hetero,
    'irt_drift': lambda r: gen_irt(r),
    'repeats': lambda r: gen_irt(r, repeat_rate=0.3),
    'skips': lambda r: gen_irt(r, skip_rate=0.15),
}

# ---------- estimators: predict P(correct) before each answered event ----------
class BKT:
    def __init__(self, skip_as_wrong=False):
        self.p = 0.2; self.skip_as_wrong = skip_as_wrong
    def predict(self, item):
        return self.p * 0.9 + (1 - self.p) * GUESS
    def update(self, item, correct, skipped):
        if skipped and not self.skip_as_wrong:
            return
        c = correct and not skipped
        if c:
            post = self.p * 0.9 / (self.p * 0.9 + (1 - self.p) * GUESS)
        else:
            post = self.p * 0.1 / (self.p * 0.1 + (1 - self.p) * (1 - GUESS))
        self.p = post + (1 - post) * 0.1

class Rolling:
    def __init__(self, w=10):
        self.h = []; self.w = w
    def predict(self, item):
        last = self.h[-self.w:]
        return (sum(last) + 1) / (len(last) + 2)
    def update(self, item, correct, skipped):
        if not skipped:
            self.h.append(1 if correct else 0)

class EloPop:
    """Shared item difficulties across learners; one rating per learner."""
    def __init__(self):
        self.b = {}; self.nb = {}
    def learner(self):
        pop = self
        class L:
            def __init__(s):
                s.t = 0.0; s.n = 0
            def predict(s, item):
                return GUESS + (1 - GUESS) * sig(s.t - pop.b.get(item, 0.0))
            def update(s, item, correct, skipped):
                if skipped:
                    return
                p = s.predict(item)
                err = (1 if correct else 0) - p
                s.n += 1
                s.t += 0.4 / (1 + 0.05 * s.n) * err * 4
                nb = pop.nb.get(item, 0) + 1
                pop.nb[item] = nb
                pop.b[item] = pop.b.get(item, 0.0) - 0.4 / (1 + 0.05 * nb) * err * 2
        return L()

def metrics(preds):
    if not preds:
        return {}
    brier = sum((p - y) ** 2 for p, y, _ in preds) / len(preds)
    ll = -sum(y * math.log(clamp(p)) + (1 - y) * math.log(clamp(1 - p)) for p, y, _ in preds) / len(preds)
    bins = [[] for _ in range(10)]
    for p, y, _ in preds:
        bins[min(int(p * 10), 9)].append((p, y))
    ece = sum(len(b) / len(preds) * abs(sum(p for p, _ in b) / len(b) - sum(y for _, y in b) / len(b)) for b in bins if b)
    ready = [(p, t) for p, _, t in preds if p >= 0.85]
    false_ready = sum(1 for _, t in ready if t < 0.7) / len(ready) if ready else None
    return {'brier': round(brier, 4), 'log_loss': round(ll, 4), 'ece': round(ece, 4),
            'n_ready_claims': len(ready), 'false_ready_rate': None if false_ready is None else round(false_ready, 4)}

def run():
    out = {'config': {'seeds': SEEDS, 'learners': N_LEARNERS, 'items': N_ITEMS, 'steps': N_STEPS, 'guess': GUESS}, 'results': {}}
    for gname, gen in GENERATORS.items():
        agg = {}
        for seed in SEEDS:
            rng = random.Random(seed)
            data = gen(rng)
            elo = EloPop()
            factories = {'bkt_fixed': lambda: BKT(), 'bkt_skip_wrong': lambda: BKT(True), 'rolling10': lambda: Rolling(), 'elo': elo.learner}
            preds = {k: [] for k in factories}
            for ev in data:
                models = {k: f() for k, f in factories.items()}
                for e in ev:
                    for k, m in models.items():
                        if not e['skipped']:
                            preds[k].append((m.predict(e['item']), 1 if e['correct'] else 0, e['p_true']))
                        m.update(e['item'], e['correct'], e['skipped'])
            for k, p in preds.items():
                for mk, mv in metrics(p).items():
                    agg.setdefault(k, {}).setdefault(mk, []).append(mv)
        out['results'][gname] = {k: {mk: (None if any(v is None for v in vs) else round(sum(vs) / len(vs), 4)) for mk, vs in m.items()} for k, m in agg.items()}
    return out

if __name__ == '__main__':
    print(json.dumps(run(), indent=1))

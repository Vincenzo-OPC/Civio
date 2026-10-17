"""Apply the Grok Bot round 03 audit edits (c1-c4) to docs/research/chatgpt-batch-003.json. Items stay draft/unreviewed.
Usage: python3 scripts/batches/fixes/b3/apply.py  (idempotent: starts from the Codex commit eca4268)."""
import json, os, subprocess, sys
here = os.path.dirname(__file__)
sys.path.insert(0, here)
import c1, c2, c3, c4
D = {**c1.D, **c2.D, **c3.D, **c4.D}
P = "docs/research/chatgpt-batch-003.json"
d = json.loads(subprocess.check_output(["git", "show", "eca4268:" + P]))
log = []
for it in d["items"]:
    e = D[it["id"][-6:]]
    ch = []
    opts = {o["option_id"]: o for o in it["options"]}
    key = opts[it["answer_option_id"]]
    if "stem" in e:
        it["stem"] = e["stem"]; ch.append("stem")
    if "k" in e:
        old = key["text"]; key["text"] = e["k"]
        it["reveal"]["why_correct"] = it["reveal"]["why_correct"].replace(f'"{old}"', f'"{e["k"]}"', 1)
        ch.append("key wording (same answer)")
    nrep = 0
    for oid, (txt, code, why) in e["o"].items():
        assert oid != it["answer_option_id"] and oid in opts, (it["id"], oid)
        if txt and txt != opts[oid]["text"]:
            opts[oid]["text"] = txt; nrep += 1
        if code:
            it["distractor_reasoning"][oid] = code
        it["reveal"]["why_wrong"][oid] = f'"{opts[oid]["text"]}" is incorrect. {why}'
    if nrep: ch.append(f"{nrep} distractor(s) replaced")
    ch.append("why-wrong rewritten"); it["reveal"]["shortcut"] = e["sc"]; ch.append("method line")
    it["notes"] = (it.get("notes", "") + " | Grok Bot audit 2026-10-17: " + "; ".join(ch) + ". Still draft for CoS.").strip(" |")
    log.append((it["id"], ch))
open(P, "w").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print(len(log), "items edited")

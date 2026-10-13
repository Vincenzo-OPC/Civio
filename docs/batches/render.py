"""Render docs/batches/batch-NNN.md from its JSON (the JSON is the source of truth).
Usage: python3 docs/batches/render.py docs/batches/batch-001.json"""
import json, sys
src = sys.argv[1]
b = json.load(open(src, encoding="utf-8"))
items = b["items"]
L = [f"# Civio {b['batch'].replace('batch-', 'batch ')} ({b['status']})", ""]
L += b["intro"] + [""]
for n, it in enumerate(items, 1):
    L += [f"## {n}. {it['id']}", "",
          f"- track: {it['track']} · domain: {it['domain']} · archetype: {it['archetype']} · difficulty: {it['difficulty']} · est: {it['est_seconds']} s",
          f"- competency: {it['competency']} · concept: {it['concept']}",
          f"- micro_skill: {it['micro_skill']}",
          f"- source: {it['source']}" + (f" ({it['source_url']})" if it.get('source_url') else ""),
          f"- status: {it['status']} · review_status: {it['review_status']}" + (f" · reviewer: {it['reviewer']} ({it['reviewed_at']})" if it.get('reviewer') else ""),
          "", f"**Stem:** {it['stem']}", "", "| option_id | text | shown as |", "|---|---|---|"]
    for i, o in enumerate(it["options"]):
        L.append(f"| {o['option_id']} | {o['text']} | {'ABCD'[i]} |")
    txt = {o["option_id"]: o["text"] for o in it["options"]}
    L += ["", f"`answer_option_id`: {it['answer_option_id']} ({txt[it['answer_option_id']]})", "",
          "`distractor_reasoning`: " + "; ".join(f"{k} = `{v}`" for k, v in it["distractor_reasoning"].items()), "",
          "**Reveal**", ""]
    r = it["reveal"]
    if r.get("terms"):
        L.append(f"1. *Meaning.* {r['terms']}")
    L += [f"2. *Shortcut.* {r['shortcut']}", f"3. *Why it is right.* {r['why_correct']}", "4. *Why the others are wrong.*"]
    for k, v in r["why_wrong"].items():
        L.append(f"   - {txt[k]}: {v}")
    L += ["", f"Review: {it.get('review_line', '[ ] CoS pass  [ ] GT approve  Notes:')}", ""]
L += b.get("outro", [])
open(src[:-5] + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")

#!/usr/bin/env python3
"""Regression tests for bank QA gates (22 Oct 2026). Run: python3 scripts/batches/qa/test_bank_gates_2026_10_22.py"""
import json, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent.parent), str(Path(__file__).parent.parent / "drafts")]
import qa  # noqa: E402

SET2 = "docs/research/batches/drafts/verbal-en-reading-set2-2026-10-22.json"
P1 = "docs/research/audit/fixes/p1-editorial-r1-2026-10-22.json"
MAN = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json"


def test_short_english_passage_fails():
    it = dict(json.load(open(SET2))["items"][0])
    it["stem"] = "Read the passage, then answer the question.\n\n" + " ".join(["word"] * 149) + "\n\nWhat is the passage mainly about?"
    assert any("minimum is 150" in e for e in qa.check_item(it)), qa.check_item(it)


def test_150_word_passage_passes_gate():
    it = dict(json.load(open(SET2))["items"][0])
    it["stem"] = "Read the passage, then answer the question.\n\n" + " ".join(["word"] * 150) + "\n\nWhat is the passage mainly about?"
    assert qa.passage_errors(it) == []


def test_instruction_line_not_counted():
    it = {"domain": "verbal_en", "passage_id": "X", "stem": "Read the passage, then answer the question.\n\n" + " ".join(["w"] * 145) + "\n\nQ?"}
    assert qa.passage_words(it) == 145


def test_sentence_vocab_item_is_not_a_passage():
    it = {"domain": "verbal_en", "archetype": "VEN-RC-VOCAB", "stem": "The officer was candid about the delay. Candid most nearly means"}
    assert qa.passage_words(it) is None


def test_every_english_passage_in_manifest_meets_gate():
    m = json.load(open(MAN))
    cache, short = {}, []
    for r in m["items"]:
        if r["domain"] != "verbal_en":
            continue
        f = r["source_file"]
        if f not in cache:
            d = json.load(open(f)); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        w = qa.passage_words(cache[f][r["id"]])
        if w is not None and w < qa.PASSAGE_MIN_WORDS:
            short.append((r["id"], w))
    assert not short, short


def test_p1_revisions_are_drafts_with_history_and_verified_keys():
    for it in json.load(open(P1))["items"]:
        assert it["status"] == "draft" and it["reviewer"] is None and it["replaces"] and it["revision_history"]
        assert qa.check_item(it) == [], (it["id"], qa.check_item(it))
        assert "method_steps" in it["reveal"]


def test_no_d1022_key_is_conspicuously_longest():
    m = json.load(open(MAN)); cache, bad = {}, []
    for r in m["items"]:
        if "D1022" not in r["id"]:
            continue
        f = r["source_file"]
        if f not in cache:
            cache[f] = {i["id"]: i for i in json.load(open(f))["items"]}
        it = cache[f][r["id"]]
        o = {x["option_id"]: x["text"] for x in it["options"]}
        k = o[it["answer_option_id"]]
        if len(k) > 30 and len(k) > 1.6 * max(len(t) for i2, t in o.items() if i2 != it["answer_option_id"]):
            bad.append(r["id"])
    assert not bad, bad


def test_recommendations_cover_queue_and_never_approve():
    import csv
    rows = list(csv.DictReader(open("docs/research/review/queue-recommendations-2026-10-22.csv")))
    m = json.load(open(MAN))
    pending = {r["id"] for r in m["items"] if r["status"] != "approved"}
    assert {r["id"] for r in rows} == pending
    assert all(r["decision_by_human"] == "" and r["recommendation"] in ("Accept", "Accept revision", "Revise", "Reject", "Escalate") for r in rows)
    assert all(r["needs_human_read"] == "yes" for r in rows if "D1022" in r["id"]), "every self-authored D1022 row needs a human read"


def test_count_is_2100():
    m = json.load(open(MAN))
    assert len(m["items"]) == 2100 and len({r["id"] for r in m["items"]}) == 2100



FILR1 = "docs/research/audit/fixes/vfil-passage-r1-2026-10-22.json"


def _fil(n, level=None, ins="Basahin ang talata:\n"):
    it = {"domain": "verbal_fil", "archetype": "VFIL-PAGBASA", "stem": ins + " ".join(["salita"] * n) + "\n\nAno ang ipinahihiwatig?"}
    if level:
        it["passage_level"] = level
    return it


def test_fil_two_levels():
    assert qa.passage_errors(_fil(79)) and "at least 80" in qa.passage_errors(_fil(79))[0]
    assert qa.passage_errors(_fil(80)) == [] and qa.fil_passage_level(80) == "short"
    assert qa.passage_errors(_fil(149)) == [] and qa.fil_passage_level(149) == "short"
    assert qa.passage_errors(_fil(150)) == [] and qa.fil_passage_level(150) == "long"
    assert qa.passage_errors(_fil(250)) == [] and "at most 250" in qa.passage_errors(_fil(251))[0]


def test_fil_declared_level_must_match_count():
    assert qa.passage_errors(_fil(100, "short")) == []
    assert "declared long" in qa.passage_errors(_fil(100, "long"))[0]
    assert "declared short" in qa.passage_errors(_fil(160, "short"))[0]


def test_fil_instruction_variants_detected_and_not_counted():
    for ins in ("Basahin ang talata:\n", "Basahin at unawain:\n", "Suriin ang talata sa ibaba:\n", "Talata:\n"):
        it = _fil(70, ins=ins); it.pop("archetype")
        assert qa.passage_words(it) == 70, ins
        assert qa.passage_errors(it), ins


def test_manifest_fil_passages_pass_or_have_r1():
    m = json.load(open(MAN)); props = {p["replaces"]: p for p in json.load(open(FILR1))["items"]}
    cache, bad = {}, []
    for r in m["items"]:
        if r["domain"] != "verbal_fil":
            continue
        f = r["source_file"]
        if f not in cache:
            d = json.load(open(f)); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        it = cache[f][r["id"]]
        if qa.passage_errors(it) and not (it["status"] == "approved" and r["id"] in props):
            bad.append(r["id"])
        if r["id"] in props:
            assert it["status"] == "approved" and props[r["id"]]["id"] not in {x["id"] for x in m["items"]}
    assert not bad, bad


def test_fil_r1_proposals_are_unapproved_and_keep_keys():
    m = json.load(open(MAN)); cache = {}
    for p in json.load(open(FILR1))["items"]:
        assert p["status"] == "draft" and p["reviewer"] is None and p["id"] == p["replaces"] + "-R1"
        assert qa.check_item(p) == [] and qa.fil_passage_level(qa.passage_words(p)) == "short"
        r = next(x for x in m["items"] if x["id"] == p["replaces"]); f = r["source_file"]
        if f not in cache:
            d = json.load(open(f)); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        o = cache[f][p["replaces"]]
        assert o["options"] == p["options"] and o["answer_option_id"] == p["answer_option_id"]
        assert o["stem"].rpartition("\n\n")[2] == p["stem"].rpartition("\n\n")[2]


def test_num_template_replacements_are_separate_verified_drafts():
    import solver_2026_10_22 as S
    m = json.load(open(MAN)); man = {r["id"]: r for r in m["items"]}
    d = json.load(open("docs/research/audit/fixes/num-template-replacements-2026-10-22.json"))["items"]
    assert d and len({x["proposed_replacement_for"] for x in d}) == len(d)
    for it in d:
        assert it["status"] == "draft" and it["reviewer"] is None and it["id"] not in man
        assert man[it["proposed_replacement_for"]]["status"] == "approved" and man[it["kept_original"]]["status"] == "approved"
        assert qa.check_item(it) == [], (it["id"], qa.check_item(it))
        if it.get("recipe"):
            assert S.solve(it) == next(o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"])


def test_adversarial_read_recorded_and_repairs_applied():
    ev = json.load(open("docs/research/review/queue-evidence-2026-10-22.json"))
    ar = [e for e in ev if "adversarial_read" in e]
    judg = [e for e in ar if e["key_check"].startswith("none")]
    assert len(judg) == 139 and len(ar) - len(judg) == 23, (len(judg), len(ar))
    assert all(e["adversarial_read"]["needs_human_read"] == "yes" for e in ar)
    d = {i["id"]: i for f in ("docs/research/batches/drafts/analytical-professional-2026-10-22.json",
                              "docs/research/batches/drafts/verbal-en-organization-reading-2026-10-22.json") for i in json.load(open(f))["items"]}
    assert "general : army" not in [o["text"] for o in d["CIVIO-D1022-ANA-0038"]["options"]]
    assert "These fees" in d["CIVIO-D1022-VEN-INS-0012"]["stem"] and "On the last Saturday" in d["CIVIO-D1022-VEN-INS-0015"]["stem"]
    assert "Those children" not in d["CIVIO-D1022-VEN-INS-0008"]["stem"]


def test_non_approved_rows_may_not_claim_approval():
    base = {"status": "draft", "notes": "New original draft, 22 Oct 2026. Design approach approved by GT; item not yet reviewed."}
    assert qa.approval_claim_errors(base) == []
    assert qa.approval_claim_errors(dict(base, notes="New original draft, 22 Oct 2026 (GT approved)."))
    assert qa.approval_claim_errors(dict(base, notes="Approved by CoS."))
    assert qa.approval_claim_errors(dict(base, approved_by="GT"))
    assert qa.approval_claim_errors(dict(base, review_status="passed"))
    assert qa.approval_claim_errors(dict(base, revisions=[{"approved_by": "GT", "change": "edit"}])) == []
    assert qa.approval_claim_errors({"status": "approved", "notes": "GT approved", "approved_by": "GT"}) == []
    assert qa.approval_claim_errors({"status": "reviewed", "review_status": "passed"}) == []


def test_no_manifest_row_claims_unearned_approval():
    m = json.load(open(MAN)); cache, bad = {}, []
    for r in m["items"]:
        f = r["source_file"]
        if f not in cache:
            d = json.load(open(f)); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        if qa.approval_claim_errors(cache[f][r["id"]]):
            bad.append(r["id"])
    assert not bad, (len(bad), bad[:5])


def test_approval_packets_cover_queue_by_evidence_type_risk_first():
    import csv, glob, re
    rows = {r["id"] for r in csv.DictReader(open("docs/research/review/queue-recommendations-2026-10-22.csv"))}
    seen, maxes = [], []
    files = sorted(glob.glob("docs/research/review/approval-packets-2026-10-22/A*.md"))
    for f in files:
        t = open(f).read()
        head, items, answers = t.split("## Items (no keys)")[0], t.split("## Items (no keys)")[1].split("## Answer sheet")[0], t.split("## Answer sheet")[1]
        assert "## One-page summary" in head and "You must check" in head and "does NOT show" in head
        assert re.search(r"(solver-verified|law-text-verified|human-judgment-needed)", f)
        ids = re.findall(r"^### \d+\. (\S+)", items, re.M)
        assert len(ids) <= 40 and all(i in answers for i in ids)
        assert "Answer:" not in items
        seen += ids
        maxes.append(int(re.search(r"Highest item risk score (\d+)", head).group(1)))
    assert sorted(seen) == sorted(rows) and maxes == sorted(maxes, reverse=True)

if __name__ == "__main__":
    fails = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_"):
            try:
                f(); print("ok  ", k)
            except AssertionError as e:
                fails += 1; print("FAIL", k, str(e)[:300])
    sys.exit(1 if fails else 0)

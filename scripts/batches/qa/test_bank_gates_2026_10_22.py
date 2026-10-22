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


def test_count_is_2100():
    m = json.load(open(MAN))
    assert len(m["items"]) == 2100 and len({r["id"] for r in m["items"]}) == 2100


if __name__ == "__main__":
    fails = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_"):
            try:
                f(); print("ok  ", k)
            except AssertionError as e:
                fails += 1; print("FAIL", k, str(e)[:300])
    sys.exit(1 if fails else 0)

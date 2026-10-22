"""Read Git objects without checking out, importing or approving question content.

python scripts/batches/audit/inventory.py --lock docs/research/bank/source-lock-2026-10-20.json --out /path/inventory.json
Fetch the lock's commit SHAs from origin first if unavailable. Stdout is a compact summary.
Identity conflicts remain explicit; file order and JSON approval labels never settle them.
"""
import argparse
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

REVIEW_FIELDS = {"status", "review_status", "reviewer", "reviewed_at", "approved_by", "approved_at"}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def normalize(text):
    return " ".join(text.casefold().split())


def inspect_item(item, path):
    raw_id = item.get("fix_of") or item.get("id")
    legacy = not isinstance(raw_id, str) or "baseline_id" in item
    identity = (f"snapshot:{path}:{raw_id}" if legacy else raw_id) if raw_id is not None else "unmapped:" + digest(item)[:20]
    options = item.get("options", [])
    texts = [o.get("text") if isinstance(o, dict) else o for o in options] if isinstance(options, list) else []
    flags = []
    if not texts or any(not isinstance(t, str) or not t.strip() for t in texts):
        flags.append("invalid-options")
    elif len(set(map(normalize, texts))) != len(texts):
        flags.append("duplicate-options")
    if "answer_option_id" in item:
        ids = [o.get("option_id") for o in options if isinstance(o, dict)]
        if ids.count(item["answer_option_id"]) != 1 or len(set(ids)) != len(ids):
            flags.append("invalid-option-identity-or-key")
    elif type(item.get("correct_option")) is not int or not 0 <= item["correct_option"] < len(texts):
        flags.append("invalid-answer-index")
    explanation = item.get("explanation") or (item.get("reveal") or {}).get("why_correct", "")
    if any(token in str(explanation).casefold() for token in ["local practice item", "do not follow the same steps", "to be quoted", "tbd"]):
        flags.append("placeholder-or-generic-explanation")
    if legacy or raw_id is None:
        flags.append("identity-mapping-required")
    content = {k: v for k, v in item.items() if k not in REVIEW_FIELDS}
    return {
        "identity": identity, "declared_id": item.get("id"), "fix_of": item.get("fix_of"),
        "legacy_snapshot_id": item.get("baseline_id", raw_id if legacy else None),
        "item_sha256": digest(item), "content_sha256": digest(content),
        "stem_sha256": digest(normalize(item["stem"])),
        "declared_status": item.get("status"), "declared_review_status": item.get("review_status"),
        "declared_reviewer": item.get("reviewer"), "flags": flags,
        "domain": item.get("domain", item.get("cat")),
        "fact_id": item.get("fact_id"), "theme": item.get("theme"), "passage_id": item.get("passage_id"),
    }


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def inventory(root, lock):
    files, occurrences = [], []
    for source in lock["sources"]:
        ref = source["commit"]
        if source["scope"] == "all-bank-artifacts":
            names = git(root, "ls-tree", "-r", "--name-only", ref, "--", "docs/batches", "docs/research", "scripts/seeds/baseline_reparameterized.json")
        else:
            names = git(root, "diff", "--name-only", "--diff-filter=ACM", source["base"], ref, "--", "docs/research", "scripts/batches")
        for path in sorted(names.decode().splitlines()):
            if Path(path).suffix not in {".json", ".csv", ".md", ".py"}:
                continue
            raw = git(root, "show", f"{ref}:{path}")
            artifact = {"source": source["name"], "commit": ref, "path": path, "sha256": hashlib.sha256(raw).hexdigest()}
            files.append(artifact)
            if not path.endswith(".json"):
                continue
            value = json.loads(raw)
            rows = value.get("items") if isinstance(value, dict) else value
            if not isinstance(rows, list):
                continue
            items = [i for i in rows if isinstance(i, dict) and isinstance(i.get("stem"), str)]
            artifact["item_occurrences"] = len(items)
            artifact["declared_statuses"] = dict(Counter(str(i.get("status", "unspecified")) for i in items))
            for ordinal, item in enumerate(items, 1):
                occurrences.append({**inspect_item(item, path), "source": source["name"], "commit": ref, "path": path, "ordinal": ordinal})
    groups = defaultdict(list)
    for occurrence in occurrences:
        groups[occurrence["identity"]].append(occurrence)
    conflicts = [{"identity": identity, "content_variants": len({i["content_sha256"] for i in rows}),
                  "locations": [{k: i[k] for k in ["source", "path", "ordinal", "content_sha256", "declared_status", "declared_review_status"]} for i in rows]}
                 for identity, rows in sorted(groups.items()) if len({i["content_sha256"] for i in rows}) > 1]
    summary = {"artifact_count": len(files), "item_occurrences": len(occurrences),
               "identity_groups": len(groups), "conflicting_identity_groups": len(conflicts),
               "flag_occurrences": dict(Counter(flag for i in occurrences for flag in i["flags"])),
               "runtime_count": "NOT VERIFIED", "independently_approved_release_count": "NOT ESTABLISHED"}
    return {"schema": 1, "scope": "Pinned file occurrences, including historical snapshots and unmerged proposals; never a live bank count.",
            "summary": summary, "sources": lock["sources"], "artifacts": files, "conflicts": conflicts, "occurrences": occurrences}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = inventory(args.root, json.loads(args.lock.read_text(encoding="utf-8")))
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()

"""Baseline bank stems found in the repo (the bank itself is not stored as data; these are its seed scripts).

Sources: scripts/*.sql and scripts/seeds/*.sql (INSERT ... stem / UPDATE ... stem=), scripts/seeds/*.php ($bank arrays),
scripts/_existing_stems.txt (a 60-character prefix list exported from the old desktop bank).
"""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SQLSTR = r"'((?:[^']|'')*)'"


def stems():
    out = []  # (source, stem, is_prefix)
    for p in glob.glob(os.path.join(ROOT, "scripts", "*.sql")) + glob.glob(os.path.join(ROOT, "scripts", "seeds", "*.sql")):
        t = open(p, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"INSERT INTO questions[^;]*?(?:VALUES \(|SELECT )\s*\d+,\s*'(?:English|Filipino)',\s*" + SQLSTR, t):
            out.append((os.path.relpath(p, ROOT), m.group(1).replace("''", "'"), False))
        for m in re.finditer(r"UPDATE questions SET[^;]*?stem=" + SQLSTR, t):
            out.append((os.path.relpath(p, ROOT), m.group(1).replace("''", "'"), False))
    for p in glob.glob(os.path.join(ROOT, "scripts", "seeds", "*.php")):
        t = open(p, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"\[\s*'((?:[^'\\]|\\.)*)'\s*,\s*\[", t):
            out.append((os.path.relpath(p, ROOT), m.group(1).replace("\\'", "'"), False))
    p = os.path.join(ROOT, "scripts", "_existing_stems.txt")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8", errors="replace"):
            if line.strip():
                out.append(("scripts/_existing_stems.txt", line.strip(), True))
    return out


def norm(s):
    s = s.lower().replace("−", "-").replace("×", "x").replace("÷", "/")
    s = re.sub(r"[^a-z0-9₱%/ +\-x]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    st = stems()
    from collections import Counter
    print(len(st), Counter(s for s, _, _ in st))

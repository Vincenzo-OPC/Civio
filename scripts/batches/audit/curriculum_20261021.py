"""Read-only curriculum audit. No imports, approvals, or database access.

Run from repository root:
python scripts/batches/audit/curriculum_20261021.py --out /tmp/civio-curriculum

Independent arithmetic uses exact fractions and a restricted AST, not generator
answer tables or qa.py solvers. A key match is NOT editorial/release approval.
The baseline equations are reviewer derivations from the dated export, not keys.
"""
import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAIN = "dbdf2bc04fe8d7edde4c8b7cf1e87be01138abe1"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def digest(item):
    return hashlib.sha256(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def expression(s):
    s = s.replace("×", "*").replace("÷", "/").replace("−", "-")
    def walk(n):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            return F(str(n.value))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            return -walk(n.operand) if isinstance(n.op, ast.USub) else walk(n.operand)
        if isinstance(n, ast.BinOp):
            a, b = walk(n.left), walk(n.right)
            if isinstance(n.op, ast.Add): return a + b
            if isinstance(n.op, ast.Sub): return a - b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Div): return a / b
            if isinstance(n.op, ast.Pow) and b.denominator == 1 and 0 <= b <= 10: return a ** int(b)
        raise ValueError("Unsupported expression")
    return walk(ast.parse(s.strip(), mode="eval").body)


def number(s):
    s = re.sub(r"[₱,]", "", s).strip()
    mixed = re.fullmatch(r"(-?\d+) (\d+)/(\d+)", s)
    if mixed:
        a, b, c = map(int, mixed.groups())
        return F(a) + F(b, c)
    # Unit labels are retained in the report; this parser compares magnitudes.
    s = re.sub(r"\s*(?:pesos|thousand pesos|liters|L|km/h|km|kg|m|hours|years|minutes|%)$", "", s).strip()
    try: return F(s)
    except (ValueError, ZeroDivisionError): return None


BASE_EQUATIONS = {
    41:"15+27",42:"96/8",43:"7*9",44:"100-37",45:"12+3",46:"40*2",47:"17+9",
    48:"13*4",49:"800*5",50:"500*90/100",173:"18*450/100",174:"3/4+2/3",175:"125*0.8",176:"2**5",177:"38*100",178:"6*4",179:"18",180:"125/1000",181:"(260-200)/200*100",182:"15-3*4+6",183:"3/(3+5)",184:"2.5*800/100",
    185:"6**2",186:"40*2",187:"5+8",188:"3/3",189:"30+12",190:"56*2",191:"31*2+1",192:"70-20",193:"6**2",194:"12+5",195:"8/2",196:"29",
    197:"180/3",198:"100/(5*2)",199:"1200*85/100",200:"60/(1-3/4)",201:"(50+8)/2",202:"750*12",203:"15*8",204:"35*2/5",205:"5000*6/100*2",206:"2*(12+5)",207:"36/8",208:"(100-40)/2",209:"900*3/(2+3+4)",210:"180/12",
    262:"7/8*64",263:"14",264:"3.5*60",265:"180/1.2",266:"20+5",267:"24*5",268:"7**2",269:"90/3/15*10",270:"3214",271:"10/4",272:"(2*10+3*20)/5",
    339:"48/6+7*2",340:"15/100*240",341:"3/5*250",342:"2.75+1.6",343:"800*0.9",344:"32*2",345:"26+11",346:"3/3",347:"34*2-2",348:"5**2",349:"18*4",350:"600*1.08",351:"180/3*5",352:"45*(1-2/3)",353:"125/5",
    485:"84/7+6*3",486:"18/100*250",487:"7/8*64",488:"6.4-2.75",489:"1500*0.88",490:"33*2-1",491:"20+10",492:"12/2",493:"24*2",494:"160/4/2",495:"2400*0.85",496:"210/3.5*2",497:"72/(3/5)",498:"18*(1-2/3)-4",540:"7*8-15",541:"55-25",542:"240/6*9"
}
BASE_NOTES = {
    177:"3847 is 47 from 3800 and 53 from 3900.",178:"Multiples 6,12,18,24 and 8,16,24 first meet at 24.",
    179:"36=2*18 and 54=3*18; gcd(2,3)=1.",196:"29 is the next prime after 23; 24 through 28 are composite.",
    263:"14*14=196; square root means the nonnegative root.",
    270:"Tax component is 30000*12/112=3214.2857..., rounded to the nearest peso. This verifies stipulated arithmetic, not tax-law scope."
}


def solve(item):
    s, a = item["stem"], item.get("archetype", "")
    if isinstance(item.get("id"), int) and item.get("cat") == "Numerical Ability":
        eq = BASE_EQUATIONS[item["id"]]
        return expression(eq), BASE_NOTES.get(item["id"], eq)
    if item.get("domain") != "numerical": return None, None
    if a == "NUM-OPS-ORDER":
        m = re.search(r"value of (.+?)\?", s)
        if m: return expression(m[1]), m[1]
    if a in ("NUM-SEQ-DIFF", "NUM-SEQ-MULT"):
        seq = re.search(r"(-?\d+(?:,\s*-?\d+){3,})", s)
        if seq:
            xs = list(map(F, seq[1].replace(" ", "").split(",")))
            ds = [y-x for x,y in zip(xs,xs[1:])]
            dds = [y-x for x,y in zip(ds,ds[1:])]
            if len(set(dds)) == 1: return xs[-1]+ds[-1]+dds[0], f"constant second difference {dds[0]}; next={xs[-1]}+{ds[-1]}+{dds[0]}"
            if ds[0] != 0:
                m = ds[1]/ds[0]; c=xs[1]-m*xs[0]
                if all(y==m*x+c for x,y in zip(xs,xs[1:])):
                    return m*xs[-1]+c, f"recurrence next={m}*previous+{c}, checked on every transition"
    money = re.findall(r"₱([\d,]+)", s)
    p = F(money[0].replace(",", "")) if money else None
    if "raised the price by" in s:
        u,d=map(F,re.findall(r"(\d+)%",s)); return p*(1+u/100)*(1-d/100),f"{p}*(1+{u}/100)*(1-{d}/100)"
    if "simple interest" in s:
        rate=F(re.search(r"(\d+)%",s)[1]); years=F(re.search(r"after (\d+) year",s)[1]); month=re.search(r"and (\d+) months",s)
        t=years+(F(int(month[1]),12) if month else 0)
        return p*rate/100*t,f"principal {p} * annual rate {rate}/100 * years {t}"
    if "% off" in s:
        d=F(re.search(r"(\d+)%",s)[1]);return p*(1-d/100),f"{p}*(100-{d})/100"
    if "in the ratio" in s and a == "NUM-WP-RATIO":
        r1,r2=map(F,re.search(r"ratio (\d+) : (\d+)",s).groups());return p*r2/(r1+r2),f"{p}*{r2}/({r1}+{r2}); asks second named share"
    if "can" in s and "together" in s.lower() and a == "NUM-WP-RATE":
        hours=list(map(F,re.findall(r"in (\d+) hours",s)))
        if len(hours)==2:
            x,y=hours;t=1/(1/x+1/y)
            assert t/x+t/y==1
            return t,f"1/(1/{x}+1/{y}); substitution verifies t/{x}+t/{y}=1 job"
    if "One more person" in s:
        n,avg,new=map(F,re.search(r"the (\d+) .*? is (\d+) years\. One more person, with (\d+)",s).groups())
        ans=(n*avg+new)/(n+1);assert ans==avg+(new-avg)/(n+1)
        return ans,f"({n}*{avg}+{new})/({n}+1); excess-over-old-mean cross-check"
    if item.get("id")=="CIVIO-NUM-WP-AVERAGE-000012":return F(5*32+44,6),"(5*32+44)/6=34; excess 12/6 raises 32 by 2"
    if "times as old" in s:
        mult=F(re.search(r"is (\d+) times",s)[1]); years=F(re.search(r"In (\d+) years",s)[1]); later=2 if "twice" in s else 3
        child=years*(later-1)/(mult-later);adult=mult*child
        assert adult+years==later*(child+years)
        return adult,f"child={years}*({later}-1)/({mult}-{later})={child}; older={adult}; substitution checked"
    if a=="NUM-WP-GEOM" and "cost" in s:
        l,w=map(F,re.findall(r"(\d+) m",s));return 2*(l+w)*p,f"({l}+{w}+{l}+{w})*{p}"
    if a=="NUM-FRAC-DEC" and "remaining" in s:
        n=F(re.search(r"had (\d+)",s)[1]);f,g=map(F,re.findall(r"\d+/\d+",s));return n*(1-f)*(1-g),f"{n}*(1-{f})*(1-{g}); second fraction uses remainder"
    special={
        "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0006":"3/4+5/6", "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0007":"2.5*0.04",
        "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0008":"7.2/0.08", "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0009":"5/8",
        "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0010":"500*(1-2/5-1/4)", "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0011":"(1+2/3)*3/5"}
    if item.get("id") in special:
        eq=special[item["id"]];return expression(eq),eq+(" > 0.6 = 3/5 > 0.58" if item["id"].endswith("0009") else "")
    return None,None


def load_items():
    out=[]
    names=git("ls-tree","-r","--name-only",MAIN,"--","docs/batches","docs/research").splitlines()
    for p in names:
        if not p.endswith(".json"):continue
        if not (p.startswith("docs/batches/batch-") or p.count("/")==2):continue
        if p.endswith(("round-02-fixes.json","shortcuts-num-001.json")):continue
        d=json.loads(git("show",f"{MAIN}:{p}"));rows=d.get("items",[]) if isinstance(d,dict) else []
        out += [(p,x) for x in rows if isinstance(x,dict) and "stem" in x]
    p="docs/research/audit/data/baseline-550-2026-10-17.json"
    out += [(p,x) for x in json.loads(git("show",f"{MAIN}:{p}"))]
    return out


def secondary_check(item):
    """Independent table arithmetic, explicit sorting and finite set logic."""
    stem = item["stem"]
    archetype = item.get("archetype")
    opts = [o["text"] for o in item["options"]]
    if archetype == "ANA-DI-TABLE":
        matches = re.findall(r"([A-Za-z ]+): ([A-Za-z]+) (\d+), ([A-Za-z]+) (\d+), ([A-Za-z]+) (\d+)", stem)
        table = {name.strip(): {m1:F(n1),m2:F(n2),m3:F(n3)} for name,m1,n1,m2,n2,m3,n3 in matches}
        total = re.search(r"How many did (.+?) use in all three months", stem)
        diff = re.search(r"In (\w+), how many more did (.+?) use than (.+?)\?", stem)
        if total:
            value = sum(table[total[1]].values())
            method = f"independent row sum: {table[total[1]]}"
        elif diff:
            month,first,second = diff.groups()
            value = table[first][month]-table[second][month]
            method = f"independent cell subtraction: {table[first][month]}-{table[second][month]}"
        else: return None, None
        return [n for n,t in enumerate(opts) if number(t)==value], method
    if archetype in ("CLR-NUMERIC", "CLR-CHRONOLOGICAL"):
        values = stem.split(": ")[-1].split(" | ")
        if archetype == "CLR-NUMERIC":
            ordered=sorted(values,key=int)
        else:
            from datetime import date
            ordered=sorted(values,key=date.fromisoformat)
        target=ordered[0] if "FIRST?" in stem else ordered[-1]
        return [n for n,t in enumerate(opts) if t==target], "explicit ascending order: " + " < ".join(ordered)
    if archetype == "ANA-SYLLOGISM" and item["id"] != "CIVIO-ANA-SYLLOGISM-000015":
        text=stem.split("Which")[0].split("What")[0]
        text=re.sub(r"Statement [12]: |Assume these are true: ", "", text)
        text=text.replace(", and ", ". ").strip(". ")
        def parse(text):
            text=text.strip(". ").lower()
            text=re.sub(r"^every one of the (.+?) is among the (.+)$", r"all \1 are \2",text)
            text=re.sub(r"^none of the (.+?) are (.+)$", r"no \1 are \2",text)
            text=re.sub(r"^a few of the (.+?) are (.+)$", r"some \1 are \2",text)
            text=re.sub(r"^all of the ", "all ",text)
            m=re.fullmatch(r"(all|some|no) (.+?) are (.+)",text)
            if not m:return None
            quant,a,b=m.groups()
            if quant=="some" and b.startswith("not "):return "some-not",a,b[4:]
            return quant,a,b
        premises=[parse(t) for t in text.split(". ")]
        options=[parse(t) for t in opts]
        if len(premises)!=2 or any(x is None for x in premises+options): return None,None
        terms=sorted({t for x in premises+options for t in x[1:]})
        if len(terms)>4:return None,None
        regions=2**len(terms)
        def true(claim,world):
            quant,a,b=claim; ai=terms.index(a);bi=terms.index(b)
            inside=[region for region in range(regions) if world>>region&1 and region>>ai&1]
            if quant=="all":return all(region>>bi&1 for region in inside)
            if quant=="no":return all(not(region>>bi&1) for region in inside)
            if quant=="some-not":return any(not(region>>bi&1) for region in inside)
            return any(region>>bi&1 for region in inside)
        worlds=[w for w in range(2**regions) if all(true(p,w) for p in premises)]
        assert worlds
        valid=[n for n,o in enumerate(options) if all(true(o,w) for w in worlds)]
        return valid,f"Exhaustive {len(worlds)} satisfying occupancy models of {regions} Venn regions; universal statements have no existential import. Parsed premises: {premises}"
    return None,None


def audit_rows(items):
    records=[]
    for p,i in items:
        oid=i.get("answer_option_id")
        texts=[o["text"] if isinstance(o,dict) else o for o in i["options"]]
        key_index=next((j for j,o in enumerate(i["options"]) if isinstance(o,dict) and o["option_id"]==oid),None) if oid else i.get("correct_option")
        key=texts[key_index] if type(key_index)==int and 0<=key_index<len(texts) else None
        flags=[]
        if len(texts)!=4 or len(set(t.strip().casefold() for t in texts))!=4:flags.append("non-distinct-or-not-four-options")
        if key is None:flags.append("missing-key")
        exp=i.get("explanation") or (i.get("reveal")or{}).get("why_correct","")
        if not exp or "Local practice item" in exp or "do not follow the same steps" in exp:flags.append("placeholder-or-generic-explanation")
        if any(" von " in " "+t+" " or t.strip()=="sixty-four" for t in texts):flags.append("option-text-artifact")
        if re.search(r"\bA (?:office|electric|umbrella|edging)\b",i["stem"]):flags.append("indefinite-article-grammar")
        if "lace border" in i["stem"] and "rectangular" in i["stem"]:flags.append("implausible-fencing-context")
        if "times as old as" in i["stem"] and re.search(r"\b(?:son|daughter)\b",i["stem"]):
            _,reason=solve(i)
            if reason:
                child=F(re.search(r"child=.*?=([^;]+);",reason)[1]);older=F(re.search(r"older=([^;]+);",reason)[1])
                if older-child<12:flags.append("parent-child-age-gap-under-12")
        value,method=solve(i)
        outcome="NOT_INDEPENDENTLY_CHECKED"
        if isinstance(item_id := i.get("id"), str):
            valid, secondary_method = secondary_check(i)
            if valid is not None:
                outcome="KEY_MATCH" if valid==[key_index] else "KEY_OR_OPTIONS_DEFECT"
                method=secondary_method
                if outcome!="KEY_MATCH":flags.append("logic-table-sorting-key-defect")
        if value is not None:
            equivalent=[j for j,t in enumerate(texts) if number(t)==value]
            outcome="KEY_MATCH" if equivalent==[key_index] else "KEY_OR_OPTIONS_DEFECT"
            if outcome!="KEY_MATCH":flags.append("numeric-key-or-equivalent-option-defect")
        records.append({"id":i["id"],"path":p,"commit":MAIN,"item_sha256":digest(i),"domain":i.get("domain",i.get("cat")),"archetype":i.get("archetype",i.get("sub")),"declared_status":i.get("status","historical-snapshot-no-status"),"declared_review_status":i.get("review_status"),"answer_check":outcome,"derived_answer":str(value) if value is not None else None,"method":method,"flags":flags,"release_approval":"NOT_ESTABLISHED_BY_THIS_AUDIT"})
    return records


def duplicate_screen(items):
    exact=defaultdict(list);frames=defaultdict(list);token_rows=[];whole=defaultdict(list)
    for p,i in items:
        identity=f"{p}#{i['id']}"
        normalized=" ".join(re.findall(r"\w+",i["stem"].casefold()))
        exact[normalized].append(identity)
        texts=sorted(" ".join(re.findall(r"\w+", (o["text"] if isinstance(o,dict) else o).casefold())) for o in i["options"])
        whole[(normalized,tuple(texts))].append(identity)
        frame=re.sub(r"\d+(?:\.\d+)?","#",normalized)
        frames[frame].append(identity)
        token_rows.append((identity,set(normalized.split()), i.get("notes",""),i["stem"]))
    near=[];siblings=0
    for n,(aid,a,an,astem) in enumerate(token_rows):
        for bid,b,bn,bstem in token_rows[n+1:]:
            if a==b:continue
            if min(len(a),len(b))/max(len(a),len(b),1)<0.65:continue
            score=len(a&b)/len(a|b)
            if score<0.65:continue
            # Exempt only same tagged passage AND identical passage body.
            pa=re.search(r"Passage ([\w-]+),",an);pb=re.search(r"Passage ([\w-]+),",bn)
            if pa and pb and pa[1]==pb[1] and astem.rsplit("\n\n",1)[0]==bstem.rsplit("\n\n",1)[0]:
                siblings+=1;continue
            near.append({"a":aid,"b":bid,"jaccard":round(score,4)})
    return {"method":"casefolded word tokens; exact punctuation-insensitive stems; Jaccard >=0.65 is a review flag, not a duplicate verdict; number-masked exact frames are candidate families, not automatically rejected clones",
            "exact_stem_and_options_groups":[v for v in whole.values() if len(v)>1],
            "exact_stem_groups":[v for v in exact.values() if len(v)>1],"number_masked_frame_groups":[v for v in frames.values() if len(v)>1],"near_pairs":near,"passage_sibling_pairs_exempted":siblings}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--out",type=Path,required=True);args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    items=load_items();rows=audit_rows(items);dupes=duplicate_screen(items)
    summary={"main_sha":MAIN,"main_primary_items":sum(isinstance(i['id'],str) for _,i in items),"baseline_snapshot_rows":sum(isinstance(i['id'],int) for _,i in items),"declared_approved_domains":dict(Counter(i['domain'] for _,i in items if i.get('status')=='approved')),"answer_checks":dict(Counter(r['answer_check'] for r in rows)),"flagged_records":sum(bool(r['flags']) for r in rows),"flags":dict(Counter(f for r in rows for f in r['flags'])),"exact_stem_and_options_groups":len(dupes["exact_stem_and_options_groups"]),"exact_stem_groups":len(dupes['exact_stem_groups']),"exact_stem_excess_records":sum(len(g)-1 for g in dupes['exact_stem_groups']),"near_pairs":len(dupes['near_pairs']),"number_masked_frame_groups":len(dupes['number_masked_frame_groups']),"full_editorial_release_certification":False}
    for name,data in [('audit',{'summary':summary,'records':rows}),('duplicate-screen',dupes)]:
        (args.out/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()

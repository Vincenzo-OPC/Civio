"""gap-fill-2000-02: Numerical basic operations (60) + number sequences (20) + Filipino reading (12) + Filipino paragraph order (16).
Shortfalls (release_manifest.py, 2026-10-18): basic ops 55, sequences 16, FIL reading 10, FIL paragraph order 14 -> filled with small buffers.
Numerical keys are integers and are recomputed by qa.py solvers (NUM-OPS-ORDER, NUM-SEQ-DIFF/MULT). No percent items. Drafts only.
Run: python3 scripts/batches/gapfill/gap_fill_2000_02.py -> docs/research/gap-fill-2000-02.json"""
import json, os, random
from collections import Counter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
import sys, glob; sys.path.insert(0, os.path.join(ROOT, "scripts", "batches"))
from common import jaccard
BANK = []
for _f in glob.glob(os.path.join(ROOT, "docs/batches/batch-*.json")) + glob.glob(os.path.join(ROOT, "docs/research/*.json")):
    if _f.endswith("gap-fill-2000-02.json"): continue
    try: _d = json.load(open(_f, encoding="utf-8"))
    except Exception: continue
    _it = _d.get("items") if isinstance(_d, dict) else _d
    BANK += [i["stem"] for i in (_it or []) if isinstance(i, dict) and i.get("domain") == "numerical" and "stem" in i]
def fresh(stem): return all(jaccard(stem, b) < 0.6 for b in BANK)
rng = random.Random(200002)
def f(n): return str(n)
# ---------- basic operations: template -> (expr, key, steps, [(value, code, why)]) ----------
def T1(a, b, c, d):
    k = a + b * c - d
    return (f"{a} + {b} × {c} − {d}", k, f"{b} × {c} = {b*c}; {a} + {b*c} = {a+b*c}; {a+b*c} − {d} = {k}",
            [((a + b) * c - d, "NUM-ORDER-OPS", f"works left to right: ({a} + {b}) × {c} − {d}. Multiplication comes before addition."),
             (a + b + c - d, "NUM-OP-SWAP", f"adds {b} and {c} instead of multiplying them."),
             (a + b * c, "NUM-PARTIAL", f"stops at {a} + {b*c} and forgets to subtract {d}.")])
def T2(a, b, c, d):
    if (a + b) * c % d or b * c % d: return None
    k = (a + b) * c // d
    return (f"({a} + {b}) × {c} ÷ {d}", k, f"{a} + {b} = {a+b}; {a+b} × {c} = {(a+b)*c}; {(a+b)*c} ÷ {d} = {k}",
            [(a + b * c // d, "NUM-ORDER-OPS", f"ignores the parentheses and computes {a} + {b} × {c} ÷ {d}."),
             ((a + b) * c, "NUM-PARTIAL", f"stops at ({a} + {b}) × {c} and forgets to divide by {d}."),
             ((a + b) * c - d, "NUM-OP-SWAP", f"subtracts {d} instead of dividing by {d}.")])
def T3(a, b, c, d):
    k = a * b - c * d
    return (f"{a} × {b} − {c} × {d}", k, f"{a} × {b} = {a*b}; {c} × {d} = {c*d}; {a*b} − {c*d} = {k}",
            [((a * b - c) * d, "NUM-ORDER-OPS", f"works left to right: ({a} × {b} − {c}) × {d}. Both products come first."),
             (a * b - c, "NUM-PARTIAL", f"subtracts only {c} and forgets to multiply it by {d}."),
             (a * b + c * d, "NUM-OP-SWAP", f"adds the two products instead of subtracting.")])
def T4(a, b, c, d):
    if a % b: return None
    k = a // b + c * d
    return (f"{a} ÷ {b} + {c} × {d}", k, f"{a} ÷ {b} = {a//b}; {c} × {d} = {c*d}; {a//b} + {c*d} = {k}",
            [((a // b + c) * d, "NUM-ORDER-OPS", f"works left to right: ({a//b} + {c}) × {d}. Multiplication comes before addition."),
             (a // b + c, "NUM-PARTIAL", f"adds {c} and forgets to multiply it by {d}."),
             (a // b + c + d, "NUM-OP-SWAP", f"adds {c} and {d} instead of multiplying them.")])
def T5(a, b, c, d):
    if a <= b: return None
    k = (a - b) * (c + d)
    return (f"({a} − {b}) × ({c} + {d})", k, f"{a} − {b} = {a-b}; {c} + {d} = {c+d}; {a-b} × {c+d} = {k}",
            [(a - b * c + d, "NUM-ORDER-OPS", f"drops the parentheses and computes {a} − {b} × {c} + {d}."),
             ((a - b) * c, "NUM-PARTIAL", f"multiplies {a-b} by {c} only and forgets to add {d} first."),
             ((a - b) + (c + d), "NUM-OP-SWAP", f"adds the two groups instead of multiplying them.")])
def T6(a, b, c, d):
    if b % c or (a - b) % c or a <= b: return None
    k = a - b // c + d
    return (f"{a} − {b} ÷ {c} + {d}", k, f"{b} ÷ {c} = {b//c}; {a} − {b//c} = {a-b//c}; {a-b//c} + {d} = {k}",
            [((a - b) // c + d, "NUM-ORDER-OPS", f"subtracts first: ({a} − {b}) ÷ {c} + {d}. Division comes before subtraction."),
             (a - b // c, "NUM-PARTIAL", f"stops at {a} − {b//c} and forgets to add {d}."),
             (a - b // c - d, "NUM-OP-SWAP", f"subtracts {d} instead of adding it.")])
def T7(a, b, c, d):
    if b <= c: return None
    k = a * (b - c) + d
    return (f"{a} × ({b} − {c}) + {d}", k, f"{b} − {c} = {b-c}; {a} × {b-c} = {a*(b-c)}; {a*(b-c)} + {d} = {k}",
            [(a * b - c + d, "NUM-ORDER-OPS", f"drops the parentheses and computes {a} × {b} − {c} + {d}."),
             (a * (b - c), "NUM-PARTIAL", f"stops at {a} × {b-c} and forgets to add {d}."),
             (a + (b - c) + d, "NUM-OP-SWAP", f"adds {a} instead of multiplying by {a}.")])
def T8(a, b, c, d):
    if c <= d or a * b % (c - d) or a * b % c: return None
    k = a * b // (c - d)
    return (f"{a} × {b} ÷ ({c} − {d})", k, f"{a} × {b} = {a*b}; {c} − {d} = {c-d}; {a*b} ÷ {c-d} = {k}",
            [(a * b // c - d, "NUM-ORDER-OPS", f"drops the parentheses and computes {a} × {b} ÷ {c} − {d}."),
             (a * b, "NUM-PARTIAL", f"stops at {a} × {b} and forgets to divide by {c-d}."),
             (a * b * (c - d), "NUM-OP-SWAP", f"multiplies by {c-d} instead of dividing.")])
TEMPL = [T1, T2, T3, T4, T5, T6, T7, T8]
LEAD = ["Find the value of {}?", "Give the value of {}?", "State the value of {}?", "Determine the value of {}?", "Calculate the value of {}?", "Work out the value of {}?"]
ops, seen = [], set()
for ti, T in enumerate(TEMPL):
    made = 0
    while made < (8 if ti < 4 else 7):
        a, b, c, d = rng.randint(11, 96), rng.randint(2, 19), rng.randint(2, 14), rng.randint(2, 17)
        if T in (T2, T8): a = rng.randint(2, 24)
        if T is T4: a = b * rng.randint(2, 12)
        if T is T6: c = rng.choice([2, 3, 4, 5]); b = c * rng.randint(2, 9); a = b + c * rng.randint(1, 9)
        r = T(a, b, c, d)
        if not r: continue
        ex, k, steps, ds = r
        vals = [k] + [v for v, _, _ in ds]
        if len(set(vals)) < 4 or k <= 0 or ex in seen: continue
        stem = rng.choice(LEAD).format(ex)
        if not fresh(stem): continue
        BANK.append(stem); seen.add(ex); made += 1
        ops.append(dict(archetype="NUM-OPS-ORDER", competency="Basic operations", concept="order of operations",
            micro_skill="apply MDAS and parentheses to whole numbers", difficulty="easy" if T in (T1, T3) else "medium", est_seconds=40,
            stem=stem, key=f(k), ds=[(f(v), c_, f"{v} {w}") for v, c_, w in ds],
            terms="\"Order of operations\": do what is in parentheses first, then × and ÷ from left to right, then + and − from left to right.",
            shortcut="Box the parentheses and every × or ÷ first. Replace each with its value, then add and subtract left to right.",
            why=f"Answer: {k}. {steps}."))
# ---------- sequences ----------
SLEAD = ["What number comes next in the series?", "Which number continues the pattern?", "What is the next number in the sequence?", "Which number should replace the blank?"]
seqs, seenq = [], set()
while len(seqs) < 20:
    if len(seqs) < 11:
        s0, d0, dd = rng.randint(2, 30), rng.randint(1, 9), rng.randint(1, 4)
        xs = [s0]; d = d0
        for _ in range(4): xs.append(xs[-1] + d); d += dd
        k = xs[-1] + d; last = xs[-1] - xs[-2]
        ds = [(xs[-1] + last, "NUM-PARTIAL", f"repeats the last jump (+{last}). The jumps grow by {dd} each time, so the next jump is +{d}."),
              (xs[-1] + d + dd, "NUM-OFF-BY-ONE", f"adds {d+dd}, skipping one step in the jumps (the next jump is +{d})."),
              (xs[-1] + d0, "NUM-SEQ-OTHER-RULE", f"adds the first jump (+{d0}) again, as if the jumps stayed the same.")]
        arch, rule = "NUM-SEQ-DIFF", f"the jumps are {', '.join(str(y-x) for x, y in zip(xs, xs[1:]))}, growing by {dd}; next jump +{d}: {xs[-1]} + {d} = {k}"
        terms = "The \"difference\" or jump is how much you add to get from one number to the next."
        sc = "Write the jumps under the numbers. If the jumps themselves change by the same amount, continue that change."
    else:
        m, c = rng.choice([2, 3]), rng.choice([-2, -1, 1, 2, 3])
        xs = [rng.randint(1, 6)]
        for _ in range(4): xs.append(xs[-1] * m + c)
        k = xs[-1] * m + c
        if k > 2000 or xs[0] * m + c <= xs[0]: continue
        sg = f"+ {c}" if c > 0 else f"− {-c}"
        ds = [(xs[-1] * m, "NUM-PARTIAL", f"multiplies by {m} but forgets to {'add' if c > 0 else 'subtract'} {abs(c)}."),
              (xs[-1] + (xs[-1] - xs[-2]), "NUM-SEQ-OTHER-RULE", f"repeats the last difference ({xs[-1]-xs[-2]}). The rule is × {m} then {sg}, not a fixed jump."),
              (xs[-1] * m + 2 * c, "NUM-EXTRA-STEP", f"applies the {sg} step twice.")]
        arch, rule = "NUM-SEQ-MULT", f"each term is the one before × {m} {sg}: {xs[-1]} × {m} = {xs[-1]*m}; {xs[-1]*m} {sg} = {k}"
        terms = "In a \"multiply-then-add\" series, each term comes from the one before by the same two steps."
        sc = f"Test × {m} on two neighbours and see what is left over; the leftover is the constant step."
    if len({k} | {v for v, _, _ in ds}) < 4 or min(v for v, _, _ in ds) <= 0 or tuple(xs) in seenq: continue
    if not fresh(f"{SLEAD[len(seqs) % 4]}  {', '.join(map(str, xs))}, ___"): continue
    seenq.add(tuple(xs))
    seqs.append(dict(archetype=arch, competency="Number sequence", concept="number series", micro_skill="find the rule and extend the series",
        difficulty="medium", est_seconds=45, stem=f"{SLEAD[len(seqs) % 4]}  {', '.join(map(str, xs))}, ___", key=f(k),
        ds=[(f(v), c_, f"{v} {w}") for v, c_, w in ds], terms=terms, shortcut=sc, why=f"Answer: {k}. Rule: {rule}."))
# ---------- Filipino reading (passage, question, key, opposite, not-in-text, too-narrow/extreme, code4, why) ----------
READ = [
("Inilunsad ng munisipyo ang online na pagkuha ng permit sa negosyo. Sa unang tatlong buwan, bumaba nang halos kalahati ang pila sa tanggapan, ngunit dumami ang tawag ng mga negosyanteng hindi marunong gumamit ng internet. Kaya nagbukas ang munisipyo ng maliit na mesang tutulong sa kanila.",
 "Ano ang pangunahing ipinahihiwatig ng talata?", "May pakinabang ang bagong sistema ngunit kailangan pa rin ng tulong ang ilan.", "Walang naitulong ang online na sistema sa pagbawas ng pila.", "Ipinasara na ng munisipyo ang tanggapan ng permit.", "Lahat ng negosyante ay ayaw gumamit ng internet.", "RC-EXTREME",
 "Bumaba ang pila (pakinabang) at may mesang tumutulong sa hindi marunong (kailangan ng tulong)."),
("Ayon sa ulat ng barangay, mas kaunti ang kaso ng dengue ngayong taon kaysa noong nakaraang taon. Iniuugnay ito ng health worker sa lingguhang paglilinis ng kanal, ngunit sinabi rin niyang mas kaunti ang ulan ngayong taon kaya hindi pa tiyak kung alin ang mas malaking dahilan.",
 "Alin ang pinakaangkop na konklusyon batay sa talata?", "Hindi pa matiyak kung ang paglilinis lamang ang nagpababa ng kaso.", "Napatunayang paglilinis ng kanal ang tanging dahilan ng pagbaba.", "Tumaas ang bilang ng kaso ng dengue ngayong taon.", "Dapat nang itigil ang lingguhang paglilinis ng kanal.", "RC-NOT-IN-TEXT",
 "Binanggit ang dalawang posibleng dahilan (paglilinis at kaunting ulan), kaya hindi pa tiyak."),
("Bago magtanim, sinusuri ng mga magsasaka sa Nueva Ecija ang lupa upang malaman kung anong pataba ang kailangan. Sa ganitong paraan, hindi sila gumagastos sa patabang hindi naman kailangan, at naiiwasan ang labis na kemikal na umaagos sa ilog.",
 "Ayon sa talata, ano ang dalawang pakinabang ng pagsusuri sa lupa?", "Nakatitipid sa gastos at nababawasan ang kemikal sa ilog.", "Dumarami ang patabang kailangang bilhin at gamitin.", "Tumataas ang presyo ng palay sa pamilihan.", "Nalalaman lamang kung kailan dapat magtanim.", "RC-TOO-NARROW",
 "Nakasaad ang pagtitipid (hindi gumagastos sa hindi kailangan) at ang pag-iwas sa kemikal sa ilog."),
("Maraming kabataan ang gumagamit ng cellphone bago matulog. Ayon sa isang pag-aaral, ang liwanag ng screen ay nakapagpapaantala ng antok. Iminumungkahi ng mga doktor na itabi ang cellphone isang oras bago matulog.",
 "Ano ang layunin ng talata?", "Magbigay ng payo upang mapabuti ang pagtulog.", "Hikayatin ang mas matagal na paggamit ng cellphone.", "Ipaliwanag kung paano gumagawa ng cellphone.", "Ipagbawal ang lahat ng gadyet sa kabataan.", "RC-EXTREME",
 "Inilahad ang problema (naaantala ang antok) at ang payo ng doktor (itabi ang cellphone)."),
("Tuwing tag-ulan, binabaha ang mababang bahagi ng bayan. Nagtayo ang pamahalaang lokal ng mas malaking daluyan ng tubig, at mula noon ay mas mabilis nang humuhupa ang baha. Gayunman, nagbabala ang inhinyero na mababara pa rin ito kung patuloy na itatapon ang basura sa kanal.",
 "Batay sa talata, ano ang kailangan upang manatiling epektibo ang daluyan?", "Hindi pagtatapon ng basura sa kanal.", "Pagtatayo ng mas maliit na daluyan.", "Paglipat ng buong bayan sa bundok.", "Paghihintay na matapos ang tag-ulan.", "RC-NOT-IN-TEXT",
 "Nagbabala ang inhinyero na mababara ang daluyan kung itatapon ang basura sa kanal."),
("Sa isang tanggapan, ipinatupad ang patakarang walang pulong na lalampas sa tatlumpung minuto. Napansin ng hepe na mas maayos nang naihahanda ng mga kawani ang kanilang ulat bago ang pulong, dahil alam nilang maikli lamang ang oras.",
 "Ano ang naging epekto ng patakaran ayon sa talata?", "Mas naghahanda ang mga kawani bago ang pulong.", "Humaba ang oras ng bawat pulong sa tanggapan.", "Inalis na ang lahat ng pulong sa tanggapan.", "Nagreklamo ang mga kawani sa bagong patakaran.", "RC-NOT-IN-TEXT",
 "Sinabi ng hepe na mas maayos nang naihahanda ng mga kawani ang ulat dahil maikli ang oras."),
("Ang bakawan ay nagsisilbing tahanan ng maraming isda at alimango. Pinoprotektahan din nito ang baybayin laban sa malalaking alon tuwing may bagyo. Dahil dito, ipinagbabawal sa maraming bayan ang pagputol ng bakawan.",
 "Bakit ipinagbabawal ang pagputol ng bakawan ayon sa talata?", "Dahil tirahan ito ng isda at panangga sa malalaking alon.", "Dahil wala itong silbi sa mga isda at alimango.", "Dahil mahal ang kahoy nito sa pamilihan.", "Dahil panangga lamang ito sa mainit na araw.", "RC-TOO-NARROW",
 "Dalawang dahilan ang nakasaad: tahanan ng isda at alimango, at proteksiyon laban sa alon."),
("Nagsimula si Aling Rosa ng maliit na tindahan ng kakanin sa harap ng bahay. Nang dumami ang suki, kumuha siya ng dalawang katulong at nagpatala sa munisipyo upang magkaroon ng permit. Ngayon, nagdadala na rin siya ng kakanin sa mga kalapit na paaralan.",
 "Ano ang pangunahing ideya ng talata?", "Unti-unting lumago ang negosyo ni Aling Rosa.", "Nalugi ang tindahan ni Aling Rosa.", "Nagturo si Aling Rosa sa paaralan.", "Kumuha lamang si Aling Rosa ng permit.", "RC-TOO-NARROW",
 "Mula sa maliit na tindahan, dumami ang suki, nagdagdag ng tauhan, at lumawak sa mga paaralan."),
("Sa silid-aklatan ng bayan, pinahihintulutan na ang paghiram ng aklat nang hanggang dalawang linggo. Dati, isang linggo lamang ito. Ayon sa tagapamahala, marami ang humiling nito dahil hindi nila natatapos ang makakapal na aklat sa loob ng pitong araw.",
 "Bakit pinahaba ang panahon ng paghiram?", "Hindi natatapos ng mambabasa ang makakapal na aklat sa isang linggo.", "Kakaunti ang nagbabasa kaya marami ang bakanteng aklat sa istante.", "Nadagdagan ang pondo kaya bumili ng mas maraming aklat.", "Lahat ng aklat sa silid-aklatan ay makakapal at mahirap basahin.", "RC-EXTREME",
 "Ayon sa tagapamahala, hindi natatapos ang makakapal na aklat sa loob ng pitong araw."),
("Hinihikayat ng paaralan ang mga magulang na dumalo sa pulong tuwing katapusan ng markahan. Dito ipinaliliwanag ng guro ang marka ng anak at ang mga paraan upang matulungan siya sa bahay. Ayon sa punong-guro, mas mabilis umunlad ang mga mag-aaral na ang magulang ay regular na dumadalo.",
 "Ano ang ipinahihiwatig ng punong-guro?", "Nakatutulong sa mag-aaral ang pakikilahok ng magulang.", "Walang epekto sa mag-aaral ang pagdalo ng magulang.", "Dapat nang alisin ang markahan sa paaralan.", "Tiyak na papasa ang lahat ng anak ng dumadalo.", "RC-EXTREME",
 "Mas mabilis umunlad ang mag-aaral na regular na dinadaluhan ng magulang ang pulong."),
("Nagpatupad ang lungsod ng bike lane sa pangunahing kalsada. Sa simula, maraming tsuper ang tumutol dahil kumitid ang daan. Pagkalipas ng isang taon, dumami ang nagbibisikleta papasok sa trabaho, at bahagyang bumaba ang trapiko sa umaga.",
 "Alin ang sinusuportahan ng talata?", "Nagkaroon ng positibong epekto ang bike lane makalipas ang isang taon.", "Lalong lumala ang trapiko sa umaga dahil sa bagong bike lane.", "Ipinagbawal na ang mga dyip at bus sa pangunahing kalsada.", "Tuluyang nawala ang trapiko sa buong lungsod pagkalipas ng isang taon.", "RC-EXTREME",
 "Dumami ang nagbibisikleta at bahagyang bumaba ang trapiko pagkalipas ng isang taon."),
("Ang kawani ng pamahalaan ay inaasahang sumagot sa mga liham ng publiko sa takdang panahon. Sa isang ahensiya, gumawa ang mga kawani ng talaan ng lahat ng liham na natatanggap upang walang makaligtaan at masubaybayan kung alin ang hindi pa nasasagot.",
 "Ano ang layunin ng talaang ginawa ng mga kawani?", "Masubaybayan ang mga liham upang walang hindi masagot.", "Itago ang mga liham upang hindi na sagutin.", "Ipadala ang mga liham sa ibang ahensiya.", "Bilangin lamang kung ilan ang liham bawat araw.", "RC-TOO-NARROW",
 "Ginawa ang talaan upang walang makaligtaan at masubaybayan ang hindi pa nasasagot."),
]
# ---------- Filipino paragraph order: topic, four sentences in logical order ----------
PO = [
("Pagkuha ng pasaporte", ["Nagpatala si Liza online para sa petsa ng appointment.", "Sa araw ng appointment, dinala niya ang kaniyang sertipiko ng kapanganakan at ID.", "Kinunan siya ng larawan at fingerprint sa tanggapan.", "Makalipas ang ilang linggo, natanggap niya ang pasaporte sa koreo."]),
("Pagtatanim ng gulay", ["Inihanda muna ni Mang Ben ang lupa sa bakuran.", "Pagkatapos, itinanim niya ang mga buto ng pechay nang may tamang pagitan.", "Dinidiligan niya ang mga ito tuwing umaga at hapon.", "Pagkaraan ng isang buwan, inani na niya ang unang pechay."]),
("Paghahain ng reklamo", ["Napansin ni Ana na mali ang singil sa kaniyang bill sa kuryente.", "Tinawagan niya ang kompanya at ipinaliwanag ang problema.", "Hiningan siya ng kopya ng bill upang masuri ang singil.", "Matapos ang pagsusuri, ibinalik sa kaniya ang sobrang bayad."]),
("Paglilinis ng estero", ["Nagpulong ang mga opisyal ng barangay tungkol sa baradong estero.", "Napagkasunduan nilang magdaos ng paglilinis sa Sabado.", "Sa araw na iyon, nagtulong-tulong ang mga residente sa paghakot ng basura.", "Mula noon, hindi na umaapaw ang tubig tuwing malakas ang ulan."]),
("Pag-aaplay sa trabaho", ["Nakita ni Carlo ang anunsiyo ng bakanteng posisyon sa munisipyo.", "Inihanda niya ang kaniyang resume at mga kinakailangang dokumento.", "Ipinatawag siya para sa panayam makalipas ang isang linggo.", "Sa wakas, natanggap siya bilang kawani ng tanggapan."]),
("Paghahanda sa bagyo", ["Inanunsiyo ng PAGASA na papalapit ang malakas na bagyo.", "Dahil dito, nag-imbak ang pamilya ng pagkain, tubig, at baterya.", "Nang lumakas ang hangin, lumikas sila sa evacuation center.", "Nang humupa ang bagyo, bumalik sila at inayos ang nasirang bubong."]),
("Pagbubukas ng account sa bangko", ["Nagpasiya si Joy na mag-ipon para sa kaniyang pag-aaral.", "Pumunta siya sa bangko dala ang dalawang valid ID.", "Pinunan niya ang form at idineposito ang unang halaga.", "Ibinigay sa kaniya ang passbook bilang patunay ng kaniyang account."]),
("Pag-aayos ng sirang gripo", ["Napansin ng tagapangalaga na tumutulo ang gripo sa palikuran.", "Isinara muna niya ang pangunahing balbula ng tubig.", "Pinalitan niya ang lumang goma sa loob ng gripo.", "Binuksan niyang muli ang balbula at tiniyak na wala nang tulo."]),
("Pagdaraos ng halalan sa samahan", ["Itinakda ng samahan ang petsa ng halalan ng mga opisyal.", "Nagsumite ng kandidatura ang mga nais tumakbo.", "Sa araw ng halalan, bumoto ang mga kasapi sa lihim na balota.", "Binilang ang mga boto at ipinahayag ang mga nanalo."]),
("Pagluluto ng sinigang", ["Pinakuluan muna ang tubig kasama ang sibuyas at kamatis.", "Nang kumulo, inilagay ang karne ng baboy at pinalambot.", "Idinagdag ang sampalok na pampaasim at ang mga gulay.", "Sa huli, tinimplahan ito ng patis bago ihain."]),
("Pagpaparehistro bilang botante", ["Inalam ni Pedro ang iskedyul ng pagpaparehistro sa COMELEC.", "Nagtungo siya sa tanggapan dala ang kaniyang ID.", "Pinunan niya ang form at kinunan ang kaniyang biometrics.", "Pagkaraan, kasama na ang kaniyang pangalan sa listahan ng botante."]),
("Pagsasaayos ng aklatan", ["Napansin ng guro na magulo ang mga aklat sa silid-aklatan.", "Kaya hinati niya ang mga aklat ayon sa paksa.", "Nilagyan niya ng etiketa ang bawat istante.", "Ngayon, mabilis nang nakikita ng mga mag-aaral ang aklat na hinahanap."]),
("Pagbabakuna ng bata", ["Nakatanggap ang ina ng paalala mula sa health center tungkol sa bakuna.", "Dinala niya ang anak sa health center sa itinakdang araw.", "Tinurukan ng nars ang bata at itinala ito sa kaniyang kard.", "Pinayuhan ang ina na bumalik pagkaraan ng isang buwan para sa susunod na dosis."]),
("Pagkukumpuni ng daan", ["Nagreklamo ang mga residente tungkol sa malalim na lubak sa kalsada.", "Sinuri ng inhinyero ng munisipyo ang lawak ng sira.", "Isinara ang isang linya ng daan habang inaayos ito.", "Binuksan muli ang kalsada nang matuyo ang bagong semento."]),
("Pagdalo sa seminar", ["Nakatanggap si Grace ng imbitasyon sa seminar tungkol sa kaligtasan sa trabaho.", "Nagpatala siya sa pamamagitan ng online na form.", "Sa araw ng seminar, nakinig siya at nagtala ng mahahalagang punto.", "Pagbalik sa opisina, ibinahagi niya sa mga kasama ang kaniyang natutuhan."]),
("Pag-uulat ng nawawalang bagay", ["Napansin ni Rico na nawawala ang kaniyang pitaka sa dyip.", "Agad siyang nagtungo sa himpilan ng pulisya.", "Itinala ng pulis ang kaniyang salaysay at mga detalye ng pitaka.", "Pagkaraan ng dalawang araw, tinawagan siya dahil may nakapagsauli nito."]),
]
items = []
def add(idn, arch, dom, lang, track, d, stem, key, ds, terms, sc, why):
    items.append(dict(_id=idn, archetype=arch, domain=dom, language=lang, track=track, d=d, stem=stem, key=key, ds=ds, terms=terms, sc=sc, why=why))
for n, o in enumerate(ops, 1):
    add(n, o["archetype"], "numerical", "en", "both", o, o["stem"], o["key"], o["ds"], o["terms"], o["shortcut"], o["why"])
for n, o in enumerate(seqs, 1):
    add(n, o["archetype"], "numerical", "en", "both", o, o["stem"], o["key"], o["ds"], o["terms"], o["shortcut"], o["why"])
for n, (p, q, k, opp, nit, oth, c4, ex) in enumerate(READ, 1):
    d = dict(competency="Reading comprehension", concept="comprehension", micro_skill="tukuyin ang ideyang sinusuportahan ng talata", difficulty="medium", est_seconds=65)
    w4 = {"RC-EXTREME": "masyadong sukdulan; hindi ganito kalakas ang sinasabi ng talata", "RC-TOO-NARROW": "isang bahagi lamang ng sagot; kulang kumpara sa sinasabi ng talata", "RC-NOT-IN-TEXT": "walang batayan sa talata; hindi ito sinabi o ipinahiwatig"}[c4]
    add(n, "VFIL-PAGBASA", "verbal_fil", "fil", "both", d, f"{['Basahin ang talata', 'Basahin at unawain', 'Suriin ang talata sa ibaba', 'Talata'][n % 4]}:\n{p}\n\n{q}", k,
        [(opp, "RC-OPPOSITE", f"\"{opp}\" — salungat sa nakasaad sa talata."), (nit, "RC-NOT-IN-TEXT", f"\"{nit}\" — hindi binanggit sa talata."), (oth, c4, f"\"{oth}\" — {w4}.")],
        "Ang tamang sagot ay tuwirang nakasaad o lohikal na suportado ng talata.", "Hanapin sa talata ang pangungusap na sumusuporta sa bawat pagpipilian; ang walang suporta ay mali.",
        f"Answer: \"{k}\" ang tamang sagot. {ex}")
L = "ABCD"
for n, (topic, ss) in enumerate(PO, 1):
    while True:
        perm = rng.sample(range(4), 4)            # perm[j] = logical index shown under label j
        if perm != [0, 1, 2, 3]: break
    lab = {perm[j]: L[j] for j in range(4)}       # logical index -> label
    def code(seq): return "-".join(lab[i] for i in seq)
    key = code([0, 1, 2, 3])
    d1, d2, d3 = code([3, 0, 1, 2]), code([0, 2, 1, 3]), code([0, 1, 3, 2])
    d = dict(competency="Paragraph organization", concept="ordering", micro_skill="ayusin ang mga pangungusap ayon sa panahon at sanhi-bunga", difficulty="medium", est_seconds=60)
    stem = f"{['Paksa', 'Pamagat', 'Sitwasyon', 'Tungkol sa'][n % 4]}: {topic}. Alin ang lohikal na pagkakasunod-sunod ng mga pangungusap?\n" + "\n".join(f"{L[j]}. {ss[perm[j]]}" for j in range(4))
    add(n, "VFIL-PAGSUSUNOD", "verbal_fil", "fil", "both", d, stem, key,
        [(d1, "PO-OPENER-MISPLACED", f"\"{d1}\" — inuna ang huling pangyayari ({lab[3]}); ang panimula ay {lab[0]}."),
         (d2, "LOG-ORDER-SWAP", f"\"{d2}\" — pinagpalit ang {lab[1]} at {lab[2]}; kailangang mauna ang {lab[1]}."),
         (d3, "PO-TRANSITION-IGNORED", f"\"{d3}\" — nauna ang {lab[3]} sa {lab[2]}, bagaman hudyat ng pagtatapos ang {lab[3]}.")],
        "Unahin ang panimulang pangyayari, saka ang mga hakbang ayon sa panahon, at huli ang kinalabasan.",
        f"Hanapin ang panimula ({lab[0]}) at ang kinalabasan ({lab[3]}); ayusin ang gitna ayon sa panahon.",
        f"Answer: \"{key}\" ang tamang sagot. Panimula ang {lab[0]}, sinundan ng {lab[1]} at {lab[2]}, at kinalabasan ang {lab[3]}.")
out = []
PFX = {"NUM-OPS-ORDER": "NUMOPS", "NUM-SEQ-DIFF": "SEQD", "NUM-SEQ-MULT": "SEQM", "VFIL-PAGBASA": "PAGBASA", "VFIL-PAGSUSUNOD": "PAGSUSUNOD"}
for n, it in enumerate(items):
    d = it["d"]; opts = [it["key"]] + [x[0] for x in it["ds"]]
    slot = n % 4; order = opts[1:]; order.insert(slot, opts[0])
    ids = ["o1", "o2", "o3", "o4"]; idx = {t: ids[i] for i, t in enumerate(order)}
    out.append(dict(id=f"CIVIO-GF2K02-{PFX[it['archetype']]}-{it['_id']:04d}", track=it["track"], domain=it["domain"], competency=d["competency"],
        concept=d["concept"], micro_skill=d["micro_skill"], archetype=it["archetype"], difficulty=d["difficulty"], est_seconds=d["est_seconds"],
        language=it["language"], stem=it["stem"], options=[{"option_id": ids[i], "text": t} for i, t in enumerate(order)], answer_option_id=idx[it["key"]],
        reveal={"terms": it["terms"], "shortcut": it["sc"], "why_correct": it["why"], "why_wrong": {idx[t]: w for t, _, w in it["ds"]}},
        distractor_reasoning={idx[t]: c for t, c, _ in it["ds"]}, source="Original, Civio", source_url=None, source_group="civio",
        status="draft", review_status="unreviewed",
        provenance={"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T02:45:00+08:00", "spec_version": "0.1.9"},
        notes="gap-fill-2000-02. Pending CoS."))
json.dump({"batch": "gap-fill-2000-02", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio",
           "notes": "Numerical basic operations + sequences (non-percent), Filipino reading + paragraph order, for the exact-2,000 Release Collection.", "items": out},
          open(os.path.join(ROOT, "docs/research/gap-fill-2000-02.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), Counter(i["archetype"] for i in out))

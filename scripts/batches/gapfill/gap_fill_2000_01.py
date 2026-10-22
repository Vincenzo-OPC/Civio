"""gap-fill-2000-01: original Filipino Verbal drafts for the 2,000 milestone (antonyms, synonyms, idioms).
Targets come from docs/research/audit/gap-2000-2026-10-18.md (FIL gap ~111: antonym ~40, synonym ~26+, idiom ~22).
Every target word/idiom is new to the bank (checked against all verbal_fil stems). KWF spelling. Drafts only.
Run: python3 scripts/batches/gapfill/gap_fill_2000_01.py  -> docs/research/gap-fill-2000-01.json"""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ANT = [  # WORD, sentence, key, synonym-trap, same-field, weaker
("MASAGANA", "MASAGANA ang ani ng palay ngayong taon dahil sa sapat na ulan.", "kakaunti", "marami", "mabigat", "katamtaman"),
("MAPAGKUMBABA", "Kahit nanalo sa halalan, nanatiling MAPAGKUMBABA ang punong-barangay.", "mapagmataas", "mababang-loob", "magalang", "mahiyain"),
("MASUNURIN", "MASUNURIN sa batas trapiko ang mga tsuper sa bayang iyon.", "suwail", "tumatalima", "maingat", "paminsan-minsang lumalabag"),
("MAPAGBIGAY", "MAPAGBIGAY ang negosyante sa mga pamilyang nasunugan.", "maramot", "matulungin", "mayaman", "minsang nagbibigay"),
("MATAPAT", "MATAPAT na iniulat ng kahera ang kulang sa kaha.", "mandaraya", "totoo", "masipag", "medyo naglilihim"),
("MABAGAL", "MABAGAL ang pila sa tanggapan dahil iisa ang bukas na bintana.", "mabilis", "makupad", "mahaba", "medyo bumibilis"),
("MAINGAY", "MAINGAY ang palengke tuwing umaga.", "tahimik", "magulo", "masikip", "bahagyang humina ang tunog"),
("MALAMIG", "MALAMIG ang pagtanggap ng konseho sa panukalang proyekto.", "mainit", "walang-gana", "mabagal", "bahagyang interesado"),
("MAKITID", "MAKITID ang daan papunta sa baryo kaya hindi makadaan ang trak.", "malapad", "masikip", "mahaba", "medyo lumuluwag"),
("MAPANGANIB", "MAPANGANIB ang pagtawid sa ilog kapag malakas ang agos.", "ligtas", "delikado", "malalim", "bahagyang nakababahala"),
("MASALITA", "MASALITA ang bagong kawani kaya madalas siyang mapagsabihan.", "walang-kibo", "madaldal", "masayahin", "paminsan-minsang nagsasalita"),
("MALINIS", "MALINIS ang talaan ng kawani: walang anumang reklamo laban sa kaniya.", "marumi", "walang-bahid", "kumpleto", "may kaunting mantsa"),
("MAHIRAP", "MAHIRAP ang pagsusulit sa matematika kahapon.", "madali", "mabigat", "mahaba", "medyo nakalilito"),
("SINAUNA", "SINAUNA ang mga kagamitang natagpuan sa kuweba.", "makabago", "makaluma", "mahalaga", "may kaunting bagong bahagi"),
("MALABO", "MALABO ang paliwanag ng tagapagsalita tungkol sa bagong patakaran.", "malinaw", "magulo", "mahaba", "bahagyang naiintindihan"),
("PAMBIHIRA", "PAMBIHIRA ang ganitong uri ng orkidyas sa kagubatan.", "karaniwan", "bihira", "maganda", "paminsan-minsang nakikita"),
("NAGPATULOY", "NAGPATULOY ang pulong kahit malakas ang ulan.", "nahinto", "nagtuloy-tuloy", "nagsimula", "bumagal"),
("TUMAAS", "TUMAAS ang presyo ng bigas noong nakaraang buwan.", "bumaba", "umakyat", "nagbago", "bahagyang nag-iba"),
("IPINAGBAWAL", "IPINAGBAWAL ng konseho ang paggamit ng plastik sa palengke.", "pinahintulutan", "hinadlangan", "ipinatupad", "nilimitahan"),
("PUMAYAG", "PUMAYAG ang mga magulang sa lakbay-aral ng mga mag-aaral.", "tumanggi", "sumang-ayon", "nagtanong", "nag-alinlangan"),
("DUMAMI", "DUMAMI ang turista sa isla nang buksan ang bagong pantalan.", "umunti", "lumago", "dumating", "nanatili"),
("NAGTAGUMPAY", "NAGTAGUMPAY ang kampanya ng barangay laban sa dengue.", "nabigo", "nanalo", "natapos", "bahagyang umusad"),
("MATAPANG", "MATAPANG na hinarap ng bumbero ang naglalagablab na apoy.", "duwag", "magiting", "malakas", "kinakabahan"),
("MASAYA", "MASAYA ang mga bata sa bagong palaruan.", "malungkot", "maligaya", "maingay", "medyo pagod"),
("MAKAPAL", "MAKAPAL ang alikabok sa lumang aparador.", "manipis", "siksik", "marumi", "bahagyang nabawasan"),
("MALAKAS", "MALAKAS ang hangin bago dumating ang bagyo.", "mahina", "marahas", "malamig", "medyo humihina"),
("KUMPLETO", "KUMPLETO ang mga dokumentong isinumite ng aplikante.", "kulang", "ganap", "nakalimbag", "halos buo"),
("MAPAYAT", "MAPAYAT ang asong napulot sa kalsada.", "mataba", "patpatin", "maliit", "bahagyang tumaba"),
("MATAMIS", "MATAMIS ang ngiti ng nagwagi sa paligsahan.", "mapait", "kaaya-aya", "maganda", "pilit"),
("MAHABA", "MAHABA ang pasensiya ng guro sa mga batang makukulit.", "maikli", "malawig", "matiyaga", "katamtaman"),
("MAPAGBANTAY", "MAPAGBANTAY ang guwardiya sa pasukan ng gusali.", "pabaya", "alisto", "matapang", "paminsan-minsang lumilingon"),
("MASIPAG", "MASIPAG ang magsasaka mula madaling-araw hanggang dapithapon.", "tamad", "masikap", "malakas", "pagod"),
("MAUNAWAIN", "MAUNAWAIN ang hepe sa mga kawaning may sakit.", "mainitin ang ulo", "mapagpasensiya", "mabait", "minsang naiinis"),
("MAGULO", "MAGULO ang mga papeles sa mesa ng kalihim.", "nakaayos", "kalat-kalat", "marami", "bahagyang inayos"),
("MAPALAD", "MAPALAD ang mga pamilyang nakaligtas sa baha.", "kapus-palad", "masuwerte", "masaya", "nag-aalala"),
("MAHAL", "MAHAL ang pamasahe sa eroplano tuwing Pasko.", "mura", "magastos", "malayo", "bahagyang tumaas"),
("SUMULONG", "SUMULONG ang proyekto matapos maaprubahan ang pondo.", "umatras", "umusad", "nagsimula", "huminto sandali"),
("BUKAS", "BUKAS ang tanggapan ng munisipyo hanggang alas-singko.", "sarado", "handang tumanggap", "abala", "bahagyang nakasara"),
("MAINIT", "MAINIT ang sabaw na inihain sa mga bisita.", "malamig", "umuusok", "masarap", "maligamgam"),
("MATALINO", "MATALINO ang mag-aaral na nanalo sa paligsahan sa agham.", "mangmang", "marunong", "masipag", "karaniwan"),
("MATANDA", "MATANDA na ang punong mangga sa plasa.", "bata", "luma", "malaki", "may edad"),
]
SYN = [  # WORD, sentence, key, antonym-trap, same-field, other-trait
("MATAIMTIM", "MATAIMTIM na nagdasal ang mga deboto sa simbahan.", "taos-puso", "pabaya", "malakas", "mabilis"),
("MASAKIM", "MASAKIM ang negosyanteng nagtago ng bigas para tumaas ang presyo.", "gahaman", "mapagbigay", "mayaman", "matalino"),
("HUMUPA", "HUMUPA ang baha kinaumagahan matapos ang malakas na ulan.", "bumaba", "tumaas", "lumamig", "luminaw"),
("NAGPUPUYOS", "NAGPUPUYOS sa galit ang may-ari ng nasirang sasakyan.", "nag-aalab", "mahinahon", "nalulungkot", "nagmamadali"),
("MAPAGKAKATIWALAAN", "MAPAGKAKATIWALAAN ang ingat-yaman ng samahan.", "maaasahan", "taksil", "mayaman", "masayahin"),
("DALISAY", "DALISAY ang tubig na umaagos mula sa bukal.", "malinis", "marumi", "malamig", "masagana"),
("MAKUPAD", "MAKUPAD kumilos ang bagong katulong sa kusina.", "mabagal", "maliksi", "mahina", "tahimik"),
("PALASAK", "PALASAK na ang ganitong biro sa mga talumpati.", "gasgas", "bago", "nakatatawa", "mahaba"),
("TIWALAG", "TIWALAG na sa samahan ang dating kasapi.", "hiwalay", "kasapi pa", "tahimik", "galit"),
("SAKUNA", "Naghanda ang barangay sa anumang SAKUNA ngayong tag-ulan.", "kalamidad", "biyaya", "bagyo", "pagsasanay"),
("SIMBUYO", "Sa SIMBUYO ng damdamin, agad siyang nagbitiw sa trabaho.", "bugso", "pagtitimpi", "lungkot", "plano"),
("KALINGA", "Lumaki ang bata sa KALINGA ng kaniyang lola.", "pag-aaruga", "pagpapabaya", "tahanan", "utos"),
("HINAING", "Pinakinggan ng alkalde ang HINAING ng mga tindero sa palengke.", "reklamo", "papuri", "pulong", "panukala"),
("LIPON", "Isang LIPON ng mga ibon ang lumipad sa ibabaw ng palayan.", "kawan", "iisa", "pugad", "awit"),
("DUKHA", "Tinulungan ng simbahan ang mga DUKHA sa pamayanan.", "mahirap", "mayaman", "maysakit", "matanda"),
("PITAGAN", "Nagsalita siya nang may PITAGAN sa harap ng hukom.", "paggalang", "kawalang-galang", "takot", "bilis"),
("MALUMANAY", "MALUMANAY na ipinaliwanag ng nars ang gamutan sa pasyente.", "mahinahon", "pabalang", "maikli", "malakas"),
("TUMALIMA", "TUMALIMA ang mga kawani sa bagong memorandum ng direktor.", "sumunod", "sumuway", "nagbasa", "nagreklamo"),
("SUKAB", "Itinuring na SUKAB ang kasamang nagbunyag ng lihim sa kalaban.", "taksil", "tapat", "duwag", "mayabang"),
("HIKAYAT", "Sa HIKAYAT ng guro, sumali si Ben sa paligsahan sa pagsulat.", "udyok", "pagpigil", "utos", "papuri"),
("MAPANGLAW", "MAPANGLAW ang kalye nang mawalan ng kuryente ang buong bayan.", "malungkot", "masigla", "madilim", "maingay"),
("PAGSUYO", "Sa matiyagang PAGSUYO, napapayag niya ang kapatid na umuwi.", "pakikiusap", "pamimilit", "regalo", "pagsisinungaling"),
("YAMOT", "YAMOT na yamot si Lito sa napakahabang pila.", "inis", "tuwa", "pagod", "gutom"),
("TIKOM", "TIKOM ang bibig ng saksi sa buong imbestigasyon.", "sarado", "bukas", "takot", "pagod"),
("MAPUSOK", "MAPUSOK ang kabataang agad nagpasiya nang hindi nag-iisip.", "padalos-dalos", "pinag-iisipan muna", "matapang", "masaya"),
("NAPAWI", "NAPAWI ang uhaw ng mga manggagawa sa malamig na tubig.", "nawala", "lumala", "napuno", "lumamig"),
("GUNITA", "Buhay pa sa GUNITA ng lola ang mga araw ng digmaan.", "alaala", "limot", "kuwento", "pangarap"),
("PAKAY", "Ano ang PAKAY mo sa pagpunta sa munisipyo ngayong umaga?", "layunin", "kawalan ng dahilan", "oras", "kasama"),
("TAGHOY", "Narinig sa buong baryo ang TAGHOY ng inang nawalan ng anak.", "pagtangis", "malakas na halakhak", "sigaw", "awit"),
("MAPAGMATYAG", "MAPAGMATYAG ang mga tanod tuwing gabi sa looban.", "alisto", "pabaya", "matapang", "masipag"),
("AMBAG", "Malaki ang AMBAG ng mga manggagawa sa ibang bansa sa ekonomiya.", "kontribusyon", "kabawasan", "buwanang sahod", "utang"),
("PANGAMBA", "May PANGAMBA ang mga residente sa paparating na bagyo.", "takot", "katiyakan", "galit", "pag-asa"),
("MAHUSAY", "MAHUSAY ang paglalahad ng tagapagsalita sa pulong.", "magaling", "palpak", "mahaba", "malakas"),
("MAALWAN", "MAALWAN ang buhay nila mula nang magkaroon ng sariling negosyo.", "maginhawa", "naghihikahos", "masaya", "abala"),
]
IDI = [  # IDIOM, sentence, key, literal, opposite, other/weaker, codes for (literal, opposite, other)
("HALIGI NG TAHANAN", "Si Mang Jose ang HALIGI NG TAHANAN mula nang magkasakit ang kaniyang asawa.", "pangunahing nagtataguyod ng pamilya", "matibay na poste ng bahay", "pinakabunsong anak sa pamilya", "kapitbahay na laging tumutulong"),
("ILAW NG TAHANAN", "Pinarangalan si Aling Rosa bilang ILAW NG TAHANAN ng taon sa kanilang bayan.", "ina ng pamilya", "bombilya sa salas", "panauhing dumadalaw", "pinakamatandang kapatid"),
("BUKAMBIBIG", "BUKAMBIBIG ni Lolo ang kaniyang kabataan sa probinsiya.", "palaging binabanggit", "laging nakabuka ang bibig", "bihirang pag-usapan", "minsang naikuwento"),
("MAHABA ANG BUNTOT", "MAHABA ANG BUNTOT ng batang laki sa layaw kaya ayaw sumunod sa utos.", "sanay sa layaw at mahirap utusan", "may buntot na mahaba", "masunurin at madaling utusan", "matangkad para sa edad niya"),
("ANAK-PAWIS", "Ipinaglaban ng unyon ang karapatan ng mga ANAK-PAWIS sa pabrika.", "mga manggagawang nagbabanat ng buto", "mga batang laging pinagpapawisan", "mga may-ari ng malalaking pabrika", "mga kawaning bagong pasok"),
("MAKATI ANG PAA", "MAKATI ANG PAA ni Carlo kaya bihira siyang nasa bahay tuwing Sabado.", "mahilig gumala", "may kati sa paa", "laging nasa bahay", "mahilig mag-ehersisyo"),
("MAY GATAS PA SA LABI", "Huwag mo munang ipagkatiwala ang proyekto sa kaniya; MAY GATAS PA SA LABI siya.", "bata pa at kulang sa karanasan", "may natirang gatas sa bibig", "bihasa at subok na sa trabaho", "mahilig uminom ng gatas"),
("PANTAY NA ANG PAA", "Nang dumating ang doktor, PANTAY NA ANG PAA ng matandang maysakit.", "patay na", "magkasinghaba ang mga paa", "magaling na at nakatayo", "malubha pa ang kalagayan"),
("ABOT-TANAW", "ABOT-TANAW na ng koponan ang kampeonato matapos ang ikalimang panalo.", "malapit nang makamit", "natatanaw mula sa malayo", "imposible nang makamit", "pinag-uusapan pa lamang"),
("MAITIM ANG BUTO", "Mag-ingat ka sa lalaking iyon; MAITIM ANG BUTO niya.", "masama ang ugali o balak", "kulay itim ang buto", "mabuti ang kalooban", "mahiyain sa ibang tao"),
("BUWAYA SA KATIHAN", "Ayaw ng mga tindero sa opisyal na BUWAYA SA KATIHAN na laging humihingi ng lagay.", "mapagsamantalang sakim", "buwayang nasa pampang", "matapat na lingkod-bayan", "mahigpit pero patas na tagasuri"),
("SANTONG-PASPASAN", "SANTONG-PASPASAN ang pagpipinta ng bakod kaya may mga bahaging hindi napinturahan.", "minadali at hindi pulido", "binasbasan ng pari", "maingat at masinsin", "ginawa nang sama-sama"),
("TULOG-MANOK", "TULOG-MANOK lang ang nanay habang binabantayan ang anak na may lagnat.", "mababaw ang tulog", "natutulog sa kulungan ng manok", "mahimbing ang tulog", "natutulog sa tanghali"),
("BUTO'T BALAT", "BUTO'T BALAT na ang aso nang matagpuan ng mga tagapagligtas.", "napakapayat", "kalansay na lamang", "malusog at mataba", "maliit ang pangangatawan"),
("LUMAKI ANG ULO", "LUMAKI ANG ULO ng bagong manedyer nang mapromote siya.", "yumabang", "namaga ang ulo", "naging mapagkumbaba", "naging mas masipag"),
("MAHABA ANG KAMAY", "Inilipat ang kahera nang mabistong MAHABA ANG KAMAY niya.", "mahilig magnakaw", "mahaba ang mga braso", "matapat sa pera", "mabilis magtrabaho"),
("BALAT-KAYO", "BALAT-KAYO lamang ang kabaitan ng manloloko sa matatanda.", "pagkukunwari", "damit na balat", "tunay na ugali", "panandaliang ugali"),
("ALOG NA ANG BABA", "ALOG NA ANG BABA ni Lolo Pedring pero masigla pa rin siyang magtanim.", "matanda na", "nanginginig ang baba", "bata pa", "maysakit"),
("NAMUTI ANG MATA", "NAMUTI ANG MATA ni Ana sa paghihintay sa dyip na hindi dumating.", "napakatagal naghintay", "nagkasakit sa mata", "agad na nakasakay", "bahagyang nainip"),
("PUSONG-BATO", "PUSONG-BATO ang may-ari na nagpaalis sa nangungupahang maysakit.", "walang awa", "may sakit sa puso", "maawain", "mahigpit sa kontrata"),
("TINIK SA LALAMUNAN", "Naging TINIK SA LALAMUNAN ng sindikato ang matapang na mamamahayag.", "hadlang sa balak", "tinik ng isda sa lalamunan", "katuwang sa balak", "bagong kasapi"),
("SALING-PUSA", "SALING-PUSA lang si Totoy sa laro kaya hindi binibilang ang puntos niya.", "hindi tunay na kasali", "pusang sumasali sa laro", "pinuno ng koponan", "pinakamagaling na manlalaro"),
("MAKAPAL ANG BULSA", "MAKAPAL ANG BULSA ni Don Andres kaya siya ang sumagot sa pista.", "mayaman", "makapal ang tela ng bulsa", "walang pera", "matipid sa gastos"),
("NAGBABANAT NG BUTO", "Araw-araw NAGBABANAT NG BUTO si Mang Ben sa konstruksiyon para sa pamilya.", "nagtatrabaho nang mabigat", "nag-iinat ng katawan", "nagpapahinga sa bahay", "nag-eehersisyo sa umaga"),
]
def mk(i, arch, concept, stem, key, ds, codes, why, wrongs, short):
    return dict(id=f"CIVIO-GF2K01-{arch}-{i:04d}", track="both", domain="verbal_fil", competency="Word meaning", concept=concept,
        micro_skill="piliin ang angkop na kahulugan ayon sa konteksto", archetype=arch, difficulty="medium", est_seconds=30 if arch != "VFIL-WIKAIN" else 35,
        language="fil", stem=stem, _opts=[key] + ds, _codes=codes, _why=why, _wrongs=wrongs, shortcut=short)
items = []
for n, (w, s, k, syn, fld, weak) in enumerate(ANT, 1):
    items.append(mk(n, "VFIL-KASALUNGAT", "antonyms", f"Alin ang kasalungat ng \"{w}\" sa pangungusap na \"{s}\"?", k, [syn, fld, weak],
        ["FIL-SYNONYM-TRAP", "FIL-SAME-FIELD", "FIL-INTENSITY"], f"\"{k}\" ang tamang sagot. Sa pangungusap, ang \"{w.lower()}\" ay kabaligtaran ng \"{k}\".",
        [f"\"{syn}\" — kasingkahulugan o kahawig ng {w.lower()}, hindi kasalungat", f"\"{fld}\" — kaugnay ng sitwasyon ngunit hindi kabaligtaran ng {w.lower()}", f"\"{weak}\" — bahagyang pagbabago lamang, hindi lubos na kabaligtaran"],
        f"Hanapin ang kabaligtaran ng {w.lower()}: {k}."))
for n, (w, s, k, ant, fld, oth) in enumerate(SYN, 1):
    items.append(mk(n, "VFIL-KASINGKAHULUGAN", "synonyms", f"Sa pangungusap na \"{s}\" ano ang pinakamalapit na kahulugan ng \"{w}\"?", k, [ant, fld, oth],
        ["FIL-ANTONYM-TRAP", "FIL-SAME-FIELD", "FIL-OTHER-TRAIT"], f"\"{k}\" ang tamang sagot. Sa konteksto, ang \"{w.lower()}\" ay nangangahulugang {k}.",
        [f"\"{ant}\" — kabaligtaran ng {w.lower()}", f"\"{fld}\" — kaugnay ng sitwasyon ngunit iba ang kahulugan", f"\"{oth}\" — ibang katangian, hindi kahulugan ng {w.lower()}"],
        f"Palitan ang {w.lower()} ng {k}; tugma pa rin ang pangungusap."))
for n, (w, s, k, lit, opp, oth) in enumerate(IDI, 1):
    items.append(mk(n, "VFIL-WIKAIN", "idioms", f"Basahin: \"{s}\" Ano ang ibig sabihin ng sawikaing \"{w}\" dito?", k, [lit, opp, oth],
        ["FIL-LITERAL", "FIL-ANTONYM-TRAP", "FIL-OTHER-TRAIT"], f"\"{k}\" ang tamang sagot. Matalinghaga ang \"{w.lower()}\"; sa pangungusap, ito ay {k}.",
        [f"\"{lit}\" — literal na pagbasa ng sawikain", f"\"{opp}\" — kabaligtaran ng tunay na kahulugan", f"\"{oth}\" — ibang katangian na hindi ipinahihiwatig ng sawikain"],
        f"Huwag basahin nang literal ang {w.lower()}: {k}."))
out = []
for n, it in enumerate(items):
    opts = it.pop("_opts"); codes = it.pop("_codes"); why = it.pop("_why"); wr = it.pop("_wrongs")
    slot = n % 4; order = opts[1:]; order.insert(slot, opts[0])
    ids = ["o1", "o2", "o3", "o4"]; idx = {t: ids[i] for i, t in enumerate(order)}
    it.update(options=[{"option_id": ids[i], "text": t} for i, t in enumerate(order)], answer_option_id=idx[opts[0]],
        reveal={"terms": {"VFIL-KASALUNGAT": "Ang kasalungat ay salitang may kabaligtarang kahulugan.", "VFIL-KASINGKAHULUGAN": "Ang kasingkahulugan ay salitang may katulad na kahulugan.", "VFIL-WIKAIN": "Ang sawikain ay may matalinghagang kahulugan, hindi literal."}[it["archetype"]],
                "shortcut": it["shortcut"], "why_correct": why, "why_wrong": {idx[d]: w for d, w in zip(opts[1:], wr)}},
        distractor_reasoning={idx[d]: c for d, c in zip(opts[1:], codes)}, source="Original, Civio", source_url=None, source_group="civio",
        status="draft", review_status="unreviewed",
        provenance={"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T03:30:00+08:00", "spec_version": "0.1.9"},
        notes="gap-fill-2000-01 (Filipino Verbal). Pending CoS.")
    out.append(it)
json.dump({"batch": "gap-fill-2000-01", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio",
           "notes": "Filipino Verbal gap fill for the 2,000 milestone: antonyms, synonyms, idioms. All targets new to the bank.", "items": out},
          open(os.path.join(ROOT, "docs/research/gap-fill-2000-01.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), Counter(i["archetype"] for i in out))

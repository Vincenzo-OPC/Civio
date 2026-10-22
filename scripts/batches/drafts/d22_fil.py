"""B1 subprofessional Filipino (50): kasingkahulugan 15, kasalungat 15, balarila 12, pagbasa 8 (4 passages x 2).
KWF spelling (kaniya, no 'nakaka-'); a vocabulary stem never contains any of its options."""
from d22_common import mk

T, D = "subprofessional", "verbal_fil"
ITEMS = []
AS, SY, SF, OT, IN, LI = "FIL-ANTONYM-TRAP", "FIL-SYNONYM-TRAP", "FIL-SAME-FIELD", "FIL-OTHER-TRAIT", "FIL-INTENSITY", "FIL-LITERAL"

SYN = [  # (TARGET, sentence with TARGET, key, [(wrong, code, why)], meaning note)
 ("MASIKAP", "Dahil MASIKAP si Aling Nena, natapos niya ang pagtatahi ng limampung uniporme bago ang pista.", "masipag",
  [("tamad", AS, "Ito ang kabaligtaran: ang tamad ay umiiwas sa gawain."), ("matalino", OT, "Ibang katangian ito; ang pangungusap ay tungkol sa sipag, hindi sa talino."), ("mabilis", SF, "Maaaring mabilis ang masikap, pero ang diin ay ang tiyaga sa trabaho.")],
  "Ang masikap ay matiyaga at hindi tumitigil sa paggawa hanggang matapos."),
 ("DALUBHASA", "Isang DALUBHASA sa batas-pandagat ang inanyayahan upang ipaliwanag ang bagong kasunduan sa pangingisda.", "eksperto",
  [("baguhan", AS, "Ang baguhan ay nagsisimula pa lamang; kabaligtaran ito ng dalubhasa."), ("tagapagsalita", SF, "Nagsalita nga siya, pero ang salita ay tumutukoy sa lalim ng kaalaman, hindi sa papel sa programa."), ("tanyag", OT, "Ang tanyag ay kilala ng marami; hindi ito nangangahulugang marunong.")],
  "Ang dalubhasa ay may malalim at espesyal na kaalaman sa isang larangan."),
 ("MARALITA", "Nagbigay ang simbahan ng libreng bigas sa mga pamilyang MARALITA sa tabing-ilog.", "mahirap",
  [("mayaman", AS, "Kabaligtaran ito ng maralita."), ("matipid", OT, "Ang matipid ay maingat gumastos; hindi ito tumutukoy sa kakulangan sa yaman."), ("maysakit", SF, "Maaaring tulungan din ang maysakit, pero ang maralita ay tungkol sa kabuhayan.")],
  "Ang maralita ay salat sa pera at kabuhayan."),
 ("MAPANLINLANG", "Binalaan ng pulisya ang mga mamimili laban sa isang MAPANLINLANG na tindero na nagbebenta ng pekeng gamot.", "mandaraya",
  [("tapat", AS, "Ang tapat ay hindi nanloloko, kabaligtaran ng mapanlinlang."), ("madaldal", OT, "Ang madaldal ay maraming sinasabi; hindi ito nangangahulugang nanloloko."), ("masungit", OT, "Ang masungit ay mainitin ang ulo, ibang ugali.")],
  "Ang mapanlinlang ay nanloloko o nandaraya sa kapwa."),
 ("NAGLAHO", "Nang sumikat ang araw, NAGLAHO ang makapal na hamog sa bukid.", "nawala",
  [("lumitaw", AS, "Kabaligtaran ito: lumitaw ang isang bagay na dati ay hindi makita."), ("lumabo", IN, "Ang lumabo ay humina lamang ang linaw; ang naglaho ay tuluyang nawala."), ("lumipat", LI, "Walang paglipat ng lugar; ang hamog ay tuluyang nawala.")],
  "Ang naglaho ay tuluyang nawala sa paningin."),
 ("SALAWAHAN", "Ayon sa kuwento, SALAWAHAN ang binata dahil iba-iba ang nililigawan niya bawat linggo.", "pabago-bago ang pasya",
  [("tapat sa pangako", AS, "Kabaligtaran ito; ang salawahan ay hindi nananatili sa isang pasya o tao."), ("maramdamin", OT, "Ang maramdamin ay madaling masaktan, ibang katangian."), ("mapusok", OT, "Ang mapusok ay padalos-dalos; hindi ito ang ibig sabihin ng salawahan.")],
  "Ang salawahan ay hindi matatag ang damdamin o pasya; pabago-bago."),
 ("KAWANGIS", "KAWANGIS ng kaniyang lola ang batang si Mira, lalo na sa hugis ng mata at ngiti.", "kamukha",
  [("kaiba", AS, "Kabaligtaran ito; ang kaiba ay hindi kahawig."), ("kasama", LI, "Ang kasama ay kasabay sa isang lugar, hindi kahawig."), ("kaapu-apuhan", SF, "Ugnayang pampamilya ito, hindi pagkakahawig.")],
  "Ang kawangis ay kahawig o kamukha."),
 ("TIGIB", "TIGIB ng luha ang mga mata ng ina nang makita niyang ligtas ang anak pagkatapos ng baha.", "puno",
  [("kulang", AS, "Kabaligtaran ito ng tigib."), ("tuyo", AS, "Ang tuyo ay walang luha; kabaligtaran ng sinasabi ng pangungusap."), ("pagod", SF, "Damdamin ito na maaaring kasabay ng pag-iyak, pero hindi kahulugan ng tigib.")],
  "Ang tigib ay lipos o punong-puno."),
 ("PINAGTIBAY", "PINAGTIBAY ng Sangguniang Bayan ang ordinansa laban sa paggamit ng plastik sa palengke.", "inaprubahan",
  [("ibinasura", AS, "Kabaligtaran ito; ang ibinasura ay tinanggihan."), ("pinag-aralan", SF, "Bahagi ng proseso ito, pero ang pinagtibay ay ang pag-apruba mismo."), ("ipinaskil", LI, "Ang ipinaskil ay idinikit para mabasa; hindi ito pag-apruba.")],
  "Ang pinagtibay ay inaprubahan o ginawang opisyal."),
 ("NAGSUMAMO", "NAGSUMAMO ang matanda sa guwardiya na papasukin siya upang makuha ang kaniyang pensiyon.", "nagmakaawa",
  [("nag-utos", AS, "Ang nag-utos ay may kapangyarihan; ang nagsumamo ay nakikiusap nang may pagpapakumbaba."), ("nagreklamo", OT, "Ang nagreklamo ay nagpahayag ng hinaing, hindi nakiusap."), ("nagpasalamat", SF, "Pagpapahayag din ito sa kapwa, pero iba ang layunin.")],
  "Ang nagsumamo ay buong-pusong nakiusap o nagmakaawa."),
 ("HINAGPIS", "Ramdam sa awit ang HINAGPIS ng mga naulila ng bagyo.", "matinding pighati",
  [("matinding tuwa", AS, "Kabaligtaran ito ng hinagpis."), ("kaunting lungkot", IN, "Lungkot nga, pero masyadong mahina; ang hinagpis ay matindi."), ("matinding galit", OT, "Ibang damdamin ang galit.")],
  "Ang hinagpis ay matinding dalamhati o pighati."),
 ("SUMIBOL", "Pagkaraan ng unang ulan, SUMIBOL ang mga bagong dahon sa mga punong itinanim ng mga mag-aaral.", "umusbong",
  [("nalanta", AS, "Kabaligtaran ito; ang nalanta ay natuyo at nanghina."), ("nalagas", AS, "Ang nalagas ay nahulog na mga dahon, kabaligtaran ng pagtubo."), ("lumago", IN, "Ang lumago ay paglaki ng dati nang tumubo; ang sumibol ay ang unang paglitaw.")],
  "Ang sumibol ay unang tumubo o umusbong."),
 ("MAPAGPANGGAP", "Hindi pinagkatiwalaan ng mga kasapi ang MAPAGPANGGAP na pinunong laging nagkukunwaring abala.", "mapagkunwari",
  [("totoo sa sarili", AS, "Kabaligtaran ito ng mapagpanggap."), ("mahiyain", OT, "Ang mahiyain ay umiiwas sa pansin; hindi siya nagkukunwari."), ("mayabang", OT, "Ang mayabang ay nagmamalaki; maaaring totoo ang ipinagmamalaki niya.")],
  "Ang mapagpanggap ay nagkukunwari o nagpapakita ng hindi totoo."),
 ("TALAMAK", "TALAMAK ang ilegal na pagtotroso sa bundok kaya nagpadala ng dagdag na bantay ang pamahalaan.", "laganap",
  [("bihira", AS, "Kabaligtaran ito; ang bihira ay madalang mangyari."), ("mapanganib", OT, "Maaaring mapanganib ang pagtotroso, pero ang talamak ay tungkol sa dalas at lawak."), ("lihim", SF, "Maaaring lihim ang gawain, pero hindi iyon ang kahulugan ng salita.")],
  "Ang talamak ay laganap at matagal nang nangyayari."),
 ("MALIGAMGAM", "Pinainom ng nars ang bata ng MALIGAMGAM na tubig na may kaunting asin.", "katamtamang init",
  [("nagyeyelo", AS, "Kabaligtaran ito; ang maligamgam ay may kaunting init."), ("kumukulo", IN, "Sobra ito; ang maligamgam ay hindi mainit na mainit."), ("malinis", OT, "Kalinisan ito ng tubig, hindi temperatura.")],
  "Ang maligamgam ay may katamtamang init, hindi malamig at hindi kumukulo."),
]

ANT = [
 ("MARAMOT", "MARAMOT ang may-ari ng tindahan; ni minsan ay hindi siya nagbigay ng tulong sa mga nasunugan.", "mapagbigay",
  [("kuripot", SY, "Kasingkahulugan ito ng maramot, hindi kasalungat."), ("mahirap", OT, "Kalagayan sa buhay ito, hindi ugali sa pagbibigay."), ("masungit", OT, "Ibang ugali ito; puwedeng masungit ang taong mapagbigay.")],
  "Ang maramot ay ayaw magbahagi; ang kasalungat ay mapagbigay."),
 ("MAHINA", "MAHINA ang signal ng telepono sa itaas ng bundok kaya hindi makatawag ang mga turista.", "malakas",
  [("marupok", SY, "Malapit sa kahulugan ng mahina, kaya hindi ito kasalungat."), ("mabagal", SF, "Bilis ito, hindi lakas."), ("malabo", SY, "Kahawig ito ng mahinang signal, hindi kasalungat.")],
  "Mahina ↔ malakas ang tuwirang magkasalungat."),
 ("PAGSANG-AYON", "Ipinahayag ng mga magsasaka ang kanilang PAGSANG-AYON sa planong patubig ng bayan.", "pagtutol",
  [("pagpayag", SY, "Kasingkahulugan ito, hindi kasalungat."), ("pag-aalinlangan", IN, "Ito ay pagdududa, hindi pa tahasang pagtutol."), ("pagtatanong", OT, "Ang pagtatanong ay paghingi ng impormasyon, hindi pagtanggi.")],
  "Ang kasalungat ng pagsang-ayon ay pagtutol."),
 ("KAKAPUSAN", "Dahil sa tagtuyot, nagkaroon ng KAKAPUSAN sa tubig sa tatlong barangay.", "kasaganaan",
  [("kakulangan", SY, "Kasingkahulugan ito ng kakapusan."), ("kahirapan", SF, "Kaugnay na kalagayan ito, hindi kabaligtaran."), ("katipiran", OT, "Paraan ito ng paggamit, hindi dami ng suplay.")],
  "Kakapusan (kulang) ↔ kasaganaan (sobra o sapat na sapat)."),
 ("MASUNGIT", "MASUNGIT ang bantay sa tarangkahan kaya nag-aatubiling magtanong ang mga bisita.", "magiliw",
  [("suplado", SY, "Kasingkahulugan ito ng masungit."), ("tahimik", OT, "Ang tahimik ay hindi maingay; maaari pa ring masungit."), ("mahiyain", OT, "Ang mahiyain ay umiiwas, hindi naman masungit o magiliw.")],
  "Ang masungit ay mainit ang ulo; ang magiliw ay malugod at palakaibigan."),
 ("MATAMLAY", "MATAMLAY ang mga mag-aaral sa huling klase dahil sa matinding init ng hapon.", "masigla",
  [("nanghihina", SY, "Kasingkahulugan ito ng matamlay."), ("malungkot", SF, "Damdamin ito; ang matamlay ay tungkol sa sigla ng katawan."), ("seryoso", OT, "Ibang katangian; puwedeng seryoso ang masigla.")],
  "Matamlay (walang sigla) ↔ masigla."),
 ("LIGTAS", "LIGTAS na ang mga residente matapos silang ilikas sa paaralan bago dumating ang bagyo.", "nanganganib",
  [("protektado", SY, "Kasingkahulugan ito ng ligtas."), ("sugatan", IN, "Maaaring kinalabasan ng panganib ito, pero hindi tuwirang kasalungat."), ("nawawala", OT, "Ibang kalagayan ang nawawala.")],
  "Ligtas ↔ nanganganib o nasa panganib."),
 ("MAKABAGO", "MAKABAGO ang disenyo ng bagong munisipyo, may solar panel at bukás na bulwagan.", "makaluma",
  [("moderno", SY, "Kasingkahulugan ito ng makabago."), ("mamahalin", OT, "Presyo ito, hindi panahon ng estilo."), ("malaki", OT, "Sukat ito, hindi estilo.")],
  "Makabago (moderno) ↔ makaluma."),
 ("PANSAMANTALA", "PANSAMANTALA lamang ang pagsasara ng tulay habang inaayos ang mga poste nito.", "permanente",
  [("panandalian", SY, "Kasingkahulugan ito ng pansamantala."), ("madalian", SF, "Bilis ng gawain ito, hindi haba ng panahon."), ("paminsan-minsan", OT, "Dalas ito, hindi haba ng bisa.")],
  "Pansamantala (sa maikling panahon) ↔ permanente."),
 ("MAPAGMATAAS", "Iniwasan ng mga katrabaho ang MAPAGMATAAS na kawaning laging nagmamalaki sa kaniyang posisyon.", "mapagpakumbaba",
  [("hambog", SY, "Kasingkahulugan ito ng mapagmataas."), ("masungit", OT, "Ibang ugali ito."), ("matapang", OT, "Ang matapang ay walang takot; hindi ito tungkol sa pagmamalaki.")],
  "Mapagmataas ↔ mapagpakumbaba."),
 ("MAGASTOS", "MAGASTOS ang paghahanda ng handaan kaya nagpasya ang pamilya na magpakain na lamang ng kaunting bisita.", "matipid",
  [("bulagsak", SY, "Kahawig ng magastos ang bulagsak, hindi kasalungat."), ("mayaman", OT, "Kalagayan ito, hindi paraan ng paggastos."), ("maramot", OT, "Ugali ito sa pagbibigay sa iba, hindi dami ng gastos.")],
  "Magastos ↔ matipid."),
 ("LUMUWAG", "LUMUWAG ang trapiko sa EDSA nang matapos ang pagkukumpuni ng kalsada.", "sumikip",
  [("gumaan", SY, "Kahawig ito ng lumuwag na trapiko."), ("bumagal", SF, "Kaugnay ito, pero ang kasalungat ng luwag ay sikip."), ("tumahimik", OT, "Ingay ito, hindi luwag ng daan.")],
  "Lumuwag ↔ sumikip."),
 ("BUMABA", "BUMABA ang presyo ng gulay sa palengke nang dumating ang ani mula sa lalawigan.", "tumaas",
  [("bumagsak", SY, "Kasingkahulugan ito ng bumaba."), ("tumatag", OT, "Ang tumatag ay hindi na nagbago, hindi kabaligtaran ng pagbaba."), ("nagbago", SF, "Masyadong pangkalahatan ito.")],
  "Bumaba ↔ tumaas."),
 ("MAINIPIN", "MAINIPIN si Jun kaya umalis siya sa pila bago pa siya natawag.", "matiyaga",
  [("atat", SY, "Kahawig ito ng mainipin."), ("masipag", OT, "Ibang katangian; ang tiyaga sa paghihintay ang kasalungat."), ("maagap", OT, "Ang maagap ay maaga, hindi kasalungat ng pagkainip.")],
  "Mainipin ↔ matiyaga o mapagtiis maghintay."),
 ("PINAYAGAN", "PINAYAGAN ng punong-guro ang mga mag-aaral na gamitin ang silid-aklatan tuwing Sabado.", "ipinagbawal",
  [("pinahintulutan", SY, "Kasingkahulugan ito ng pinayagan."), ("ipinagpaliban", OT, "Ang ipinagpaliban ay inilipat sa ibang araw, hindi tinanggihan."), ("iminungkahi", SF, "Ang iminungkahi ay inilapit bilang ideya pa lamang.")],
  "Pinayagan ↔ ipinagbawal."),
]


def vocab(i, row, kind):
    tgt, sent, key, wrong, note = row
    q = "ano ang pinakamalapit na kahulugan ng" if kind == "syn" else "ano ang kasalungat ng"
    arch = "VFIL-KASINGKAHULUGAN" if kind == "syn" else "VFIL-KASALUNGAT"
    stem = f"Sa pangungusap na \"{sent}\" {q} \"{tgt}\"?"
    return mk(id=f"CIVIO-D1022-SPFIL-{i:04d}", track=T, domain=D, competency="Talasalitaan", concept="kasingkahulugan" if kind == "syn" else "kasalungat",
              micro_skill="gamitin ang konteksto ng pangungusap", archetype=arch, difficulty="easy" if kind == "syn" else "medium",
              est=20 if kind == "syn" else 25, language="fil", stem=stem, correct=key, wrong=wrong,
              terms=f"{'Kasingkahulugan: salitang pareho ang ibig sabihin.' if kind == 'syn' else 'Kasalungat: salitang kabaligtaran ang ibig sabihin.'} {note}",
              shortcut="Palitan ang salitang nakasulat sa malalaking titik ng bawat sagot; ang tamang pamalit ay hindi dapat magpabago ng diwa ng pangungusap." if kind == "syn"
              else "Tanungin: alin ang magbabaligtad ng diwa ng pangungusap? Iwasan muna ang mga sagot na kapareho ng salita.",
              why_correct=f"Ang \"{key}\" ang {'tumutugma' if kind == 'syn' else 'kabaligtaran'} ng \"{tgt.lower()}\" sa pangungusap. {note} "
                          + ("Kapag ipinalit ito sa pangungusap, nananatili ang diwa." if kind == "syn" else "Kapag ipinalit ito sa pangungusap, bumabaligtad ang diwa."))


n = 0
for r in SYN:
    n += 1; ITEMS.append(vocab(n, r, "syn"))
for r in ANT:
    n += 1; ITEMS.append(vocab(n, r, "ant"))

BAL = [
 ("Piliin ang wastong salita: \"Tumakbo ____ mabilis ang atleta upang maabutan ang kalaban.\"", "nang",
  [("ng", "FIL-SPOKEN-FORM", "Ang \"ng\" ay pananda ng layon o pagmamay-ari; bago ang pang-abay na \"mabilis\" ay \"nang\" ang tama."), ("nag", "FIL-SPOKEN-FORM", "Unlapi ang \"nag-\"; hindi ito nakatayong salita."), ("nung", "FIL-SPOKEN-FORM", "Pabalbal na anyo ng \"noong\" ito at walang kinalaman sa paraan ng pagtakbo.")],
  "Ginagamit ang \"nang\" bilang pang-angkop sa pandiwa at pang-abay (paano ginawa).", "nang/ng"),
 ("Piliin ang wastong salita: \"Bumili ____ bagong sapatos si Liza para sa kaniyang unang araw sa trabaho.\"", "ng",
  [("nang", "FIL-SPOKEN-FORM", "Ang \"nang\" ay para sa paraan o panahon; ang sapatos ay layon ng pandiwa kaya \"ng\"."), ("na", "FIL-SPOKEN-FORM", "Pang-angkop ang \"na\"; hindi nito naipapakilala ang layon ng pandiwa."), ("sa", "FIL-SPOKEN-FORM", "Pang-ukol ng lugar o direksiyon ang \"sa\"; hindi lugar ang sapatos.")],
  "Ang \"ng\" ay nauuna sa pangngalang layon ng pandiwa (bumili ng ano?).", "nang/ng"),
 ("Alin ang wastong pangungusap tungkol sa mga bata sa bagong palaruan?", "Masaya rin ang mga bata sa bagong palaruan.",
  [("Masaya din ang mga bata sa bagong palaruan.", "FIL-SPOKEN-FORM", "Nagtatapos sa patinig ang \"masaya\", kaya \"rin\" ang dapat."), ("Masaya rin din ang mga bata sa bagong palaruan.", "FIL-SPOKEN-FORM", "Inuulit nang walang dahilan ang pananda."), ("Masaya ring ang mga bata sa bagong palaruan.", "FIL-SPOKEN-FORM", "Walang pang-angkop na kailangan dito; hindi tama ang \"ring\" bago ang \"ang\".")],
  "Rin/din: \"rin\" pagkatapos ng patinig o malapatinig (w, y); \"din\" pagkatapos ng katinig.", "rin/din"),
 ("Piliin ang wastong salita: \"Darating ____ ang inspektor mula sa probinsiya bukas ng umaga.\"", "daw",
  [("raw", "FIL-SPOKEN-FORM", "Nagtatapos sa katinig na \"g\" ang \"darating\", kaya \"daw\" ang tama."), ("ba", "FIL-SPOKEN-FORM", "Pananong ang \"ba\"; hindi ito pangungusap na patanong."), ("pa", "FIL-SPOKEN-FORM", "Nagbabago ang diwa: ang \"pa\" ay nagsasabing hindi pa ito nangyayari, hindi na may nagsabi lamang.")],
  "Daw/raw: \"raw\" pagkatapos ng patinig o w/y; \"daw\" pagkatapos ng katinig.", "daw/raw"),
 ("Piliin ang wastong salita: \"____ bagong patakaran ang tanggapan tungkol sa pagpasok ng mga bisita.\"", "May",
  [("Mayroon", "FIL-SPOKEN-FORM", "Kailangan ng \"mayroong\" (may -ng) kung susundan ng pang-uri; ang \"Mayroon bagong\" ay mali."), ("Meron", "FIL-SPOKEN-FORM", "Pabalbal na baybay ito ng \"mayroon\"."), ("Mayron", "FIL-SPOKEN-FORM", "Maling baybay ng \"mayroon\".")],
  "Ginagamit ang \"may\" kapag sinusundan ng pangngalan, pandiwa o pang-uri; \"mayroon\" kapag may panghalip o kataga sa pagitan.", "may/mayroon"),
 ("Piliin ang wastong salita: \"____ mo ang mga tuyong dahon at ilagay sa sako.\"", "Walisin",
  [("Walisan", "FIL-SPOKEN-FORM", "Ang \"walisan\" ay para sa lugar na nililinis (walisan ang bakuran); ang dahon ang tinatanggal kaya \"walisin\"."), ("Winalis", "VEN-TENSE", "Naganap na ito; utos ang pangungusap."), ("Magwalis", "FIL-SPOKEN-FORM", "Hindi tugma ang \"mo\" sa anyong \"magwalis\".")],
  "Hulaping -in: ang bagay na tinatanggal o ginagawan; hulaping -an: ang lugar na ginagawan.", "-in/-an"),
 ("Piliin ang wastong salita: \"Kailangang ____ si Lito sa susunod na linggo dahil sa apendisitis.\"", "operahan",
  [("operahin", "FIL-SPOKEN-FORM", "Ang \"operahin\" ay para sa bahaging aalisin o aayusin (operahin ang bukol); ang tao ay \"operahan\"."), ("inoperahan", "VEN-TENSE", "Naganap na ito; ang pangungusap ay tungkol sa susunod na linggo."), ("mag-opera", "FIL-SPOKEN-FORM", "Ang doktor ang nag-oopera; si Lito ang ooperahan.")],
  "Operahan ang tao (pinaggagawan); operahin ang bahagi ng katawan na inaayos.", "-in/-an"),
 ("Piliin ang wastong salita: \"Nakatayo ang guwardiya sa ____ ng bulwagan upang salubungin ang mga panauhin.\"", "pintuan",
  [("pinto", "FIL-SPOKEN-FORM", "Ang \"pinto\" ay ang mismong tabla na isinasara at binubuksan; ang daanan o lugar ay \"pintuan\"."), ("bintana", "FIL-SPOKEN-FORM", "Hindi daanan ng tao ang bintana."), ("pintuhan", "FIL-SPOKEN-FORM", "Maling anyo ito ng \"pintuan\".")],
  "Pinto: ang isinasara at binubuksan. Pintuan: ang daanan o puwang na kinalalagyan nito.", "pinto/pintuan"),
 ("Piliin ang wastong anyo ng pandiwa: \"Bukas ng hapon ____ ang pulong ng konseho sa bulwagan.\"", "gaganapin",
  [("ginanap", "VEN-TENSE", "Naganap na ito (perpektibo); \"bukas\" ang panahon kaya kontemplatibo."), ("ginaganap", "VEN-TENSE", "Kasalukuyang nagaganap ito (imperpektibo)."), ("ganapin", "FIL-SPOKEN-FORM", "Pawatas o utos ito, hindi aspekto ng pandiwa.")],
  "Aspekto ng pandiwa: perpektibo (naganap na), imperpektibo (nagaganap), kontemplatibo (gaganapin pa).", "aspekto"),
 ("Piliin ang wastong salita: \"Ayon ____ Kapitan Reyes, sarado ang kalsada hanggang Biyernes.\"", "kay",
  [("sa", "FIL-SPOKEN-FORM", "Ang \"ayon sa\" ay para sa karaniwang pangngalan (ayon sa ulat); sa pangalan ng tao ay \"ayon kay\"."), ("kina", "FIL-SPOKEN-FORM", "Pangmaramihan ang \"kina\"; iisa lamang ang kapitan."), ("ni", "FIL-SPOKEN-FORM", "Hindi ginagamit ang \"ni\" pagkatapos ng \"ayon\".")],
  "Ayon sa + karaniwang pangngalan; ayon kay + pangalan ng isang tao; ayon kina + pangalan ng dalawa o higit pa.", "kay/sa"),
 ("Piliin ang wastong salita: \"Ipinadala ng kalihim ang paanyaya ____ Ana at Ben.\"", "kina",
  [("nina", "FIL-SPOKEN-FORM", "Ang \"nina\" ay pananda ng gumagawa (ipinadala nina Ana); dito sila ang tatanggap kaya \"kina\"."), ("sina", "FIL-SPOKEN-FORM", "Pananda ng paksa ang \"sina\"; ang paanyaya ang paksa ng pangungusap."), ("kay", "FIL-SPOKEN-FORM", "Pang-isahan ang \"kay\"; dalawa ang tatanggap.")],
  "Kina: pinag-uukulan na dalawa o higit pa. Nina: gumagawa. Sina: paksa.", "kina/nina"),
 ("Alin ang wastong baybay ayon sa tuntunin ng gitling?", "mag-aaral",
  [("magaaral", "FIL-SPOKEN-FORM", "Kailangan ng gitling kapag ang unlaping nagtatapos sa katinig ay sinusundan ng salitang-ugat na nagsisimula sa patinig."), ("mag aaral", "FIL-SPOKEN-FORM", "Hindi hinihiwalay ng puwang ang unlapi sa salitang-ugat."), ("mag-araal", "FIL-SPOKEN-FORM", "Mali ang pag-uulit: ang inuulit ay ang unang pantig ng ugat (a), kaya mag-aaral.")],
  "Ginigitlingan ang unlaping nagtatapos sa katinig kapag sinusundan ng ugat na nagsisimula sa patinig (mag-aral, mag-aaral).", "gitling"),
]
for stem, key, wrong, rule_, concept in BAL:
    n += 1
    ITEMS.append(mk(id=f"CIVIO-D1022-SPFIL-{n:04d}", track=T, domain=D, competency="Balarila", concept=concept, micro_skill="pumili ng wastong gamit ayon sa tuntunin",
                    archetype="VFIL-BALARILA", difficulty="medium", est=30, language="fil", stem=stem, correct=key, wrong=wrong,
                    terms=rule_, shortcut="Tingnan ang salitang kasunod o nauuna: ito ang nagsasabi kung aling anyo ang tama.",
                    why_correct=f"Tama ang \"{key}\" dahil sa tuntuning ito: {rule_}"))

P = [
 ("SPFIL-P1", "Sa bayan ng San Isidro, sinimulan ng pamahalaang lokal ang programang \"Gulayan sa Bakuran\" noong tag-ulan. Binigyan ang bawat pamilyang kasali ng binhi ng pechay, talong at kamatis, pati ng maikling pagsasanay sa paggawa ng abono mula sa tirang pagkain. Sa unang tatlong buwan, mahigit dalawang daang bakuran ang natamnan. Napansin ng mga nanay na nakatipid sila sa pamamalengke, at may ilan pang nakapagbenta ng sobrang ani sa kapitbahay. Ayon sa agriculturist ng bayan, mas masigasig ang mga pamilyang may kasamang bata dahil ang mga bata ang nagpapaalala sa araw-araw na pagdidilig. Gayunman, hindi lahat ay nagtagumpay. Ang mga pamilyang nakatira sa masisikip na eskinita ay walang sapat na lupa o sikat ng araw. Para sa kanila, nagbukas ang barangay ng isang pampublikong taniman sa likod ng paaralan, kung saan maaari silang maghati-hati sa maliliit na tumpok ng lupa. Sa ngayon, pinag-aaralan ng munisipyo kung paano ito gagawing tuloy-tuloy kahit sa tag-araw, kapag kakaunti ang tubig.",
  [("Ano ang pangunahing paksa ng talata?", "Ang programang pantaniman ng bayan, ang mga bunga nito at ang mga hamong hinarap",
    [("Ang paggawa ng abono mula sa tirang pagkain", "RC-TOO-NARROW", "Bahagi lamang ng pagsasanay ang abono; hindi ito ang buong talata."),
     ("Ang kakulangan ng tubig sa buong lalawigan tuwing tag-araw", "RC-NOT-IN-TEXT", "Binanggit ang tubig sa dulo bilang alalahanin, hindi bilang paksa, at walang sinabing buong lalawigan."),
     ("Ang mataas na presyo ng gulay sa mga palengke", "RC-NOT-IN-TEXT", "Pagtitipid ang sinabi, hindi presyo sa palengke.")], "VFIL-PAGBASA", "pangunahing ideya"),
   ("Bakit nagbukas ang barangay ng pampublikong taniman sa likod ng paaralan?", "Para may mataniman ang mga pamilyang walang sapat na lupa o araw sa kanilang tirahan",
    [("Para may dagdag na kita ang paaralan", "RC-NOT-IN-TEXT", "Walang binanggit na kita ng paaralan."),
     ("Dahil nabigo ang lahat ng bakuran sa unang tatlong buwan", "RC-EXTREME", "Mahigit dalawang daang bakuran ang natamnan; hindi lahat nabigo."),
     ("Upang doon na lamang magtanim ang lahat ng pamilya", "RC-EXTREME", "Para lamang ito sa mga walang sapat na lupa, hindi sa lahat.")], "VFIL-PAGBASA", "hinuha")]),
 ("SPFIL-P2", "Tuwing Lunes, maaga pa lamang ay mahaba na ang pila sa tanggapan ng sibil na rehistro. Karamihan sa mga nakapila ay kumukuha ng kopya ng sertipiko ng kapanganakan para sa trabaho o pasaporte. Upang mabawasan ang paghihintay, naglagay ang tanggapan ng isang mesa ng paunang pagsusuri sa may pintuan. Doon, sinisiyasat ng isang kawani kung kumpleto ang mga dala ng aplikante bago pa siya pumila. Ang mga kulang ang papeles ay agad na sinasabihan kung ano ang kailangan, sa halip na malaman pa nila ito pagkatapos ng dalawang oras na paghihintay. Ayon sa tala ng tanggapan, bumaba sa kalahati ang karaniwang oras ng paghihintay pagkaraan ng isang buwan. May ilang aplikanteng nagreklamo noong una dahil inakala nilang dagdag na pila lamang ang mesa, ngunit nang makita nila ang bilis ng serbisyo, nawala ang kanilang reklamo. Balak ngayon ng tanggapan na ipaskil sa internet ang listahan ng mga kailangang dokumento, upang mas kaunti pa ang bumabalik dahil kulang ang dala.",
  [("Ano ang ginagawa sa mesa ng paunang pagsusuri?", "Tinitingnan kung kumpleto ang dalang dokumento bago pumila ang aplikante",
    [("Doon na mismo inilalabas ang sertipiko ng kapanganakan", "RC-NOT-IN-TEXT", "Pagsusuri lamang ng papeles ang ginagawa roon, hindi paglalabas ng sertipiko."),
     ("Doon tinatanggap ang bayad para sa pasaporte", "RC-NOT-IN-TEXT", "Walang binanggit na bayad sa pasaporte."),
     ("Doon itinatala ang mga reklamo ng aplikante", "RC-SUPPORTED-NOT-ASKED", "May reklamo noong una, pero hindi iyon ang tungkulin ng mesa.")], "VFIL-PAGBASA", "detalye"),
   ("Ano ang mahihinuha kung bakit nawala ang reklamo ng mga aplikante?", "Nakita nilang napabilis ng mesa ang kanilang pagkuha ng serbisyo",
    [("Inalis na ng tanggapan ang mesa ng paunang pagsusuri", "RC-OPPOSITE", "Walang sinabing inalis ang mesa; ang balak pa nga ay dagdagan ang tulong sa internet."),
     ("Pinagbawalan silang magreklamo ng mga kawani", "RC-NOT-IN-TEXT", "Walang ganitong sinabi ang talata."),
     ("Lumipat sila sa ibang tanggapan na walang pila", "RC-NOT-IN-TEXT", "Walang binanggit na ibang tanggapan.")], "VFIL-PAGBASA", "hinuha")]),
 ("SPFIL-P3", "Isa sa pinakamatandang tradisyon sa mga baybaying nayon ang bayanihan sa paglulunsad ng bangka. Kapag may bagong bangkang yari sa kahoy, nagtitipon ang mga kalalakihan upang buhatin ito mula sa pagawaan hanggang sa dalampasigan. Karaniwang ginagawa ito sa umaga, bago tumaas ang tubig, habang umaawit ang matatanda upang magsabay-sabay ang hakbang ng mga nagbubuhat. Ang mga kababaihan naman ay naghahanda ng nilagang saging at kape para sa lahat. Walang bayad ang tulong; ang inaasahan lamang ay ang pagbabalik ng pabor kapag ang ibang pamilya naman ang may ilulunsad. Sa paglipas ng panahon, napalitan ng fiberglass ang maraming bangka, at mas magaan na ang mga ito. Hindi na kailangan ang dalawampung katao para buhatin ang isang bangka. Gayunpaman, ipinagpapatuloy pa rin ng ilang nayon ang pagtitipon. Para sa matatanda, ang mahalaga ay hindi na ang bigat ng bangka kundi ang pagkakataong magkita-kita ang magkakapitbahay at ipakita sa kabataan kung paano nagtutulungan ang isang komunidad.",
  [("Ayon sa talata, bakit ipinagpapatuloy pa rin ang pagtitipon kahit magaan na ang mga bangka?", "Upang mapanatili ang samahan ng magkakapitbahay at maipasa ang pagtutulungan sa kabataan",
    [("Dahil mabigat pa rin ang mga bangkang fiberglass", "RC-OPPOSITE", "Sinabi ng talata na mas magaan na ang mga ito."),
     ("Upang kumita ang mga kalalakihan sa pagbubuhat", "RC-OPPOSITE", "Walang bayad ang tulong ayon sa talata."),
     ("Dahil iniuutos ito ng pamahalaang lokal", "RC-NOT-IN-TEXT", "Walang binanggit na utos ng pamahalaan.")], "VFIL-PAGBASA", "detalye"),
   ("Sa talata, ano ang ibig sabihin ng \"pagbabalik ng pabor\"?", "Pagtulong din sa pamilyang tumulong sa iyo kapag sila naman ang nangangailangan",
    [("Pagsasauli ng hiniram na bangka", "RC-NOT-IN-TEXT", "Walang hiniram na bangka sa talata; tulong ang ibinabalik."),
     ("Pagbabayad ng utang sa pagawaan", "RC-NOT-IN-TEXT", "Walang utang na binanggit."),
     ("Paghingi ng tawad sa matatanda", "RC-NOT-IN-TEXT", "Walang kinalaman ang paghingi ng tawad sa pagtutulungan.")], "VFIL-PAGBASA", "kahulugan sa konteksto")]),
 ("SPFIL-P4", "Noong nakaraang taon, nagpasya ang isang pampublikong mataas na paaralan sa Quezon na ipagbawal ang paggamit ng cellphone sa loob ng silid-aralan. Hindi kinumpiska ang mga telepono; sa halip, inilalagay ang mga ito sa isang kahon sa harap ng klase at ibinabalik tuwing oras ng pahinga at uwian. Sa simula, maraming mag-aaral ang tumutol dahil ginagamit daw nila ang telepono sa pananaliksik. Ilang guro rin ang nag-alinlangan dahil baka mahirapan silang bantayan ang kahon araw-araw. Kaya pinayagan ng paaralan ang paggamit nito sa mga takdang gawain na may pahintulot ng guro. Pagkaraan ng isang semestre, napansin ng mga guro na mas aktibo ang talakayan at mas kaunti ang nahuhuli sa pagsusumite ng takdang-aralin. Sinabi naman ng ilang magulang na mas madalas nang nakikipag-usap ang kanilang mga anak sa hapag-kainan. Hindi pa tiyak kung ang mga pagbabagong ito ay dahil lamang sa patakaran, ngunit balak ng paaralan na ituloy ito at pag-aralan nang mas maigi sa susunod na taon.",
  [("Ano ang ginawa ng paaralan matapos tumutol ang mga mag-aaral?", "Pinayagan ang paggamit ng telepono sa mga gawaing may pahintulot ng guro",
    [("Tuluyang kinumpiska ang lahat ng telepono", "RC-OPPOSITE", "Hindi kinumpiska ang mga telepono, ayon sa talata."),
     ("Inalis na ang buong patakaran", "RC-OPPOSITE", "Balak pa ngang ituloy ang patakaran."),
     ("Pinatawag ang mga magulang sa paaralan", "RC-NOT-IN-TEXT", "Walang binanggit na pagpapatawag sa magulang.")], "VFIL-PAGBASA", "detalye"),
   ("Ano ang pinakaangkop na hinuha tungkol sa mga resulta ng patakaran?", "Mukhang nakatulong ito, ngunit kailangan pang pag-aralan kung ito talaga ang sanhi",
    [("Napatunayang ang patakaran lamang ang dahilan ng lahat ng pagbabago", "RC-EXTREME", "Sinabi mismo ng talata na hindi pa tiyak kung dahil lamang sa patakaran."),
     ("Walang naging epekto ang patakaran", "RC-OPPOSITE", "May napansing pagbabago ang mga guro at magulang."),
     ("Lumala ang pagsusumite ng takdang-aralin", "RC-OPPOSITE", "Mas kaunti ang nahuhuli, ayon sa talata.")], "VFIL-PAGBASA", "hinuha")]),
]
for pid, passage, qs in P:
    for k, (q, key, wrong, arch, concept) in enumerate(qs, 1):
        n += 1
        stem = f"Basahin ang talata at sagutin ang tanong.\n\n{passage}\n\n{q}"
        ITEMS.append(mk(id=f"CIVIO-D1022-SPFIL-{n:04d}", track=T, domain=D, competency="Pag-unawa sa binasa", concept=concept,
                        micro_skill="unawain ang detalye at hinuha mula sa talata", archetype=arch, difficulty="medium", est=60, language="fil",
                        stem=stem, correct=key, wrong=wrong,
                        terms="Detalye: tahasang sinabi sa talata. Hinuha: makatwirang konklusyon mula sa sinabi, hindi hula.",
                        shortcut="Hanapin sa talata ang pangungusap na sumusuporta sa sagot bago pumili.",
                        why_correct=f"Ang tamang sagot ay \"{key}\" dahil ito ang tuwirang sinusuportahan ng talata, hindi lamang bahagi nito o labis na pahayag.",
                        passage_id=f"CIVIO-D1022-{pid}", notes=f"Passage CIVIO-D1022-{pid}, question {k} of {len(qs)}. New original draft, 22 Oct 2026. Design approach approved by GT; item not yet reviewed."))

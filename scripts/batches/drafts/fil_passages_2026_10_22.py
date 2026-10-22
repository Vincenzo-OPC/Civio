"""GT decision 15:48 (22 Oct 2026): Filipino reading passages come in two levels, SHORT (at least 80 words) and LONG (150-250).
Every Filipino passage in the flat-2100 manifest was under 80 words. This module lengthens each one to a SHORT passage by adding
neutral background sentences that keep the question, key and every wrong option exactly as valid as before (each addition was
read against all of its questions). Keyed by the first item id of each passage; siblings share the passage text."""

ADD = {
 "CIVIO-VFIL-PAGBASA-040076": "Bawat klase ay may sariling istante ng aklat na pinipili ng mga mag-aaral, at itinatala ng guro ang pamagat at bilang ng pahinang natapos ng bawat bata. Ayon sa punong-guro, kailangan pa ng isa o dalawang buwan ng tala bago masabi kung umunlad ang pag-unawa. Ihahambing nila ang mga sagot sa unang linggo at sa huling linggo ng markahan.",
 "CIVIO-VFIL-PAGBASA-040077": "Sa panahon ng pagsubok, umaalis ang trak bago pa sumikat ang araw, kaya mas maraming tindahan ang nakatanggap ng sariwang gatas bago magbukas at kakaunti ang ibinalik na maasim na. Gayunman, kinailangang magbayad ng dagdag na oras sa drayber at ng mas maraming krudo dahil dalawang beses nang bumibiyahe ang sasakyan.",
 "CIVIO-VFIL-PAGBASA-040078": "Kasama sa ulat ang bilang ng pamilyang nakatanggap ng bigas, de-lata at gamot, at ang kabuuang halagang ginastos. Nang may magtanong kung bakit kulang ang detalye sa listahan, sinabi ng kalihim na maaaring suriin ng awditor ang buong talaan, ngunit hindi ilalagay sa pisara ang personal na detalye ng bawat pamilya.",
 "CIVIO-VFIL-PAGBASA-040079": "Gumamit sila ng pintura at isinulat ang petsa sa tabi ng bawat marka upang makita ang pagbabago sa paglipas ng panahon. Itinala rin nila kung ilang oras bago humupa ang tubig. Bukod sa mga dokumento, inilipat din nila sa mas mataas na istante ang mga gamot at kagamitang de-kuryente.",
 "CIVIO-VFIL-PAGBASA-040080": "Kulay ang ginamit sa mga palatandaan: berde para sa laboratoryo, asul para sa parmasya at dilaw para sa konsultasyon, at may mapa ng gusali sa may pasukan. Ayon sa mga bantay, mas bihira na silang lapitan para itanong kung nasaan ang isang silid. Ang haba ng pila para sa doktor ay nakadepende pa rin sa dami ng pasyente sa araw na iyon.",
 "CIVIO-VFIL-PAGBASA-040081": "Halos magkasindami ang tubig na ibinigay sa dalawang taniman tuwing umaga. Sinukat ng mga bata ang taas ng mga halaman tuwing Biyernes at isinulat ito sa kuwaderno. Iminungkahi ng guro na sa susunod na pagtatanim, ilagay ang dalawang uri sa iisang bahagi ng hardin upang mas patas ang paghahambing.",
 "CIVIO-VFIL-PAGBASA-040082": "Tumulo ang tubig-ulan sa ilang estante noong nakaraang bagyo, kaya maraming aklat ang kailangang patuyuin at linisin isa-isa. Habang inaayos ang mga ito, bukas muna ang aklatan tuwing umaga para sa mga aklat pambata at mga sanggunian. Nakasulat sa pisara kung aling bahagi ng koleksiyon ang maaari nang hiramin at kung kailan inaasahang mabubuksan ang iba.",
 "CIVIO-VFIL-PAGBASA-040083": "Dalawang linggong nagbilang ang mga kawani ng munisipyo gamit ang simpleng talaan. Sa umaga, karaniwang mabilis ang daloy dahil kakaunti pa ang mamimili. Sa hapon, sabay-sabay dumarating ang mga manggagawang pauwi, kaya humahaba ang pila sa mga puwesto ng isda at gulay.",
 "CIVIO-VFIL-PAGBASA-040084": "Kadalasang nagmumula ang ulat sa PAGASA o sa tanggapan ng Coast Guard sa lalawigan. Mahalaga ito sa mga mangingisdang nagpapasya kung papalaot o hindi. Kapag nagbago ang lagay ng dagat sa hapon, agad na naglalabas ng bagong babala ang istasyon at inuulit ito bawat oras.",
 "CIVIO-VFIL-PAGBASA-040085": "Sa loob ng isang linggo, itinala nila ang natirang galunggong, tilapia, bangus at pusit. Ang ilan ay nag-iimbak ng natirang isda sa yelo para ibenta kinabukasan, ngunit bumababa ang kalidad nito. Nais ng grupo na mabawasan ang nasasayang na isda nang hindi nalulugi sa pagbaba ng presyo.",
 "CIVIO-VFIL-PAGBASA-040086": "Ipinadala ang text message tuwing Lunes ng gabi, habang ang anunsiyo ay nakapaskil sa pintuan ng silid-pulungan. Pagkalipas ng isang buwan, tinanong ng kalihim ang mga kasapi kung saan nila nalaman ang mga pulong at bayarin. Karamihan ay sumagot na sa telepono, ngunit ang ilang lolo at lola na nag-aalaga ng apo ay umaasa pa rin sa nakapaskil na papel.",
 "CIVIO-VFIL-PAGBASA-040087": "Ang larawan ay isang lumang litrato ng plasa na ibinigay ng isang pamilya sa bayan. Ginamit ng museo ang mga kuhang litrato bago ang paglilinis bilang batayan sa paghahambing. Sinubukan nila ang kemikal sa isang sulok na halos hindi nakikita upang hindi madamay ang mukha ng mga tao sa larawan.",
 "CIVIO-VFIL-PAGBASA-040088": "Binuksan ang terminal noong nakaraang buwan para sa mga bus at van papuntang lalawigan. Tumatanggap ng kargamento hanggang tatlumpung minuto bago ang alis upang may panahon ang mga kargador na isakay ito sa ilalim ng sasakyan. Dahil sa kalituhan, may mga kahong naiwan at ipinadala na lamang sa susunod na biyahe.",
 "CIVIO-VFIL-PAGBASA-040089": "Gumagamit sila ng checklist: may bulok bang bahagi ang puno, may sanga bang nakabitin sa daanan, at may ugat bang umaangat sa bangketa. Kapag ligtas at malusog ang puno, iniiwan ito kahit gaano pa ito kataas. Itinatala rin nila ang bawat pinutol na sanga at ang dahilan nito.",
 "CIVIO-VFIL-PAGBASA-040090": "Inilagay ang kahon ng mungkahi sa barangay hall at tumanggap din ng mungkahi sa text sa loob ng dalawang linggo. Mahigit animnapung mungkahi ang natanggap tungkol sa oras ng katahimikan, paradahan at pagtatapon ng basura. Pinagsama ng kalihim ang magkakatulad na mungkahi bago ito pag-usapan ng konseho.",
 "CIVIO-VFIL-20261013-0055": "Kabilang dito ang mga baterya ng remote, relo at laruan. Hindi tinatanggap sa kahon ang baterya ng sasakyan dahil may ibang paraan ng pagtatapon para rito. Hinihikayat din ng mga opisyal ang mga residente na balutin ng tape ang dulo ng baterya bago ito ihulog, dahil mas ligtas ito para sa mga tagapangalap.",
 "CIVIO-VFIL-20261013-0059": "Ang dagdag na pila ay nasa unang palapag, malapit sa pasukan, at may sariling upuan para sa naghihintay. Isang kawani ang itinalaga upang tingnan ang ID ng mga pumipila rito. Itinatala ng opisina ang oras ng pagdating at pag-alis ng bawat aplikante sa lahat ng pila, at ihahambing ito sa datos noong nakaraang buwan.",
 "CIVIO-VFIL-20261013-0063": "Ang silid ay dating bodega ng mga lumang mesa at upuan. Pinintahan ito ng mapusyaw na kulay at nilagyan ng banig at maliliit na unan para sa mga batang magbabasa. Hahatiin ang mga aklat ayon sa baitang upang madaling makahanap ang mga bata ng angkop na babasahin.",
 "CIVIO-VFIL-20261013-0067": "Dati, may kani-kaniyang kopya ang bawat yunit, kaya may mga anunsiyong magkakaiba ang petsa at oras. Ngayon, nasa iisang shared folder ang talaan at may petsa ang bawat pagbabago. Kapag may tanong ang publiko, ito lamang ang tinitingnan ng mga kawani sa harapang mesa.",
 "CIVIO-VFIL-20261013-0071": "Gulay at prutas mula sa mga kasaping magsasaka ang karaniwang ani ng kooperatiba. Isinusulat sa pisara ang dami ng bawat uri pagkatapos magbilang. Tuwing alas-tres ng hapon, sinusuri nilang muli ang mga order bago magpasya kung ano ang gagawin sa natira.",
 "CIVIO-GF2K02-PAGBASA-0001": "Dati, kailangang pumila nang ilang oras at bumalik nang dalawa o tatlong beses ang mga negosyante para sa isang permit. Sa bagong sistema, maaari nang punan ang form at magbayad gamit ang telepono. May kawani sa mesa ng tulong na gagabay sa mga hindi sanay sa internet hanggang matapos nila ang aplikasyon.",
 "CIVIO-GF2K02-PAGBASA-0002": "Noong nakaraang taon, mahigit apatnapung kaso ang naitala sa barangay; ngayong taon, labinlima pa lamang. Tuwing Sabado, sama-samang naglilinis ng kanal ang mga residente at tinatanggal ang mga lalagyang naiipunan ng tubig. Plano ng health worker na ipagpatuloy ang paglilinis at ihambing ang datos sa susunod na taon.",
 "CIVIO-GF2K02-PAGBASA-0003": "Kumukuha sila ng kaunting lupa mula sa iba't ibang bahagi ng bukid at dinadala ito sa tanggapan ng agrikultura. Sa loob ng isang linggo, nalalaman nila kung kulang ang lupa sa nitroheno, posporo o potasa. Batay sa resulta, binibili lamang nila ang patabang tugma sa pangangailangan ng kanilang lupa.",
 "CIVIO-GF2K02-PAGBASA-0004": "Kapag naantala ang antok, mas maikli ang tulog at mas mahirap gumising nang maaga para pumasok sa paaralan. Napapansin din ng mga guro na inaantok sa klase ang ilang mag-aaral na puyat. Sa halip na cellphone, maaaring magbasa ng aklat o makinig ng mahinang musika bago humiga. Mas mainam din kung madilim at tahimik ang silid-tulugan.",
 "CIVIO-GF2K02-PAGBASA-0005": "Bago itayo ang daluyan, inaabot ng dalawa o tatlong araw bago humupa ang tubig, at maraming pamilya ang lumilikas sa paaralan. Ngayon, kadalasang nawawala ang baha sa loob ng ilang oras. Sa huling paglilinis, nakita ng mga manggagawa na plastik at bote ang karaniwang nakabara sa mga rehas ng daluyan.",
 "CIVIO-GF2K02-PAGBASA-0006": "Dati, umaabot ng dalawang oras ang lingguhang pulong at madalas walang malinaw na napagkasunduan. Sa bagong patakaran, ipinapadala ang agenda isang araw bago ang pulong. Kapag hindi natapos ang isang paksa, itinatala ito at pinag-uusapan sa susunod na pulong. Ang hepe mismo ang nagbabantay sa oras ng bawat pulong.",
 "CIVIO-GF2K02-PAGBASA-0007": "Matatagpuan ang bakawan sa maputik na baybayin kung saan nagsasalubong ang tubig-alat at tubig-tabang. Sa mga ugat nito nangingitlog at lumalaki ang maraming maliliit na isda bago lumabas sa dagat. Sa ilang bayan, nagtatanim pa ang mga residente at mag-aaral ng bagong punla ng bakawan tuwing tag-ulan. Binabantayan ng mga bantay-dagat ang mga lugar na ito laban sa ilegal na pagputol.",
 "CIVIO-GF2K02-PAGBASA-0008": "Sa simula, siya lamang ang nagluluto ng biko, puto at kutsinta tuwing madaling-araw. Nang lumaki ang benta, naglagay siya ng mesa at payong sa harap ng bahay para sa mga mamimili. Nag-iipon din siya ng bahagi ng kita upang makabili ng mas malaking kalan.",
 "CIVIO-GF2K02-PAGBASA-0009": "Karamihan sa humiling ay mga mag-aaral sa kolehiyo at mga gurong nagbabasa ng makakapal na sanggunian. Upang hindi magkulang ang aklat sa istante, gumawa ang silid-aklatan ng listahan ng naghihintay para sa mga aklat na nakahiram na. Maaari ring i-renew ang hiram nang isang beses kung walang naghihintay.",
 "CIVIO-GF2K02-PAGBASA-0010": "Karaniwang ginagawa ang pulong sa Sabado ng umaga upang makadalo ang mga magulang na nagtatrabaho. Binibigyan ang bawat magulang ng maikling ulat tungkol sa lakas at kahinaan ng anak. Ang mga hindi makadalo ay tinatawagan ng guro o pinadadalhan ng sulat.",
 "CIVIO-GF2K02-PAGBASA-0011": "Pininturahan ng berde ang bike lane at nilagyan ng plastik na harang upang hindi pumasok ang mga sasakyan. Nagbigay rin ang lungsod ng libreng pagsasanay sa ligtas na pagbibisikleta tuwing Linggo. Ayon sa tanggapan ng trapiko, mga kawani at mag-aaral ang karaniwang gumagamit ng bike lane.",
 "CIVIO-GF2K02-PAGBASA-0012": "Nakalagay sa talaan ang petsa ng pagtanggap, pangalan ng sumulat, paksa at kawaning nakatalaga. Tuwing Biyernes, tinitingnan ng hepe kung aling liham ang malapit nang lumampas sa takdang panahon. Kapag nasagot na ang liham, isinusulat ang petsa ng sagot sa tabi nito.",
}

# Where the addition goes: "end" (after the passage) or "before_last" (before its last sentence, so a closing line stays last)
WHERE = {"CIVIO-VFIL-PAGBASA-040086": "before_last", "CIVIO-VFIL-PAGBASA-040087": "before_last", "CIVIO-VFIL-PAGBASA-040079": "before_last"}


def split(stem):
    """(instruction line, passage, question) of a Filipino passage stem."""
    body, _, q = stem.rpartition("\n\n")
    first, _, rest = body.partition("\n")
    if first.rstrip().endswith(":"):
        return first, rest.strip(), q
    return "", body.strip(), q


def lengthen(stem, add, where="end"):
    ins, p, q = split(stem)
    if where == "before_last":
        head, _, last = p.rstrip().rpartition(". ")
        p = f"{head}. {add} {last}" if head else f"{p} {add}"
    else:
        p = f"{p} {add}"
    return (ins + "\n" if ins else "") + p + "\n\n" + q

# Grok Bot audit of chatgpt-batch-003, items 060076-060100 (environment laws).
S, B, W, N = "GI-SIBLING-TERM", "GI-WRONG-BODY", "GI-SOUNDS-RIGHT", "GI-NEIGHBOR-NUMBER"
REC = ("Right of access to public records", S)
DMG = ("Right to compensation for personal damages", S)
SUE = ("Right to sue to stop environmental violations", S)
D = {
"060076": dict(sc="R.A. 9003, Sec. 3(jj): segregation at source = separating different materials at the point of origin.", o={
  "o2": ("Composting", S, "Composting turns organic waste into a humus-like product; the family is only separating materials."),
  "o3": ("Resource recovery", S, "Resource recovery extracts value from collected waste; separating waste at home before collection is segregation at source."),
  "o4": ("Recycling", S, "Recycling turns discarded materials into new products; separating them at home is segregation at source.")}),
"060077": dict(sc="R.A. 9003 (Ecological Solid Waste Management Act), Sec. 22(b): containers marked compostable, non-recyclable, recyclable or special waste.", o={
  "o1": (None, S, "R.A. 8749 is the Clean Air Act; it does not set waste-container labels."),
  "o3": (None, S, "R.A. 9729 is the Climate Change Act; it does not set waste-container labels."),
  "o4": (None, S, "R.A. 9275 is the Clean Water Act; it does not set waste-container labels.")}),
"060078": dict(sc="R.A. 9003, Sec. 10: barangay collects biodegradable, compostable and reusable waste; city or municipality collects non-recyclable and special waste.", o={
  "o2": ("Provincial level", B, "Sec. 10 assigns this collection to the barangay, not the province."),
  "o3": ("Regional DENR office", B, "DENR offices supervise and enforce; collection is assigned to local governments."),
  "o4": ("National Solid Waste Management Commission", B, "The Commission sets national policy; it does not collect household waste.")}),
"060079": dict(sc="R.A. 9003, Sec. 10: non-recyclable materials and special wastes are the responsibility of the municipality or city.", o={
  "o1": (None, B, "Barangays collect biodegradable, compostable and reusable wastes; non-recyclable and special wastes are the city's or municipality's job."),
  "o2": ("The province", B, "Sec. 10 assigns this collection to the municipality or city, not the province."),
  "o3": ("The National Solid Waste Management Commission", B, "The Commission sets policy; it does not collect waste.")}),
"060080": dict(sc="R.A. 9003, Sec. 10: LGUs are primarily responsible for implementing and enforcing the Act within their jurisdictions.", o={
  "o2": ("Department of Environment and Natural Resources", B, "DENR is the lead national agency, but Sec. 10 makes LGUs primarily responsible within their jurisdictions."),
  "o3": ("National Solid Waste Management Commission", B, "The Commission oversees the national framework; implementation within a locality is primarily the LGU's duty."),
  "o4": ("Private waste haulers", W, "Haulers may be hired, but responsibility stays with the LGU.")}),
"060081": dict(sc="R.A. 9003, Sec. 3(r): an MRF includes a transfer or sorting station, drop-off center, composting facility and recycling facility.", o={
  "o1": ("Sanitary landfill", S, "A sanitary landfill is a disposal site; sorting, drop-off and composting happen at a materials recovery facility."),
  "o2": ("Controlled dump", S, "A controlled dump is a transitional disposal site; it does not sort or compost."),
  "o4": ("Open dump", S, "Open dumps are prohibited (Sec. 37); they do not sort or recover materials.")}),
"060082": dict(sc="R.A. 9003, Sec. 3(f): composting = controlled decomposition of organic matter by micro-organisms into a humus-like product.", o={
  "o2": ("Recycling", S, "Recycling turns discarded materials into new products; microbial decomposition of organics is composting."),
  "o3": ("Segregation at source", S, "Segregation only separates waste; it does not decompose it."),
  "o4": ("Incineration", S, "Incineration burns waste; composting decomposes organic matter with micro-organisms.")}),
"060083": dict(sc="R.A. 9003, Sec. 48(3) lists the open burning of solid waste as a prohibited act.", o={
  "o1": ("Littering in public places", S, "Littering is also prohibited (Sec. 48(1)), but the plan here is to burn waste."),
  "o2": ("Open dumping in flood-prone areas", S, "Open dumping is also prohibited (Sec. 48(6)), but the plan here is burning, not dumping."),
  "o3": ("Collection of non-segregated waste", S, "Collecting unsorted waste is prohibited (Sec. 48(4)), but the act described is burning.")}),
"060084": dict(sc="R.A. 8749, Sec. 2: the State recognizes the principle that 'polluters must pay'.", o={
  "o1": ("The State bears all cleanup costs", W, "R.A. 8749 recognizes that polluters must pay; cleanup costs are not shifted wholly to the State."),
  "o2": ("Pollution prevention over control", S, "That is a policy in Sec. 3(c); who bears the cost is the polluters-must-pay principle in Sec. 2."),
  "o4": ("Use of market-based instruments", S, "Market-based instruments (Sec. 3(b)) encourage self-regulation; they do not say who pays for pollution.")}),
"060085": dict(stem="Residents of an industrial district complain that factory smoke makes the air unhealthy to breathe. Which right recognized by the Clean Air Act most directly applies?",
  sc="R.A. 8749, Sec. 4(a) lists first the right to breathe clean air.", o={
  "o1": ("Right to use natural resources sustainably", S, "Sec. 4(b) concerns use of natural resources; unhealthy air falls under the right to breathe clean air."),
  "o3": (REC[0], S, "Sec. 4(f) concerns access to records; the complaint is about the air itself."),
  "o4": (DMG[0], S, "Sec. 4(h) is for suing after harm is done; the complaint is about the air they breathe.")}),
"060086": dict(k="Participation in planning and monitoring environmental policies", sc="R.A. 8749, Sec. 4(c): the right to participate in formulating, planning, implementing and monitoring environmental policies.", o={
  "o1": (SUE[0], S, "Sec. 4(g) concerns court action; being consulted in planning is participation (Sec. 4(c))."),
  "o2": (REC[0], S, "Sec. 4(f) concerns access to records, not consultation in planning."),
  "o4": (DMG[0], S, "Sec. 4(h) concerns suing for damages, not consultation in planning.")}),
"060087": dict(k="Right to be told of hazards and of pollution increases", sc="R.A. 8749, Sec. 4(e): the right to be informed of potential hazards and served timely notice of any significant rise in pollution.", o={
  "o1": (REC[0], S, "Sec. 4(f) concerns records a citizen asks for; the households want to be told of hazards and pollution increases (Sec. 4(e))."),
  "o2": (DMG[0], S, "Sec. 4(h) concerns suing for damages after harm; the households want advance notice."),
  "o3": (SUE[0], S, "Sec. 4(g) concerns court action; the households want information and timely notice.")}),
"060088": dict(sc="R.A. 8749, Sec. 3(c): focus primarily on pollution prevention rather than on control.", o={
  "o2": ("Use of market-based instruments", S, "Market-based instruments (Sec. 3(b)) encourage self-regulation; stopping pollution before it happens is prevention (Sec. 3(c))."),
  "o3": ("Polluters must pay", S, "That assigns costs after pollution happens; the planner here acts before it happens."),
  "o4": ("Pollution control after emissions occur", S, "Sec. 3(c) focuses primarily on prevention rather than on control.")}),
"060089": dict(sc="R.A. 9275, Sec. 2: protection, preservation and revival of the quality of fresh, brackish and marine waters.", o={
  "o1": (None, S, "The policy also covers brackish and marine waters."),
  "o2": ("Fresh and brackish waters only", S, "The policy also covers marine waters."),
  "o4": ("Groundwater only", S, "Groundwater is covered, but the policy protects fresh, brackish and marine waters generally.")}),
"060090": dict(sc="R.A. 9275, Sec. 3: applies to all water bodies, but primarily to pollution from land-based sources.", o={
  "o2": ("Sea-based sources such as ships", S, "The Act covers all water bodies, but it primarily addresses land-based sources."),
  "o3": ("Air emissions from vehicles", S, "Vehicle emissions are covered by the Clean Air Act (R.A. 8749)."),
  "o4": ("Solid waste in dumpsites", S, "Dumpsites fall under R.A. 9003; R.A. 9275 primarily addresses land-based sources of water pollution.")}),
"060091": dict(sc="R.A. 9275, Sec. 2(g): a comprehensive water-pollution program focusing on pollution prevention.", o={
  "o1": ("Cleanup after contamination occurs", S, "Sec. 2(g) focuses water-pollution management on prevention, before contamination happens."),
  "o2": ("Water quality management areas", S, "Management areas organize water bodies by watershed or basin; the policy reflected here is prevention."),
  "o3": ("Streamlining permit procedures", S, "Sec. 2(a) streamlines procedures; it is not the prevention focus.")}),
"060092": dict(sc="R.A. 9275, Sec. 4(a): aquifer = an underground water-bearing rock layer that supplies wells or springs.", o={
  "o2": ("Groundwater", S, "Groundwater is the water itself; the rock layer that holds and transmits it is an aquifer."),
  "o3": ("Watershed", S, "A watershed is a land area that drains to a water body, not an underground layer."),
  "o4": (None, S, "An estuary is where a river meets the sea, not an underground layer.")}),
"060093": dict(k="Public information, education and participation", sc="R.A. 9275, Sec. 2(h): promote public information and education, and encourage an informed, active public in water-quality monitoring.", o={
  "o1": ("Water quality management areas", S, "Management areas organize water bodies; residents learning and joining monitoring reflects public participation."),
  "o3": ("Streamlined permit procedures", S, "Sec. 2(a) concerns procedures, not public participation."),
  "o4": ("Accountability for environmental damage", S, "Sec. 2(i) concerns accountability; learning and joining monitoring is public participation.")}),
"060094": dict(sc="R.A. 9729 (Climate Change Act of 2009), Sec. 4 created the Climate Change Commission.", o={
  "o1": (None, S, "R.A. 8749 is the Clean Air Act."),
  "o2": (None, S, "R.A. 9003 is the Ecological Solid Waste Management Act."),
  "o4": (None, S, "R.A. 9275 is the Clean Water Act.")}),
"060095": dict(sc="Adaptation = adjusting to climate effects (raise, protect, prepare). Mitigation = cutting greenhouse-gas emissions.", o={
  "o1": ("Mitigation", S, "Mitigation reduces greenhouse-gas emissions; raising equipment to cope with flooding is adaptation."),
  "o2": ("Carbon sequestration", S, "Sequestration removes carbon from the air; it does not protect equipment from floods."),
  "o3": ("Renewable energy transition", S, "Renewable energy cuts emissions, which is mitigation; it does not protect equipment from floods.")}),
"060096": dict(sc="R.A. 9729, Sec. 3(c): anthropogenic causes = causes resulting from human activities.", o={
  "o1": ("Natural", S, "Natural causes are not human-made; anthropogenic means caused by human activity."),
  "o2": ("Biogenic", S, "Biogenic means produced by living things in general; the law's term for human causes is anthropogenic."),
  "o4": ("Atmospheric", S, "Atmospheric describes where gases are, not what causes them.")}),
"060097": dict(k="Mainstreaming climate change into development plans", sc="R.A. 9729, Sec. 9(a): mainstream climate change, in synergy with disaster risk reduction, into national, sectoral and local plans.", o={
  "o1": ("Coordinating agency climate programs", S, "Sec. 9(b) coordinates national agencies' programs; building climate risk into a province's plans is mainstreaming (Sec. 9(a))."),
  "o3": ("Formulating the Framework Strategy", S, "The Framework Strategy (Sec. 9(c)) is a national plan; including climate risk in local plans is mainstreaming."),
  "o4": ("Approving local government budgets", W, "The Commission does not approve local budgets; its role here is mainstreaming climate change into plans.")}),
"060098": dict(sc="R.A. 9729, Sec. 2: a gender-sensitive, pro-children and pro-poor perspective in all climate change efforts.", o={
  "o2": ("The Precautionary Principle", S, "Sec. 2 uses the Precautionary Principle to guide climate-risk decisions; including women, children and the poor is the gender-sensitive, pro-children, pro-poor perspective."),
  "o3": ("Sustainable development under Philippine Agenda 21", S, "Agenda 21 is the general sustainability framework; the specific perspective for women, children and the poor is stated separately."),
  "o4": ("Market-based incentives for businesses", W, "Nothing here concerns business incentives.")}),
"060099": dict(sc="R.A. 9147 = Wildlife Resources Conservation and Protection Act (2001).", o={
  "o1": (None, S, "R.A. 8749 is the Clean Air Act."),
  "o2": (None, S, "R.A. 9275 is the Clean Water Act."),
  "o3": (None, S, "R.A. 9003 is the Ecological Solid Waste Management Act.")}),
"060100": dict(sc="R.A. 9147, Sec. 2: (a) conserve species and habitats, (b) regulate collection and trade, (c) international commitments, (d) scientific studies.", o={
  "o2": ("Conserving wildlife species and their habitats", S, "That is objective (a); checking the conditions for collecting and trading wildlife is objective (b)."),
  "o3": ("Pursuing commitments under international conventions", S, "That is objective (c), about treaties."),
  "o4": ("Supporting scientific studies on biodiversity", S, "That is objective (d), about research.")}),
}

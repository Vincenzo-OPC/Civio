"""gap-fill-2000-03 analogy content (data only; imported by the generator and by qa.solve_ana).
Row: (a, b, arch, difficulty, sentence, key_pair, [(x, y, code, note), x3])
sentence uses {x} {y} and {ax} {ay} (a/an + word). Notes explain each distractor's real link."""
D, S, P, F, M = "ANA-ANALOGY-DEGREE", "ANA-ANALOGY-SYN", "ANA-ANALOGY-PART", "ANA-ANALOGY-FUNCTION", "ANA-ANALOGY-FORM"
DEG = '"{y}" is a stronger degree of "{x}"'
SYN = '"{x}" and "{y}" mean nearly the same thing'
ANT = '"{x}" is the opposite of "{y}"'
R, T, O, L, SN = "ANA-REVERSED", "ANA-SAME-TOPIC", "ANA-OTHER-RELATION", "ANA-ONE-LINK", "ANA-SOUND"
ROWS = [
# ---- DEGREE (lesser : greater) ----
("annoy", "infuriate", D, "medium", DEG, ("tease", "torment"), [
  ("soak", "dampen", R, "goes from strong to mild: the right link in the reverse order"),
  ("insult", "apology", T, "is an offense and the act that answers it, not a mild and a strong form of one thing"),
  ("calm", "agitate", O, "is a pair of opposites, not a mild and a strong form of one action")]),
("glance", "stare", D, "easy", DEG, ("sip", "gulp"), [
  ("devour", "nibble", R, "goes from strong to mild: the reverse order"),
  ("eye", "eyelid", T, "is about the eye, but an eyelid is a part of the eye, not a stronger look"),
  ("glimpse", "peek", O, "is two words of about the same strength (near synonyms), not mild to strong")]),
("damp", "drenched", D, "easy", DEG, ("chilly", "freezing"), [
  ("scorching", "warm", R, "goes from strong to mild: the reverse order"),
  ("rain", "umbrella", T, "is about wet weather, but it is a problem and the thing that protects you from it"),
  ("wet", "dry", O, "is a pair of opposites, not two degrees of one quality")]),
("dislike", "loathe", D, "medium", DEG, ("admire", "worship"), [
  ("terrify", "startle", R, "goes from strong to mild: the reverse order"),
  ("hatred", "enemy", T, "is about hostility, but it is a feeling and the person it is aimed at"),
  ("hate", "love", O, "is a pair of opposites, not two degrees of one feeling")]),
("pleased", "ecstatic", D, "medium", DEG, ("worried", "panicked"), [
  ("furious", "cross", R, "goes from strong to mild: the reverse order"),
  ("gift", "birthday", T, "is about celebrating, but it is a thing and the occasion for it"),
  ("joyful", "glum", O, "is a pair of opposites, not two degrees of one feeling")]),
("simmer", "boil", D, "medium", DEG, ("smolder", "blaze"), [
  ("torrent", "trickle", R, "goes from strong to weak: the reverse order"),
  ("pot", "stove", T, "is about cooking, but it is a container and the appliance it sits on"),
  ("freeze", "thaw", O, "is a pair of opposite processes, not a weak and a strong form of one")]),
("village", "city", D, "easy", DEG, ("stream", "river"), [
  ("ocean", "sea", R, "goes from larger to smaller: the reverse order"),
  ("plaza", "market", T, "is two places found in a town, not a smaller and a larger form of one thing"),
  ("urban", "rural", O, "is a pair of opposites, not a smaller and a larger form")]),
("dent", "wreck", D, "medium", DEG, ("bruise", "fracture"), [
  ("catastrophe", "setback", R, "goes from severe to mild: the reverse order"),
  ("car", "mechanic", T, "is about car damage, but it is a thing and the worker who fixes it"),
  ("repair", "damage", O, "is a pair of opposite actions, not two degrees of harm")]),
("chuckle", "guffaw", D, "hard", DEG, ("whimper", "wail"), [
  ("bellow", "mutter", R, "goes from loud to quiet: the reverse order"),
  ("joke", "comedian", T, "is about laughter, but it is a product and the person who tells it"),
  ("grin", "frown", O, "is a pair of opposite expressions, not two degrees of one")]),
("frugal", "miserly", D, "hard", DEG, ("confident", "arrogant"), [
  ("reckless", "bold", R, "goes from the excess back to the healthy trait: the reverse order"),
  ("budget", "savings", T, "is about money, but it is a plan and its result"),
  ("thrifty", "wasteful", O, "is a pair of opposites, not a trait and its excess")]),
("request", "demand", D, "medium", DEG, ("suggest", "order"), [
  ("insist", "ask", R, "goes from forceful to mild: the reverse order"),
  ("letter", "memo", T, "is two kinds of written message, not a mild and a forceful way of asking"),
  ("approve", "deny", O, "is a pair of opposite answers, not two degrees of asking")]),
("skirmish", "war", D, "hard", DEG, ("squabble", "feud"), [
  ("deluge", "shower", R, "goes from heavy to light: the reverse order"),
  ("soldier", "army", T, "is about the military, but it is a member and its group"),
  ("peace", "conflict", O, "is a pair of opposites, not a small and a large form of fighting")]),
("thin", "emaciated", D, "hard", DEG, ("plump", "obese"), [
  ("gigantic", "large", R, "goes from extreme to ordinary: the reverse order"),
  ("diet", "weight", T, "is about body size, but it is an action and what it affects"),
  ("slim", "slender", O, "is two words of about the same degree (near synonyms)")]),
("good", "excellent", D, "easy", DEG, ("bad", "terrible"), [
  ("huge", "big", R, "goes from extreme to ordinary: the reverse order"),
  ("grade", "report card", T, "is about school marks, but it is an item and the document that lists it"),
  ("fine", "poor", O, "is a pair of opposites, not two degrees of one quality")]),
("crack", "shatter", D, "medium", DEG, ("bend", "snap"), [
  ("destroy", "damage", R, "goes from severe to mild: the reverse order"),
  ("glass", "window", T, "is about breakable things, but it is a material and what is made from it"),
  ("fix", "break", O, "is a pair of opposite actions, not two degrees of breaking")]),
("snack", "feast", D, "easy", DEG, ("jog", "sprint"), [
  ("mansion", "cottage", R, "goes from large to small: the reverse order"),
  ("dinner", "plate", T, "is about meals, but it is a meal and the dish it is served on"),
  ("hunger", "food", O, "is a need and the thing that satisfies it")]),
("respect", "reverence", D, "hard", DEG, ("fondness", "adoration"), [
  ("panic", "concern", R, "goes from intense to mild: the reverse order"),
  ("elder", "ceremony", T, "is about showing respect, but it is a person and an event"),
  ("honor", "disgrace", O, "is a pair of opposites, not two degrees of one feeling")]),
# ---- SYNONYM / ANTONYM (symmetric links: no reversed distractor) ----
("abundant", "plentiful", S, "medium", SYN, ("brief", "short"), [
  ("ample", "lacking", O, "is a pair of opposites, not two words with the same meaning"),
  ("harvest", "granary", T, "is about plenty of grain, but it is a crop and the building that stores it"),
  ("plenty", "plenary", SN, "only look and sound alike; \"plenary\" means attended by all members")]),
("diligent", "industrious", S, "medium", SYN, ("honest", "truthful"), [
  ("lazy", "hardworking", O, "is a pair of opposites, not two words with the same meaning"),
  ("office", "overtime", T, "is about work, but it is a place and extra hours"),
  ("council", "counsel", SN, "only sound alike; a council is a body of people, counsel is advice")]),
("candid", "frank", S, "medium", SYN, ("hidden", "concealed"), [
  ("open", "secretive", O, "is a pair of opposites, not two words with the same meaning"),
  ("interview", "reporter", T, "is about speaking openly, but it is an event and the person who conducts it"),
  ("stationary", "stationery", SN, "only look alike; one means not moving, the other means writing supplies")]),
("lenient", "tolerant", S, "hard", SYN, ("stern", "severe"), [
  ("gentle", "harsh", O, "is a pair of opposites, not two words with the same meaning"),
  ("judge", "sentence", T, "is about punishment, but it is a person and the penalty that person gives"),
  ("principal", "principle", SN, "only sound alike; a principal is a head of school, a principle is a rule")]),
("obtain", "acquire", S, "medium", SYN, ("assist", "help"), [
  ("gather", "scatter", O, "is a pair of opposites, not two words with the same meaning"),
  ("purchase", "store", T, "is about getting things, but it is an action and the place where it happens"),
  ("cite", "site", SN, "only sound alike; to cite is to quote, a site is a place")]),
("vacant", "empty", S, "easy", SYN, ("quick", "swift"), [
  ("full", "hollow", O, "is a pair of opposites, not two words with the same meaning"),
  ("room", "tenant", T, "is about a vacant space, but it is a place and the person who rents it"),
  ("breath", "breadth", SN, "only look and sound alike; breath is air, breadth is width")]),
("meticulous", "thorough", S, "hard", SYN, ("hasty", "rushed"), [
  ("precise", "sloppy", O, "is a pair of opposites, not two words with the same meaning"),
  ("audit", "ledger", T, "is about careful checking, but it is a task and the record it checks"),
  ("complement", "compliment", SN, "only look and sound alike; one completes, the other praises")]),
("permanent", "temporary", S, "medium", ANT, ("rigid", "flexible"), [
  ("lasting", "enduring", O, "is two words with the same meaning, not opposites"),
  ("employee", "contract", T, "is about job status, but it is a person and a document"),
  ("adapt", "adopt", SN, "only look alike; to adapt is to adjust, to adopt is to take as your own")]),
("transparent", "opaque", S, "hard", ANT, ("shallow", "deep"), [
  ("clear", "lucid", O, "is two words with the same meaning, not opposites"),
  ("curtain", "sunlight", T, "is about blocking light, but it is a thing and what it blocks"),
  ("moral", "morale", SN, "only look alike; moral is about right and wrong, morale is team spirit")]),
("ascend", "descend", S, "easy", ANT, ("advance", "retreat"), [
  ("climb", "rise", O, "is two words with the same meaning, not opposites"),
  ("stairs", "elevator", T, "is about going up and down, but it is two ways of doing it"),
  ("personal", "personnel", SN, "only look alike; personal means private, personnel means staff")]),
("frequent", "rare", S, "medium", ANT, ("common", "unusual"), [
  ("constant", "continual", O, "is two words with nearly the same meaning, not opposites"),
  ("visit", "guest", T, "is about frequent visits, but it is an action and the person who does it"),
  ("loose", "lose", SN, "only look alike; loose means not tight, lose means to misplace")]),
("guilty", "innocent", S, "easy", ANT, ("present", "absent"), [
  ("blameless", "faultless", O, "is two words with the same meaning, not opposites"),
  ("verdict", "court", T, "is about a trial, but it is a decision and the place where it is made"),
  ("elicit", "illicit", SN, "only sound alike; to elicit is to draw out, illicit means unlawful")]),
("praise", "criticize", S, "medium", ANT, ("reward", "punish"), [
  ("commend", "applaud", O, "is two words with the same meaning, not opposites"),
  ("speech", "audience", T, "is about public comment, but it is an event and the people who hear it"),
  ("canvas", "canvass", SN, "only look alike; canvas is cloth, to canvass is to seek votes")]),
("novice", "expert", S, "medium", ANT, ("follower", "leader"), [
  ("rookie", "beginner", O, "is two words with the same meaning, not opposites"),
  ("training", "seminar", T, "is about learning a skill, but it is two kinds of learning event"),
  ("desert", "dessert", SN, "only look alike; a desert is dry land, a dessert is a sweet dish")]),
# ---- PART : WHOLE / MEMBER : GROUP ----
("room", "house", P, "easy", '{ax} is one part of {ay}', ("link", "chain"), [
  ("orchestra", "violinist", R, "is the whole and then one member: the reverse order"),
  ("rent", "tenant", T, "is about a house, but it is a payment and the person who pays it"),
  ("door", "open", O, "is a thing and the action done with it, not a part and its whole")]),
("senator", "senate", P, "medium", '{ax} is one member of {ay}', ("juror", "jury"), [
  ("choir", "singer", R, "is the group and then one member: the reverse order"),
  ("law", "bill", T, "is about lawmaking, but a bill is a proposal that may become a law"),
  ("voter", "ballot", O, "is a person and the thing that person uses, not a member and a group")]),
("key", "keyboard", P, "easy", '{ax} is one part of {ay}', ("tooth", "comb"), [
  ("piano", "string", R, "is the whole and then one part: the reverse order"),
  ("printer", "paper", T, "is about office machines, but it is a machine and the material it uses"),
  ("brush", "paint", O, "is a tool and what it applies, not a part and its whole")]),
("wolf", "pack", P, "easy", '{ax} is one member of {ay}', ("sheep", "flock"), [
  ("herd", "cow", R, "is the group and then one member: the reverse order"),
  ("howl", "moon", T, "is about wolves, but it is a sound and something it is linked with in stories"),
  ("cat", "kitten", O, "is an adult animal and its young, not a member and a group")]),
("wheel", "car", P, "easy", '{ax} is one part of {ay}', ("wing", "airplane"), [
  ("house", "roof", R, "is the whole and then one part: the reverse order"),
  ("car", "garage", L, "repeats \"car\" from the first pair; a garage is where a car is kept, not a part"),
  ("road", "traffic", T, "is about driving, but it is a place and what moves on it")]),
("lens", "camera", P, "medium", '{ax} is one part of {ay}', ("bulb", "lamp"), [
  ("bicycle", "pedal", R, "is the whole and then one part: the reverse order"),
  ("photographer", "studio", T, "is about photography, but it is a worker and a workplace"),
  ("photo", "memory", O, "is a thing and what it preserves, not a part and its whole")]),
("clause", "contract", P, "hard", '{ax} is one part of {ay}', ("article", "constitution"), [
  ("treaty", "provision", R, "is the whole and then one part: the reverse order"),
  ("notary", "seal", T, "is about legal papers, but it is a person and the stamp that person uses"),
  ("signature", "approval", O, "is a mark and what it shows, not a part and its whole")]),
("ingredient", "dish", P, "medium", '{ax} is one part of {ay}', ("thread", "fabric"), [
  ("salad", "lettuce", R, "is the whole and then one part: the reverse order"),
  ("chef", "menu", T, "is about food, but it is a worker and a list"),
  ("spoon", "stir", O, "is a tool and its use, not a part and its whole")]),
("planet", "solar system", P, "medium", '{ax} is one part of {ay}', ("atom", "molecule"), [
  ("galaxy", "star", R, "is the whole and then one part: the reverse order"),
  ("telescope", "astronomer", T, "is about space, but it is a tool and the person who uses it"),
  ("fire", "smoke", O, "is a source and what it gives off, not a part and its whole")]),
("letter", "alphabet", P, "medium", '{ax} is one part of {ay}', ("digit", "number"), [
  ("word", "syllable", R, "is the whole and then one part: the reverse order"),
  ("vowel", "accent", T, "is about speech sounds, but neither is a part of the other"),
  ("ink", "pen", O, "is contents and the container that holds them, not a part and its whole")]),
("tree", "forest", P, "easy", '{ax} is one part of {ay}', ("tile", "mosaic"), [
  ("bouquet", "rose", R, "is the whole and then one part: the reverse order"),
  ("lumber", "sawmill", T, "is about wood, but it is a product and the place that makes it"),
  ("seed", "sprout", O, "is an early stage and a later stage, not a part and its whole")]),
("cell", "organism", P, "hard", '{ax} is one part of {ay}', ("pixel", "image"), [
  ("body", "organ", R, "is the whole and then one part: the reverse order"),
  ("microscope", "biologist", T, "is about biology, but it is a tool and the person who uses it"),
  ("virus", "disease", O, "is a cause and its effect, not a part and its whole")]),
# ---- FUNCTION (tool : use, worker : tool/product, container : contents) ----
("stethoscope", "listen", F, "medium", '{ax} is used to {y}', ("ladder", "climb"), [
  ("dig", "shovel", R, "is the action and then the tool: the reverse order"),
  ("heart", "pulse", T, "is about health checks, but it is an organ and its beat"),
  ("doctor", "patient", O, "is a worker and the person served, not a tool and its use")]),
("carpenter", "saw", F, "medium", '{ax} works with {ay}', ("tailor", "needle"), [
  ("brush", "painter", R, "is the tool and then the worker: the reverse order"),
  ("wood", "varnish", T, "is about woodwork, but it is a material and its coating"),
  ("apprentice", "master", O, "is a learner and a teacher, not a worker and a tool")]),
("baker", "bread", F, "easy", '{ax} makes {y}', ("weaver", "cloth"), [
  ("statue", "sculptor", R, "is the product and then the maker: the reverse order"),
  ("oven", "flour", T, "is about baking, but it is an appliance and an ingredient"),
  ("customer", "bakery", O, "is a buyer and a shop, not a maker and a product")]),
("wallet", "money", F, "easy", '{ax} holds {y}', ("envelope", "letter"), [
  ("water", "bucket", R, "is the contents and then the container: the reverse order"),
  ("bank", "loan", T, "is about money, but it is a lender and what it lends"),
  ("purse", "handbag", O, "is two words for nearly the same thing, not a container and contents")]),
("eraser", "mistake", F, "medium", '{ax} removes {ay}', ("detergent", "stain"), [
  ("weed", "herbicide", R, "is the thing removed and then the remover: the reverse order"),
  ("pencil", "paper", T, "is about writing, but it is a tool and the surface it marks"),
  ("error", "correction", O, "is a problem and the act of fixing it, not a remover and what it removes")]),
("auditor", "accounts", F, "hard", '{ax} examines {y}', ("proofreader", "manuscripts"), [
  ("patient", "physician", R, "is the one examined and then the examiner: the reverse order"),
  ("calculator", "ledger", T, "is about bookkeeping, but it is a device and a record book"),
  ("salary", "employee", O, "is pay and the person who receives it, not an examiner and what is examined")]),
("oven", "bake", F, "easy", '{ax} is used to {y}', ("kettle", "boil"), [
  ("slice", "knife", R, "is the action and then the tool: the reverse order"),
  ("cake", "frosting", T, "is about baking, but it is a food and its topping"),
  ("stove", "kitchen", O, "is an appliance and the room it is in, not a tool and its use")]),
("ruler", "measure", F, "easy", '{ax} is used to {y}', ("scale", "weigh"), [
  ("chop", "axe", R, "is the action and then the tool: the reverse order"),
  ("line", "notebook", T, "is about measuring and writing, but it is a mark and the book it is in"),
  ("pencil", "eraser", O, "is two writing tools used together, not a tool and its use")]),
("plumber", "pipes", F, "medium", '{ax} repairs {y}', ("mechanic", "engines"), [
  ("wires", "electrician", R, "is the thing repaired and then the worker: the reverse order"),
  ("water", "faucet", T, "is about plumbing, but it is a liquid and the fixture it flows from"),
  ("tenant", "landlord", O, "is a renter and an owner, not a worker and what that worker repairs")]),
("brake", "stop", F, "medium", '{ax} is used to {y}', ("rudder", "steer"), [
  ("inflate", "pump", R, "is the action and then the device: the reverse order"),
  ("traffic", "road", T, "is about driving, but it is moving vehicles and the place they move"),
  ("driver", "passenger", O, "is two kinds of person in a vehicle, not a device and its use")]),
("passport", "travel", F, "medium", '{ax} allows you to {y}', ("ticket", "board"), [
  ("vote", "ballot", R, "is the action and then the document: the reverse order"),
  ("airport", "luggage", T, "is about travel, but it is a place and what passengers carry"),
  ("visa", "embassy", O, "is a document and the office that issues it, not a document and what it allows")]),
("dentist", "teeth", F, "medium", '{ax} treats {y}', ("veterinarian", "animals"), [
  ("eyes", "optometrist", R, "is what is treated and then the worker: the reverse order"),
  ("toothbrush", "toothpaste", T, "is about teeth, but it is two things used together"),
  ("receptionist", "clinic", O, "is a worker and a workplace, not a worker and what that worker treats")]),
# ---- FORM (real word forms) ----
("mouse", "mice", M, "easy", '"{y}" is the plural of "{x}"', ("goose", "geese"), [
  ("teeth", "tooth", R, "is plural and then singular: the reverse order"),
  ("cheese", "trap", T, "is about mice, but it is bait and the device it is put in"),
  ("child", "childhood", O, "is a person and the stage of life, not a singular and its plural")]),
("criterion", "criteria", M, "hard", '"{y}" is the plural of "{x}"', ("phenomenon", "phenomena"), [
  ("bacteria", "bacterium", R, "is plural and then singular: the reverse order"),
  ("assessment", "scorecard", T, "is about judging work, but it is a process and the record of its result"),
  ("standard", "guideline", O, "is two words with nearly the same meaning, not a singular and its plural")]),
("analysis", "analyses", M, "hard", '"{y}" is the plural of "{x}"', ("crisis", "crises"), [
  ("oases", "oasis", R, "is plural and then singular: the reverse order"),
  ("report", "study", T, "is about research, but it is two kinds of document"),
  ("emphasis", "emphasize", O, "is a noun and its verb, not a singular and its plural")]),
("go", "went", M, "easy", '"{y}" is the past tense of "{x}"', ("bring", "brought"), [
  ("taught", "teach", R, "is the past tense and then the base form: the reverse order"),
  ("travel", "trip", T, "is about going places, but it is an action and an event"),
  ("swim", "swum", O, "is the base form and the past participle (\"have swum\"), not the simple past (\"swam\")")]),
("he", "him", M, "medium", '"{y}" is the object form of "{x}"', ("they", "them"), [
  ("her", "she", R, "is the object form and then the subject form: the reverse order"),
  ("we", "our", O, "is a subject pronoun and its possessive form, not its object form"),
  ("I", "myself", O, "is a subject pronoun and its reflexive form, not its object form")]),
("we", "ours", M, "medium", '"{y}" is the possessive pronoun of "{x}"', ("they", "theirs"), [
  ("yours", "you", R, "is the possessive and then the subject form: the reverse order"),
  ("he", "himself", O, "is a subject pronoun and its reflexive form, not its possessive"),
  ("owner", "property", T, "is about ownership, but it is a person and what that person owns")]),
("good", "better", M, "easy", '"{y}" is the comparative form of "{x}"', ("bad", "worse"), [
  ("farther", "far", R, "is the comparative and then the base form: the reverse order"),
  ("little", "least", O, "is the base form and the superlative (most extreme), not the comparative (\"less\")"),
  ("grade", "rank", T, "is about comparing results, but it is two kinds of standing")]),
("brave", "bravery", M, "medium", '"{y}" is the noun form of the adjective "{x}"', ("honest", "honesty"), [
  ("kindness", "kind", R, "is the noun and then the adjective: the reverse order"),
  ("loyal", "loyally", O, "is an adjective and its adverb, not its noun"),
  ("hero", "medal", T, "is about bravery, but it is a person and an award")]),
("decide", "decision", M, "medium", '"{y}" is the noun form of the verb "{x}"', ("conclude", "conclusion"), [
  ("permission", "permit", R, "is the noun and then the verb: the reverse order"),
  ("include", "inclusive", O, "is a verb and its adjective, not its noun"),
  ("vote", "choice", T, "is about deciding, but it is an act and what is chosen")]),
("Department", "Dept.", M, "medium", '"{y}" is the standard abbreviation of "{x}"', ("Avenue", "Ave."), [
  ("St.", "Street", R, "is the abbreviation and then the full word: the reverse order"),
  ("Mister", "Sir", O, "is two forms of address, not a word and its abbreviation"),
  ("Secretary", "Cabinet", T, "is about government offices, but it is an official and the body that official sits in")]),
("write", "written", M, "hard", '"{y}" is the past participle of "{x}"', ("speak", "spoken"), [
  ("eaten", "eat", R, "is the past participle and then the base form: the reverse order"),
  ("take", "took", O, "is the base form and the simple past, not the past participle (\"taken\")"),
  ("pen", "notebook", T, "is about writing, but it is a tool and what it writes in")]),
("prince", "princess", M, "medium", '"{y}" is the female form of "{x}"', ("host", "hostess"), [
  ("heroine", "hero", R, "is the female form and then the male form: the reverse order"),
  ("king", "kingdom", O, "is a ruler and the land ruled, not a male and a female form"),
  ("palace", "throne", T, "is about royalty, but it is a building and a seat")]),
]
REL = {D: "lesser : greater degree", S: None, P: None, F: None, M: None}
# Solver registry in the analytical.ANALOGIES shape: (a, b, rel, arch, good, bad)
ANALOGIES = [(a.lower(), b.lower(), "", arch, k, [(x, y, c) for x, y, c, _ in ds]) for a, b, arch, _, _, k, ds in ROWS]

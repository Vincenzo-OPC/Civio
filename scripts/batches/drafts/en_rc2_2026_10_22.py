"""Original reading passages, set 2 (22 Oct 2026, afternoon). Same tuple format as en_rc_2026_10_22.RC, plus an optional
6th element naming the skill when it is author's purpose or the relation between parts (both under VEN-RC-INFER)."""
M, D, I, V = "VEN-RC-MAIN", "VEN-RC-DETAIL", "VEN-RC-INFER", "VEN-RC-VOCAB"
NT, BR, NA, EX, OP, SY = "RC-NOT-IN-TEXT", "RC-TOO-BROAD", "RC-TOO-NARROW", "RC-EXTREME", "RC-OPPOSITE", "VRB-SYNONYM-TRAP"
PUR, REL = "author's purpose", "relation between parts"
RC2 = [
("Seed bank",
 "In a farming town in Nueva Ecija, an old storeroom behind the municipal hall now holds hundreds of glass jars of seeds. Each jar is labeled with the name of a rice, corn or vegetable variety, the farm it came from and the year it was harvested. The collection began after a typhoon flooded the lowland fields and ruined the seed that many families had saved for the next planting. Farmers who wanted to replant had to buy commercial seed, which was costly and did not always suit the local soil. A retired agriculturist suggested that the town keep a shared reserve. Farmers now deposit a small part of each harvest and may borrow seed when they need it, returning twice the amount after their next harvest. The arrangement is not free of problems. Seeds lose their ability to sprout if they are stored too long or kept in damp jars, so volunteers test a sample from each jar every year. Even so, the storeroom has already supplied seed to forty households after a second flood.",
 [(M, "What is the passage mainly about?", "A shared seed reserve that helps farmers replant after disasters", [
    ("How typhoons damage lowland rice fields", NA, "The flood explains why the reserve began; it is not the subject."),
    ("Why commercial seed is better than saved seed", OP, "The passage says commercial seed was costly and did not always suit the soil."),
    ("The history of farming in the Philippines", BR, "The passage covers one town's reserve, not national history.")],
   "The passage explains why the town began the reserve, how it works, its main problem and its results."),
  (D, "According to the passage, how much seed must a borrower return?", "Twice the amount borrowed, after the next harvest", [
    ("The same amount, within a month", NT, "No one-month rule is given, and the amount is twice, not the same."),
    ("A small part of each harvest", SY, "That is what every farmer deposits, not what a borrower repays."),
    ("Nothing, since the seed is free", OP, "Borrowers must return seed; the reserve is not a gift.")],
   "The passage says farmers may borrow seed, \"returning twice the amount after their next harvest.\""),
  (I, "Why do volunteers test a sample from each jar every year?", "To find seed that may no longer sprout", [
    ("To decide which farmer may borrow first", NT, "Testing is about the seed, not about the order of borrowers."),
    ("To count how many jars were borrowed", NT, "Counting jars is never mentioned."),
    ("To prove that commercial seed is weaker", NT, "The tests compare nothing with commercial seed.")],
   "The sentence before the tests says seeds lose their ability to sprout if stored too long or kept damp; the tests catch that."),
  (I, "What is the purpose of the sentence \"The arrangement is not free of problems\"?", "It introduces a difficulty before the passage describes how it is handled", [
    ("It shows that the reserve has failed", EX, "The passage goes on to say the reserve still supplied forty households."),
    ("It repeats the cause of the first flood", NT, "The flood was described earlier; this sentence turns to a new point."),
    ("It explains why farmers distrust the agriculturist", NT, "No distrust is described.")],
   "The sentence is a turn: it signals the storage problem, which the next sentences describe and answer with yearly testing.", REL)]),
("Night market rules",
 "Every Friday, a street in a Cagayan de Oro barangay closes to traffic and fills with food stalls. The night market began as a way to help small vendors, but within a year residents were complaining about the noise, the smoke from grills and the trash left behind until morning. Instead of closing the market, the barangay council met with vendors and residents together. They agreed on a short list of rules. Grills must sit at the downwind end of the street, music must stop at ten, and every vendor must clean the space in front of the stall before leaving. A vendor who breaks a rule twice loses the stall for a month. The rules were posted on a board at both entrances so that customers, too, would know what to expect. Complaints fell sharply in the following months. The council credits the change less to the penalties than to the meeting itself, where residents and vendors heard each other's concerns for the first time and wrote rules that both groups considered fair.",
 [(D, "According to the passage, what happens to a vendor who breaks a rule twice?", "The vendor loses the stall for a month", [
    ("The vendor pays a fine to the barangay", NT, "No fine is mentioned."),
    ("The vendor is banned from the market for good", EX, "The penalty lasts one month, not forever."),
    ("The vendor must move to the downwind end", SY, "That is where grills must be placed, not a penalty.")],
   "The passage states: \"A vendor who breaks a rule twice loses the stall for a month.\""),
  (I, "What can be inferred about why the council met with both groups instead of closing the market?", "It wanted to keep the market's benefit to vendors while fixing the residents' complaints", [
    ("It had no power to close the market", NT, "Nothing says the council lacked that power."),
    ("Residents had asked for the market to grow", OP, "Residents were complaining about it."),
    ("Vendors had threatened to leave the barangay", NT, "No threat is mentioned.")],
   "The market began to help small vendors; the council kept it and addressed the complaints, so it sought both aims."),
  (V, "As used in the passage, the word \"credits\" most nearly means", "gives the reason for a result to", [
    ("lends money to", SY, "\"Credit\" can mean a loan, but here the council is explaining what caused the change."),
    ("blames for a problem", OP, "The change was good; the council is praising the meeting, not blaming it."),
    ("pays back", NT, "No payment is involved.")],
   "The council \"credits the change less to the penalties than to the meeting\": it says the meeting, more than the penalties, caused the drop."),
  (I, "What is the author's main purpose in the last sentence?", "To explain what the council believes made the rules work", [
    ("To list the penalties a second time", NA, "The sentence mentions penalties only to set them aside."),
    ("To argue that penalties never work", EX, "The council says less, not never."),
    ("To describe the food sold at the stalls", NT, "Food is not discussed there.")],
   "The final sentence gives the council's explanation for the fall in complaints: the joint meeting and the fair rules it produced.", PUR)]),
("School gardens",
 "When food prices rose sharply one year, a public elementary school in Leyte turned a muddy corner of its grounds into a vegetable garden. Pupils in the upper grades were assigned small plots, and each class kept a notebook recording what was planted, how often it was watered and how much was harvested. Teachers used the notebooks in their lessons. In mathematics, pupils compared the yields of different plots; in science, they tested whether plots with compost grew faster than plots without it. The harvest went to the school's feeding program for pupils who were underweight. At first some parents objected, saying their children were sent to school to study, not to farm. Their view changed when they saw the notebooks at a parents' meeting and realized that the garden was part of the lessons rather than a distraction from them. Several parents later donated seedlings and tools. The principal admits that the garden does not feed every child who needs help, but she says it has taught pupils that what they learn in class can be used outside it.",
 [(M, "Which statement best expresses the main idea of the passage?", "A school garden became both a food source and a way to teach regular lessons", [
    ("Pupils with compost plots always harvest more", EX, "The class tested compost; no result, let alone \"always,\" is given."),
    ("Parents should decide what schools teach", NT, "The passage does not argue this."),
    ("Food prices in Leyte rose sharply one year", NA, "This is the background, not the main point.")],
   "The passage shows the garden feeding underweight pupils and serving math and science lessons, which is why parents came to accept it."),
  (D, "According to the passage, what did pupils test in science?", "Whether plots with compost grew faster than plots without it", [
    ("Which vegetables underweight pupils liked best", NT, "Pupils' food preferences are not mentioned."),
    ("How much water each plot needed to survive", SY, "Watering was recorded in notebooks, but the test was about compost."),
    ("How the yields of different plots compared", SY, "Comparing yields was the mathematics activity.")],
   "The passage says that in science, pupils tested whether plots with compost grew faster than plots without it."),
  (I, "Why did some parents change their view of the garden?", "They saw that the garden was used in their children's lessons", [
    ("The school stopped assigning plots to pupils", OP, "Pupils kept their plots."),
    ("They were given vegetables from the harvest", NT, "The harvest went to the feeding program; nothing says parents received it."),
    ("The principal ordered them to accept it", NT, "No order is mentioned.")],
   "Parents changed their view at the meeting when the notebooks showed the garden was part of the lessons."),
  (I, "How does the last sentence relate to the rest of the passage?", "It admits a limit of the garden and then names its broader value", [
    ("It contradicts the claim that the garden helped anyone", OP, "It confirms the garden helps, though not every child."),
    ("It introduces a new problem the school must solve", NT, "No new problem is introduced."),
    ("It repeats the parents' original objection", NT, "The parents' objection was about farming, not about feeding every child.")],
   "The principal concedes the garden cannot feed every child, then states its larger lesson: classroom learning can be used outside class.", REL)]),
("Records in the cloud",
 "A city treasurer's office in Laguna once kept every tax receipt on paper, filed in steel cabinets that filled two rooms. Finding an old receipt could take a clerk half a day, and a leaking roof had already ruined one cabinet's contents. The office decided to scan its records and store the files on a secure online system. The project took longer than planned. Many receipts were faded or torn, and clerks had to type in details that the scanner could not read. Staff also debated whether to throw away the paper once it had been scanned. In the end, the office kept the paper copies of receipts from the last ten years, as the auditors advised, and sent older papers to the national archives. Today, a clerk can find most receipts in less than a minute, and taxpayers can request copies by email. The treasurer warns other offices, however, that scanning is only half the work: a digital file is useful only if it is named, dated and filed in a way that others can search.",
 [(D, "According to the passage, why did clerks have to type in some details by hand?", "Many receipts were too faded or torn for the scanner to read", [
    ("The online system did not accept scanned files", OP, "The office stored scanned files on the system."),
    ("Auditors asked for typed copies of every receipt", NT, "Auditors advised keeping ten years of paper, not typing."),
    ("The scanner was damaged by the leaking roof", NT, "The roof ruined a cabinet, not the scanner.")],
   "The passage says many receipts were faded or torn, so clerks typed details the scanner could not read."),
  (V, "As used in the passage, the word \"secure\" most nearly means", "protected from loss or misuse", [
    ("certain to be approved", SY, "\"Secure\" can mean to obtain or make certain, but here it describes a storage system."),
    ("tied down tightly", SY, "That sense fits ropes and cargo, not an online system."),
    ("open to anyone", OP, "A secure system limits access; it is not open to all.")],
   "A \"secure online system\" keeps records safe, which is the point after a roof leak destroyed paper files."),
  (I, "What does the treasurer's warning suggest about offices that only scan their papers?", "They may still be unable to find their records quickly", [
    ("They must throw away their paper copies", NT, "The warning is about naming and filing, not disposal."),
    ("They will never need auditors again", EX, "Nothing supports this."),
    ("They should stop accepting tax payments", NT, "Nothing in the passage suggests this.")],
   "The treasurer says a file is useful only if named, dated and filed so others can search; without that, records stay hard to find."),
  (I, "Why does the author mention the leaking roof?", "To show one reason why paper records were risky to keep", [
    ("To explain why the project took longer than planned", SY, "The delay came from faded and torn receipts."),
    ("To show that the office needed a new building", NT, "No new building is discussed."),
    ("To prove that scanning damages old paper", OP, "The roof, not scanning, damaged the paper.")],
   "The roof is part of the opening problem: paper was slow to search and could be destroyed, which led to scanning.", PUR)]),
("Barangay first aid",
 "In a fishing barangay in Quezon, the nearest hospital is an hour away by road, longer when the bridge floods. For years, residents with injuries simply waited for a ride. Two years ago, the barangay asked the Red Cross chapter to train volunteers in first aid. Thirty residents, among them tanods, teachers and a few fishermen, completed the course. They learned how to stop bleeding, how to keep an injured person still until help arrives and how to recognize signs of a stroke. The barangay also bought a stretcher and a supply box, kept at the hall and checked every month. The volunteers do not replace doctors, and they are taught to call for transport at once in any serious case. What they provide is the first half hour of care, which nurses at the hospital say often makes the difference. Last rainy season, volunteers kept a boy with a deep leg cut stable during a long wait for a boat. The barangay now hopes to train a volunteer in every purok, so that help is never more than a short walk away.",
 [(M, "Which title best fits the passage?", "Trained Neighbors Who Bridge the Wait for a Hospital", [
    ("How to Treat a Deep Leg Cut", NA, "The leg cut is one example."),
    ("The Hospitals of Quezon Province", BR, "Hospitals are only the far destination."),
    ("Why Volunteers Should Replace Doctors", OP, "The passage says volunteers do not replace doctors.")],
   "The passage is about volunteers trained to give care during the long wait before hospital treatment."),
  (D, "According to the passage, where is the stretcher kept?", "At the barangay hall", [
    ("At the nearest hospital", NT, "The hospital is an hour away; the stretcher stays in the barangay."),
    ("With the Red Cross chapter", SY, "The Red Cross gave the training, not the storage."),
    ("In every purok", SY, "Training a volunteer in every purok is a hope, not where the stretcher is.")],
   "The passage says the stretcher and supply box are kept at the hall and checked every month."),
  (V, "As used in the passage, the word \"stable\" most nearly means", "not getting worse", [
    ("kept inside a shed for animals", SY, "That is the noun \"stable,\" which does not fit an injured boy."),
    ("calm and cheerful", NT, "The point is his medical condition, not his mood."),
    ("fully healed", EX, "He was kept stable during a wait, not cured.")],
   "Volunteers \"kept a boy ... stable during a long wait\": they stopped his condition from worsening until transport came."),
  (I, "What is the purpose of the example of the boy with the leg cut?", "To show the volunteers' first half hour of care in a real case", [
    ("To prove that the bridge should be rebuilt", NT, "The bridge is mentioned only as a cause of delay."),
    ("To show that volunteers can perform surgery", EX, "They kept him stable; no surgery is described."),
    ("To explain why fishermen joined the course", NT, "The example is not about who joined.")],
   "The example follows the claim that the first half hour matters, and it illustrates exactly that kind of care.", PUR)]),
("Bike lanes",
 "When a city in Iloilo painted bike lanes along its main avenue, few people used them at first. Cyclists said the lanes ended suddenly at busy corners, leaving them to merge with jeepneys, and parked cars often blocked the painted strip. The city responded in stages. It first placed low concrete barriers along the most crowded section, so cars could no longer park in the lane. Next, it linked the avenue's lanes to the roads leading to two universities and the public market. Finally, it added bicycle racks near offices and the city hall. Counts by the city's traffic unit showed that cyclists on the avenue nearly tripled within a year of the last change. Some motorists still grumble that the barriers narrowed the road for cars. Planners answer that a lane is not useful merely because it exists; people ride when the route is safe, connects the places they need to go and lets them leave the bike somewhere at the end.",
 [(M, "What is the main idea of the passage?", "Bike lanes were used more once they were protected, connected and supported by parking", [
    ("Motorists dislike any change to the road", EX, "Only some motorists grumble, about one change."),
    ("Bicycle racks are the most important part of a lane", NA, "Racks were one of three changes."),
    ("Most cities in the country have bike lanes", BR, "The passage is about one city.")],
   "The passage traces three changes and the rise in cyclists, and the planners' closing point names all three conditions."),
  (D, "According to the passage, what was the city's first change?", "Placing low concrete barriers along the most crowded section", [
    ("Adding bicycle racks near offices", SY, "Racks came last."),
    ("Linking the lanes to the universities and market", SY, "Linking came second."),
    ("Painting new lanes on side streets", NT, "No new side-street lanes are mentioned.")],
   "The passage says the city \"first placed low concrete barriers\" along the most crowded section."),
  (I, "What can be inferred about why few people used the lanes at first?", "The lanes did not feel safe or lead anywhere useful", [
    ("Most residents did not own bicycles", NT, "Bicycle ownership is never discussed."),
    ("The lanes were painted in the wrong color", NT, "Color is not mentioned."),
    ("Cyclists preferred to ride with jeepneys", OP, "Cyclists complained about having to merge with jeepneys.")],
   "Cyclists said the lanes ended at busy corners and were blocked by cars, so the lanes were unsafe and incomplete."),
  (I, "How do the sentences beginning \"It first,\" \"Next\" and \"Finally\" relate to one another?", "They describe the city's changes in the order they were made", [
    ("They compare three different cities", NT, "All three describe the same city."),
    ("They list three complaints from motorists", NT, "They list the city's actions, not complaints."),
    ("They give three reasons the lanes failed", OP, "They describe the fixes that made the lanes succeed.")],
   "\"First,\" \"next\" and \"finally\" mark a sequence of actions taken in stages.", REL)]),
("Water refilling stations",
 "Water refilling stations have spread across Philippine towns because many households do not trust their tap water for drinking. A station filters and disinfects water and sells it in returnable containers, usually for much less than bottled water. Their spread, however, has worried health officers. A station is only as safe as its equipment and its habits: filters must be changed on time, containers must be washed and sanitized, and water samples must be tested regularly by an accredited laboratory. In one province, the health office found that a few stations had skipped tests for months. It did not close all the stations, which many families now depend on. Instead, it began posting the date of each station's latest passing test on a public list and visiting stations without warning. Owners who kept good records soon used the list in their advertising. Health officers say customers can protect themselves too, by asking to see the station's most recent laboratory result and by noticing whether containers are cleaned before they are refilled.",
 [(D, "According to the passage, who must test a station's water samples?", "An accredited laboratory", [
    ("The station owner", SY, "Owners keep records, but testing is done by an accredited laboratory."),
    ("The customers who buy the water", NT, "Customers may ask for results; they do not run tests."),
    ("The town's water district", NT, "The water district is not mentioned.")],
   "The passage says water samples must be tested regularly by an accredited laboratory."),
  (V, "As used in the passage, the word \"accredited\" most nearly means", "officially approved to do the work", [
    ("paid in advance", SY, "\"Credit\" suggests payment, but accredited means officially recognized."),
    ("located nearby", NT, "Nothing suggests nearness."),
    ("newly opened", NT, "Age of the laboratory is not the point.")],
   "An \"accredited laboratory\" is one officially recognized as able to test water, which is why its results can be trusted."),
  (I, "Why did the health office post the dates of the latest passing tests instead of closing all stations?", "Families depend on the stations, and the list pushes owners to keep up their tests", [
    ("The law did not allow it to close any station", NT, "Its powers are not discussed."),
    ("Every station had passed its tests", OP, "A few had skipped tests for months."),
    ("Customers had asked it to stop inspections", NT, "No such request is mentioned.")],
   "The passage says many families depend on the stations, and the list let customers and owners see who kept up with testing."),
  (I, "What is the main purpose of the last sentence?", "To tell readers what they themselves can do to stay safe", [
    ("To criticize customers for buying cheap water", NT, "No criticism of customers is made."),
    ("To argue that bottled water is safer", NT, "The passage does not compare safety with bottled water."),
    ("To describe how filters are changed", NT, "Filters are mentioned earlier, not in the last sentence.")],
   "After describing the health office's steps, the passage ends with steps customers can take: ask for the result and watch the cleaning.", PUR)]),
("Recycled uniforms",
 "Every June, parents in a Bulacan town line up to buy new school uniforms, though many children have outgrown uniforms that are still in good condition. A group of mothers decided to set up a uniform exchange at the public elementary school. Families bring clean uniforms their children no longer fit into and take home ones in the right size. Uniforms with small tears are mended by volunteers who know how to sew. In its first year, the exchange handed out more than three hundred sets. The mothers expected that only poor families would come. To their surprise, families of every income level took part, some because they saw no reason to buy new clothes that would be outgrown within a year, others because they liked that less cloth would be thrown away. The school now lends the mothers a classroom every May. The group keeps the exchange simple on purpose: there are no fees, no forms, and no questions about why a family needs a uniform, so that no one feels embarrassed to come.",
 [(M, "What is the passage mainly about?", "A uniform exchange that many kinds of families found useful", [
    ("How to mend torn school uniforms", NA, "Mending is one detail."),
    ("Why school uniforms should be banned", NT, "The passage does not argue against uniforms."),
    ("The rising cost of education in the Philippines", BR, "The passage covers one exchange in one town.")],
   "The passage explains how the exchange works, who used it and why it is kept simple."),
  (D, "According to the passage, how many sets did the exchange hand out in its first year?", "More than three hundred", [
    ("Exactly one hundred", NT, "The passage gives more than three hundred."),
    ("Fewer than fifty", OP, "The number was large, not small."),
    ("One for every pupil in the town", EX, "No such claim is made.")],
   "The passage says that in its first year, the exchange handed out more than three hundred sets."),
  (I, "What surprised the mothers who started the exchange?", "Families of every income level took part", [
    ("No families came in the first year", OP, "More than three hundred sets were handed out."),
    ("The school refused to lend a classroom", OP, "The school now lends them a classroom every May."),
    ("Volunteers could not mend the uniforms", NT, "Volunteers did mend them.")],
   "They expected only poor families, but \"to their surprise, families of every income level took part.\""),
  (I, "Why does the group keep the exchange free of fees, forms and questions?", "So that no family feels embarrassed to take part", [
    ("Because the school does not allow written forms", NT, "No school rule is mentioned."),
    ("Because the volunteers cannot read the forms", NT, "Nothing supports this."),
    ("So that only poor families will come", OP, "The aim is to let anyone come without embarrassment.")],
   "The last sentence gives the reason directly: \"so that no one feels embarrassed to come.\"", PUR)]),
("Mangrove boardwalk",
 "A coastal town in Aklan built a wooden boardwalk through its mangrove forest to attract visitors. The project divided the town at first. Fishermen worried that crowds would disturb the young fish that shelter among the mangrove roots, and environmental groups feared that visitors would leave trash or break branches. The town tried to answer both concerns. The boardwalk was raised above the water so that it did not touch the roots, visitors were limited to set hours, and every group was led by a guide from the local fishermen's association. Guides were trained to explain how mangroves protect the shore from storm waves and serve as nurseries for fish. Part of each entrance fee now pays the guides and part funds the planting of new seedlings. Visitor numbers have grown steadily, and the association reports that catches near the forest have not declined. The town's tourism officer says the boardwalk taught her that a natural site can earn money for a community only if the community protects the very thing visitors come to see.",
 [(D, "According to the passage, who leads every group of visitors?", "A guide from the local fishermen's association", [
    ("A member of an environmental group", SY, "Environmental groups raised concerns; guides come from the fishermen's association."),
    ("The town's tourism officer", NT, "The officer is quoted, but she does not lead groups."),
    ("A teacher from the nearby school", NT, "No teacher is mentioned.")],
   "The passage says every group was led by a guide from the local fishermen's association."),
  (V, "As used in the passage, the word \"nurseries\" most nearly means", "places where young creatures grow safely", [
    ("rooms for babies in a hospital", SY, "That is a common meaning, but here the word describes mangroves and fish."),
    ("shops that sell plants", SY, "A plant nursery sells seedlings, but here mangroves shelter young fish."),
    ("schools for small children", NT, "No school is involved.")],
   "Mangroves \"serve as nurseries for fish\": young fish shelter and grow among the roots, as the passage said earlier."),
  (I, "What does the report about the catches suggest?", "The boardwalk has not harmed the fish the fishermen worried about", [
    ("The fishermen have stopped fishing near the forest", NT, "Nothing says fishing stopped."),
    ("Visitors now catch most of the fish", NT, "Visitors are not described fishing."),
    ("The mangrove forest is shrinking", OP, "New seedlings are being planted, and catches have held.")],
   "Fishermen feared crowds would disturb young fish; catches near the forest have not declined, so that fear has not come true."),
  (I, "How does the second paragraph of ideas, beginning \"The town tried to answer both concerns,\" relate to the sentences before it?", "It describes the steps taken in response to the worries just described", [
    ("It argues that the worries were unreasonable", OP, "The town took the worries seriously and acted on them."),
    ("It adds a third worry raised by visitors", NT, "No visitor worry is added."),
    ("It repeats the worries in different words", NT, "It moves from worries to solutions.")],
   "The earlier sentences give the fishermen's and environmentalists' concerns; the next ones list the measures that answer each concern.", REL)]),
("Typhoon warnings by text",
 "In many provinces, people now receive emergency text alerts before a strong typhoon arrives. The messages are short: the storm's expected landfall, the wind signal for the area and an instruction such as \"Prepare to evacuate.\" Disaster officials in one Samar town noticed, however, that many residents read the alerts but did not act on them. When they asked why, residents gave two main reasons. Some did not understand what a wind signal number meant for their own homes. Others did not know which evacuation center they were assigned to, so they waited for a barangay official to tell them. The town did not change the national alerts, which it does not control. Instead, it held short meetings in every purok before the typhoon season, explaining in the local language what each signal meant and marking every family's assigned center on a printed map left with the household. During the next typhoon, the town reported that more families moved to the centers early. Officials concluded that a warning works only when people already know what it asks them to do.",
 [(M, "Which statement best expresses the main idea of the passage?", "Text alerts led to action once residents understood what the alerts meant for them", [
    ("National text alerts should be written in local languages", NT, "The town did not change the national alerts."),
    ("Typhoons in Samar have become more frequent", NT, "Frequency is never discussed."),
    ("Text alerts give the storm's expected landfall", NA, "That is one detail of the alerts.")],
   "The passage moves from residents ignoring alerts, to their reasons, to the meetings and the earlier evacuations that followed."),
  (D, "According to the passage, what was left with each household after the purok meetings?", "A printed map marking the family's assigned center", [
    ("A list of national emergency hotlines", NT, "No hotline list is mentioned."),
    ("A phone that receives text alerts", NT, "No phones were given out."),
    ("A copy of the national alert rules", NT, "The national alerts were not changed or distributed.")],
   "The passage says the town marked every family's assigned center on a printed map left with the household."),
  (I, "Why did the town hold meetings instead of changing the alerts?", "It had no control over the national alerts", [
    ("Residents had asked for longer alerts", NT, "No such request is reported."),
    ("The alerts were usually wrong", NT, "Accuracy of the alerts is not questioned."),
    ("Meetings cost less than text messages", NT, "Costs are not compared.")],
   "The passage says the town did not change the national alerts, \"which it does not control.\""),
  (I, "What is the purpose of the sentence \"When they asked why, residents gave two main reasons\"?", "It introduces the causes that the town's solution later addresses", [
    ("It ends the passage with a conclusion", NT, "It comes in the middle and leads into the reasons."),
    ("It shows that residents refused to evacuate on purpose", OP, "The reasons are confusion and missing information, not refusal."),
    ("It compares Samar with other provinces", NT, "No comparison follows.")],
   "The sentence sets up the two reasons, and each reason is answered by part of the solution: signal meanings and assigned centers.", REL)]),
("Public library by boat",
 "On a group of small islands in Palawan, many children had never held a storybook that was not a school textbook. A teacher who grew up on one of the islands began loading boxes of donated books onto a small motorboat every Saturday. She stops at a different island each week, spreads mats on the shore and lets children read for two hours. Children may borrow one book each and return it on her next visit. At first, parents doubted that the books would come back, since some families move between islands during the fishing season. The teacher solved part of the problem by asking older children to collect books from families who had moved. Nearly all the books have returned, though a few have been lost to rain and sea spray. The boxes are now lined with plastic. Teachers on the islands report that children who join the reading days talk more in class and are quicker to ask questions. The teacher says her goal is modest: she wants every child to know that books can be read for pleasure, not only for tests.",
 [(D, "According to the passage, how many books may each child borrow?", "One book", [
    ("Two books", NT, "The two refers to hours of reading, not books."),
    ("As many as the child can carry", EX, "The limit is one book."),
    ("None; books must stay on the boat", OP, "Children may borrow and return books.")],
   "The passage says children may borrow one book each and return it on her next visit."),
  (V, "As used in the passage, the word \"modest\" most nearly means", "simple and not overly ambitious", [
    ("shy about one's own success", SY, "\"Modest\" can describe a humble person, but here it describes a goal."),
    ("cheaply priced", SY, "A modest price is low, but the passage describes a goal."),
    ("dressed plainly", SY, "That sense applies to clothing, not to a goal.")],
   "Her goal is \"modest\": simply that children know books can be read for pleasure, not a large program."),
  (I, "Why are the boxes now lined with plastic?", "To protect the books from rain and sea spray", [
    ("To make the boxes lighter to carry", NT, "Weight is not mentioned."),
    ("To keep children from opening the boxes", NT, "Children are meant to use the books."),
    ("To mark which island a box belongs to", NT, "Labeling is not mentioned.")],
   "The sentence before says a few books were lost to rain and sea spray; the plastic lining answers that."),
  (I, "What is the author's purpose in mentioning what island teachers report?", "To show an effect of the reading days on children's schoolwork", [
    ("To argue that teachers should run the boat library", NT, "The passage does not argue this."),
    ("To show that the books were lost", NT, "Lost books are discussed earlier."),
    ("To prove that every child now reads daily", EX, "The report says children talk and ask more; it says nothing about reading daily.")],
   "The teachers' report gives evidence of a benefit: children who join talk more in class and ask questions sooner.", PUR)]),
("Market weighing scale",
 "Shoppers at a public market in Davao often suspected that some vendors' scales showed more weight than the goods really had. Complaints reached the city's market office, but they were hard to prove, since a buyer rarely carried a scale of her own. The office set up a free public scale, checked by city inspectors, near the market's main entrance. A large sign invited shoppers to reweigh their purchases. Any buyer who found a difference could report the stall number on the spot. The office then inspected the vendor's scale and, if it was faulty, sealed it until it was repaired. Within a few months, reports dropped. Vendors who were honest welcomed the public scale, since it gave them a way to show customers that their scales were accurate. The office believes that the scale works less by catching cheaters than by making cheating risky: a vendor cannot know which buyer will walk to the entrance and check.",
 [(M, "What is the passage mainly about?", "How a public scale helped reduce cheating on weights at a market", [
    ("How city inspectors repair faulty scales", NA, "Repairs are one step in the process."),
    ("Why shoppers should carry their own scales", OP, "The public scale made that unnecessary."),
    ("The prices of goods in Davao markets", NT, "Prices are not discussed.")],
   "The passage explains the problem of short weights, the public scale, the response to reports and the results."),
  (D, "According to the passage, what happens to a vendor's scale that inspectors find faulty?", "It is sealed until it is repaired", [
    ("It is replaced by the city for free", NT, "No free replacement is mentioned."),
    ("It is moved to the main entrance", SY, "The public scale is at the entrance; faulty scales are sealed."),
    ("It is returned after the vendor pays a fine", NT, "No fine is mentioned.")],
   "The passage says that if the scale was faulty, the office sealed it until it was repaired."),
  (I, "Why did honest vendors welcome the public scale?", "It let them show customers that their scales were accurate", [
    ("It allowed them to raise their prices", NT, "Prices are not discussed."),
    ("It reported other vendors automatically", NT, "Reports come from buyers, not from the scale."),
    ("It meant their own scales were never inspected", OP, "Any scale can be inspected after a report.")],
   "The passage states that honest vendors welcomed it because it gave them a way to show their scales were accurate."),
  (I, "How does the last sentence relate to the rest of the passage?", "It explains why reports dropped after the scale was set up", [
    ("It describes a new rule for vendors", NT, "No new rule is added."),
    ("It shows that the scale caught many cheaters", OP, "It says the scale works less by catching cheaters."),
    ("It repeats the shoppers' first complaint", NT, "It explains the result, not the complaint.")],
   "After reporting that complaints dropped, the passage ends with the office's explanation: cheating became too risky to try.", REL)]),
]

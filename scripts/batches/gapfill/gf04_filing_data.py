"""Hand-written filing sets for gap-fill-2000-04: (rank, kind P/B, ARMA rule targeted, four names as listed in the stem)."""
SETS = [
# Rule 2: leading "The", & and minor words (business)
("LAST", "B", 2, ["The Golden Wok Restaurant", "Golden Harvest Rice Mill", "Gold Coast Travel", "Goldfield Hardware"]),
("FIRST", "B", 2, ["Santos Bakeshop Supply", "Santos & Garcia Law Office", "Santos Carwash Center", "Santos Garments Outlet"]),
("THIRD", "B", 2, ["The Mango Tree Café", "Manalo Drugstore", "Mangyan Weaves", "Mango Republic Shakes"]),
("SECOND", "B", 2, ["Reyes & Daughters Bakery", "Reyes Electrical", "Reyes Bicycle Shop", "Reyes Funeral Homes"]),
("LAST", "B", 2, ["Pacific Seafoods", "The Palawan Pearl Shop", "Pala-Pala Grill", "Pancit ni Aling Dely"]),
("ORDER", "B", 2, ["The Bamboo House", "Banal & Sons Trucking", "Bamboo Organ Tours", "Banaba Tea Traders"]),
("SECOND", "B", 2, ["Lopez Pharmacy", "Lim & Uy Accounting", "The Lucky Juice Bar", "Lim Bakeshop"]),
# Rule 3: punctuation, hyphens, possessives
("FIRST", "P", 3, ["Teodoro S. Reyes", "Ana B. Reyes-Tan", "Liza P. Reyna", "Victor C. Reyes"]),
("FIRST", "B", 3, ["Nena's Carinderia", "Nenas Beauty Salon", "Nenita Variety Store", "Nena Printing"]),
("LAST", "P", 3, ["Carlos M. Cruz-Manalo", "Jose Luis L. Cruz", "Ramon Jose T. Cruzado", "Elena Marie V. Cruz"]),
("ORDER", "B", 3, ["Lola's Kitchen", "Lola Fe Bakery", "Lolo Ben Sari-Sari Store", "Lola Kitchenette"]),
("FIRST", "B", 3, ["Ka-Tropa Cycle Shop", "Kat's Corner Store", "Katipunan Dental Clinic", "Kata Surf School"]),
("LAST", "P", 3, ["Gloria R. Santos-Ocampo", "Felipe A. Santos", "Pedro D. Santos", "Ernesto F. Santos"]),
# Rule 4: abbreviations, initials, acronyms
("FIRST", "B", 4, ["St. Jude Pharmacy", "Santos Clinic", "Sto. Tomas Bakery", "Stuart Printing"]),
("THIRD", "B", 4, ["Mt. Apo Tours", "Mountain View Inn", "Mulawin Hardware", "Motorline Parts"]),
("FIRST", "P", 4, ["Ma. Teresa L. Gomez", "Mario D. Gomez", "Marco B. Gomez", "Maricel T. Gomez"]),
("SECOND", "B", 4, ["Sta. Cruz Pawnshop", "Santa Ana Bakery", "Stanley Auto Parts", "Sison Printing"]),
("SECOND", "P", 4, ["Ma. Cristina P. Valdez", "Marlon S. Valdez", "Maria A. Valdez", "Mark A. Valdez"]),
("ORDER", "B", 4, ["Ft. Santiago Tours", "Fortune Rice Dealer", "Fuentes Bakery", "Fort Bonifacio Cleaners"]),
("THIRD", "B", 4, ["Sto. Tomas Lumber", "Santo Cristo Hardware", "Silang Feeds", "Sumilao Farms"]),
# Rule 5: titles and suffixes
("FIRST", "P", 5, ["Dr. Rafael M. Ilagan", "Atty. Victoria S. Ilagan", "Benito C. Ilagan", "Engr. Alfredo T. Ilagan"]),
("SECOND", "P", 5, ["Jose R. Lim Jr.", "Jose R. Lim II", "Jose R. Lim", "Jose R. Lim III"]),
("LAST", "P", 5, ["Danilo P. Aquino Sr.", "Danilo P. Aquino Jr.", "Danilo P. Aquino III", "Danilo P. Aquino II"]),
("THIRD", "P", 5, ["Prof. Lourdes A. Navarro", "Hon. Imelda B. Navarro", "Cristina Q. Navarro", "Dr. Andres E. Navarro"]),
("ORDER", "P", 5, ["Ramon T. Bautista Jr.", "Ramon T. Bautista Sr.", "Ramon T. Bautista", "Ramon T. Bautista II"]),
("LAST", "P", 5, ["Atty. Benito F. Salazar", "Dr. Corazon L. Salvador", "Engr. Mario P. Saldana", "Mrs. Lourdes R. Salas"]),
# Rule 6: prefixes
("FIRST", "P", 6, ["Andres P. De Vera", "Gloria S. Dimaculangan", "Mario L. Vergara", "Nora C. Esguerra"]),
("FIRST", "P", 6, ["Elena R. Vasquez", "Ramon D. Van Buren", "Liza M. Valencia", "Eduardo T. Vallejo"]),
("LAST", "P", 6, ["Felipe N. McKinley", "Rosario A. Macaraeg", "Benito O. Maceda", "Cristina T. Madrid"]),
("SECOND", "P", 6, ["Victoria L. O'Hara", "Rodrigo P. Ocampo", "Imelda S. Obispo", "Danilo C. Ortega"]),
("SECOND", "P", 6, ["Teresita G. Del Mundo", "Ernesto B. Mundo", "Corazon P. Delgado", "Alfredo M. Dela Paz"]),
("ORDER", "P", 6, ["Evelyn R. San Pedro", "Rafael T. Sanchez", "Juan C. Pedrosa", "Lourdes M. Santos"]),
("LAST", "P", 6, ["Benito R. Delos Reyes", "Maria T. Reyes", "Andres F. Delos Santos", "Gloria E. Delmonte"]),
("FIRST", "P", 6, ["Nora V. San Juan", "Eduardo M. Juanico", "Felipe R. Sanjuan", "Rosario B. Salas"]),
# Rule 7: numbers in business names
("FIRST", "B", 7, ["15 Stars Printing", "8 Stars Printing", "Eight Stars Printing", "Starlight Printing"]),
("LAST", "B", 7, ["1st Choice Travel", "21st Century Gym", "3 Kings Bakery", "Alpha Travel Agency"]),
("THIRD", "B", 7, ["100 Islands Resort", "12 Islands Diving", "9 Islands Seafood", "Island Hopper Tours"]),
("ORDER", "B", 7, ["Seven Seas Shipping", "7 Seas Laundry", "70 Seas Water Station", "Sevilla Seafood"]),
("THIRD", "B", 7, ["4th Street Eatery", "40 Hands Crafts", "Four Seasons Florist", "5 Stars Hotel"]),
("FIRST", "B", 7, ["Twenty Pesos Store", "20 Pesos Store", "200 Pesos Store", "Twelve Pesos Store"]),
("LAST", "B", 7, ["6 Brothers Lumber", "Sixto Hardware", "60 Brothers Lumber", "16 Brothers Lumber"]),
# Rule 8: organizations as written
("FIRST", "B", 8, ["University of Southern Mindanao Alumni Club", "Southern Mindanao Teachers Club", "Unity Credit Cooperative", "Samahan ng Tsuper ng Davao"]),
("LAST", "B", 8, ["Kapisanan ng mga Mangingisda ng Bataan", "Bataan Fishers Cooperative", "Kalayaan Credit Cooperative", "Kapit-Bisig Foundation"]),
("THIRD", "B", 8, ["Association of Rice Traders", "Rice Millers League", "Asosasyon ng Magsasaka", "Ascend Youth Society"]),
("ORDER", "B", 8, ["Federation of Market Vendors", "Market Vendors Cooperative", "Feliz Dance Club", "Fernandez Family Foundation"]),
("LAST", "B", 8, ["College of Nursing Alumni", "Nightingale Nursing Review", "Colegio de San Lorenzo", "Coleman Tutorial Center"]),
# Rule 1 mixed (personal names, surname first)
("THIRD", "P", 1, ["Victoria A. Tolentino", "Andres B. Toledo", "Corazon D. Tolosa", "Benito E. Tolentino"]),
("ORDER", "P", 1, ["Rafael C. Villareal", "Evelyn D. Villar", "Alfredo P. Villa", "Nora S. Villanueva"]),
]

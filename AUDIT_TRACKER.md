
## Round 03: ChatGPT batch 001 (100 Filipino Verbal), CoS verdict applied, 2026-10-13

- CoS verdict: 89 pass, 11 fixed. 040029 stem giveaway removed; 040065 "sa daan ___ kabundukan"; 040092 A reworded for planning; 040013 key "may saklaw o pananagutan", o2 "nakatataas na tanggapan"; 040047 kaniyang; KWF 040033 nakadaraan, 040053 nakasasakit, 040030 nakasasabay (x2), 040008 nagmamaliit; 040043 o3, 040045 o3, 040006 o2 to FIL-SAME-FIELD; 040080 o4 to RC-NOT-IN-TEXT; 040057 o2 kawalang-hiya; 040074 o3 wording.
- New targets: 040012 MAALAB, 040023 MATIGAS, 040027 MAAYOS, 040032 MALABAY (unique in the bank).
- FIL-SPOKEN-FORM for all ng/nang, din/rin, daw/raw and pang-angkop errors (040061-040070, 040073). Spec 0.1.8.
- qa.py: nakaka- and kanya/kanyang checks in every field; option-in-stem check for Filipino vocabulary. Fixed one "kanyang" in filipino-supplement-001 (0015).
- Key/trap separation: in `MockPoolState` (session builder), with tests; `qa_fil.py` lists remaining pairs.
- All 100 approved/passed by Chief of Staff, 2026-10-13. No deploy.

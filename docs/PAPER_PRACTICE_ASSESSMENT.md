# Print a Practice Mock - assessment only

Pen-and-paper rehearsal with a persistent booklet reference is useful. This assessment does not implement the flow. The Complete Reviewer book remains a separate, unbuilt editorial project.

## Required future contract

Create an immutable, versioned booklet record before export. Its reference must identify the exact question snapshots (stable bank identity and content revision), wording, complete option order, scoring rules and versioned grading key. Retain the snapshot even if a bank row is corrected, retired or deleted. ExamSession question IDs alone cannot provide this guarantee.

The learner enters answers under that booklet reference. Authorize access to the booklet and grade against its recorded version on the server; never reconstruct it from today's bank or trust a client key. Reveal feedback after submission. A separately requested offline key, if offered, must refer to the same booklet version. Keep current can_download_pdf authorization; do not invent payment tiers. Keep PDF libraries and the printable renderer lazy.

## Corrections and errata

Preserve the issued booklet and original grading result. Publish an independently reviewed, append-only erratum tied to the exact booklet/item/key version, describing the correction and its effect. A corrected edition receives a new version/reference. For an existing submission, retain the original result and attach a clearly labelled corrected result under the erratum's grading-key version; do not silently rewrite history. Invalid or ambiguous items can be excluded under an explicit, versioned errata rule shown with the corrected denominator.

## Evidence boundary

Paper Practice cannot verify elapsed time, outside help or prior answer-key access. Label it practice history and keep it separate from protected Strict Mock evidence. It must not feed unsupported readiness or pass-probability claims. Booklet provenance and editorial approval are prerequisites, not claims about the current bank.

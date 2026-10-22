# Bank import approval boundary

Engineering checkpoint, 20 October 2026. This is a console-import boundary, not certification of the existing bank. No live migration, import, approval or deployment was performed.

## Trust and review

Active imports and all baseline replacements require a detached **GT Ed25519 SSHSIG** signature over a separate approval JSON. The signature namespace is `civio-bank-approval`. PHP Sodium verifies signatures directly; no SSH executable is required by the application. Protocol reference: [OpenSSH PROTOCOL.sshsig](https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.sshsig).

The operator provisions GT's public key through `CIVIO_BANK_APPROVAL_PUBLIC_KEY` (an OpenSSH `ssh-ed25519 BASE64` public key). No trusted key ships in the repository; absent trust fails closed. Do not use the public test fixture key as real trust. The importer accepts no signer override, private key, approval checkbox or self-signing command. Private signing keys remain under GT's control and must never enter this checkout or agent context.

The independent reviewer must differ from the author. GT reviews the exact manifest, reviewer identity and report before signing. The signature proves GT authorized that assertion; software cannot prove a reviewer actually performed the work or that the content is correct. A modified manifest, report, record, signature, source fingerprint or replacement content invalidates the operation.

Approval JSON (the example contains placeholders and grants no authority):

```json
{
  "schema": 1,
  "operation": "replace-baseline",
  "approver": "GT",
  "author": "AUTHOR_IDENTITY",
  "reviewer": "INDEPENDENT_REVIEWER_IDENTITY",
  "manifest_sha256": "SHA256_OF_EXACT_MANIFEST_BYTES",
  "review_report_sha256": "SHA256_OF_EXACT_REVIEW_REPORT_BYTES",
  "expires_at": "2026-11-01T00:00:00Z"
}
```

Use `import-batch-active` for batch activation. The operation determines the authorized effect: baseline replacement inserts an active replacement and drafts its original; batch activation inserts or promotes only the reviewed content. Approvals must remain unexpired even for dry runs and active reruns. Preserve the signed record, `.sig`, manifest and report together outside mutable working inputs. The ledger retains their digests and signer-key digest for provenance; it does not retain private keys or full artifact text.

After independent review and GT's approval, GT signs with their own tooling:

```sh
ssh-keygen -Y sign -f <GT-controlled-key> -n civio-bank-approval approval.json
```

This creates `approval.json.sig`. Engineering does not run this with a real approving key. Tests use ephemeral synthetic keys; the committed interoperability fixture contains only a public key, synthetic record and signature.

## Replacement manifest

A nonempty JSON list is required. Every item must contain `id`, `prior_stem`, `original_sha256`, `language`, `stem`, four ordered `options`, integer `correct_option`, and `explanation`. IDs must be stable revision identities using letters, digits, dot, underscore, colon or hyphen (maximum 191 characters). Language is `English` or `Filipino`.

`original_sha256` is `BankContent::fingerprint()` of the independently reviewed baseline original in an **isolated review database**. It hashes a recursively key-sorted JSON object containing category/subcategory names, language, stem, ordered options, integer answer, explanation and source group. JSON uses unescaped Unicode/slashes and no extra whitespace. It excludes machine-local database IDs and mutable status. Reviewers must retain the exact original content behind this digest; an old `replaces_id` is not identity evidence.

The exact prior stem must identify one baseline row and its digest must match. Other source groups cannot satisfy that lookup. New replacement stems cannot collide with any existing question after case/whitespace normalization. Existing replacement links or untracked legacy replacements are refused, not adopted or overwritten. Changed revisions require a separate reviewed revision workflow; this command never edits an existing replacement's content.

```sh
php artisan civio:reparameterize-baseline --path=replacements.json --approval=approval.json --review-report=review.md --dry-run
```

Removing `--dry-run` executes the same validation and locked plan. It is not authorized against the live study database by these instructions. The legacy 496-item manifest has no valid reviewed identity/fingerprint/approval contract and is intentionally rejected.

## General batches and draft quarantine

`civio:import-batch` retains the existing batch schema. Active mode additionally requires each item's declared `approved/passed` labels **and** the independent signed approval. Labels alone have no authority.

`--status=draft` remains available for isolated, non-serving quarantine without approval. It validates shape, options, identities and collisions; it cannot overwrite, adopt, demote or change an existing revision. Once unchanged draft content has been independently reviewed and signed, active import may promote that exact tracked row while preserving its question ID. Review-label changes are allowed; content changes require a separate revision. No existing live items are enrolled or relabeled automatically.

The shared import ledger serializes these commands, locks/revalidates source rows, and records immutable identity/content relationships. Validation finishes before any question writes. All writes roll back together. Import-triggered question/category/subcategory observer invalidation waits until commit. Dry runs and no-ops do not invalidate caches. The schema migration creates only ledger/lock infrastructure, with no question backfill or status changes.

Limits: the console ledger does not prohibit unrelated admin/editing paths from changing questions; a later rerun detects such drift. It is not yet a collection or complete content-versioning system. PostgreSQL concurrency has not been exercised under load; SQLite regressions establish validation, stale-content rejection and rollback behavior.

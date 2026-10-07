-- Civio: remove "(variant N)" clone questions. Same rules as
--   php artisan civio:remove-variant-clones
-- * clone not referenced anywhere          -> DELETE
-- * referenced by an attempt (question_ids or an answers key), a saved drill
--   item or a question feedback report, and still active -> status = 'draft'
--   (archived: never enters the active pool; history rows keep their target)
-- * referenced and already draft           -> skipped
-- Idempotent: a second run deletes 0 and archives 0.
-- ASCII-only file. Preview first with the SELECT in docs/DESKTOP_PATCHES_TO_PORT.md.
BEGIN;

CREATE TEMP TABLE civio_variant_clones ON COMMIT DROP AS
SELECT q.id,
       q.status,
       (
           EXISTS (
               SELECT 1 FROM exam_attempts a
               WHERE a.question_ids @> jsonb_build_array(q.id)
                  OR a.question_ids @> jsonb_build_array(q.id::text)
                  OR (jsonb_typeof(a.answers) = 'object' AND a.answers ? q.id::text)
           )
           OR EXISTS (SELECT 1 FROM saved_drill_items s WHERE s.question_id = q.id)
           OR EXISTS (
               SELECT 1 FROM feedbacks f
               WHERE f.flaggable_type = 'App\Models\Question' AND f.flaggable_id = q.id
           )
       ) AS referenced
FROM questions q
WHERE q.stem ~* '\(variant\s*[0-9]+\)';

SELECT count(*) FILTER (WHERE NOT referenced)                    AS deleted,
       count(*) FILTER (WHERE referenced AND status = 'active')  AS archived,
       count(*) FILTER (WHERE referenced AND status <> 'active') AS skipped
FROM civio_variant_clones;

UPDATE questions q
SET status = 'draft', updated_at = now()
FROM civio_variant_clones v
WHERE q.id = v.id AND v.referenced AND q.status = 'active';

DELETE FROM questions q
USING civio_variant_clones v
WHERE q.id = v.id AND NOT v.referenced;

-- The app caches the active pool forever. With the database cache store,
-- drop those entries so the change shows up without restarting anything.
DO $$
BEGIN
    IF to_regclass('cache') IS NOT NULL THEN
        DELETE FROM cache WHERE key LIKE '%questions.active' OR key LIKE '%categories.tree';
    END IF;
END $$;

COMMIT;

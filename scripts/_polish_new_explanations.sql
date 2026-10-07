SET client_encoding = 'UTF8'; -- UTF-8 file: import with psql -f, never through a PowerShell pipe (see scripts/seeds/README.md)
BEGIN;
UPDATE questions
SET explanation = replace(explanation, 'The other choices fail because the other choices ', 'The other choices fail because ')
WHERE id >= 1413 AND status='active';
UPDATE questions
SET explanation = regexp_replace(explanation, 'The correct option is "([^"]+)\." The', 'The correct option is "\1". The')
WHERE id >= 1413 AND status='active';
COMMIT;

BEGIN;
UPDATE questions
SET explanation = replace(explanation, 'The other choices fail because the other choices ', 'The other choices fail because ')
WHERE id >= 1413 AND status='active';
UPDATE questions
SET explanation = regexp_replace(explanation, 'The correct option is "([^"]+)\." The', 'The correct option is "\1". The')
WHERE id >= 1413 AND status='active';
COMMIT;

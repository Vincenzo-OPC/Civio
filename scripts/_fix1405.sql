SET client_encoding = 'UTF8'; -- UTF-8 file: import with psql -f, never through a PowerShell pipe (see scripts/seeds/README.md)
UPDATE questions SET explanation='Each term is multiplied by 2 and then reduced by 2: 34 multiplied by 2 minus 2 equals 66. The correct option is "66." The other choices fail to apply the recurring rule to the last term.' WHERE id=1405;

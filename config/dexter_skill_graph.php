<?php

/*
 * Dexter prerequisite graph (deterministic, no AI). Skill ids are the spec
 * archetype codes (docs/CSE-Question-Design-Spec.md section 3), so a question's
 * `archetype` column maps straight onto a node. Edges point to prerequisites.
 * Bump `version` on any change; SkillGraphTest rejects cycles and dangling ids.
 */
return [
    'version' => '2026-10-22.1',

    'skills' => [
        // Numerical (both levels; Subprofessional priority)
        'NUM-OPS-ORDER' => ['label' => 'Order of operations', 'domain' => 'numerical', 'prerequisites' => []],
        'NUM-FRAC-DEC' => ['label' => 'Fractions and decimals', 'domain' => 'numerical', 'prerequisites' => ['NUM-OPS-ORDER']],
        'NUM-PCT-BASIC' => ['label' => 'Basic percent', 'domain' => 'numerical', 'prerequisites' => ['NUM-FRAC-DEC']],
        'NUM-WP-PCT-CHANGE' => ['label' => 'Percent change, discounts and markups', 'domain' => 'numerical', 'prerequisites' => ['NUM-PCT-BASIC']],
        'NUM-WP-RATIO' => ['label' => 'Ratio and proportion', 'domain' => 'numerical', 'prerequisites' => ['NUM-FRAC-DEC']],
        'NUM-WP-AVERAGE' => ['label' => 'Averages', 'domain' => 'numerical', 'prerequisites' => ['NUM-OPS-ORDER']],
        'NUM-WP-ALGEBRA' => ['label' => 'Word problems to equations (incl. age problems)', 'domain' => 'numerical', 'prerequisites' => ['NUM-OPS-ORDER', 'NUM-FRAC-DEC']],
        'NUM-WP-RATE' => ['label' => 'Rates: speed, work and unit price', 'domain' => 'numerical', 'prerequisites' => ['NUM-WP-RATIO', 'NUM-WP-ALGEBRA']],
        'NUM-WP-GEOM' => ['label' => 'Perimeter and area', 'domain' => 'numerical', 'prerequisites' => ['NUM-OPS-ORDER']],
        'NUM-SEQ-DIFF' => ['label' => 'Number series by differences', 'domain' => 'numerical', 'prerequisites' => ['NUM-OPS-ORDER']],
        'NUM-SEQ-MULT' => ['label' => 'Number series by multiplying', 'domain' => 'numerical', 'prerequisites' => ['NUM-SEQ-DIFF']],

        // Clerical (Subprofessional only)
        'CLR-SPELL-RIGHT' => ['label' => 'Spelling: pick the correct spelling', 'domain' => 'clerical', 'prerequisites' => []],
        'CLR-SPELL-WRONG' => ['label' => 'Spelling: find the misspelled word', 'domain' => 'clerical', 'prerequisites' => ['CLR-SPELL-RIGHT']],
        'CLR-FILE-POSITION' => ['label' => 'Alphabetical filing', 'domain' => 'clerical', 'prerequisites' => []],
    ],
];

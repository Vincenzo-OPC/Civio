import { CheckCircle2, Clock, Info, Laptop, ListChecks } from 'lucide-react';
import { Card } from '@/components/ui/card';

const LAST_CHECKED = '23 September 2026';

const checklist = [
    'Pick a level. Professional covers second-level posts and includes Analytical Ability. Subprofessional covers clerical work and uses Clerical Ability instead.',
    'Prefer CSDEx when your region actually has open slots. Keep a paper-and-pencil (PPT) plan ready in parallel. Do not wait on COMEX — that computerized system is the legacy path.',
    'Finish one full CIVIO mock at or above 80% on scored items before you treat yourself as ready.',
    'Drill the weakest subject twice, including Filipino verbal items, not only English.',
    'On review, use Explain with Dexter for misses and keep one tip you will apply on the next mock.',
    'The week you intend to file, re-read the current CSC examination announcement. This page is not that announcement.',
];

export function CsePathsGuide() {
    return (
        <div className="space-y-6">
            <div className="flex items-start gap-3.5 rounded-2xl border border-amber-200 bg-amber-50/80 p-5 dark:border-amber-900/40 dark:bg-amber-950/20">
                <Info className="mt-0.5 size-5 shrink-0 text-amber-700 dark:text-amber-400" />
                <div className="space-y-1">
                    <h3 className="text-sm font-bold text-amber-950 dark:text-amber-200">
                        Study notes, not a CSC bulletin
                    </h3>
                    <p className="text-sm leading-relaxed text-amber-900/90 dark:text-amber-300/90">
                        Last checked {LAST_CHECKED}. CIVIO is an independent
                        study tool. It is not affiliated with the Civil Service
                        Commission and it is not official CSDEx software.
                        Counts below follow the CSC Examinee's Guide for
                        the July 2026 CSE pen-and-paper test (150 scored items
                        plus 20 personal-data items for Professional). Slot
                        status and the next exam calendar change. Confirm on
                        csc.gov.ph before you apply.
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <Card className="space-y-4 border border-border bg-card p-6">
                    <div className="flex items-center gap-3">
                        <div className="flex size-11 items-center justify-center rounded-xl border border-blue-200 bg-blue-50 text-blue-600 dark:border-blue-900/40 dark:bg-blue-950/40 dark:text-blue-400">
                            <ListChecks className="size-5" />
                        </div>
                        <h3 className="font-heading text-lg font-black">
                            CSE overview
                        </h3>
                    </div>
                    <p className="text-sm leading-relaxed text-muted-foreground">
                        The Career Service Examination has two levels. A
                        general rating of at least 80.00 is the published
                        passing mark. The July 2026 PPT guide lists Professional
                        as 150 test-proper items plus 20 examinee data items
                        (170 in the booklet, 3 hours 10 minutes) and
                        Subprofessional as 145 plus 20 (165 in the booklet, 2
                        hours 40 minutes).
                    </p>
                    <p className="text-sm leading-relaxed text-muted-foreground">
                        CIVIO mocks skip that personal-data block. A fresh
                        Professional mock starts on scored question 1 and aims
                        for about 150 items (Verbal 45, Analytical 52,
                        Numerical 45, General Information 8). Subprofessional
                        aims for about 145. The clock stays the official 3h 10m
                        / 2h 40m so you are not tighter than test day.
                    </p>
                </Card>

                <Card className="space-y-4 border border-border bg-card p-6">
                    <div className="flex items-center gap-3">
                        <div className="flex size-11 items-center justify-center rounded-xl border border-violet-200 bg-violet-50 text-violet-600 dark:border-violet-900/40 dark:bg-violet-950/40 dark:text-violet-400">
                            <Laptop className="size-5" />
                        </div>
                        <h3 className="font-heading text-lg font-black">
                            CSDEx vs PPT
                        </h3>
                    </div>
                    <ul className="space-y-3 text-sm leading-relaxed text-muted-foreground">
                        <li>
                            <strong className="text-foreground">
                                CSDEx (Civil Service Digital Examination).
                            </strong>{' '}
                            Prefer this when slots are actually open in your
                            region. Public CSC and PIA notes from early 2026
                            describe it as the newer digital mode, including a
                            Bicol pilot, meant to replace the old computerized
                            exam. It is not nationwide-by-default. CIVIO does
                            not reserve slots.
                        </li>
                        <li>
                            <strong className="text-foreground">
                                PPT (pen and paper).
                            </strong>{' '}
                            Prepare for this in parallel. Examination
                            Announcement No. 08, s. 2025 scheduled 2026 CSE-PPT
                            on 8 March and 9 August. Both dates are past as of
                            this check. The next window is whatever CSC posts
                            next.
                        </li>
                        <li>
                            <strong className="text-foreground">
                                COMEX is legacy.
                            </strong>{' '}
                            Do not make the older computerized exam your
                            primary apply path. Same subjects can appear there,
                            but it is the system CSDEx is intended to replace.
                        </li>
                    </ul>
                </Card>

                <Card className="space-y-4 border border-border bg-card p-6">
                    <div className="flex items-center gap-3">
                        <div className="flex size-11 items-center justify-center rounded-xl border border-emerald-200 bg-emerald-50 text-emerald-600 dark:border-emerald-900/40 dark:bg-emerald-950/40 dark:text-emerald-400">
                            <Clock className="size-5" />
                        </div>
                        <h3 className="font-heading text-lg font-black">
                            Techniques
                        </h3>
                    </div>
                    <ul className="space-y-2 text-sm leading-relaxed text-muted-foreground">
                        <li>
                            The full Professional booklet is about 67 seconds
                            per item (170 items, 3h 10m). A CIVIO scored mock
                            is about 76 seconds because the 20 data items are
                            omitted and the clock is unchanged.
                        </li>
                        <li>
                            First pass: answer what you know, flag the rest,
                            and do not camp on one stem. Second pass is flags
                            only.
                        </li>
                        <li>
                            No calculator. Estimate, then compute. For verbal,
                            drill Filipino as well as English.
                        </li>
                        <li>
                            Afterward, ask Dexter to explain why the wrong
                            option lost. Unique stems only — skip anything that
                            is the same question with a “(variant N)” tag.
                        </li>
                    </ul>
                </Card>

                <Card className="space-y-4 border border-border bg-card p-6">
                    <div className="flex items-center gap-3">
                        <div className="flex size-11 items-center justify-center rounded-xl border border-rose-200 bg-rose-50 text-rose-600 dark:border-rose-900/40 dark:bg-rose-950/40 dark:text-rose-400">
                            <CheckCircle2 className="size-5" />
                        </div>
                        <h3 className="font-heading text-lg font-black">
                            Readiness checklist
                        </h3>
                    </div>
                    <ul className="space-y-2.5">
                        {checklist.map((item) => (
                            <li
                                key={item}
                                className="flex items-start gap-2 text-sm leading-relaxed text-muted-foreground"
                            >
                                <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-500" />
                                <span>{item}</span>
                            </li>
                        ))}
                    </ul>
                </Card>
            </div>
        </div>
    );
}

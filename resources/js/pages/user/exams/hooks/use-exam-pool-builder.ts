import { useCallback, useMemo } from 'react';
import { fallbackDemographicQuestions } from '@/data/fallback-demographics';
import { readGuestStudyBias } from '@/lib/guest-study-bias';
import type { Question } from '../types';
import {
    fisherYatesShuffle,
    isDemographicQuestion,
    EXAM_CONSTANTS,
    shuffleHardBiased,
    dedupeNearDuplicateStems,
    stemDedupeKey,
    preferUniqueStemsFirst,
} from '../utils/exam-utils';

export function shuffleOptionsForQuestion(q: Question): Question {
    let options = q.options;
    const hasKey = typeof q.correct_option === 'number';
    let correctOption = hasKey ? (q.correct_option as number) : 0;

    if (options.length > 5) {
        options = options.slice(0, 5);

        if (hasKey && correctOption >= 5) {
            correctOption = 0;
        }
    }

    const indices = options.map((_, i) => i);
    const shuffledIndices = fisherYatesShuffle(indices);

    const shuffledOptions = shuffledIndices.map((i) => options[i]);
    // When answer keys are withheld, omit remapped correct_option (Reveal uses /exams/reveal).
    const remapped: Question = {
        ...q,
        options: shuffledOptions,
        originalOptionIndices: shuffledIndices,
    };

    if (hasKey) {
        remapped.correct_option = shuffledIndices.indexOf(correctOption);
    } else {
        delete remapped.correct_option;
        delete remapped.explanation;
    }

    return remapped;
}

function quotasForSubcats(
    names: string[],
    groups: Record<string, Question[]>,
    targetCount: number,
    weakSubSet: Set<string>,
): Record<string, number> {
    const quotas: Record<string, number> = {};
    names.forEach((name) => {
        quotas[name] = 0;
    });

    const place = (bucket: string[], share: number): number => {
        if (bucket.length === 0 || share <= 0) {
            return 0;
        }

        let left = share;
        const base = Math.floor(share / bucket.length);
        let rem = share % bucket.length;

        for (const name of bucket) {
            const want = base + (rem > 0 ? 1 : 0);

            if (rem > 0) {
                rem--;
            }

            const give = Math.min(groups[name]?.length ?? 0, want);
            quotas[name] += give;
            left -= give;
        }

        if (left > 0) {
            for (const name of bucket) {
                if (left <= 0) {
                    break;
                }

                const room = (groups[name]?.length ?? 0) - quotas[name];
                const add = Math.min(Math.max(0, room), left);
                quotas[name] += add;
                left -= add;
            }
        }

        return share - left;
    };

    const weakNames = names.filter((name) => weakSubSet.has(name));
    const otherNames = names.filter((name) => !weakSubSet.has(name));

    if (weakNames.length > 0 && otherNames.length > 0) {
        const weakAvailable = weakNames.reduce(
            (sum, name) => sum + (groups[name]?.length ?? 0),
            0,
        );
        const weakShare = Math.min(
            weakAvailable,
            Math.round(targetCount * EXAM_CONSTANTS.WRONG_PRIORITY_PERCENTAGE),
        );
        const placedWeak = place(weakNames, weakShare);
        place(otherNames, Math.max(0, targetCount - placedWeak));
    } else {
        const baseQuota = Math.floor(targetCount / names.length);
        let remainder = targetCount % names.length;

        for (const name of names) {
            quotas[name] = baseQuota + (remainder > 0 ? 1 : 0);

            if (remainder > 0) {
                remainder--;
            }
        }
    }

    return quotas;
}

/**
 * About half the scored fill should come from previously-weak categories
 * when that browser still has unused items in those categories.
 * Does not add demographic items.
 */
function raiseWeakCategoryShare(
    scoredPool: Question[],
    sourcePool: Question[],
    weakCategories: string[],
    targetCount: number,
): Question[] {
    if (weakCategories.length === 0 || scoredPool.length === 0) {
        return scoredPool;
    }

    const weakSet = new Set(weakCategories);
    const isWeak = (q: Question) => weakSet.has(q.category || '');
    const weakTarget = Math.min(
        targetCount,
        Math.round(targetCount * EXAM_CONSTANTS.WRONG_PRIORITY_PERCENTAGE),
    );
    const result = [...scoredPool];
    let weakCount = result.filter(isWeak).length;

    if (weakCount >= weakTarget) {
        return result;
    }

    const used = new Set(result.map((q) => q.id));
    const extras = fisherYatesShuffle(
        sourcePool.filter(
            (q) => !used.has(q.id) && !isDemographicQuestion(q) && isWeak(q),
        ),
    );
    let extraIdx = 0;

    for (
        let i = result.length - 1;
        i >= 0 && weakCount < weakTarget && extraIdx < extras.length;
        i--
    ) {
        if (!isWeak(result[i])) {
            result[i] = extras[extraIdx++];
            weakCount++;
        }
    }

    return result;
}

interface UseExamPoolBuilderProps {
    questions?: Question[];
    seenQuestionIdsByTrack?: {
        Professional: number[];
        Subprofessional: number[];
        Drill: number[];
    };
    wrongQuestionIdsByTrack?: {
        Professional: number[];
        Subprofessional: number[];
        Drill: number[];
    };
    selectedExamId: number | null;
    activeQuestions: Question[];
}

export function useExamPoolBuilder({
    questions = [],
    seenQuestionIdsByTrack = {
        Professional: [],
        Subprofessional: [],
        Drill: [],
    },
    wrongQuestionIdsByTrack = {
        Professional: [],
        Subprofessional: [],
        Drill: [],
    },
    selectedExamId,
    activeQuestions,
}: UseExamPoolBuilderProps) {
    const fallbackQuestions: Question[] = questions;
    const demographicQuestions: Question[] = useMemo(
        () => questions.filter((q) => isDemographicQuestion(q)),
        [questions],
    );

    const getTrackNameForExam = useCallback((examId: number | null) => {
        return examId === 2 ? 'Subprofessional' : 'Professional';
    }, []);

    const getSeenIdsForExam = useCallback(
        (examId: number | null) => {
            const track = getTrackNameForExam(examId);
            const fromServer =
                seenQuestionIdsByTrack[
                    track as keyof typeof seenQuestionIdsByTrack
                ] ?? [];
            const fromCurrentSession =
                selectedExamId === examId && activeQuestions.length > 0
                    ? activeQuestions.map((q) => q.id)
                    : [];

            return [...new Set([...fromServer, ...fromCurrentSession])];
        },
        [
            seenQuestionIdsByTrack,
            selectedExamId,
            activeQuestions,
            getTrackNameForExam,
        ],
    );

    const getWrongIdsForExam = useCallback(
        (examId: number | null) => {
            const track = getTrackNameForExam(examId);
            const fromServer =
                wrongQuestionIdsByTrack[
                    track as keyof typeof wrongQuestionIdsByTrack
                ] ?? [];
            const fromBrowser =
                examId === 1 || examId === 2
                    ? (readGuestStudyBias()[
                          track as 'Professional' | 'Subprofessional'
                      ]?.wrongIds ?? [])
                    : [];

            return [...new Set([...fromServer, ...fromBrowser])];
        },
        [wrongQuestionIdsByTrack, getTrackNameForExam],
    );

    const buildFreshExamPool = useCallback(
        (examId: number | null) => {
            const sourcePool =
                questions.length > 0 ? questions : fallbackQuestions;

            const verbalPool = sourcePool.filter(
                (q) => q.category === 'Verbal Ability',
            );
            const analyticalPool = sourcePool.filter(
                (q) => q.category === 'Analytical Ability',
            );
            const numericalPool = sourcePool.filter(
                (q) => q.category === 'Numerical Ability',
            );
            const clericalPool = sourcePool.filter(
                (q) => q.category === 'Clerical Ability',
            );
            const generalPool = sourcePool.filter(
                (q) => q.category === 'General Information',
            );

            const seenSet = new Set(getSeenIdsForExam(examId));
            const wrongSet = new Set(getWrongIdsForExam(examId));
            const weakSubSet = new Set(
                examId === 1 || examId === 2
                    ? (readGuestStudyBias()[
                          getTrackNameForExam(examId) as
                              | 'Professional'
                              | 'Subprofessional'
                      ]?.weakSubcategories ?? [])
                    : [],
            );

            const pickFlat = (
                pool: Question[],
                count: number,
                catName: string,
                subName?: string,
            ): Question[] => {
                const wrongFromSeen = pool.filter((q) => wrongSet.has(q.id));
                const unseen = pool.filter((q) => !seenSet.has(q.id));
                const seenCorrect = pool.filter(
                    (q) => seenSet.has(q.id) && !wrongSet.has(q.id),
                );

                const picked: Question[] = [];

                /**
                 * Phase A (unique): skip near-duplicate stems.
                 * Phase B (fill): allow variants / near-dups so quota can reach count.
                 */
                const pushWithLimit = (
                    items: Question[],
                    quota: number,
                    allowNearDup = false,
                ) => {
                    let added = 0;
                    const candidates = allowNearDup
                        ? items.filter(
                              (q) => !picked.some((p) => p.id === q.id),
                          )
                        : dedupeNearDuplicateStems([
                              ...picked,
                              ...items,
                          ]).filter((q) => !picked.some((p) => p.id === q.id));

                    for (const q of candidates) {
                        if (added >= quota) {
                            break;
                        }

                        if (picked.some((p) => p.id === q.id)) {
                            continue;
                        }

                        if (!allowNearDup) {
                            const key = stemDedupeKey(
                                q.stem || '',
                                EXAM_CONSTANTS.STEM_DEDUP_PREFIX_LEN,
                            );

                            if (
                                key &&
                                picked.some(
                                    (p) =>
                                        stemDedupeKey(
                                            p.stem || '',
                                            EXAM_CONSTANTS.STEM_DEDUP_PREFIX_LEN,
                                        ) === key,
                                )
                            ) {
                                continue;
                            }
                        }

                        picked.push(q);
                        added++;
                    }
                };

                const wrongQuota = Math.ceil(
                    count * EXAM_CONSTANTS.WRONG_PRIORITY_PERCENTAGE,
                );

                // Prefer unique stems first within each priority band
                const wrongPicked = shuffleHardBiased(
                    preferUniqueStemsFirst(fisherYatesShuffle(wrongFromSeen)),
                );
                pushWithLimit(wrongPicked, wrongQuota, false);

                let remaining = count - picked.length;

                if (remaining > 0) {
                    pushWithLimit(
                        shuffleHardBiased(preferUniqueStemsFirst(unseen)),
                        remaining,
                        false,
                    );
                }

                remaining = count - picked.length;

                if (remaining > 0) {
                    pushWithLimit(
                        shuffleHardBiased(preferUniqueStemsFirst(seenCorrect)),
                        remaining,
                        false,
                    );
                }

                remaining = count - picked.length;

                if (remaining > 0) {
                    pushWithLimit(
                        shuffleHardBiased(fisherYatesShuffle(wrongPicked)),
                        remaining,
                        false,
                    );
                }

                if (picked.length < count) {
                    const fbPool = fallbackQuestions.filter(
                        (q) =>
                            q.category === catName &&
                            (!subName || q.subcategory === subName) &&
                            !picked.some((p) => p.id === q.id),
                    );
                    pushWithLimit(
                        shuffleHardBiased(preferUniqueStemsFirst(fbPool)),
                        count - picked.length,
                        false,
                    );
                }

                // FILL-TO-QUOTA: after unique stems exhausted, use shuffled variants
                remaining = count - picked.length;

                if (
                    remaining > 0 &&
                    EXAM_CONSTANTS.FILL_VARIANTS_AFTER_UNIQUE
                ) {
                    const leftover = preferUniqueStemsFirst(
                        pool.filter(
                            (q) => !picked.some((p) => p.id === q.id),
                        ),
                    );
                    // Hard-bias still applies; variants allowed (allowNearDup=true)
                    pushWithLimit(
                        shuffleHardBiased(fisherYatesShuffle(leftover)),
                        remaining,
                        true,
                    );
                }

                // Absolute last resort: still short and pool fully used — stop short
                // rather than cloning the same Question object (breaks scorecard).
                return fisherYatesShuffle(picked.slice(0, count));
            };

            const pickBalanced = (
                pool: Question[],
                targetCount: number,
                catName: string,
                splitLanguage = false,
            ): Question[] => {
                const groups: Record<string, Question[]> = {};
                pool.forEach((q) => {
                    const key = q.subcategory || 'General';

                    if (!groups[key]) {
                        groups[key] = [];
                    }

                    groups[key].push(q);
                });

                // Shuffle subcategory key order — Object.keys can be sticky insertion order
                const subcatNames = fisherYatesShuffle(Object.keys(groups));

                if (subcatNames.length === 0) {
                    return pickFlat(pool, targetCount, catName);
                }

                const quotas = quotasForSubcats(
                    subcatNames,
                    groups,
                    targetCount,
                    weakSubSet,
                );
                const picked: Question[] = [];

                for (const subName of subcatNames) {
                    const quota = quotas[subName] ?? 0;

                    if (quota <= 0) {
                        continue;
                    }

                    const subPool = groups[subName];

                    if (splitLanguage || subName === 'Word analogy') {
                        const engPool = subPool.filter((q) => {
                            const lang = (q.language || '').toLowerCase();

                            return lang === 'english' || lang === '';
                        });
                        const filPool = subPool.filter((q) => {
                            const lang = (q.language || '').toLowerCase();

                            return (
                                lang.includes('filipino') ||
                                lang.includes('tagalog')
                            );
                        });

                        const filQuota =
                            filPool.length > 0
                                ? Math.min(
                                      Math.floor(quota / 2),
                                      filPool.length,
                                  )
                                : 0;
                        const engQuota = quota - filQuota;

                        picked.push(
                            ...pickFlat(engPool, engQuota, catName, subName),
                            ...pickFlat(filPool, filQuota, catName, subName),
                        );
                    } else {
                        picked.push(
                            ...pickFlat(subPool, quota, catName, subName),
                        );
                    }
                }

                // Category-level fill if subcategory splits left a shortfall
                if (
                    picked.length < targetCount &&
                    EXAM_CONSTANTS.FILL_VARIANTS_AFTER_UNIQUE
                ) {
                    const need = targetCount - picked.length;
                    const leftover = pool.filter(
                        (q) => !picked.some((p) => p.id === q.id),
                    );
                    picked.push(
                        ...pickFlat(leftover, need, catName),
                    );
                }

                return fisherYatesShuffle(picked.slice(0, targetCount));
            };

            const scoredPool: Question[] = [];
            const scoredTarget =
                examId === 1
                    ? EXAM_CONSTANTS.PROFESSIONAL_SCORED_ITEMS
                    : EXAM_CONSTANTS.SUBPROFESSIONAL_SCORED_ITEMS;

            if (examId === 1) {
                // Professional: 150 scored
                scoredPool.push(
                    ...pickBalanced(verbalPool, 45, 'Verbal Ability', true),
                );
                scoredPool.push(
                    ...pickBalanced(analyticalPool, 52, 'Analytical Ability'),
                );
                scoredPool.push(
                    ...pickBalanced(numericalPool, 45, 'Numerical Ability'),
                );
                scoredPool.push(
                    ...pickBalanced(generalPool, 8, 'General Information'),
                );
            } else {
                // Subprofessional: 145 scored
                scoredPool.push(
                    ...pickBalanced(verbalPool, 45, 'Verbal Ability', true),
                );
                scoredPool.push(
                    ...pickBalanced(clericalPool, 47, 'Clerical Ability'),
                );
                scoredPool.push(
                    ...pickBalanced(numericalPool, 45, 'Numerical Ability'),
                );
                scoredPool.push(
                    ...pickBalanced(generalPool, 8, 'General Information'),
                );
            }

            // Exam-level safety net: if category pools still left us short, fill
            // from remaining non-demographic items (variants OK). Prefer same
            // Professional / Subprofessional category set.
            if (
                scoredPool.length < scoredTarget &&
                EXAM_CONSTANTS.FILL_VARIANTS_AFTER_UNIQUE
            ) {
                const used = new Set(scoredPool.map((q) => q.id));
                const preferredCats =
                    examId === 1
                        ? new Set([
                              'Verbal Ability',
                              'Analytical Ability',
                              'Numerical Ability',
                              'General Information',
                          ])
                        : new Set([
                              'Verbal Ability',
                              'Clerical Ability',
                              'Numerical Ability',
                              'General Information',
                          ]);
                const leftoverPreferred = shuffleHardBiased(
                    fisherYatesShuffle(
                        sourcePool.filter(
                            (q) =>
                                !used.has(q.id) &&
                                !isDemographicQuestion(q) &&
                                preferredCats.has(q.category || ''),
                        ),
                    ),
                );

                for (const q of leftoverPreferred) {
                    if (scoredPool.length >= scoredTarget) {
                        break;
                    }

                    scoredPool.push(q);
                    used.add(q.id);
                }

                if (scoredPool.length < scoredTarget) {
                    const anyLeftover = fisherYatesShuffle(
                        sourcePool.filter(
                            (q) =>
                                !used.has(q.id) &&
                                !isDemographicQuestion(q),
                        ),
                    );

                    for (const q of anyLeftover) {
                        if (scoredPool.length >= scoredTarget) {
                            break;
                        }

                        scoredPool.push(q);
                    }
                }
            }

            // CIVIO local mock: demographics OPTIONAL — omit EDQ block so mocks
            // go straight into scored items. Skip button remains in live view for
            // resumed sessions that still contain demographics.
            const includeDemographics = false;

            let finalDemographics: Question[] = [];

            if (includeDemographics) {
                finalDemographics = [...demographicQuestions];

                if (
                    finalDemographics.length <
                    EXAM_CONSTANTS.DEMOGRAPHIC_QUESTION_COUNT
                ) {
                    const needed =
                        EXAM_CONSTANTS.DEMOGRAPHIC_QUESTION_COUNT -
                        finalDemographics.length;
                    const shuffledFallbacks = fisherYatesShuffle(
                        fallbackDemographicQuestions,
                    );
                    finalDemographics = [
                        ...finalDemographics,
                        ...shuffledFallbacks.slice(0, needed),
                    ];
                } else if (
                    finalDemographics.length >
                    EXAM_CONSTANTS.DEMOGRAPHIC_QUESTION_COUNT
                ) {
                    finalDemographics = fisherYatesShuffle(
                        finalDemographics,
                    ).slice(0, EXAM_CONSTANTS.DEMOGRAPHIC_QUESTION_COUNT);
                }

                finalDemographics = fisherYatesShuffle(finalDemographics);
            }

            const guestWeakCategories =
                examId === 1 || examId === 2
                    ? (readGuestStudyBias()[
                          getTrackNameForExam(examId) as
                              | 'Professional'
                              | 'Subprofessional'
                      ]?.weakCategories ?? [])
                    : [];
            const biasedScored = raiseWeakCategoryShare(
                scoredPool,
                sourcePool,
                guestWeakCategories,
                scoredTarget,
            );

            // Extra full Fisher-Yates on final scored pool (crypto-backed when available)
            const shuffledScored = fisherYatesShuffle(biasedScored);
            const finalPool = [...finalDemographics, ...shuffledScored];

            return finalPool.map(shuffleOptionsForQuestion);
        },
        [
            questions,
            fallbackQuestions,
            demographicQuestions,
            getSeenIdsForExam,
            getWrongIdsForExam,
            getTrackNameForExam,
        ],
    );

    return {
        buildFreshExamPool,
        demographicQuestions,
        fallbackQuestions,
    };
}

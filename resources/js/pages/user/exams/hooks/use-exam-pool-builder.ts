import { useCallback, useMemo } from 'react';
import { fallbackDemographicQuestions } from '@/data/fallback-demographics';
import { readGuestStudyBias } from '@/lib/guest-study-bias';
import type { Question } from '../types';
import {
    fisherYatesShuffle,
    isDemographicQuestion,
    EXAM_CONSTANTS,
} from '../utils/exam-utils';
import {
    buildMockScoredPool,
    shuffleOptionsForQuestion,
} from '../utils/mock-pool';

export { shuffleOptionsForQuestion };

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
            const guestBias =
                examId === 1 || examId === 2
                    ? readGuestStudyBias()[
                          getTrackNameForExam(examId) as
                              | 'Professional'
                              | 'Subprofessional'
                      ]
                    : undefined;

            // Unique items only (no "(variant N)" clones, no padding). A short
            // bank gives a shorter mock; beginExamSession tells the user.
            const { items: scoredItems } = buildMockScoredPool(
                sourcePool,
                examId,
                {
                    seenIds: getSeenIdsForExam(examId),
                    wrongIds: getWrongIdsForExam(examId),
                    weakSubcategories: guestBias?.weakSubcategories ?? [],
                    weakCategories: guestBias?.weakCategories ?? [],
                },
            );

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

            const finalPool = [...finalDemographics, ...scoredItems];

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

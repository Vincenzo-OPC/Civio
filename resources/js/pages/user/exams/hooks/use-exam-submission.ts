import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { useGuestUnlimited } from '@/lib/civio-study';
import {
    recordGuestStudyBias,
    studyBiasInputFromServer,
    studyTrackForExam,
} from '@/lib/guest-study-bias';
import type { Question, ExamResults, CategoryScore } from '../types';
import { isDemographicQuestion, apiPost } from '../utils/exam-utils';

interface UseExamSubmissionProps {
    activeQuestions: Question[];
    answers: Record<number, number>;
    flagged?: Record<number, boolean>;
    questionTimes: Record<number, number>;
    answerChanges: Record<number, number>;
    selectedExamId: number | null;
    /** Server-side mock session (Lite L1); null for drills and retakes. */
    examSessionId?: string | null;
    isTimed: boolean;
    sessionTimeLimitSecs: number;
    timeLeft: number;
    drillCategoryId: number | null;
    drillCategoryName: string | null;
    drillSubcategories: string[];
    drillLanguage: string;
    drillQuestionCount: number | 'all';
    isFreeAttempt: boolean;
    setShowRegisterModal: (val: boolean) => void;
    setIsExamSubmitted: (val: boolean) => void;
    setIsExamActive: (val: boolean) => void;
    setResults: (val: ExamResults | null) => void;
    setSubmittedByTimer: (val: boolean) => void;
}

export function useExamSubmission({
    activeQuestions,
    answers,
    flagged = {},
    questionTimes,
    answerChanges,
    selectedExamId,
    examSessionId = null,
    isTimed,
    sessionTimeLimitSecs,
    timeLeft,
    drillCategoryId,
    drillCategoryName,
    drillSubcategories,
    drillLanguage,
    drillQuestionCount,
    isFreeAttempt,
    setShowRegisterModal,
    setIsExamSubmitted,
    setIsExamActive,
    setResults,
    setSubmittedByTimer,
}: UseExamSubmissionProps) {
    const guestUnlimited = useGuestUnlimited();
    const [lastStoredAttemptId, setLastStoredAttemptId] = useState<
        number | null
    >(null);

    const [confirmModal, setConfirmModal] = useState<{
        isOpen: boolean;
        title: string;
        message: string;
        confirmLabel: string;
        variant: 'success' | 'danger';
        onConfirm: () => void;
    }>({
        isOpen: false,
        title: '',
        message: '',
        confirmLabel: '',
        variant: 'success',
        onConfirm: () => {},
    });

    const executeSubmit = useCallback(
        (autoByTimer = false) => {
            // Local study / CIVIO: guests may submit & see scorecard when unlimited.
            if (isFreeAttempt && !guestUnlimited) {
                setShowRegisterModal(true);

                return;
            }

            // Build ID-keyed answers using original (bank) option indexes, not shuffled positions.
            const answersByQuestionId: Record<number, number> = {};
            activeQuestions.forEach((q, idx) => {
                const chosen = answers[idx];

                if (chosen === undefined || chosen === null) {
                    return;
                }

                const originalIndex =
                    q.originalOptionIndices?.[Number(chosen)] ?? Number(chosen);
                answersByQuestionId[q.id] = originalIndex;
            });

            // Optimistic local tally only when keys are present (scorecard reload / review).
            // Authoritative score always comes from the server response.
            let correctCount = 0;
            let wrongCount = 0;
            let skippedCount = 0;
            const catMap: Record<string, CategoryScore> = {};
            const keysAvailable = activeQuestions.some(
                (q) => typeof q.correct_option === 'number',
            );

            activeQuestions.forEach((q, idx) => {
                const isDemographic = isDemographicQuestion(q);

                if (isDemographic) {
                    return;
                }

                const catName = q.category || 'General Information';
                const subcatName = q.subcategory || 'General Concepts';

                if (!catMap[catName]) {
                    catMap[catName] = { correct: 0, total: 0, subcats: {} };
                }

                if (!catMap[catName].subcats[subcatName]) {
                    catMap[catName].subcats[subcatName] = {
                        correct: 0,
                        total: 0,
                    };
                }

                catMap[catName].total += 1;
                catMap[catName].subcats[subcatName].total += 1;

                const chosenShuffled = answers[idx];
                const chosenOriginal =
                    chosenShuffled === undefined || chosenShuffled === null
                        ? undefined
                        : (q.originalOptionIndices?.[Number(chosenShuffled)] ??
                          Number(chosenShuffled));

                if (chosenOriginal === undefined) {
                    skippedCount += 1;
                } else if (
                    keysAvailable &&
                    Number(chosenOriginal) === Number(q.correct_option)
                ) {
                    correctCount += 1;
                    catMap[catName].correct += 1;
                    catMap[catName].subcats[subcatName].correct += 1;
                } else if (keysAvailable) {
                    wrongCount += 1;
                }
                // Keys withheld: leave counts for the server to fill in.
            });

            const totalScoredQuestions =
                correctCount + wrongCount + skippedCount ||
                activeQuestions.filter((q) => !isDemographicQuestion(q)).length;
            const scorePercentage =
                keysAvailable && totalScoredQuestions > 0
                    ? Math.round((correctCount / totalScoredQuestions) * 100)
                    : 0;
            const elapsedSecs = isTimed
                ? Math.max(0, sessionTimeLimitSecs - timeLeft)
                : timeLeft;

            const computedResults: ExamResults = {
                score: scorePercentage,
                total: totalScoredQuestions,
                percentage: scorePercentage,
                correctCount,
                wrongCount,
                skippedCount,
                categoryScoreMap: catMap,
                elapsedSecs,
            };

            setResults(computedResults);
            // Study bias is recorded only from the server's grading below:
            // answer keys are withheld in live play, so a local tally here
            // would mark every answered item as a miss.
            const studyTrack = studyTrackForExam(selectedExamId);

            setIsExamSubmitted(true);
            setIsExamActive(false);
            setSubmittedByTimer(autoByTimer);

            // Save active session cleanup
            if (typeof window !== 'undefined') {
                localStorage.removeItem('active_exam_session');
                localStorage.removeItem('active_exam_session_v1');
            }

            const payload = {
                category_id: drillCategoryId ?? selectedExamId,
                exam_session_id: examSessionId,
                question_ids: activeQuestions.map((q) => q.id),
                answers: answersByQuestionId,
                metadata: {
                    track:
                        selectedExamId === 1
                            ? 'Professional'
                            : selectedExamId === 2
                              ? 'Subprofessional'
                              : 'Drill',
                    category_name:
                        drillCategoryName || 'Civil Service Examination',
                    duration_secs: elapsedSecs,
                    is_timed: isTimed,
                    question_times: questionTimes,
                    answer_changes: answerChanges,
                    selected_subcategories: drillSubcategories,
                    language: drillLanguage,
                    question_count: drillQuestionCount,
                },
            };

                        apiPost('/exams/attempts', payload)
                .then((data: any) => {
                    if (data?.attempt_id) {
                        setLastStoredAttemptId(data.attempt_id);
                    }

                    const biasInput = studyBiasInputFromServer(data);

                    if (biasInput) {
                        // Tutor loop: misses and weak topics feed the next
                        // mock / drill pool (stored per track in this browser).
                        recordGuestStudyBias(studyTrack, biasInput);
                    }

                    if (data?.success && typeof data.score === 'number') {
                        const serverMap = data.cat_scores?.categoryScoreMap ?? catMap;
                        setResults({
                            score: data.score,
                            total: data.total_questions ?? totalScoredQuestions,
                            percentage: data.score,
                            correctCount: data.correct_count ?? correctCount,
                            wrongCount: data.wrong_count ?? wrongCount,
                            skippedCount: data.skipped_count ?? skippedCount,
                            categoryScoreMap: serverMap,
                            elapsedSecs,
                        });
                    }

                    if (Array.isArray(data?.answer_keys)) {
                        // Merge withheld keys into in-memory questions for review UI.
                        const keyById = new Map<
                            number,
                            { correct_option: number; explanation: string }
                        >(
                            data.answer_keys.map(
                                (k: {
                                    id: number;
                                    correct_option: number;
                                    explanation: string;
                                }) => [
                                    k.id,
                                    {
                                        correct_option: k.correct_option,
                                        explanation: k.explanation ?? '',
                                    },
                                ],
                            ),
                        );

                        // Notify via custom event — exam state listens and patches activeQuestions.
                        if (typeof window !== 'undefined') {
                            window.dispatchEvent(
                                new CustomEvent('civio:exam-answer-keys', {
                                    detail: {
                                        keys: Object.fromEntries(keyById),
                                        answers: data.answers ?? answersByQuestionId,
                                    },
                                }),
                            );
                        }
                    }
                })
                .catch(() => {
                    toast.error(
                        'Session finished locally, but server sync failed. Progress saved.',
                    );
                });
        },
        [
            activeQuestions,
            answers,
            questionTimes,
            answerChanges,
            selectedExamId,
            examSessionId,
            isTimed,
            sessionTimeLimitSecs,
            timeLeft,
            drillCategoryId,
            drillCategoryName,
            drillSubcategories,
            drillLanguage,
            drillQuestionCount,
            isFreeAttempt,
            guestUnlimited,
            setShowRegisterModal,
            setIsExamSubmitted,
            setIsExamActive,
            setResults,
            setSubmittedByTimer,
        ],
    );

    const handleSubmitExam = useCallback(
        (autoByTimer = false) => {
            if (autoByTimer) {
                executeSubmit(true);

                return;
            }

            let scoredTotal = 0;
            let answeredCount = 0;
            let flaggedCount = 0;

            activeQuestions.forEach((q, idx) => {
                if (isDemographicQuestion(q)) {
                    return;
                }

                scoredTotal++;

                if (answers[idx] !== undefined && answers[idx] !== null) {
                    answeredCount++;
                }

                if (flagged[idx]) {
                    flaggedCount++;
                }
            });

            const unansweredCount = Math.max(0, scoredTotal - answeredCount);

            const title =
                unansweredCount > 0
                    ? 'Submit Exam with Unanswered Questions?'
                    : 'Submit Examination?';

            let message = `You have answered ${answeredCount} of ${scoredTotal} graded questions.`;

            if (unansweredCount > 0) {
                message += ` ⚠️ ${unansweredCount} question${unansweredCount > 1 ? 's are' : ' is'} left unanswered.`;
            }

            if (flaggedCount > 0) {
                message += ` You also have ${flaggedCount} item${flaggedCount > 1 ? 's' : ''} flagged for review.`;
            }

            message +=
                ' Once submitted, your exam will be finalized and graded immediately.';

            setConfirmModal({
                isOpen: true,
                title,
                message,
                confirmLabel:
                    unansweredCount > 0 ? 'Submit Anyway' : 'Submit Exam',
                variant: unansweredCount > 0 ? 'danger' : 'success',
                onConfirm: () => executeSubmit(false),
            });
        },
        [activeQuestions, answers, flagged, executeSubmit],
    );

    return {
        executeSubmit,
        handleSubmitExam,
        confirmModal,
        setConfirmModal,
        lastStoredAttemptId,
    };
}


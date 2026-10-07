import { useEffect, useCallback } from 'react';
import type { Question } from '../types';
import { isDemographicQuestion } from '../utils/exam-utils';

const PERSISTENCE_KEY = 'active_exam_session_v1';

function remapIndexedRecord<T>(
    record: Record<number, T> | undefined,
    oldQuestions: Question[],
    newQuestions: Question[],
): Record<number, T> {
    const remapped: Record<number, T> = {};

    newQuestions.forEach((question, newIdx) => {
        const oldIdx = oldQuestions.findIndex((q) => q.id === question.id);

        if (oldIdx >= 0 && record?.[oldIdx] !== undefined) {
            remapped[newIdx] = record[oldIdx];
        }
    });

    return remapped;
}

export interface ActiveSessionData {
    selectedExamId: number | null;
    /** Server-side mock session (Lite L1), so a resumed mock still submits. */
    examSessionId?: string | null;
    activeQuestions: Question[];
    currentIdx: number;
    answers: Record<number, number>;
    questionTimes: Record<number, number>;
    answerChanges: Record<number, number>;
    flagged: Record<number, boolean>;
    scratchpads?: Record<number, string>;
    sessionTimeLimitSecs: number;
    timeLeft: number;
    isTimed: boolean;
    timestamp: number;
}

interface UseExamPersistenceProps {
    isExamActive: boolean;
    isExamSubmitted: boolean;
    selectedExamId: number | null;
    examSessionId?: string | null;
    activeQuestions: Question[];
    currentIdx: number;
    answers: Record<number, number>;
    questionTimes: Record<number, number>;
    answerChanges: Record<number, number>;
    flagged: Record<number, boolean>;
    scratchpads?: Record<number, string>;
    sessionTimeLimitSecs: number;
    timeLeft: number;
    isTimed: boolean;
    onRestoreSession: (data: ActiveSessionData) => void;
}

export function useExamPersistence({
    isExamActive,
    isExamSubmitted,
    selectedExamId,
    examSessionId = null,
    activeQuestions,
    currentIdx,
    answers,
    questionTimes,
    answerChanges,
    flagged,
    scratchpads,
    sessionTimeLimitSecs,
    timeLeft,
    isTimed,
    onRestoreSession,
}: UseExamPersistenceProps) {
    const saveSession = useCallback(() => {
        if (!isExamActive || isExamSubmitted || activeQuestions.length === 0) {
            return;
        }

        const scoredQuestions = activeQuestions.filter(
            (q) => !isDemographicQuestion(q),
        );
        const sessionData: ActiveSessionData = {
            selectedExamId,
            examSessionId,
            activeQuestions: scoredQuestions,
            currentIdx: Math.min(currentIdx, Math.max(0, scoredQuestions.length - 1)),
            answers: remapIndexedRecord(answers, activeQuestions, scoredQuestions),
            questionTimes: remapIndexedRecord(questionTimes, activeQuestions, scoredQuestions),
            answerChanges: remapIndexedRecord(answerChanges, activeQuestions, scoredQuestions),
            flagged: remapIndexedRecord(flagged, activeQuestions, scoredQuestions),
            scratchpads: remapIndexedRecord(scratchpads, activeQuestions, scoredQuestions),
            sessionTimeLimitSecs,
            timeLeft,
            isTimed,
            timestamp: Date.now(),
        };

        try {
            localStorage.setItem(PERSISTENCE_KEY, JSON.stringify(sessionData));
        } catch {
            /* storage limit error safeguard */
        }
    }, [
        isExamActive,
        isExamSubmitted,
        selectedExamId,
        examSessionId,
        activeQuestions,
        currentIdx,
        answers,
        questionTimes,
        answerChanges,
        flagged,
        scratchpads,
        sessionTimeLimitSecs,
        timeLeft,
        isTimed,
    ]);

    const clearSession = useCallback(() => {
        try {
            localStorage.removeItem(PERSISTENCE_KEY);
        } catch {
            /* storage safeguard */
        }
    }, []);

    // Check for crash recovery on initial mount
    useEffect(() => {
        try {
            const rawData = localStorage.getItem(PERSISTENCE_KEY);

            if (!rawData) {
                return;
            }

            const data: ActiveSessionData = JSON.parse(rawData);
            // LOCAL study: keep crash/shutdown resume for 30 days (was 12 hours)
            const maxAgeMs = 30 * 24 * 60 * 60 * 1000;

            if (Date.now() - data.timestamp > maxAgeMs) {
                clearSession();

                return;
            }

            if (data.activeQuestions && data.activeQuestions.length > 0) {
                // Local CIVIO study: never resume Demographic Profile / EDQ items.
                const scoredOnly = data.activeQuestions.filter(
                    (q) => !isDemographicQuestion(q),
                );

                if (scoredOnly.length === 0) {
                    localStorage.removeItem(PERSISTENCE_KEY);

                    return;
                }

                const remappedAnswers: Record<number, number> = {};
                const remappedTimes: Record<number, number> = {};
                const remappedChanges: Record<number, number> = {};
                const remappedFlagged: Record<number, boolean> = {};
                const remappedScratch: Record<number, string> = {};
                const oldQs = data.activeQuestions;
                scoredOnly.forEach((q, newIdx) => {
                    const oldIdx = oldQs.findIndex((oq) => oq.id === q.id);

                    if (oldIdx < 0) {
return;
}

                    if (data.answers?.[oldIdx] !== undefined) {
                        remappedAnswers[newIdx] = data.answers[oldIdx];
                    }

                    if (data.questionTimes?.[oldIdx] !== undefined) {
                        remappedTimes[newIdx] = data.questionTimes[oldIdx];
                    }

                    if (data.answerChanges?.[oldIdx] !== undefined) {
                        remappedChanges[newIdx] = data.answerChanges[oldIdx];
                    }

                    if (data.flagged?.[oldIdx]) {
                        remappedFlagged[newIdx] = true;
                    }

                    if (data.scratchpads?.[oldIdx] !== undefined) {
                        remappedScratch[newIdx] = data.scratchpads[oldIdx];
                    }
                });
                const firstUnanswered = scoredOnly.findIndex(
                    (_, i) => remappedAnswers[i] === undefined,
                );
                onRestoreSession({
                    ...data,
                    activeQuestions: scoredOnly,
                    answers: remappedAnswers,
                    questionTimes: remappedTimes,
                    answerChanges: remappedChanges,
                    flagged: remappedFlagged,
                    scratchpads: remappedScratch,
                    currentIdx:
                        firstUnanswered >= 0
                            ? firstUnanswered
                            : Math.min(
                                  data.currentIdx || 0,
                                  scoredOnly.length - 1,
                              ),
                });
            }
        } catch {
            clearSession();
        }
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    // Auto-save on answer change or interval
    useEffect(() => {
        if (isExamActive && !isExamSubmitted) {
            saveSession();
        }
    }, [
        answers,
        currentIdx,
        flagged,
        isExamActive,
        isExamSubmitted,
        saveSession,
    ]);

    // Interval save every 30s
    useEffect(() => {
        if (!isExamActive || isExamSubmitted) {
            return;
        }

        const interval = setInterval(() => {
            saveSession();
        }, 30000);

        return () => clearInterval(interval);
    }, [isExamActive, isExamSubmitted, saveSession]);


    // Flush to localStorage on tab close / PC sleep so progress survives shutdown
    useEffect(() => {
        if (!isExamActive || isExamSubmitted) {
            return;
        }

        const flush = () => {
            saveSession();
        };

        window.addEventListener('pagehide', flush);
        window.addEventListener('beforeunload', flush);
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'hidden') {
                flush();
            }
        });

        return () => {
            window.removeEventListener('pagehide', flush);
            window.removeEventListener('beforeunload', flush);
        };
    }, [isExamActive, isExamSubmitted, saveSession]);

    return {
        saveSession,
        clearSession,
    };
}

import { useCallback, useEffect, useRef, useState } from 'react';
import type { Dispatch, SetStateAction } from 'react';
import { toast } from 'sonner';
import type { Question } from '../types';
import { restoreAnswerPositions } from '../utils/answer-state';
import { apiPost } from '../utils/exam-utils';
import { localDeadline } from '../utils/server-clock';

interface Progress {
    deadline_at: string | null;
    server_now: string;
    answers: Record<string, number | null>;
    save_version: number;
    submitted: boolean;
}

export function useServerExamProgress(
    sessionId: string | null,
    enabled: boolean,
    questions: Question[],
    setAnswers: Dispatch<SetStateAction<Record<number, number>>>,
) {
    const [readyId, setReadyId] = useState<string | null>(null);
    const [deadline, setDeadline] = useState<number | null>(null);
    const version = useRef(0);
    const generation = useRef(0);
    const canSave = useRef(false);
    const queue = useRef<Promise<void>>(Promise.resolve());

    useEffect(() => {
        const current = ++generation.current;
        canSave.current = false;

        if (!enabled || !sessionId) {
            return;
        }

        queue.current = Promise.resolve();
        const requestedAt = Date.now();
        void apiPost<Progress>('/exams/sessions/progress', {
            exam_session_id: sessionId,
        })
            .then((data) => {
                if (generation.current !== current) {
                    return;
                }

                if (data.submitted) {
                    toast.error('Mock submitted. Open its scorecard.');

                    return;
                }

                version.current = data.save_version;
                setAnswers(restoreAnswerPositions(questions, data.answers));
                setDeadline(
                    data.deadline_at
                        ? localDeadline(
                              data.deadline_at,
                              data.server_now,
                              requestedAt,
                          )
                        : null,
                );
                canSave.current = true;
                setReadyId(sessionId);
            })
            .catch(() =>
                toast.error('Reconnect and reload to recover saved answers.'),
            );

        return () => {
            generation.current = current + 1;
            canSave.current = false;
        };
    }, [sessionId, enabled, questions, setAnswers]);

    const saveAnswer = useCallback(
        (question: Question, chosen: number | null) => {
            if (!enabled || !sessionId || !canSave.current) {
                return;
            }

            const current = generation.current;
            const original =
                chosen === null
                    ? null
                    : (question.originalOptionIndices?.[chosen] ?? chosen);
            queue.current = queue.current
                .then(async () => {
                    if (!canSave.current || generation.current !== current) {
                        return;
                    }

                    const data = await apiPost<Progress>(
                        '/exams/sessions/progress',
                        {
                            exam_session_id: sessionId,
                            expected_version: version.current,
                            answers: { [question.id]: original },
                        },
                    );

                    if (generation.current === current) {
                        version.current = data.save_version;
                    }
                })
                .catch(() => {
                    if (generation.current !== current) {
                        return;
                    }

                    canSave.current = false;
                    setReadyId(null);
                    toast.error(
                        'Save failed. Reload to recover server answers. Late submission uses saved answers only.',
                    );
                });
        },
        [enabled, sessionId],
    );

    return {
        ready: enabled ? readyId === sessionId : true,
        deadline: enabled ? deadline : null,
        saveAnswer,
    };
}

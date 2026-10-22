import { useCallback, useEffect, useRef, useState } from 'react';
import type { Dispatch, SetStateAction } from 'react';
import { toast } from 'sonner';
import type { Question } from '../types';
import { restoreAnswerPositions } from '../utils/answer-state';
import { apiPost } from '../utils/exam-utils';
import type { ProgressPost, SaveState } from '../utils/progress-save';
import { localDeadline } from '../utils/server-clock';

interface Progress {
    deadline_at: string | null;
    server_now: string;
    answers: Record<string, number | null>;
    save_version: number;
    submitted: boolean;
}

function forgetLocalSession(): void {
    try {
        localStorage.removeItem('active_exam_session_v1');
    } catch {
        /* storage unavailable */
    }
}

export function useServerExamProgress(
    sessionId: string | null,
    enabled: boolean,
    questions: Question[],
    setAnswers: Dispatch<SetStateAction<Record<number, number>>>,
    onSubmitted?: () => void,
) {
    const [readyId, setReadyId] = useState<string | null>(null);
    const [deadline, setDeadline] = useState<number | null>(null);
    const version = useRef(0);
    const generation = useRef(0);
    const canSave = useRef(false);
    const queue = useRef<Promise<void>>(Promise.resolve());
    const questionsRef = useRef(questions);
    const onSubmittedRef = useRef(onSubmitted);
    useEffect(() => {
        questionsRef.current = questions;
        onSubmittedRef.current = onSubmitted;
    });

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
                    forgetLocalSession();
                    onSubmittedRef.current?.();
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

    // Answers the server has not confirmed because the connection dropped.
    // Kept per item (latest choice wins) and resent on reconnect.
    // Items reported withdrawn are never resent.
    const [state] = useState<SaveState>(() => ({
        pending: new Map(),
        withdrawnIds: new Set(),
        offline: { current: false },
    }));

    const send = useCallback(
        (batch: Record<number, number | null>) => {
            if (!enabled || !sessionId || !canSave.current) {
                return;
            }

            const current = generation.current;
            queue.current = queue.current
                .then(async () => {
                    if (!canSave.current || generation.current !== current) {
                        return;
                    }

                    const post: ProgressPost = (payload) =>
                        apiPost<Progress>('/exams/sessions/progress', payload);
                    // Loaded on first save so the exam chunk stays in budget.
                    const save = await import('../utils/progress-save');
                    const answers = save.withoutWithdrawn(
                        batch,
                        state.withdrawnIds,
                    );

                    if (Object.keys(answers).length === 0) {
                        return;
                    }

                    const outcome = await save.saveProgressPatch(
                        post,
                        sessionId,
                        answers,
                        version.current,
                    );

                    if (generation.current !== current) {
                        return;
                    }

                    const next = save.settleSave(outcome, answers, state, {
                        setAnswers,
                        hydrate: (server) =>
                            setAnswers(
                                restoreAnswerPositions(
                                    questionsRef.current,
                                    server,
                                ),
                            ),
                        notify: (level, message) => toast[level](message),
                        closed: (submitted) => {
                            canSave.current = false;

                            if (submitted) {
                                forgetLocalSession();
                                onSubmittedRef.current?.();
                            }
                        },
                    });

                    if (next !== null) {
                        version.current = next;
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
        [enabled, sessionId, setAnswers, state],
    );

    const saveAnswer = useCallback(
        (question: Question, chosen: number | null) => {
            const original =
                chosen === null
                    ? null
                    : (question.originalOptionIndices?.[chosen] ?? chosen);

            if (state.pending.has(question.id)) {
                state.pending.set(question.id, original);
            }

            send({ [question.id]: original });
        },
        [send, state],
    );

    useEffect(() => {
        if (!enabled || !sessionId) {
            return;
        }

        const flush = () => {
            // One patch for everything held while offline. It may mix active
            // and withdrawn items; the server saves the active ones.
            if (state.pending.size > 0) {
                send(Object.fromEntries(state.pending));
            }
        };
        window.addEventListener('online', flush);
        const timer = window.setInterval(() => {
            if (state.pending.size > 0) {
                flush();
            }
        }, 20000);

        return () => {
            window.removeEventListener('online', flush);
            window.clearInterval(timer);
            state.pending.clear();
            state.withdrawnIds.clear();
            state.offline.current = false;
        };
    }, [enabled, sessionId, send, state]);

    return {
        ready: enabled ? readyId === sessionId : true,
        deadline: enabled ? deadline : null,
        saveAnswer,
    };
}

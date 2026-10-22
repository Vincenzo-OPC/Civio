import { useState, useEffect, useRef, useCallback } from 'react';
import type { SetStateAction } from 'react';
import { toast } from 'sonner';
import { shouldRunExamClock } from '../utils/answer-state';
import { secondsUntil } from '../utils/server-clock';

export interface ExamClockSnapshot {
    timeLeft: number;
    itemElapsed: number;
}

interface UseExamTimerProps {
    isExamActive: boolean;
    isExamSubmitted: boolean;
    isTimed: boolean;
    sessionTimeLimitSecs: number;
    currentIdx: number;
    isPaused?: boolean;
    onTimerExpired: () => void;
    deadlineMs?: number | null;
}

/**
 * The visible clocks subscribe to a snapshot. React state is flushed every
 * 15 seconds so a tick does not re-render the question paper or rewrite
 * localStorage. Submit and recovery read the refs, which stay current.
 */
export function useExamTimer({
    isExamActive,
    isExamSubmitted,
    isTimed,
    sessionTimeLimitSecs,
    currentIdx,
    isPaused = false,
    onTimerExpired,
    deadlineMs = null,
}: UseExamTimerProps) {
    const [timeLeft, setTimeLeftState] = useState(sessionTimeLimitSecs);
    const [questionTimes, setQuestionTimesState] = useState<
        Record<number, number>
    >({});
    const [itemElapsed, setItemElapsed] = useState(0);
    const timeLeftRef = useRef(sessionTimeLimitSecs);
    const questionTimesRef = useRef<Record<number, number>>({});
    const currentIdxRef = useRef(currentIdx);
    const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
    const warned10MinRef = useRef(false);
    const warned1MinRef = useRef(false);
    const listenersRef = useRef(new Set<() => void>());
    const snapshotRef = useRef<ExamClockSnapshot>({
        timeLeft: sessionTimeLimitSecs,
        itemElapsed: 0,
    });

    const publishClock = useCallback(
        (nextLeft: number, nextElapsed: number) => {
            timeLeftRef.current = nextLeft;
            snapshotRef.current = {
                timeLeft: nextLeft,
                itemElapsed: nextElapsed,
            };
            listenersRef.current.forEach((listener) => listener());
        },
        [],
    );

    const subscribeClock = useCallback((listener: () => void) => {
        listenersRef.current.add(listener);

        return () => {
            listenersRef.current.delete(listener);
        };
    }, []);

    const getClockSnapshot = useCallback(() => snapshotRef.current, []);

    const setTimeLeft = useCallback(
        (value: SetStateAction<number>) => {
            const next =
                typeof value === 'function'
                    ? value(timeLeftRef.current)
                    : value;
            publishClock(next, snapshotRef.current.itemElapsed);
            setTimeLeftState(next);
        },
        [publishClock],
    );

    const setQuestionTimes = useCallback(
        (value: SetStateAction<Record<number, number>>) => {
            setQuestionTimesState((prev) => {
                const next = typeof value === 'function' ? value(prev) : value;
                questionTimesRef.current = { ...next };

                return next;
            });
        },
        [],
    );

    useEffect(() => {
        currentIdxRef.current = currentIdx;
    }, [currentIdx]);

    // Visible per-item clock. Resets on next, previous, or palette.
    // questionTimes stays cumulative for submit analytics.
    const itemIdxRef = useRef(currentIdx);
    useEffect(() => {
        if (itemIdxRef.current !== currentIdx) {
            itemIdxRef.current = currentIdx;
            publishClock(timeLeftRef.current, 0);
            setItemElapsed(0);
        }
    }, [currentIdx, publishClock]);

    const resetTimer = useCallback(
        (newLimitSecs: number) => {
            warned10MinRef.current = false;
            warned1MinRef.current = false;
            publishClock(newLimitSecs, 0);
            setTimeLeftState(newLimitSecs);
            setItemElapsed(0);
        },
        [publishClock],
    );

    // Live countdown timer & per-question time tracking.
    // One interval. It updates refs and the clock snapshot only.
    useEffect(() => {
        if (
            !shouldRunExamClock({
                isExamActive,
                isExamSubmitted,
                isPaused: deadlineMs !== null ? false : isPaused,
            })
        ) {
            return;
        }

        let ticks = 0;
        timerRef.current = setInterval(() => {
            const activeIdx = currentIdxRef.current;
            const times = questionTimesRef.current;
            times[activeIdx] = (times[activeIdx] || 0) + 1;
            const nextElapsed = snapshotRef.current.itemElapsed + 1;
            ticks += 1;

            const flush = (nextLeft: number, elapsed: number) => {
                setTimeLeftState(nextLeft);
                setItemElapsed(elapsed);
                setQuestionTimesState({ ...questionTimesRef.current });
            };

            if (isTimed) {
                const prev =
                    deadlineMs !== null
                        ? secondsUntil(deadlineMs, Date.now())
                        : timeLeftRef.current;

                if (prev <= (deadlineMs !== null ? 0 : 1)) {
                    if (timerRef.current) {
                        clearInterval(timerRef.current);
                    }

                    publishClock(0, nextElapsed);
                    flush(0, nextElapsed);
                    onTimerExpired();

                    return;
                }

                const next = deadlineMs !== null ? prev : prev - 1;
                publishClock(next, nextElapsed);

                if (next === 600 && !warned10MinRef.current) {
                    warned10MinRef.current = true;
                    toast.warning('10 minutes remaining in this session.', {
                        id: 'timer-warning-10m',
                    });
                } else if (next === 60 && !warned1MinRef.current) {
                    warned1MinRef.current = true;
                    toast.error(
                        '1 minute remaining! Your exam will auto-submit soon.',
                        {
                            id: 'timer-warning-1m',
                            duration: 10000,
                        },
                    );
                }

                if (ticks % 15 === 0) {
                    flush(next, nextElapsed);
                }
            } else {
                const next = timeLeftRef.current + 1;
                publishClock(next, nextElapsed);

                if (ticks % 15 === 0) {
                    flush(next, nextElapsed);
                }
            }
        }, 1000);

        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }

            // Pause, submit, or leave: keep React state aligned with the refs.
            setTimeLeftState(timeLeftRef.current);
            setItemElapsed(snapshotRef.current.itemElapsed);
            setQuestionTimesState({ ...questionTimesRef.current });
        };
    }, [
        isExamActive,
        isExamSubmitted,
        isTimed,
        isPaused,
        onTimerExpired,
        deadlineMs,
        publishClock,
    ]);

    const formatTime = useCallback((secs: number) => {
        const h = Math.floor(secs / 3600);
        const m = Math.floor((secs % 3600) / 60);
        const s = secs % 60;

        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }, []);

    return {
        timeLeft,
        setTimeLeft,
        questionTimes,
        setQuestionTimes,
        itemElapsed,
        formatTime,
        resetTimer,
        timeLeftRef,
        questionTimesRef,
        subscribeClock,
        getClockSnapshot,
    };
}

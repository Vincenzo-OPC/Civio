import { useEffect, useMemo, useState } from 'react';
import type { AiHandoffAttemptState } from '@/lib/ai-handoff';
import { correctDisplayIndex } from '@/lib/offline/grader';
import type { OfflinePackItem } from '@/lib/offline/types';
import { LiteExamBody } from '@/pages/user/exams/components/lite-exam-body';
import type { LiteRevealedAnswer } from '@/pages/user/exams/components/lite-exam-body';
import type { Question } from '@/pages/user/exams/types';

const LETTERS = ['A', 'B', 'C', 'D', 'E'];

export interface OfflineSession {
    title: string;
    items: OfflinePackItem[];
    questions: Question[];
}

interface OfflineDrillRunnerProps {
    session: OfflineSession;
    onFinish: (answers: Record<number, number>) => void;
    onExit: () => void;
}

function formatTime(secs: number): string {
    const m = Math.floor(secs / 60);
    const s = secs % 60;

    return `${m}:${String(s).padStart(2, '0')}`;
}

/**
 * Offline drill: the Lite drill screen, graded on the device. Reveal shows the
 * pack's key and explanation; Copy for AI works as in online drills.
 */
export function OfflineDrillRunner({
    session,
    onFinish,
    onExit,
}: OfflineDrillRunnerProps) {
    const { items, questions, title } = session;
    const [currentIdx, setCurrentIdx] = useState(0);
    const [answers, setAnswers] = useState<Record<number, number>>({});
    const [flagged, setFlagged] = useState<Record<number, boolean>>({});
    const [revealedIdx, setRevealedIdx] = useState<Record<number, boolean>>({});
    const [itemStart, setItemStart] = useState(() => Date.now());
    const [now, setNow] = useState(() => Date.now());

    useEffect(() => {
        const timer = window.setInterval(() => setNow(Date.now()), 1000);

        return () => window.clearInterval(timer);
    }, []);

    const itemElapsed = Math.max(0, Math.floor((now - itemStart) / 1000));

    const navigate = (idx: number) => {
        const at = Date.now();
        setCurrentIdx(idx);
        setItemStart(at);
        setNow(at);
    };

    const question = questions[currentIdx];
    const item = items[currentIdx];
    const isRevealed = !!revealedIdx[currentIdx];
    const correctIdx =
        question && item ? correctDisplayIndex(question, item) : null;

    const revealed: LiteRevealedAnswer | null =
        isRevealed && question && item && correctIdx !== null
            ? {
                  letter: LETTERS[correctIdx] ?? String(correctIdx + 1),
                  text: question.options[correctIdx] ?? '',
                  explanation: item.explanation || null,
              }
            : null;

    const copyAttempt = useMemo<AiHandoffAttemptState>(
        () => ({
            selectedDisplayIndex: answers[currentIdx] ?? null,
            mode: 'study',
            revealed: isRevealed,
            verifiedCorrectDisplayIndex: isRevealed ? correctIdx : null,
            verifiedExplanation: isRevealed ? item?.explanation || null : null,
            questionNumber: currentIdx + 1,
            totalQuestions: questions.length,
            examLevel: 'Practice',
        }),
        [answers, currentIdx, isRevealed, correctIdx, item, questions.length],
    );

    return (
        <LiteExamBody
            title={title}
            isDrillSession
            question={question}
            questions={questions}
            currentIdx={currentIdx}
            answers={answers}
            flagged={flagged}
            answeredCount={Object.keys(answers).length}
            isTimed={false}
            timeLeft={0}
            itemElapsed={itemElapsed}
            formatTime={formatTime}
            onSelect={(optionIdx) =>
                setAnswers((current) => ({
                    ...current,
                    [currentIdx]: optionIdx,
                }))
            }
            onNavigate={navigate}
            onToggleFlag={(idx) =>
                setFlagged((current) => ({ ...current, [idx]: !current[idx] }))
            }
            onSubmit={() => onFinish(answers)}
            onExit={onExit}
            onReveal={() =>
                setRevealedIdx((current) => ({
                    ...current,
                    [currentIdx]: true,
                }))
            }
            revealed={revealed}
            onHideReveal={() =>
                setRevealedIdx((current) => ({
                    ...current,
                    [currentIdx]: false,
                }))
            }
            copyAttempt={copyAttempt}
        />
    );
}

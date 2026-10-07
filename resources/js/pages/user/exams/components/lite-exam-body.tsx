import { useState } from 'react';
import LiteModeToggle from '@/components/shared/lite-mode-toggle';
import type { AiHandoffAttemptState } from '@/lib/ai-handoff';
import { renderFormattedText } from '@/lib/exam-formatters';
import type { Question } from '../types';
import { CopyForAiButton } from './copy-for-ai-button';

export interface LiteRevealedAnswer {
    letter: string;
    text: string;
    explanation?: string | null;
    hasConflict?: boolean;
}

interface LiteExamBodyProps {
    title: string;
    isDrillSession: boolean;
    question: Question | undefined;
    questions: Question[];
    currentIdx: number;
    answers: Record<number, number>;
    flagged: Record<number, boolean>;
    answeredCount: number;
    isTimed: boolean;
    timeLeft: number;
    itemElapsed: number;
    formatTime: (secs: number) => string;
    onSelect: (optionIdx: number) => void;
    onNavigate: (idx: number) => void;
    onToggleFlag: (idx: number) => void;
    onSubmit: () => void;
    onExit: () => void;
    onReveal: () => void;
    revealed: LiteRevealedAnswer | null;
    onHideReveal: () => void;
    copyAttempt: AiHandoffAttemptState | null;
}

const LETTERS = ['A', 'B', 'C', 'D', 'E'];

/**
 * Lite mode exam / drill screen: question, choices, Reveal, Copy for AI and
 * Next with minimal chrome. The palette sits behind "View all". Same state
 * and handlers as the full view (grading, keys and shuffle mapping unchanged).
 */
export function LiteExamBody({
    title,
    isDrillSession,
    question,
    questions,
    currentIdx,
    answers,
    flagged,
    answeredCount,
    isTimed,
    timeLeft,
    itemElapsed,
    formatTime,
    onSelect,
    onNavigate,
    onToggleFlag,
    onSubmit,
    onExit,
    onReveal,
    revealed,
    onHideReveal,
    copyAttempt,
}: LiteExamBodyProps) {
    const [showAll, setShowAll] = useState(false);
    const total = questions.length;
    const isLast = currentIdx >= total - 1;
    const button =
        'lite-tap rounded-lg border border-border px-4 text-sm font-semibold';

    return (
        <div className="flex flex-1 flex-col overflow-y-auto bg-background p-3 text-foreground sm:p-6">
            <div className="mx-auto flex w-full max-w-2xl flex-col gap-3">
                <div className="flex items-center justify-between gap-2">
                    <button type="button" onClick={onExit} className={button}>
                        Exit
                    </button>
                    <span className="min-w-0 truncate text-sm font-semibold">
                        {title}
                    </span>
                    <LiteModeToggle />
                </div>

                <p className="text-sm" aria-live="off">
                    {isTimed
                        ? `${isDrillSession ? 'Drill' : 'Exam'} left ${formatTime(timeLeft)} · `
                        : ''}
                    This item {formatTime(itemElapsed)}
                </p>
                <p className="text-sm text-muted-foreground">
                    Item {currentIdx + 1} of {total} · {answeredCount} answered
                    {flagged[currentIdx] ? ' · Flagged' : ''}
                </p>

                {question ? (
                    <>
                        <div className="text-base leading-relaxed">
                            {renderFormattedText(question.stem, true)}
                        </div>

                        <div className="flex flex-col gap-2" role="radiogroup">
                            {question.options.map((option, idx) => {
                                const selected = answers[currentIdx] === idx;

                                return (
                                    <button
                                        key={idx}
                                        type="button"
                                        role="radio"
                                        aria-checked={selected}
                                        onClick={() => onSelect(idx)}
                                        className={`lite-tap flex w-full items-start gap-3 rounded-lg border px-4 py-3 text-left text-base ${
                                            selected
                                                ? 'border-blue-600 bg-blue-50 font-semibold dark:bg-blue-950'
                                                : 'border-border'
                                        }`}
                                    >
                                        <span className="font-bold">
                                            {LETTERS[idx] ?? idx + 1}.
                                        </span>
                                        <span>
                                            {renderFormattedText(option, true)}
                                        </span>
                                    </button>
                                );
                            })}
                        </div>

                        <div className="flex flex-wrap gap-2">
                            <button
                                type="button"
                                onClick={onReveal}
                                className={button}
                            >
                                Reveal
                            </button>
                            {copyAttempt && (
                                <CopyForAiButton
                                    question={question}
                                    attempt={copyAttempt}
                                />
                            )}
                            <button
                                type="button"
                                onClick={() => onToggleFlag(currentIdx)}
                                className={button}
                                aria-pressed={!!flagged[currentIdx]}
                            >
                                {flagged[currentIdx] ? 'Unflag' : 'Flag'}
                            </button>
                        </div>

                        {revealed && (
                            <div className="rounded-lg border border-amber-300 p-3 text-sm">
                                <p className="font-bold">
                                    {revealed.hasConflict
                                        ? 'Answer key conflict'
                                        : 'Answer'}
                                    : {revealed.letter}. {revealed.text}
                                </p>
                                {revealed.hasConflict && (
                                    <p>
                                        Dexter detected a possible error in the
                                        stored answer.
                                    </p>
                                )}
                                {revealed.explanation && (
                                    <p className="mt-1">
                                        {revealed.explanation}
                                    </p>
                                )}
                                <button
                                    type="button"
                                    onClick={onHideReveal}
                                    className="mt-2 underline"
                                >
                                    Hide
                                </button>
                            </div>
                        )}
                    </>
                ) : (
                    <p className="text-sm">No item to show.</p>
                )}

                <div className="flex gap-2">
                    <button
                        type="button"
                        onClick={() => onNavigate(Math.max(0, currentIdx - 1))}
                        disabled={currentIdx === 0}
                        className={`${button} flex-1 disabled:opacity-40`}
                    >
                        Previous
                    </button>
                    {isLast ? (
                        <button
                            type="button"
                            onClick={onSubmit}
                            className="lite-tap flex-1 rounded-lg bg-emerald-700 px-4 text-sm font-bold text-white"
                        >
                            Submit
                        </button>
                    ) : (
                        <button
                            type="button"
                            onClick={() => onNavigate(currentIdx + 1)}
                            className="lite-tap flex-1 rounded-lg bg-blue-700 px-4 text-sm font-bold text-white"
                        >
                            Next
                        </button>
                    )}
                </div>

                <button
                    type="button"
                    onClick={() => setShowAll((open) => !open)}
                    aria-expanded={showAll}
                    className={button}
                >
                    {showAll ? 'Hide items' : 'View all'}
                </button>

                {showAll && (
                    <div className="flex flex-col gap-3">
                        <p className="text-xs text-muted-foreground">
                            • answered · F flagged
                        </p>
                        <div className="grid grid-cols-6 gap-1.5 sm:grid-cols-10">
                            {questions.map((q, idx) => (
                                <button
                                    key={q.id}
                                    type="button"
                                    onClick={() => {
                                        onNavigate(idx);
                                        setShowAll(false);
                                    }}
                                    aria-current={
                                        idx === currentIdx ? 'step' : undefined
                                    }
                                    className={`lite-tap rounded border text-xs ${
                                        idx === currentIdx
                                            ? 'border-blue-600 font-bold'
                                            : 'border-border'
                                    }`}
                                >
                                    {idx + 1}
                                    {answers[idx] !== undefined ? '•' : ''}
                                    {flagged[idx] ? 'F' : ''}
                                </button>
                            ))}
                        </div>
                        <button
                            type="button"
                            onClick={onSubmit}
                            className="lite-tap rounded-lg bg-emerald-700 px-4 text-sm font-bold text-white"
                        >
                            Submit now
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

import { useState } from 'react';
import LiteModeToggle from '@/components/shared/lite-mode-toggle';
import { DarkModeToggle } from '@/components/shared/theme-toggle';
import type { AiHandoffAttemptState } from '@/lib/ai-handoff';
import { renderFormattedText } from '@/lib/exam-formatters';
import type { ExamClockSnapshot } from '../hooks/use-exam-timer';
import type { Question } from '../types';
import { answerOptionVisual } from '../utils/answer-state';
import { AskAssistantButton } from './ask-assistant-button';
import { CopyForAiButton } from './copy-for-ai-button';
import { ExamTimerDisplay } from './exam-timer-display';
import { AnswerOption } from './session/answer-option';
import { AnswerReveal } from './session/answer-reveal';
import type { RevealTutorPayload } from './session/answer-reveal';

export interface LiteRevealedAnswer {
    letter: string;
    text: string;
    explanation?: string | null;
    hasConflict?: boolean;
    displayIndex?: number;
    tutor?: RevealTutorPayload | null;
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
    totalSeconds?: number;
    subscribeClock?: (listener: () => void) => () => void;
    getClockSnapshot?: () => ExamClockSnapshot;
    onSelect: (optionIdx: number) => void;
    onNavigate: (idx: number) => void;
    onToggleFlag: (idx: number) => void;
    onSubmit: () => void;
    onExit: () => void;
    /** False in a Strict Mock: no Reveal, Dexter or Copy for AI. */
    showStudyTools?: boolean;
    strict?: boolean;
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
    totalSeconds,
    subscribeClock,
    getClockSnapshot,
    onSelect,
    onNavigate,
    onToggleFlag,
    onSubmit,
    onExit,
    showStudyTools = true,
    strict = false,
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
                        {isDrillSession ? 'Drill' : 'Exam'}
                        <span className="mx-1 text-[var(--civio-ink)]/40">
                            ·
                        </span>
                        {title}
                    </span>
                    <span className="flex shrink-0 items-center gap-2">
                        <DarkModeToggle className="size-9" />
                        <LiteModeToggle />
                    </span>
                </div>

                <ExamTimerDisplay
                    isTimed={isTimed}
                    timeLeft={timeLeft}
                    itemElapsed={itemElapsed}
                    formatTime={formatTime}
                    totalSeconds={totalSeconds}
                    subscribeClock={subscribeClock}
                    getClockSnapshot={getClockSnapshot}
                />
                <p className="text-sm text-[var(--civio-ink)]/70">
                    {currentIdx + 1} of {total}
                    <span className="mx-1.5">·</span>
                    {answeredCount} answered
                    {flagged[currentIdx] ? ' · Flagged' : ''}
                </p>

                {question ? (
                    <>
                        <div className="text-lg leading-relaxed">
                            {renderFormattedText(question.stem, true)}
                        </div>

                        <div className="flex flex-col" role="radiogroup">
                            {question.options.map((option, idx) => {
                                const revealedHere = revealed !== null;
                                const choice = answerOptionVisual({
                                    optionIndex: idx,
                                    selectedIndex: answers[currentIdx],
                                    revealed: revealedHere,
                                    strict,
                                    correctIndex: revealedHere
                                        ? (revealed?.displayIndex ?? null)
                                        : null,
                                });

                                return (
                                    <AnswerOption
                                        key={idx}
                                        letter={LETTERS[idx] ?? String(idx + 1)}
                                        visual={choice.visual}
                                        status={choice.status}
                                        onSelect={() => onSelect(idx)}
                                    >
                                        {renderFormattedText(option, true)}
                                    </AnswerOption>
                                );
                            })}
                        </div>

                        <div className="flex flex-wrap gap-2">
                            {showStudyTools && (
                                <button
                                    type="button"
                                    onClick={() =>
                                        revealed ? onHideReveal() : onReveal()
                                    }
                                    className={
                                        revealed
                                            ? 'civio-action'
                                            : 'civio-action civio-action-primary'
                                    }
                                >
                                    {revealed
                                        ? 'Hide Explanation'
                                        : 'Show Explanation'}
                                </button>
                            )}
                            {showStudyTools && copyAttempt && (
                                <CopyForAiButton
                                    question={question}
                                    attempt={copyAttempt}
                                    className="civio-action"
                                />
                            )}
                            {showStudyTools && copyAttempt && (
                                <AskAssistantButton
                                    question={question}
                                    attempt={copyAttempt}
                                    className="civio-action"
                                />
                            )}
                            <button
                                type="button"
                                onClick={() => onToggleFlag(currentIdx)}
                                className="civio-action"
                                aria-pressed={!!flagged[currentIdx]}
                            >
                                {flagged[currentIdx] ? 'Unflag' : 'Flag'}
                            </button>
                        </div>

                        {showStudyTools && revealed && question && (
                            <AnswerReveal
                                letter={revealed.letter}
                                text={revealed.text}
                                explanation={revealed.explanation}
                                hasConflict={revealed.hasConflict}
                                tutor={revealed.tutor}
                                chosenIndex={answers[currentIdx] ?? null}
                                correctIndex={revealed.displayIndex ?? null}
                                ask={
                                    copyAttempt
                                        ? {
                                              question,
                                              attempt: copyAttempt,
                                          }
                                        : null
                                }
                            />
                        )}
                    </>
                ) : (
                    <p className="text-sm">No item to show.</p>
                )}

                <div className="sticky bottom-0 flex gap-2 bg-[var(--civio-paper)] py-3">
                    <button
                        type="button"
                        onClick={() => onNavigate(Math.max(0, currentIdx - 1))}
                        disabled={currentIdx === 0}
                        className="civio-nav"
                    >
                        Previous
                    </button>
                    {isLast ? (
                        <button
                            type="button"
                            onClick={onSubmit}
                            className="civio-nav civio-nav-primary"
                        >
                            Submit
                        </button>
                    ) : (
                        <button
                            type="button"
                            onClick={() => onNavigate(currentIdx + 1)}
                            className="civio-nav civio-nav-primary"
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
                                            ? 'border-[var(--civio-violet)] font-bold'
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

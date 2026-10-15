import { useState } from 'react';
import type {
    AiHandoffAttemptState,
    AiHandoffQuestion,
} from '@/lib/ai-handoff';
import { AskAssistantButton } from '../ask-assistant-button';

export interface RevealTutorPayload {
    concept: string | null;
    simpler: string | null;
    steps: string[];
    shortcut: string | null;
    commonMistakes: { choice: string; why: string }[];
    visual: {
        kind: string;
        length: number;
        width: number;
        unit: string;
    } | null;
    followUp: {
        questionId: number;
        stem: string;
        skill: string;
        direction: string;
    } | null;
}

export function readRevealTutor(value: unknown): RevealTutorPayload | null {
    if (!value || typeof value !== 'object') {
        return null;
    }

    const row = value as Record<string, unknown>;
    const visual =
        row.visual && typeof row.visual === 'object'
            ? (row.visual as Record<string, unknown>)
            : null;
    const followUp =
        row.followUp && typeof row.followUp === 'object'
            ? (row.followUp as Record<string, unknown>)
            : null;

    return {
        concept: typeof row.concept === 'string' ? row.concept : null,
        simpler: typeof row.simpler === 'string' ? row.simpler : null,
        steps: Array.isArray(row.steps)
            ? row.steps.filter(
                  (step): step is string => typeof step === 'string',
              )
            : [],
        shortcut: typeof row.shortcut === 'string' ? row.shortcut : null,
        commonMistakes: Array.isArray(row.commonMistakes)
            ? row.commonMistakes.flatMap((item) => {
                  if (!item || typeof item !== 'object') {
                      return [];
                  }

                  const mistake = item as Record<string, unknown>;

                  return typeof mistake.choice === 'string' &&
                      typeof mistake.why === 'string'
                      ? [{ choice: mistake.choice, why: mistake.why }]
                      : [];
              })
            : [],
        visual:
            visual?.kind === 'rectangle' &&
            typeof visual.length === 'number' &&
            typeof visual.width === 'number'
                ? {
                      kind: 'rectangle',
                      length: visual.length,
                      width: visual.width,
                      unit: typeof visual.unit === 'string' ? visual.unit : 'm',
                  }
                : null,
        followUp:
            typeof followUp?.questionId === 'number' &&
            typeof followUp.stem === 'string'
                ? {
                      questionId: followUp.questionId,
                      stem: followUp.stem,
                      skill:
                          typeof followUp.skill === 'string'
                              ? followUp.skill
                              : '',
                      direction:
                          typeof followUp.direction === 'string'
                              ? followUp.direction
                              : 'same',
                  }
                : null,
    };
}

interface AnswerRevealProps {
    letter: string;
    text: string;
    explanation?: string | null;
    hasConflict?: boolean;
    tutor?: RevealTutorPayload | null;
    chosenIndex?: number | null;
    correctIndex?: number | null;
    onHide: () => void;
    onOpenFollowUp?: (questionId: number) => void;
    ask?: {
        question: AiHandoffQuestion;
        attempt: AiHandoffAttemptState;
    } | null;
}

type Panel = 'steps' | 'shortcut' | 'mistakes' | 'visual' | 'simpler' | 'next';

function shortWork(explanation: string): string {
    const work = explanation.split(/The matching choice is/i)[0] ?? '';

    return work.replace(/\s+/g, ' ').trim();
}

function followUpLine(direction: string, skill: string): string {
    if (direction === 'easier') {
        return 'A similar item, a bit easier.';
    }

    if (direction === 'harder') {
        return 'A similar item, a bit harder.';
    }

    if (direction === 'other-skill') {
        return `${skill} has been the weaker set.`;
    }

    return skill ? `Another item in ${skill}.` : 'Another item on this skill.';
}

function RectangleFigure({
    length,
    width,
    unit,
}: {
    length: number;
    width: number;
    unit: string;
}) {
    const boxWidth = 168;
    const boxHeight = Math.max(
        52,
        Math.min(108, (width / Math.max(length, 1)) * boxWidth),
    );

    return (
        <svg
            viewBox={`0 0 ${boxWidth + 36} ${boxHeight + 28}`}
            className="mt-1 w-full max-w-[220px] text-[var(--civio-ink,#101426)]"
            role="img"
            aria-label={`Rectangle, ${length} ${unit} by ${width} ${unit}`}
        >
            <rect
                x="28"
                y="4"
                width={boxWidth}
                height={boxHeight}
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
            />
            <text
                x={28 + boxWidth / 2}
                y={boxHeight + 20}
                textAnchor="middle"
                fontSize="12"
                fill="currentColor"
            >
                {length} {unit}
            </text>
            <text
                x="14"
                y={4 + boxHeight / 2}
                textAnchor="middle"
                fontSize="12"
                fill="currentColor"
                transform={`rotate(-90 14 ${4 + boxHeight / 2})`}
            >
                {width} {unit}
            </text>
        </svg>
    );
}

export function AnswerReveal({
    letter,
    text,
    explanation,
    hasConflict = false,
    tutor = null,
    chosenIndex = null,
    correctIndex = null,
    onHide,
    onOpenFollowUp,
    ask = null,
}: AnswerRevealProps) {
    const [panel, setPanel] = useState<Panel | null>(null);
    const brief = explanation ? shortWork(explanation) : '';
    const marked = chosenIndex !== null && chosenIndex !== undefined;
    const verdict = !marked
        ? null
        : chosenIndex === correctIndex
          ? 'Correct'
          : 'Incorrect';
    const showingSimpler = panel === 'simpler' && !!tutor?.simpler;
    const lead = showingSimpler
        ? tutor?.simpler
        : tutor?.concept || brief || null;

    const toggle = (next: Panel) => {
        setPanel((current) => (current === next ? null : next));
    };

    const controls: { id: Panel; label: string }[] = [];

    if (tutor?.steps.length) {
        controls.push({ id: 'steps', label: 'Steps' });
    }

    if (tutor?.shortcut) {
        controls.push({ id: 'shortcut', label: 'Shortcut' });
    }

    if (tutor?.commonMistakes.length) {
        controls.push({ id: 'mistakes', label: 'Common miss' });
    }

    if (tutor?.visual?.kind === 'rectangle') {
        controls.push({ id: 'visual', label: 'Diagram' });
    }

    if (tutor?.simpler) {
        controls.push({
            id: 'simpler',
            label: showingSimpler ? 'Usual wording' : 'Explain simpler',
        });
    }

    if (tutor?.followUp) {
        controls.push({ id: 'next', label: 'Next item' });
    }

    return (
        <div className="mt-4 border-t border-[var(--civio-line,#e3e5ea)] pt-4 text-sm leading-relaxed">
            <p>
                {verdict && (
                    <>
                        <span className="font-semibold">{verdict}</span>
                        <span className="mx-2 opacity-40">·</span>
                    </>
                )}
                <span className="font-semibold text-[var(--civio-violet,#5b35f5)]">
                    {letter}
                </span>
                <span className="mx-2 opacity-40">·</span>
                <span className="font-semibold tabular-nums">{text}</span>
            </p>
            {hasConflict && (
                <p className="mt-2 text-xs">
                    Dexter detected a possible error in the stored answer.
                </p>
            )}
            {lead && <p className="mt-2">{lead}</p>}
            {controls.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1">
                    {controls.map((control) => (
                        <button
                            key={control.id}
                            type="button"
                            onClick={() => toggle(control.id)}
                            className={
                                panel === control.id
                                    ? 'font-semibold text-[var(--civio-violet,#5b35f5)]'
                                    : 'opacity-80'
                            }
                            aria-expanded={panel === control.id}
                        >
                            {control.label}
                        </button>
                    ))}
                </div>
            )}
            {panel === 'steps' && tutor && (
                <ol className="mt-3 flex flex-col gap-2">
                    {tutor.steps.map((step, index) => (
                        <li
                            key={`${index}-${step}`}
                            className="flex gap-3 tabular-nums"
                        >
                            <span className="flex size-6 shrink-0 items-center justify-center border border-[var(--civio-line,#e3e5ea)] text-xs font-semibold">
                                {index + 1}
                            </span>
                            <span>{step}</span>
                        </li>
                    ))}
                </ol>
            )}
            {panel === 'shortcut' && tutor?.shortcut && (
                <p className="mt-3 tabular-nums">{tutor.shortcut}</p>
            )}
            {panel === 'mistakes' && tutor && (
                <ul className="mt-3 flex flex-col gap-2">
                    {tutor.commonMistakes.map((mistake) => (
                        <li key={mistake.choice}>
                            <span className="font-semibold tabular-nums">
                                {mistake.choice}
                            </span>
                            <span className="mx-2 opacity-40">·</span>
                            {mistake.why}
                        </li>
                    ))}
                </ul>
            )}
            {panel === 'visual' && tutor?.visual?.kind === 'rectangle' && (
                <RectangleFigure
                    length={tutor.visual.length}
                    width={tutor.visual.width}
                    unit={tutor.visual.unit}
                />
            )}
            {panel === 'next' && tutor?.followUp && (
                <div className="mt-3">
                    <p>
                        {followUpLine(
                            tutor.followUp.direction,
                            tutor.followUp.skill,
                        )}
                    </p>
                    <p className="mt-1 opacity-80">{tutor.followUp.stem}</p>
                    {onOpenFollowUp && (
                        <button
                            type="button"
                            onClick={() =>
                                onOpenFollowUp(tutor.followUp!.questionId)
                            }
                            className="mt-2 font-semibold text-[var(--civio-violet,#5b35f5)]"
                        >
                            Open it
                        </button>
                    )}
                </div>
            )}
            <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2">
                {ask && (
                    <AskAssistantButton
                        question={ask.question}
                        attempt={ask.attempt}
                        className="inline-flex items-center gap-1.5 font-semibold no-underline"
                    />
                )}
                <button type="button" onClick={onHide} className="opacity-70">
                    Hide
                </button>
            </div>
        </div>
    );
}

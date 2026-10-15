import { useState } from 'react';
import type {
    AiHandoffAttemptState,
    AiHandoffQuestion,
} from '@/lib/ai-handoff';
import type { Question } from '../../types';
import { AskAssistantButton } from '../ask-assistant-button';

export interface RevealTutorPayload {
    concept: string | null;
    simpler: string | null;
    steps: string[];
    shortcut: string | null;
    commonMistakes: { choice: string; why: string }[];
    visual: {
        kind: string;
        length?: number;
        width?: number;
        unit?: string;
        groups?: string[];
        mark?: string;
    } | null;
    followUp: {
        questionId: number;
        stem: string;
        skill: string;
        direction: string;
        question: Question | null;
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
            rectangleVisual(visual) ??
            filingVisual(visual) ??
            labeledVisual(visual),
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
                      question: readFollowUpQuestion(followUp.question),
                  }
                : null,
    };
}

function readFollowUpQuestion(value: unknown): Question | null {
    if (!value || typeof value !== 'object') {
        return null;
    }

    const row = value as Record<string, unknown>;

    if (
        typeof row.id !== 'number' ||
        typeof row.stem !== 'string' ||
        !Array.isArray(row.options)
    ) {
        return null;
    }

    return {
        id: row.id,
        stem: row.stem,
        options: row.options.filter(
            (item): item is string => typeof item === 'string',
        ),
        category:
            typeof row.category === 'string'
                ? row.category
                : 'General Information',
        subcategory: typeof row.subcategory === 'string' ? row.subcategory : '',
        language: typeof row.language === 'string' ? row.language : 'English',
        isDemographic: row.isDemographic === true,
    };
}

function rectangleVisual(
    visual: Record<string, unknown> | null,
): RevealTutorPayload['visual'] {
    if (
        visual?.kind !== 'rectangle' ||
        typeof visual.length !== 'number' ||
        typeof visual.width !== 'number'
    ) {
        return null;
    }

    return {
        kind: 'rectangle',
        length: visual.length,
        width: visual.width,
        unit: typeof visual.unit === 'string' ? visual.unit : 'm',
    };
}

function filingVisual(
    visual: Record<string, unknown> | null,
): RevealTutorPayload['visual'] {
    if (visual?.kind !== 'filing' || !Array.isArray(visual.groups)) {
        return null;
    }

    const groups = visual.groups.filter(
        (group): group is string => typeof group === 'string',
    );

    return groups.length === 3 && visual.kind === 'filing'
        ? { kind: 'filing', groups }
        : null;
}

function labeledVisual(
    visual: Record<string, unknown> | null,
): RevealTutorPayload['visual'] {
    if (
        (visual?.kind !== 'mixture' && visual?.kind !== 'order') ||
        !Array.isArray(visual.groups)
    ) {
        return null;
    }

    const groups = visual.groups.filter(
        (group): group is string => typeof group === 'string',
    );

    if (groups.length < 2) {
        return null;
    }

    return {
        kind: visual.kind,
        groups,
        mark: typeof visual.mark === 'string' ? visual.mark : undefined,
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
    ask?: {
        question: AiHandoffQuestion;
        attempt: AiHandoffAttemptState;
    } | null;
}

type Panel = 'steps' | 'shortcut' | 'mistakes' | 'visual' | 'simpler';

const SIMILAR_ITEM_PROMPT =
    'Write one new practice question on this same skill for the Philippine Civil Service Exam. Change the numbers or the wording. Give four choices, say which one is correct, and explain it in a few lines.';

function shortWork(explanation: string): string {
    const work = explanation.split(/The matching choice is/i)[0] ?? '';

    return work.replace(/\s+/g, ' ').trim();
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

function FilingFigure({ groups }: { groups: string[] }) {
    const roles = ['Tertiary', 'Secondary', 'Primary'];

    return (
        <div
            className="mt-3 flex flex-wrap gap-2"
            role="img"
            aria-label={`Filing groups ${groups.join(', ')}. ${groups[2]} is read first.`}
        >
            {groups.map((group, index) => (
                <div
                    key={group}
                    className={
                        index === 2
                            ? 'min-w-16 border border-[var(--civio-violet,#5b35f5)] px-3 py-2 text-center'
                            : 'min-w-16 border border-[var(--civio-line,#e3e5ea)] px-3 py-2 text-center'
                    }
                >
                    <p className="text-base font-semibold tabular-nums">
                        {group}
                    </p>
                    <p className="mt-1 text-xs opacity-70">{roles[index]}</p>
                </div>
            ))}
        </div>
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
        controls.push({ id: 'steps', label: 'Step-by-Step' });
    }

    if (tutor?.shortcut) {
        controls.push({ id: 'shortcut', label: 'Exam Tip' });
    }

    if (tutor?.commonMistakes.length) {
        controls.push({ id: 'mistakes', label: 'Common Mistake' });
    }

    if (tutor?.visual) {
        controls.push({ id: 'visual', label: 'Diagram' });
    }

    if (tutor?.simpler) {
        controls.push({
            id: 'simpler',
            label: showingSimpler ? 'Usual Wording' : 'Explain Simpler',
        });
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
            {lead && (
                <div className="mt-3">
                    <p className="font-semibold">Understand the Answer</p>
                    <p className="mt-1">{lead}</p>
                </div>
            )}
            {(controls.length > 0 || ask) && (
                <div className="mt-4 flex flex-wrap gap-2">
                    {controls.map((control) => (
                        <button
                            key={control.id}
                            type="button"
                            onClick={() => toggle(control.id)}
                            className={`inline-flex items-center rounded-lg border px-3 py-1.5 text-xs font-semibold ${
                                panel === control.id
                                    ? 'border-[var(--civio-violet,#5b35f5)] bg-[var(--civio-violet,#5b35f5)]/10'
                                    : 'border-[var(--civio-line,#e3e5ea)]'
                            }`}
                            aria-expanded={panel === control.id}
                        >
                            {control.label}
                        </button>
                    ))}
                    {ask && (
                        <AskAssistantButton
                            question={ask.question}
                            attempt={ask.attempt}
                            label="Similar Item"
                            title="Opens your assistant in a new tab and asks for one similar question. You stay on this item."
                            options={{ closingPrompt: SIMILAR_ITEM_PROMPT }}
                            className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--civio-line,#e3e5ea)] px-3 py-1.5 text-xs font-semibold no-underline"
                        />
                    )}
                    {ask && (
                        <AskAssistantButton
                            question={ask.question}
                            attempt={ask.attempt}
                            className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--civio-line,#e3e5ea)] px-3 py-1.5 text-xs font-semibold no-underline"
                        />
                    )}
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
                    length={tutor.visual.length ?? 0}
                    width={tutor.visual.width ?? 0}
                    unit={tutor.visual.unit ?? 'm'}
                />
            )}
            {panel === 'visual' &&
                tutor?.visual?.kind === 'filing' &&
                tutor.visual.groups && (
                    <FilingFigure groups={tutor.visual.groups} />
                )}
            {panel === 'visual' &&
                (tutor?.visual?.kind === 'mixture' ||
                    tutor?.visual?.kind === 'order') &&
                tutor.visual.groups && (
                    <ol className="mt-3 flex flex-col gap-1">
                        {tutor.visual.groups.map((label) => (
                            <li
                                key={label}
                                className={
                                    label === tutor.visual?.mark
                                        ? 'font-semibold text-[var(--civio-violet,#5b35f5)]'
                                        : undefined
                                }
                            >
                                {label}
                            </li>
                        ))}
                    </ol>
                )}
        </div>
    );
}

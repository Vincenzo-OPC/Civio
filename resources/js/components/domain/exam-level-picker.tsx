import { useRef } from 'react';
import { TimeDial } from '@/components/domain/time-dial';
import { EXAM_DIALS } from '@/lib/exam-dials';
import type { ExamDialId } from '@/lib/exam-dials';

const LEVELS = [EXAM_DIALS.professional, EXAM_DIALS.subprofessional] as const;

interface ExamLevelPickerProps {
    value: ExamDialId;
    onChange: (id: ExamDialId) => void;
}

export function ExamLevelPicker({ value, onChange }: ExamLevelPickerProps) {
    const buttons = useRef<Record<string, HTMLButtonElement | null>>({});

    const move = (direction: 1 | -1) => {
        const index = LEVELS.findIndex((level) => level.id === value);
        const next =
            LEVELS[(index + direction + LEVELS.length) % LEVELS.length];

        onChange(next.id);
        buttons.current[next.id]?.focus();
    };

    return (
        <div>
            <div
                role="radiogroup"
                aria-label="Choose Your Exam"
                className="grid gap-3 sm:grid-cols-2"
                onKeyDown={(event) => {
                    if (
                        event.key === 'ArrowRight' ||
                        event.key === 'ArrowDown'
                    ) {
                        event.preventDefault();
                        move(1);
                    }

                    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
                        event.preventDefault();
                        move(-1);
                    }
                }}
            >
                {LEVELS.map((level) => {
                    const selected = level.id === value;
                    const hours = Math.floor(level.seconds / 3600);
                    const minutes = Math.floor((level.seconds % 3600) / 60);

                    return (
                        <button
                            key={level.id}
                            type="button"
                            role="radio"
                            aria-checked={selected}
                            aria-label={`${level.name}, ${level.questions} Questions, ${hours} hours ${minutes} minutes. ${level.description}`}
                            tabIndex={selected ? 0 : -1}
                            ref={(node) => {
                                buttons.current[level.id] = node;
                            }}
                            onClick={() => onChange(level.id)}
                            className={`flex h-full flex-col items-center rounded-2xl border bg-white px-4 py-5 text-center text-[#101426] transition-[transform,border-color,box-shadow] duration-200 ease-out outline-none focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAFAF7] motion-reduce:transform-none motion-reduce:transition-none sm:px-5 dark:bg-[#1a1e30] dark:text-[#FAFAF7] dark:focus-visible:ring-[#C4B6FF] dark:focus-visible:ring-offset-[#101426] ${
                                selected
                                    ? '-translate-y-0.5 border-[#5B35F5] shadow-sm dark:border-[#C4B6FF]'
                                    : 'border-[#E3E5EA] hover:-translate-y-0.5 hover:border-[#5B35F5]/40 hover:shadow-sm dark:border-[#3a415c] dark:hover:border-[#C4B6FF]/60'
                            }`}
                        >
                            <TimeDial
                                totalSeconds={level.seconds}
                                quiet={!selected}
                                decorative
                            />
                            <span
                                className={`mt-3 font-heading text-lg font-semibold tracking-tight ${
                                    selected
                                        ? 'text-[#5B35F5] dark:text-[#C4B6FF]'
                                        : ''
                                }`}
                            >
                                {level.name}
                            </span>
                            <span className="mt-1 text-sm leading-relaxed">
                                <span className="font-semibold tabular-nums">
                                    {level.questions} questions
                                </span>
                            </span>
                        </button>
                    );
                })}
            </div>
            <p className="mt-3 text-sm leading-relaxed opacity-70">
                The ring shows the full time limit, not a score.
            </p>
        </div>
    );
}

import { CircleCheck } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { TimeDial } from '@/components/domain/time-dial';
import { EXAM_DIALS } from '@/lib/exam-dials';
import type { ExamDialId } from '@/lib/exam-dials';

const LEVELS = [EXAM_DIALS.professional, EXAM_DIALS.subprofessional] as const;

interface ExamLevelPickerProps {
    value: ExamDialId;
    onChange: (id: ExamDialId) => void;
}

function useCount(target: number): number {
    const [shown, setShown] = useState(0);
    const from = useRef(0);

    useEffect(() => {
        const reduce = window.matchMedia(
            '(prefers-reduced-motion: reduce)',
        ).matches;

        if (reduce) {
            from.current = target;
            const frame = requestAnimationFrame(() => setShown(target));

            return () => cancelAnimationFrame(frame);
        }

        const startValue = from.current;
        const start = performance.now();
        let frame = 0;
        const tick = (now: number) => {
            const progress = Math.min(1, (now - start) / 460);
            const eased = 1 - (1 - progress) ** 3;

            setShown(Math.round(startValue + (target - startValue) * eased));

            if (progress < 1) {
                frame = requestAnimationFrame(tick);
            } else {
                from.current = target;
            }
        };

        frame = requestAnimationFrame(tick);

        return () => cancelAnimationFrame(frame);
    }, [target]);

    return shown;
}

function pad(value: number): string {
    return String(value).padStart(2, '0');
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
        <div
            role="radiogroup"
            aria-label="Choose Your Exam"
            className="grid gap-3 sm:grid-cols-2"
            onKeyDown={(event) => {
                if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
                    event.preventDefault();
                    move(1);
                }

                if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
                    event.preventDefault();
                    move(-1);
                }
            }}
        >
            {LEVELS.map((level, index) => (
                <ExamCard
                    key={level.id}
                    level={level}
                    selected={level.id === value}
                    delay={index}
                    onChange={onChange}
                    setButton={(node) => {
                        buttons.current[level.id] = node;
                    }}
                />
            ))}
        </div>
    );
}

function ExamCard({
    level,
    selected,
    delay,
    onChange,
    setButton,
}: {
    level: (typeof LEVELS)[number];
    selected: boolean;
    delay: number;
    onChange: (id: ExamDialId) => void;
    setButton: (node: HTMLButtonElement | null) => void;
}) {
    const hours = useCount(Math.floor(level.seconds / 3600));
    const minutes = useCount(Math.floor((level.seconds % 3600) / 60));
    const questions = useCount(level.questions);

    return (
        <button
            type="button"
            role="radio"
            aria-checked={selected}
            aria-label={`${level.name}, ${level.questions} Questions, ${pad(Math.floor(level.seconds / 3600))}h ${pad(Math.floor((level.seconds % 3600) / 60))}m. ${level.description}`}
            tabIndex={selected ? 0 : -1}
            ref={setButton}
            onClick={() => onChange(level.id)}
            style={{ animationDelay: `${120 + delay * 90}ms` }}
            className={`civio-rise flex h-full flex-col rounded-2xl border bg-white px-5 py-5 text-left text-[#101426] transition-[transform,border-color,box-shadow] duration-200 ease-out outline-none focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAFAF7] motion-reduce:transform-none sm:px-6 dark:bg-[#1a1e30] dark:text-[#FAFAF7] dark:focus-visible:ring-[#C4B6FF] dark:focus-visible:ring-offset-[#101426] ${
                selected
                    ? 'border-2 border-[#5B35F5] shadow-sm dark:border-[#C4B6FF]'
                    : 'border-[#E3E5EA] hover:-translate-y-0.5 hover:border-[#5B35F5]/45 hover:shadow-sm dark:border-[#3a415c] dark:hover:border-[#C4B6FF]/60'
            }`}
        >
            <span className="flex items-start justify-between gap-3">
                <span className="font-heading text-xl font-semibold tracking-tight text-balance">
                    {level.name}
                </span>
                <CircleCheck
                    aria-hidden
                    className={`size-5 shrink-0 transition-opacity ${
                        selected
                            ? 'text-[#5B35F5] opacity-100 dark:text-[#C4B6FF]'
                            : 'opacity-0'
                    }`}
                />
            </span>
            <span className="mt-2 min-h-[3.25rem] text-sm leading-relaxed text-[#101426]/75 dark:text-[#FAFAF7]/75">
                {level.description}
            </span>
            <span className="mt-5 flex items-end justify-between gap-3">
                <span>
                    <span className="block font-heading text-4xl leading-none font-semibold tracking-tight tabular-nums">
                        {questions}
                    </span>
                    <span className="mt-1 block text-xs tracking-wide">
                        Questions
                    </span>
                </span>
                <span className="flex items-center gap-2">
                    <TimeDial
                        totalSeconds={level.seconds}
                        quiet={!selected}
                        decorative
                        className="size-14"
                    />
                    <span>
                        <span className="block font-heading text-2xl leading-none font-semibold tracking-tight tabular-nums">
                            {pad(hours)}h {pad(minutes)}m
                        </span>
                        <span className="mt-1 block text-right text-xs tracking-wide">
                            Duration
                        </span>
                    </span>
                </span>
            </span>
        </button>
    );
}

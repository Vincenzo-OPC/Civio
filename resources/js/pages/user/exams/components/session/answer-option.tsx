import type { ReactNode } from 'react';
import type { AnswerVisual } from '../../utils/answer-state';

const SHELL: Record<AnswerVisual, string> = {
    unanswered:
        'border-[var(--civio-line)] bg-transparent text-[var(--civio-ink)]',
    selected:
        'border-[var(--civio-violet)] bg-[var(--civio-violet)]/10 text-[var(--civio-ink)]',
    correct:
        'border-[var(--civio-lime)] bg-[var(--civio-lime)] text-[var(--civio-ink)]',
    'correct-unselected':
        'border-[var(--civio-lime)] bg-[var(--civio-lime)]/35 text-[var(--civio-ink)]',
    incorrect:
        'border-[var(--civio-error)] bg-[var(--civio-error)]/10 text-[var(--civio-ink)]',
};

const BADGE: Record<AnswerVisual, string> = {
    unanswered: 'border-[var(--civio-line)] text-[var(--civio-ink)]',
    selected:
        'border-[var(--civio-violet)] bg-[var(--civio-violet)] text-white',
    correct:
        'border-[var(--civio-ink)] bg-[var(--civio-ink)] text-[var(--civio-lime)]',
    'correct-unselected':
        'border-[var(--civio-ink)] bg-[var(--civio-ink)] text-[var(--civio-lime)]',
    incorrect: 'border-[var(--civio-error)] text-[var(--civio-error)]',
};

interface AnswerOptionProps {
    letter: string;
    visual: AnswerVisual;
    status: string | null;
    eliminated?: boolean;
    onSelect: () => void;
    trailing?: ReactNode;
    children: ReactNode;
}

export function AnswerOption({
    letter,
    visual,
    status,
    eliminated = false,
    onSelect,
    trailing,
    children,
}: AnswerOptionProps) {
    return (
        <div
            className={`flex min-h-12 items-start gap-3 border-b px-1 py-3.5 ${
                eliminated ? 'border-dashed opacity-45' : SHELL[visual]
            } border-x-0 border-t-0`}
        >
            <button
                type="button"
                role="radio"
                aria-checked={
                    visual === 'selected' ||
                    visual === 'correct' ||
                    visual === 'incorrect'
                }
                onClick={onSelect}
                disabled={eliminated}
                className="flex min-w-0 flex-1 items-start gap-3 text-left disabled:cursor-not-allowed"
            >
                <span
                    className={`flex size-7 shrink-0 items-center justify-center border text-xs font-bold ${BADGE[eliminated ? 'unanswered' : visual]}`}
                >
                    {letter}
                </span>
                <span className="min-w-0 flex-1 text-sm leading-relaxed md:text-base">
                    {children}
                    {status && (
                        <span className="mt-1 block text-xs font-semibold tracking-wide uppercase">
                            {status}
                        </span>
                    )}
                </span>
            </button>
            {trailing}
        </div>
    );
}

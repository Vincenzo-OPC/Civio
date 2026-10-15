import { ChevronLeft, Flag, LayoutGrid, Moon } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner';
import type { AiHandoffAttemptState } from '@/lib/ai-handoff';
import { AskAssistantButton } from '@/pages/user/exams/components/ask-assistant-button';
import { CopyForAiButton } from '@/pages/user/exams/components/copy-for-ai-button';

const OPTIONS = ['₱150', '₱300', '₱350', '₱1,700'] as const;
const CORRECT = 1;

const QUESTION = {
    stem: '15% of ₱2,000 is:',
    options: [...OPTIONS],
    category: 'Numerical',
    subcategory: 'Percentage',
};

/**
 * A working sample of Study Mode. The item is not from the bank and is not scored.
 * Report, Show Explanation, Copy Question, and Ask use the same actions as a mock.
 */
export function ExamScreenPreview() {
    const [selected, setSelected] = useState<number | null>(1);
    const [explained, setExplained] = useState(false);

    const attempt: AiHandoffAttemptState = {
        selectedDisplayIndex: selected,
        mode: 'study',
        examLevel: 'Professional',
        revealed: explained,
        questionNumber: 1,
        totalQuestions: 150,
        verifiedCorrectDisplayIndex: explained ? CORRECT : null,
        verifiedExplanation: explained
            ? '15% means 15 out of 100. 0.15 × 2,000 = 300.'
            : null,
        result:
            !explained || selected === null
                ? null
                : selected === CORRECT
                  ? 'Correct'
                  : 'Incorrect',
    };

    return (
        <figure className="civio-session overflow-hidden border border-[var(--civio-line)] bg-[var(--civio-paper)] text-[var(--civio-ink)]">
            <div className="flex items-center gap-0.5 border-b border-[var(--civio-line)] px-1 py-1 sm:px-2">
                <span className="flex size-9 shrink-0 items-center justify-center">
                    <ChevronLeft className="size-5" />
                </span>
                <span className="min-w-0 flex-1" />
                <span className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-ink)]/60">
                    <Moon className="size-4" />
                </span>
                <span className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-ink)]/60">
                    <Flag className="size-4" />
                </span>
                <span className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-violet)]">
                    <LayoutGrid className="size-4" />
                </span>
            </div>

            <div className="flex items-center justify-between gap-3 px-3 py-2 text-xs sm:px-5">
                <p className="min-w-0">
                    <span className="text-sm font-semibold">Study Mode</span>
                    <span className="mx-1.5 opacity-40">·</span>
                    <span className="font-semibold">1 of 150</span>
                    <span className="mt-0.5 block opacity-60">
                        Professional
                    </span>
                </p>
                <p className="shrink-0 font-semibold">
                    <span className="opacity-70">Tools</span>
                    <span className="ml-3">Pause</span>
                </p>
            </div>

            <div className="h-1 bg-[var(--civio-line)]" aria-hidden>
                <div
                    className="h-full bg-[var(--civio-violet)]"
                    style={{ width: `${(1 / 150) * 100}%` }}
                />
            </div>

            <div className="px-4 py-5 sm:px-6 sm:py-6">
                <p className="text-lg leading-relaxed md:text-xl">
                    {QUESTION.stem}
                </p>
                <p className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2">
                    <button
                        type="button"
                        onClick={() =>
                            toast.message(
                                'This sample is not a bank item. Report is for a question inside a mock.',
                                { id: 'sample-report' },
                            )
                        }
                        className="text-xs font-semibold text-[var(--civio-ink)]/60"
                    >
                        Report
                    </button>
                    <button
                        type="button"
                        onClick={() => setExplained((open) => !open)}
                        className={`inline-flex items-center rounded-lg px-2.5 py-1.5 text-[11px] font-bold ${
                            explained
                                ? 'text-[var(--civio-ink)]/70'
                                : 'bg-[var(--civio-violet)] text-white'
                        }`}
                    >
                        {explained ? 'Hide Explanation' : 'Show Explanation'}
                    </button>
                    <CopyForAiButton question={QUESTION} attempt={attempt} />
                    <AskAssistantButton question={QUESTION} attempt={attempt} />
                </p>
                {explained && (
                    <div className="mt-4 border border-[var(--civio-line)] px-4 py-3 text-sm leading-relaxed">
                        <p className="font-semibold">
                            {selected === CORRECT ? 'Correct' : 'Incorrect'}. B.
                            ₱300
                        </p>
                        <p className="mt-2 text-[var(--civio-ink)]/80">
                            15% means 15 out of 100. 0.15 × 2,000 = 300. ₱150 is
                            15% of 1,000, not of 2,000.
                        </p>
                    </div>
                )}
                <div
                    className="mt-4 flex flex-col"
                    role="radiogroup"
                    aria-label="Sample choices"
                >
                    {OPTIONS.map((text, index) => {
                        const chosen = selected === index;

                        return (
                            <button
                                key={text}
                                type="button"
                                role="radio"
                                aria-checked={chosen}
                                onClick={() => setSelected(index)}
                                className={`flex min-h-12 items-start gap-3 border-x-0 border-t-0 border-b px-1 py-3.5 text-left ${
                                    chosen
                                        ? 'border-[var(--civio-violet)] bg-[var(--civio-violet)]/10'
                                        : 'border-[var(--civio-line)]'
                                }`}
                            >
                                <span
                                    className={`flex size-7 shrink-0 items-center justify-center border text-xs font-bold ${
                                        chosen
                                            ? 'border-[var(--civio-violet)] bg-[var(--civio-violet)] text-white'
                                            : 'border-[var(--civio-line)]'
                                    }`}
                                >
                                    {String.fromCharCode(65 + index)}
                                </span>
                                <span className="text-sm leading-relaxed md:text-base">
                                    {text}
                                    {chosen && (
                                        <span className="mt-1 block text-xs font-semibold">
                                            Selected
                                        </span>
                                    )}
                                </span>
                            </button>
                        );
                    })}
                </div>
            </div>
            <figcaption className="sr-only">
                A sample Study Mode item. It is not scored.
            </figcaption>
        </figure>
    );
}

import {
    ChevronLeft,
    Edit3,
    Flag,
    Keyboard,
    LayoutGrid,
    Maximize2,
    Moon,
    Sun,
} from 'lucide-react';
import { useRef, useState } from 'react';
import { toast } from 'sonner';
import { useAppearance } from '@/hooks/use-appearance';
import { useLiteMode } from '@/hooks/use-lite-mode';
import type { AiHandoffAttemptState } from '@/lib/ai-handoff';
import { AskAssistantButton } from '@/pages/user/exams/components/ask-assistant-button';
import { CopyForAiButton } from '@/pages/user/exams/components/copy-for-ai-button';

const OPTIONS = ['₱150', '₱300', '₱350', '₱1,700'] as const;
const CORRECT = 1;
const MAP = [1, 2, 3, 4, 5, 6, 7, 8] as const;

const QUESTION = {
    stem: '15% of ₱2,000 is:',
    options: [...OPTIONS],
    category: 'Numerical',
    subcategory: 'Percentage',
};

/**
 * A working sample of Study Mode. The item is not from the bank and is not scored.
 */
export function ExamScreenPreview() {
    const frame = useRef<HTMLElement>(null);
    const { resolvedAppearance, updateAppearance } = useAppearance();
    const { lite, toggle: toggleLite } = useLiteMode();
    const dark = resolvedAppearance === 'dark';
    const [selected, setSelected] = useState<number | null>(1);
    const [explained, setExplained] = useState(false);
    const [toolsOpen, setToolsOpen] = useState(false);
    const [paused, setPaused] = useState(false);
    const [flagged, setFlagged] = useState(false);
    const [mapOpen, setMapOpen] = useState(false);
    const [notesOpen, setNotesOpen] = useState(false);
    const [keysOpen, setKeysOpen] = useState(false);
    const [note, setNote] = useState('');

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

    const choose = (index: number) => {
        setSelected(index);
    };

    return (
        <figure
            ref={frame}
            className="civio-session relative overflow-hidden border border-[var(--civio-line)] bg-[var(--civio-paper)] text-[var(--civio-ink)]"
        >
            <div className="flex items-center gap-0.5 border-b border-[var(--civio-line)] px-1 py-1 sm:px-2">
                <button
                    type="button"
                    aria-label="Back to Choose Your Exam"
                    onClick={() =>
                        document
                            .getElementById('choose-exam')
                            ?.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start',
                            })
                    }
                    className="flex size-9 shrink-0 items-center justify-center"
                >
                    <ChevronLeft className="size-5" />
                </button>
                <span className="min-w-0 flex-1" />
                <button
                    type="button"
                    aria-pressed={dark}
                    aria-label={
                        dark ? 'Switch to light mode' : 'Switch to dark mode'
                    }
                    onClick={() => updateAppearance(dark ? 'light' : 'dark')}
                    className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-ink)]/70"
                >
                    {dark ? (
                        <Sun className="size-4" />
                    ) : (
                        <Moon className="size-4" />
                    )}
                </button>
                <button
                    type="button"
                    aria-pressed={flagged}
                    aria-label={
                        flagged ? 'Unflag this sample' : 'Flag this sample'
                    }
                    onClick={() => setFlagged((on) => !on)}
                    className={`flex size-9 shrink-0 items-center justify-center ${
                        flagged
                            ? 'text-[var(--civio-violet)]'
                            : 'text-[var(--civio-ink)]/60'
                    }`}
                >
                    <Flag
                        className={`size-4 ${flagged ? 'fill-current' : ''}`}
                    />
                </button>
                <button
                    type="button"
                    aria-expanded={mapOpen}
                    aria-label="Question map"
                    onClick={() => setMapOpen((open) => !open)}
                    className={`flex size-9 shrink-0 items-center justify-center ${
                        mapOpen
                            ? 'text-[var(--civio-violet)]'
                            : 'text-[var(--civio-ink)]/60'
                    }`}
                >
                    <LayoutGrid className="size-4" />
                </button>
            </div>

            {mapOpen && (
                <div className="border-b border-[var(--civio-line)] px-4 py-3">
                    <p className="text-xs font-semibold">Items</p>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                        {MAP.map((number) => (
                            <button
                                key={number}
                                type="button"
                                aria-current={number === 1 ? 'true' : undefined}
                                onClick={() => {
                                    if (number !== 1) {
                                        toast.message(
                                            'This preview has one item.',
                                            { id: 'sample-map' },
                                        );
                                    }
                                }}
                                className={`flex size-8 items-center justify-center border text-xs font-semibold ${
                                    number === 1
                                        ? 'border-[var(--civio-violet)] bg-[var(--civio-violet)] text-white'
                                        : 'border-[var(--civio-line)]'
                                }`}
                            >
                                {number}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <div className="flex items-center justify-between gap-3 px-3 py-2 text-xs sm:px-5">
                <p className="min-w-0">
                    <span className="text-sm font-semibold">Study Mode</span>
                    <span className="mx-1.5 opacity-40">·</span>
                    <span className="font-semibold">1 of 150</span>
                    <span className="mt-0.5 block opacity-60">
                        Professional
                    </span>
                </p>
                <p className="flex shrink-0 items-center font-semibold">
                    <button
                        type="button"
                        aria-expanded={toolsOpen}
                        onClick={() => setToolsOpen((open) => !open)}
                        className="h-8 rounded-lg px-2 text-[var(--civio-ink)]/70"
                    >
                        Tools
                    </button>
                    <button
                        type="button"
                        onClick={() => setPaused(true)}
                        className="h-8 rounded-lg px-2"
                    >
                        Pause
                    </button>
                </p>
            </div>

            {toolsOpen && (
                <div className="flex flex-wrap items-center gap-2 border-t border-[var(--civio-line)] px-3 py-2 sm:px-5">
                    <button
                        type="button"
                        aria-expanded={notesOpen}
                        onClick={() => setNotesOpen((open) => !open)}
                        className="civio-action"
                    >
                        <Edit3 className="mr-1 inline size-3.5" />
                        Notes
                    </button>
                    <button
                        type="button"
                        aria-expanded={keysOpen}
                        onClick={() => setKeysOpen((open) => !open)}
                        className="civio-action"
                    >
                        <Keyboard className="mr-1 inline size-3.5" />
                        Keys
                    </button>
                    <button
                        type="button"
                        onClick={() => {
                            const node = frame.current;

                            if (!node) {
                                return;
                            }

                            if (document.fullscreenElement === node) {
                                void document.exitFullscreen();
                            } else {
                                void node.requestFullscreen?.();
                            }
                        }}
                        className="civio-action"
                    >
                        <Maximize2 className="mr-1 inline size-3.5" />
                        Focus
                    </button>
                    <button
                        type="button"
                        role="switch"
                        aria-checked={lite}
                        onClick={toggleLite}
                        className="civio-action"
                    >
                        Lite {lite ? 'on' : 'off'}
                    </button>
                </div>
            )}

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
                <div className="mt-5 flex flex-wrap items-center gap-3">
                    <button
                        type="button"
                        onClick={() =>
                            toast.message(
                                'This sample is not a bank item. Report is for a question inside a mock.',
                                { id: 'sample-report' },
                            )
                        }
                        className="civio-action"
                    >
                        Report
                    </button>
                    <button
                        type="button"
                        onClick={() => setExplained((open) => !open)}
                        className={
                            explained
                                ? 'civio-action'
                                : 'civio-action civio-action-primary'
                        }
                    >
                        {explained ? 'Hide Explanation' : 'Show Explanation'}
                    </button>
                    <CopyForAiButton
                        question={QUESTION}
                        attempt={attempt}
                        className="civio-action"
                    />
                    <AskAssistantButton
                        question={QUESTION}
                        attempt={attempt}
                        className="civio-action"
                    />
                </div>
                {notesOpen && (
                    <label className="mt-4 block text-xs font-semibold">
                        Notes
                        <textarea
                            value={note}
                            onChange={(event) => setNote(event.target.value)}
                            rows={2}
                            className="mt-1 w-full border border-[var(--civio-line)] bg-transparent px-3 py-2 text-sm font-normal"
                        />
                    </label>
                )}
                {keysOpen && (
                    <p className="mt-3 text-xs leading-relaxed text-[var(--civio-ink)]/70">
                        In a mock, 1 to 4 choose an answer. N moves on. This
                        sample uses the buttons on screen.
                    </p>
                )}
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
                                onClick={() => choose(index)}
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
            {paused && (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-[var(--civio-paper)]/92 px-6 text-center">
                    <p className="font-heading text-2xl font-semibold tracking-tight">
                        Paused
                    </p>
                    <p className="max-w-xs text-sm leading-relaxed text-[var(--civio-ink)]/70">
                        This sample is not timed. A mock pauses the clock here.
                    </p>
                    <button
                        type="button"
                        onClick={() => setPaused(false)}
                        className="mt-1 h-10 rounded-lg bg-[var(--civio-violet)] px-4 text-sm font-semibold text-white"
                    >
                        Resume
                    </button>
                </div>
            )}
            <figcaption className="sr-only">
                A sample Study Mode item. It is not scored.
            </figcaption>
        </figure>
    );
}

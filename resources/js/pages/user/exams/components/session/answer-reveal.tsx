import { useState } from 'react';

interface Expound {
    rule: string | null;
    steps: string[];
}

interface AnswerRevealProps {
    questionId: number;
    letter: string;
    text: string;
    explanation?: string | null;
    hasConflict?: boolean;
    onHide: () => void;
}

function shortWork(explanation: string): string {
    const work = explanation.split(/The matching choice is/i)[0] ?? '';

    return work.replace(/\s+/g, ' ').trim();
}

export function AnswerReveal({
    questionId,
    letter,
    text,
    explanation,
    hasConflict = false,
    onHide,
}: AnswerRevealProps) {
    const [expound, setExpound] = useState<Expound | null>(null);
    const [failed, setFailed] = useState(false);
    const [loading, setLoading] = useState(false);
    const brief = explanation ? shortWork(explanation) : '';

    const load = async () => {
        if (loading || expound) {
            return;
        }

        setLoading(true);
        setFailed(false);

        try {
            const res = await fetch('/exams/expound', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN':
                        document
                            .querySelector('meta[name="csrf-token"]')
                            ?.getAttribute('content') || '',
                },
                body: JSON.stringify({ question_id: questionId }),
            });
            const data = await res.json();

            if (!res.ok || !data.success || !Array.isArray(data.steps)) {
                setFailed(true);

                return;
            }

            setExpound({
                rule: typeof data.rule === 'string' ? data.rule : null,
                steps: data.steps.filter(
                    (step: unknown): step is string => typeof step === 'string',
                ),
            });
        } catch {
            setFailed(true);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-4 border-t border-[var(--civio-line,#e3e5ea)] pt-4 text-sm leading-relaxed">
            <p>
                <span className="font-semibold text-[var(--civio-violet,#5b35f5)]">
                    {letter}
                </span>
                <span className="mx-2 opacity-40">·</span>
                <span className="font-semibold">{text}</span>
            </p>
            {hasConflict && (
                <p className="mt-2 text-xs">
                    Dexter detected a possible error in the stored answer.
                </p>
            )}
            {brief && !expound && <p className="mt-2 opacity-80">{brief}</p>}
            {expound && (
                <div className="mt-4 flex flex-col gap-3">
                    {expound.rule && <p>{expound.rule}</p>}
                    <ol className="flex flex-col gap-2">
                        {expound.steps.map((step, index) => (
                            <li key={`${index}-${step}`} className="flex gap-3">
                                <span className="flex size-6 shrink-0 items-center justify-center border border-[var(--civio-line,#e3e5ea)] text-xs font-semibold">
                                    {index + 1}
                                </span>
                                <span>{step}</span>
                            </li>
                        ))}
                    </ol>
                </div>
            )}
            {failed && (
                <p className="mt-2">The explanation could not be loaded.</p>
            )}
            <div className="mt-3 flex gap-4">
                {!expound && (
                    <button
                        type="button"
                        onClick={load}
                        disabled={loading}
                        className="font-semibold text-[var(--civio-violet,#5b35f5)] disabled:opacity-50"
                    >
                        {loading ? 'Expounding' : 'Expound'}
                    </button>
                )}
                <button type="button" onClick={onHide} className="opacity-70">
                    Hide
                </button>
            </div>
        </div>
    );
}

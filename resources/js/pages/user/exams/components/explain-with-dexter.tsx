import { usePage } from '@inertiajs/react';
import { Sparkles } from 'lucide-react';
import { useState } from 'react';
import type { Question } from '../types';
import { apiPost } from '../utils/exam-utils';

interface ExplainPayload {
    eli5: string;
    why_right: string;
    why_wrong: string;
    tip: string;
    citation: string | null;
    provider: string;
    notice?: string;
}

interface ExplainWithDexterProps {
    question: Question;
    chosenIndex?: number | null;
}

export function ExplainWithDexter({
    question,
    chosenIndex,
}: ExplainWithDexterProps) {
    const tutor =
        (
            usePage().props as {
                civio?: { tutorName?: string };
            }
        ).civio?.tutorName || 'Dexter';
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ExplainPayload | null>(null);

    const explain = async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await apiPost<{
                success: boolean;
                explain: ExplainPayload;
            }>('/exams/explain', {
                stem: question.stem,
                options: question.options,
                chosen_index:
                    chosenIndex === undefined || chosenIndex === null
                        ? null
                        : chosenIndex,
                correct_index: question.correct_option,
                explanation: question.explanation || null,
                category: question.category || null,
                subcategory: question.subcategory || null,
            });
            setResult(data.explain);
        } catch {
            setError(
                `${tutor} could not explain this one just now. The written rationale above is still available.`,
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-3 overflow-hidden rounded-2xl border border-blue-200 bg-blue-50/50 dark:border-blue-900/40 dark:bg-blue-950/20">
            <div className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between sm:p-5">
                <div>
                    <p className="font-heading text-sm font-bold text-foreground">
                        Explain this with {tutor}
                    </p>
                    <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                        Plain language, why the choice is right or wrong, a
                        study tip, and a law cite only when the item is actually
                        about one.
                    </p>
                </div>
                <button
                    type="button"
                    onClick={explain}
                    disabled={loading}
                    className="inline-flex cursor-pointer items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-bold text-white transition hover:bg-blue-700 disabled:opacity-60"
                >
                    <Sparkles className="size-3.5" />
                    {loading ? 'Dexter is thinking…' : `Explain with ${tutor}`}
                </button>
            </div>
            {error && (
                <p className="border-t border-blue-200 px-4 py-3 text-xs text-rose-700 sm:px-5 dark:border-blue-900/40 dark:text-rose-300">
                    {error}
                </p>
            )}
            {result && (
                <div className="space-y-3 border-t border-blue-200 px-4 py-4 text-sm leading-relaxed text-foreground sm:px-5 dark:border-blue-900/40">
                    {result.notice && (
                        <p className="text-xs text-muted-foreground">
                            {result.notice}
                        </p>
                    )}
                    <p>{result.eli5}</p>
                    <p>
                        <span className="font-bold">Why this is right. </span>
                        {result.why_right}
                    </p>
                    <p>
                        <span className="font-bold">Why the miss fails. </span>
                        {result.why_wrong}
                    </p>
                    <p>
                        <span className="font-bold">Tip. </span>
                        {result.tip}
                    </p>
                    {result.citation && (
                        <p className="text-xs font-semibold text-muted-foreground">
                            Cite for study: {result.citation}. Practice
                            paraphrase only — not an official CSC text.
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

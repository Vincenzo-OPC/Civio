import { useState } from 'react';
import type { Question } from '../types';
import { apiPost } from '../utils/exam-utils';

export function RememberQuestionForm({ question }: { question?: Question }) {
    const [open, setOpen] = useState(false);
    const [stem, setStem] = useState('');
    const [note, setNote] = useState('');
    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [sending, setSending] = useState(false);

    const submit = async () => {
        setSending(true);
        setError(null);
        setMessage(null);

        try {
            const data = await apiPost<{ message: string }>(
                '/community/recalled-questions',
                {
                    stem,
                    note: note || null,
                    category: question?.category || null,
                    subcategory: question?.subcategory || null,
                },
            );
            setMessage(data.message);
            setStem('');
            setNote('');
        } catch {
            setError(
                'Could not save that paraphrase. Write it in your own words and do not call it an official CSC paper.',
            );
        } finally {
            setSending(false);
        }
    };

    return (
        <div className="mt-3 rounded-2xl border border-border bg-card p-4 sm:p-5">
            <button
                type="button"
                onClick={() => setOpen((value) => !value)}
                className="cursor-pointer text-left"
            >
                <p className="font-heading text-sm font-bold text-foreground">
                    I remember a question
                </p>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                    Send a paraphrase to the practice queue. A moderator reviews
                    it before anyone studies from it. This is not an official
                    CSC or CSDEx paper.
                </p>
            </button>
            {open && (
                <div className="mt-3 space-y-3">
                    <textarea
                        value={stem}
                        onChange={(event) => setStem(event.target.value)}
                        rows={4}
                        placeholder="Paraphrase the question in your own words."
                        className="w-full rounded-xl border border-border bg-background px-3 py-2 text-sm"
                    />
                    <input
                        value={note}
                        onChange={(event) => setNote(event.target.value)}
                        placeholder="Optional note (topic, what felt tricky)"
                        className="w-full rounded-xl border border-border bg-background px-3 py-2 text-sm"
                    />
                    <button
                        type="button"
                        onClick={submit}
                        disabled={sending || stem.trim().length < 12}
                        className="cursor-pointer rounded-xl bg-foreground px-4 py-2 text-xs font-bold text-background disabled:opacity-50"
                    >
                        {sending ? 'Sending…' : 'Submit paraphrase'}
                    </button>
                    {message && (
                        <p className="text-xs font-medium text-emerald-700 dark:text-emerald-300">
                            {message}
                        </p>
                    )}
                    {error && (
                        <p className="text-xs font-medium text-rose-700 dark:text-rose-300">
                            {error}
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

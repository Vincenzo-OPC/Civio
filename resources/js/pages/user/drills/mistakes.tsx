import { Head, Link } from '@inertiajs/react';

interface MistakeItem {
    question_id: number;
    stem: string;
    subject: string;
    wrong_count: number;
}

export default function ReviewMistakes({
    title,
    note,
    items,
}: {
    title: string;
    note: string;
    items: MistakeItem[];
}) {
    const ids = items.map((item) => item.question_id);
    const retry =
        ids.length > 0
            ? `/exams?drill=true&custom_question_ids=${encodeURIComponent(JSON.stringify(ids))}`
            : null;

    return (
        <>
            <Head title={title} />
            <main className="mx-auto flex w-full max-w-3xl flex-col gap-4 px-4 py-6">
                <h1 className="font-heading text-2xl font-semibold tracking-tight">
                    {title}
                </h1>
                <p className="text-sm leading-relaxed text-[var(--civio-ink)]/70">
                    {note}
                </p>
                {items.length === 0 ? (
                    <p className="rounded-xl border border-[var(--civio-line)] px-4 py-6 text-sm">
                        No mistakes to review yet.
                    </p>
                ) : (
                    <>
                        <ul className="flex flex-col gap-3">
                            {items.map((item) => (
                                <li
                                    key={item.question_id}
                                    className="rounded-xl border border-[var(--civio-line)] px-4 py-3"
                                >
                                    <p className="text-xs font-semibold tracking-wide uppercase">
                                        {item.subject}
                                    </p>
                                    <p className="mt-1 text-sm leading-relaxed">
                                        {item.stem}
                                    </p>
                                    <p className="mt-2 text-xs tabular-nums">
                                        Wrong {item.wrong_count}{' '}
                                        {item.wrong_count === 1
                                            ? 'time'
                                            : 'times'}
                                    </p>
                                </li>
                            ))}
                        </ul>
                        {retry && (
                            <Link
                                href={retry}
                                className="inline-flex min-h-11 items-center justify-center rounded-lg bg-[#5B35F5] px-4 text-sm font-semibold text-white dark:bg-[#B3F52D] dark:text-[#0A0A0A]"
                            >
                                Retry these items
                            </Link>
                        )}
                    </>
                )}
            </main>
        </>
    );
}

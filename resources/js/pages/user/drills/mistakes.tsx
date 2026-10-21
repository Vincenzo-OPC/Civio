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
    page,
    lastPage,
    total,
}: {
    title: string;
    note: string;
    items: MistakeItem[];
    page: number;
    lastPage: number;
    total: number;
}) {
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
                        <p className="text-xs text-[var(--civio-ink)]/60 tabular-nums">
                            {total} still open. Page {page} of {lastPage}.
                        </p>
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
                                    <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                                        <p className="text-xs tabular-nums">
                                            Wrong {item.wrong_count}{' '}
                                            {item.wrong_count === 1
                                                ? 'time'
                                                : 'times'}
                                        </p>
                                        <Link
                                            href={`/exams?drill=true&custom_question_ids=${encodeURIComponent(JSON.stringify([item.question_id]))}`}
                                            className="inline-flex min-h-11 items-center justify-center rounded-lg bg-[#5B35F5] px-4 text-sm font-semibold text-white dark:bg-[#B3F52D] dark:text-[#0A0A0A]"
                                        >
                                            Retry
                                        </Link>
                                    </div>
                                </li>
                            ))}
                        </ul>
                        {lastPage > 1 && (
                            <nav className="flex gap-3">
                                {page > 1 && (
                                    <Link
                                        href={`/reviews/mistakes?page=${page - 1}`}
                                        className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                                    >
                                        Newer
                                    </Link>
                                )}
                                {page < lastPage && (
                                    <Link
                                        href={`/reviews/mistakes?page=${page + 1}`}
                                        className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                                    >
                                        Older
                                    </Link>
                                )}
                            </nav>
                        )}
                    </>
                )}
            </main>
        </>
    );
}

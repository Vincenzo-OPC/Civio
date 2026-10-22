import { Head, Link } from '@inertiajs/react';

interface ReviewRow {
    question_id: number;
    stem: string;
    subject: string;
    wrong_count: number;
    status_label: string;
    due_label?: string;
}

function listHref(page: number, duePage: number): string {
    const params = new URLSearchParams();

    if (page > 1) {
        params.set('page', String(page));
    }

    if (duePage > 1) {
        params.set('due_page', String(duePage));
    }

    const query = params.toString();

    return query === '' ? '/reviews/mistakes' : `/reviews/mistakes?${query}`;
}

function retryHref(ids: number[]): string {
    return `/exams?drill=true&custom_question_ids=${encodeURIComponent(JSON.stringify(ids))}`;
}

function Row({ item, action }: { item: ReviewRow; action: boolean }) {
    return (
        <li className="rounded-xl border border-[var(--civio-line)] px-4 py-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-xs font-semibold tracking-wide uppercase">
                    {item.subject}
                </p>
                <p className="text-xs font-semibold">{item.status_label}</p>
            </div>
            <p className="mt-1 text-sm leading-relaxed">{item.stem}</p>
            <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs tabular-nums">
                    {item.due_label
                        ? item.due_label
                        : `Wrong ${item.wrong_count} ${item.wrong_count === 1 ? 'time' : 'times'}`}
                </p>
                {action ? (
                    <Link
                        href={retryHref([item.question_id])}
                        className="inline-flex min-h-11 items-center justify-center rounded-lg bg-[#5B35F5] px-4 text-sm font-semibold text-white dark:bg-[#B3F52D] dark:text-[#0A0A0A]"
                    >
                        Retry
                    </Link>
                ) : null}
            </div>
        </li>
    );
}

export default function ReviewMistakes({
    title,
    note,
    emptyLabel,
    completeLabel,
    dueLabel,
    upcomingLabel,
    needsLabel,
    scheduleNotice,
    scheduleRetryLabel,
    state,
    due,
    dueTotal,
    duePage,
    dueLastPage,
    upcoming,
    nextDueLabel,
    completedCount,
    items,
    page,
    lastPage,
    total,
    freshSameSkillCount = 0,
    freshNotice = null,
}: {
    title: string;
    note: string;
    emptyLabel: string;
    completeLabel: string;
    dueLabel: string;
    upcomingLabel: string;
    needsLabel: string;
    scheduleNotice: string | null;
    scheduleRetryLabel: string;
    state: 'empty' | 'open' | 'complete';
    due: ReviewRow[];
    dueTotal: number;
    duePage: number;
    dueLastPage: number;
    upcoming: ReviewRow[];
    nextDueLabel: string | null;
    completedCount: number;
    items: ReviewRow[];
    page: number;
    lastPage: number;
    total: number;
    freshSameSkillCount?: number;
    freshNotice?: string | null;
}) {
    const dueIds = due.map((item) => item.question_id);

    return (
        <>
            <Head title={title} />
            <main className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-6">
                <header className="flex flex-col gap-2">
                    <h1 className="font-heading text-2xl font-semibold tracking-tight">
                        {title}
                    </h1>
                    <p className="max-w-2xl text-sm leading-relaxed text-[var(--civio-ink)]/70">
                        {note}
                    </p>
                    {freshNotice ? (
                        <p
                            role="status"
                            className="rounded-xl border border-[var(--civio-line)] px-4 py-3 text-sm"
                        >
                            {freshNotice}
                        </p>
                    ) : null}
                    {scheduleNotice ? (
                        <div className="flex flex-col gap-3 rounded-xl border border-[var(--civio-line)] px-4 py-4">
                            <p className="text-sm leading-relaxed">
                                {scheduleNotice}
                            </p>
                            <Link
                                href="/reviews/schedules/retry"
                                method="post"
                                as="button"
                                className="inline-flex min-h-11 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                            >
                                {scheduleRetryLabel}
                            </Link>
                        </div>
                    ) : null}
                    {completedCount > 0 ? (
                        <p className="text-xs text-[var(--civio-ink)]/60 tabular-nums">
                            Completed reviews {completedCount}
                        </p>
                    ) : null}
                </header>

                {state === 'empty' ? (
                    <p className="rounded-xl border border-[var(--civio-line)] px-4 py-6 text-sm">
                        {emptyLabel}
                    </p>
                ) : null}

                {state === 'complete' ? (
                    <p className="rounded-xl border border-[var(--civio-line)] px-4 py-6 text-sm font-semibold">
                        {completeLabel}
                    </p>
                ) : null}

                {due.length > 0 ? (
                    <section className="flex flex-col gap-3">
                        <h2 className="font-heading text-lg font-semibold tracking-tight">
                            {dueLabel}
                        </h2>
                        <p className="text-xs text-[var(--civio-ink)]/60 tabular-nums">
                            {dueTotal} ready now.
                            {dueLastPage > 1
                                ? ` Page ${duePage} of ${dueLastPage}.`
                                : ''}
                        </p>
                        <ul className="flex flex-col gap-3">
                            {due.map((item) => (
                                <Row
                                    key={item.question_id}
                                    item={item}
                                    action
                                />
                            ))}
                        </ul>
                        {dueIds.length > 1 ? (
                            <Link
                                href={retryHref(dueIds)}
                                className="inline-flex min-h-11 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                            >
                                Review Due
                            </Link>
                        ) : null}
                        {freshSameSkillCount > 0 ? (
                            <Link
                                href="/exams?drill=true&fresh_same_skill=1&category_name=Fresh%20practice"
                                className="inline-flex min-h-11 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                            >
                                Practice New Questions on These Skills
                            </Link>
                        ) : (
                            <p className="text-sm">
                                No new questions are left on these skills yet.
                                Review the items above instead.
                            </p>
                        )}
                        {dueLastPage > 1 ? (
                            <nav className="flex gap-3">
                                {duePage > 1 ? (
                                    <Link
                                        href={listHref(page, duePage - 1)}
                                        className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                                    >
                                        Previous
                                    </Link>
                                ) : null}
                                {duePage < dueLastPage ? (
                                    <Link
                                        href={listHref(page, duePage + 1)}
                                        className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                                    >
                                        Next
                                    </Link>
                                ) : null}
                            </nav>
                        ) : null}
                    </section>
                ) : null}

                {upcoming.length > 0 ? (
                    <section className="flex flex-col gap-3">
                        <h2 className="font-heading text-lg font-semibold tracking-tight">
                            {upcomingLabel}
                        </h2>
                        {nextDueLabel ? (
                            <p className="text-xs text-[var(--civio-ink)]/60 tabular-nums">
                                Next review {nextDueLabel}.
                            </p>
                        ) : null}
                        <ul className="flex flex-col gap-3">
                            {upcoming.map((item) => (
                                <Row
                                    key={item.question_id}
                                    item={item}
                                    action={false}
                                />
                            ))}
                        </ul>
                    </section>
                ) : null}

                {state === 'open' ? (
                    <section className="flex flex-col gap-3">
                        <h2 className="font-heading text-lg font-semibold tracking-tight">
                            {needsLabel}
                        </h2>
                        {items.length === 0 ? (
                            <p className="text-sm text-[var(--civio-ink)]/70">
                                None waiting outside the due list.
                            </p>
                        ) : (
                            <>
                                <p className="text-xs text-[var(--civio-ink)]/60 tabular-nums">
                                    {total} still open. Page {page} of{' '}
                                    {lastPage}.
                                </p>
                                <ul className="flex flex-col gap-3">
                                    {items.map((item) => (
                                        <Row
                                            key={item.question_id}
                                            item={item}
                                            action
                                        />
                                    ))}
                                </ul>
                                {lastPage > 1 && (
                                    <nav className="flex gap-3">
                                        {page > 1 && (
                                            <Link
                                                href={listHref(
                                                    page - 1,
                                                    duePage,
                                                )}
                                                className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                                            >
                                                Newer
                                            </Link>
                                        )}
                                        {page < lastPage && (
                                            <Link
                                                href={listHref(
                                                    page + 1,
                                                    duePage,
                                                )}
                                                className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-[var(--civio-line)] px-4 text-sm font-semibold"
                                            >
                                                Older
                                            </Link>
                                        )}
                                    </nav>
                                )}
                            </>
                        )}
                    </section>
                ) : null}
            </main>
        </>
    );
}

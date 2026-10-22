import type { StudyTotals } from '../types';

/** Plain counts from submitted sessions. No scores, rates or forecasts. */
export function StudyTotalsCard({ totals }: { totals?: StudyTotals | null }) {
    const items = totals
        ? [
              { label: 'Sessions submitted', value: totals.sessions },
              { label: 'Questions answered', value: totals.questionsAnswered },
              { label: 'Sessions this week', value: totals.sessionsThisWeek },
          ]
        : [];

    return (
        <section
            aria-labelledby="study-totals-title"
            className="rounded-xl border border-[#E3E5EA] p-5 sm:p-6 dark:border-[#2a2a2a]"
        >
            <h2
                id="study-totals-title"
                className="text-sm font-semibold text-[#101426] dark:text-[#FAFAF7]"
            >
                Your Study So Far
            </h2>
            {totals && totals.sessions > 0 ? (
                <dl className="mt-4 grid grid-cols-3 gap-3">
                    {items.map((item) => (
                        <div key={item.label} className="min-w-0">
                            <dt className="text-xs leading-snug text-[#101426]/60 dark:text-[#FAFAF7]/60">
                                {item.label}
                            </dt>
                            <dd className="mt-1 text-2xl font-semibold text-[#101426] tabular-nums dark:text-[#FAFAF7]">
                                {item.value.toLocaleString()}
                            </dd>
                        </div>
                    ))}
                </dl>
            ) : (
                <p className="mt-2 text-sm text-[#101426]/65 dark:text-[#FAFAF7]/65">
                    No submitted sessions yet. Your counts appear after your
                    first drill or mock.
                </p>
            )}
        </section>
    );
}

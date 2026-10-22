import type { StudyTotals } from '../types';

/** Plain counts from submitted sessions. No scores, rates or forecasts. */
export function StudyTotalsCard({ totals }: { totals?: StudyTotals | null }) {
    const items = totals
        ? [
              { label: 'Sessions', value: totals.sessions },
              { label: 'Questions', value: totals.questionsAnswered },
              { label: 'This Week', value: totals.sessionsThisWeek },
          ]
        : [];
    const hasData = !!totals && totals.sessions > 0;

    return (
        <section
            aria-labelledby="study-totals-title"
            className="dash-panel flex flex-col gap-4 lg:col-span-2 lg:flex-row lg:items-center lg:justify-between"
        >
            <div className="min-w-0">
                <h2 id="study-totals-title" className="dash-title">
                    Study Overview
                </h2>
                <p className="dash-muted mt-0.5 text-sm">
                    {hasData
                        ? 'Counts from your submitted drills and mocks.'
                        : 'No submitted sessions yet. Counts appear after your first drill or mock.'}
                </p>
            </div>
            {hasData ? (
                <dl className="grid grid-cols-3 gap-3 sm:gap-4 lg:w-[34rem] lg:shrink-0">
                    {items.map((item) => (
                        <div
                            key={item.label}
                            className="dash-tile min-w-0 px-3 py-2.5 sm:px-4 sm:py-3"
                        >
                            <dt className="dash-muted text-xs leading-snug">
                                {item.label}
                            </dt>
                            <dd className="mt-1 font-heading text-2xl font-semibold tabular-nums">
                                {item.value.toLocaleString()}
                            </dd>
                        </div>
                    ))}
                </dl>
            ) : null}
        </section>
    );
}

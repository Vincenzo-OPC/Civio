import type { AnalyticsCategory, ChartDataPoint, PacingTrend } from '../types';

/** Lite mode: the same numbers as the charts, as plain text tables. */
export function LiteAnalyticsTables({
    chartData,
    categories,
    pacingTrend,
}: {
    chartData: ChartDataPoint[];
    categories: AnalyticsCategory[];
    pacingTrend: PacingTrend[];
}) {
    const cell = 'border-b px-2 py-1.5 text-left';

    return (
        <div className="flex flex-col gap-5 text-sm">
            <section>
                <h2 className="mb-2 font-semibold">Score history</h2>
                {chartData.length === 0 ? (
                    <p className="text-muted-foreground">No attempts yet.</p>
                ) : (
                    <table className="w-full border-collapse">
                        <thead>
                            <tr>
                                <th className={cell}>Date</th>
                                <th className={cell}>Track</th>
                                <th className={cell}>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {chartData.map((point, i) => (
                                <tr key={`${point.date}-${i}`}>
                                    <td className={cell}>{point.date}</td>
                                    <td className={cell}>{point.track}</td>
                                    <td className={cell}>{point.score}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </section>

            <section>
                <h2 className="mb-2 font-semibold">Subjects</h2>
                {categories.length === 0 ? (
                    <p className="text-muted-foreground">
                        No subject data yet.
                    </p>
                ) : (
                    <table className="w-full border-collapse">
                        <thead>
                            <tr>
                                <th className={cell}>Subject</th>
                                <th className={cell}>Correct</th>
                                <th className={cell}>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {categories.map((category) => (
                                <tr key={category.name}>
                                    <td className={cell}>{category.name}</td>
                                    <td className={cell}>
                                        {category.correct} / {category.total}
                                    </td>
                                    <td className={cell}>
                                        {Math.round(category.percentage)}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </section>

            {pacingTrend.length > 0 && (
                <section>
                    <h2 className="mb-2 font-semibold">Pacing</h2>
                    <table className="w-full border-collapse">
                        <thead>
                            <tr>
                                <th className={cell}>Attempt</th>
                                <th className={cell}>Seconds per item</th>
                                <th className={cell}>Accuracy</th>
                            </tr>
                        </thead>
                        <tbody>
                            {pacingTrend.map((row, i) => (
                                <tr key={`${row.date}-${i}`}>
                                    <td className={cell}>
                                        {row.date || row.name}
                                    </td>
                                    <td className={cell}>
                                        {Math.round(row.secondsPerQuestion)}s
                                        (target about 54s)
                                    </td>
                                    <td className={cell}>
                                        {Math.round(row.accuracy)}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </section>
            )}
        </div>
    );
}

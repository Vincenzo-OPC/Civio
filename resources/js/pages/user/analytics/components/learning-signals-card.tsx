import { Card } from '@/components/ui/card';
import type { LearningSignals } from '../types';

/**
 * Plain-text card (no chart library, Lite-safe). Accuracy counts only answers
 * given without help. A timed-practice note is a suggestion, not a rating.
 */
export function LearningSignalsCard({
    learning,
}: {
    learning: LearningSignals;
}) {
    if (learning.mastery.length === 0 && learning.pace.length === 0) {
        return null;
    }

    const pace = new Map(learning.pace.map((p) => [p.name, p]));

    return (
        <Card className="p-4 sm:p-6">
            <h2 className="text-base font-semibold">
                Independent accuracy and pace
            </h2>
            <p className="mt-1 text-sm text-muted-foreground">
                Counts only answers you gave without seeing the explanation.
            </p>
            <table className="mt-3 w-full text-sm">
                <thead>
                    <tr className="text-left text-muted-foreground">
                        <th className="py-1 font-medium">Subject</th>
                        <th className="py-1 font-medium">Accuracy</th>
                        <th className="py-1 font-medium">Sec / item</th>
                    </tr>
                </thead>
                <tbody>
                    {learning.mastery.map((m) => (
                        <tr key={m.name} className="border-t">
                            <td className="py-1">{m.name}</td>
                            <td className="py-1">
                                {m.percentage}% ({m.correct}/{m.total})
                            </td>
                            <td className="py-1">
                                {pace.get(m.name)?.secondsPerItem ?? '—'}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {learning.skills && learning.skills.length > 0 ? (
                <div className="mt-4">
                    <h3 className="text-sm font-semibold">Skills to work on</h3>
                    <ul className="mt-2 flex flex-col gap-2 text-sm">
                        {learning.skills.map((s) => (
                            <li key={`${s.subject}-${s.skill}`}>
                                <span className="font-medium">{s.skill}</span> (
                                {s.subject}): {s.percentage}% of {s.total} on
                                your own. Next: {s.next}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : null}
            <p className="mt-3 text-sm">
                {learning.retention
                    ? `Still correct a day or more later: ${learning.retention.kept} of ${learning.retention.checked} (${learning.retention.percentage}%).`
                    : 'Retention appears after at least 10 items are re-checked a day or more later.'}
            </p>
            {learning.timedSuggestions.length > 0 ? (
                <p className="mt-3 text-sm">
                    Ready to try timed practice in:{' '}
                    {learning.timedSuggestions.join(', ')}. This is a
                    suggestion; keep checking accuracy under time.
                </p>
            ) : null}
        </Card>
    );
}

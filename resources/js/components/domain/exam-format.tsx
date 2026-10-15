const TRACKS = [
    {
        name: 'Professional',
        count: '150',
        time: '3 hours 10 minutes',
        posts: 'Professional, technical, and supervisory posts.',
    },
    {
        name: 'Subprofessional',
        count: '145',
        time: '2 hours 40 minutes',
        posts: 'Clerical, trades, and custodial posts.',
    },
] as const;

export default function ExamFormat() {
    return (
        <section
            aria-label="Exam format"
            className="border-t border-[var(--civio-line,#e3e5ea)]"
        >
            {TRACKS.map((track) => (
                <div
                    key={track.name}
                    className="grid gap-1 border-b border-[var(--civio-line,#e3e5ea)] py-4 sm:grid-cols-[11rem_1fr] sm:items-baseline sm:gap-6"
                >
                    <h2 className="text-sm font-semibold">{track.name}</h2>
                    <div>
                        <p className="text-sm leading-relaxed">
                            <span className="font-heading text-xl font-semibold tracking-tight">
                                {track.count}
                            </span>{' '}
                            scored items
                            <span className="mx-2 opacity-40">·</span>
                            {track.time}
                        </p>
                        <p className="mt-1 text-sm leading-relaxed opacity-70">
                            {track.posts}
                        </p>
                    </div>
                </div>
            ))}
            <p className="py-4 text-sm leading-relaxed">
                The published general passing rating is at least 80.00. Civio is
                not the Civil Service Commission and is not an official CSC
                reviewer. A practice score is not your result.
            </p>
        </section>
    );
}

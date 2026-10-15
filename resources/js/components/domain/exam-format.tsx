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

const MARK = 120;
const MARK_CENTER = MARK / 2;
const MARK_RADIUS = 46;

export default function ExamFormat() {
    const ring = 2 * Math.PI * MARK_RADIUS;

    return (
        <section
            aria-label="Exam format"
            className="rounded-2xl border border-[#E3E5EA] bg-white p-5 text-[#101426] sm:p-6 dark:border-[#3a415c] dark:bg-[#1a1e30] dark:text-[#FAFAF7]"
        >
            <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-center">
                <div className="relative size-36 shrink-0">
                    <svg
                        viewBox={`0 0 ${MARK} ${MARK}`}
                        className="size-full text-[#101426] dark:text-[#FAFAF7]"
                        aria-hidden
                        style={{ ['--ring' as string]: String(ring) }}
                    >
                        <circle
                            cx={MARK_CENTER}
                            cy={MARK_CENTER}
                            r={MARK_RADIUS}
                            fill="none"
                            stroke="currentColor"
                            strokeOpacity={0.14}
                            strokeWidth={8}
                        />
                        <circle
                            className="civio-pass civio-pass-draw text-[#5B35F5] dark:text-[#C4B6FF]"
                            cx={MARK_CENTER}
                            cy={MARK_CENTER}
                            r={MARK_RADIUS}
                            fill="none"
                            stroke="currentColor"
                            strokeWidth={8}
                            strokeLinecap="round"
                            transform={`rotate(-90 ${MARK_CENTER} ${MARK_CENTER})`}
                        />
                    </svg>
                    <p className="absolute inset-0 flex items-center justify-center font-heading text-3xl font-semibold tracking-tight tabular-nums">
                        80.00
                    </p>
                </div>

                <div className="grid w-full flex-1 gap-5 sm:grid-cols-2">
                    {TRACKS.map((track) => (
                        <div key={track.name}>
                            <h2 className="font-heading text-base font-semibold tracking-tight">
                                {track.name}
                            </h2>
                            <p className="mt-2 leading-none">
                                <span className="font-heading text-2xl font-semibold tracking-tight tabular-nums">
                                    {track.count}
                                </span>
                                <span className="ml-2 text-sm">
                                    scored items
                                </span>
                            </p>
                            <p className="mt-2 text-sm tabular-nums">
                                {track.time}
                            </p>
                            <p className="mt-1 text-sm leading-relaxed text-[#101426]/70 dark:text-[#FAFAF7]/75">
                                {track.posts}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
            <p className="mt-5 text-sm leading-relaxed text-[#101426]/75 dark:text-[#FAFAF7]/75">
                The published general passing rating is at least 80.00. Civio is
                not the Civil Service Commission and is not an official CSC
                reviewer. A practice score is not your result.
            </p>
        </section>
    );
}

import { ArrowUpRight } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const MARK = 120;
const MARK_CENTER = MARK / 2;
const MARK_RADIUS = 46;
const CSC_REFERENCE =
    'https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf';

function useCount(target: number): number {
    const [shown, setShown] = useState(0);
    const from = useRef(0);

    useEffect(() => {
        const reduce = window.matchMedia(
            '(prefers-reduced-motion: reduce)',
        ).matches;

        if (reduce) {
            from.current = target;
            const frame = requestAnimationFrame(() => setShown(target));

            return () => cancelAnimationFrame(frame);
        }

        const startValue = from.current;
        const start = performance.now();
        let frame = 0;
        const tick = (now: number) => {
            const progress = Math.min(1, (now - start) / 700);
            const eased = 1 - (1 - progress) ** 3;

            setShown(Math.round(startValue + (target - startValue) * eased));

            if (progress < 1) {
                frame = requestAnimationFrame(tick);
            } else {
                from.current = target;
            }
        };

        frame = requestAnimationFrame(tick);

        return () => cancelAnimationFrame(frame);
    }, [target]);

    return shown;
}

export default function ExamFormat() {
    const ring = 2 * Math.PI * MARK_RADIUS;
    const mark = useCount(80);

    return (
        <section
            aria-label="About the Exam"
            className="civio-glass civio-rise rounded-2xl border border-white/70 p-5 text-[#101426] sm:p-6 dark:border-white/10 dark:text-[#FAFAF7]"
            style={{ animationDelay: '280ms' }}
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
                            className="civio-pass civio-pass-draw text-[#5B35F5] dark:text-[#B6F72D]"
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
                    <p className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="font-heading text-3xl leading-none font-semibold tracking-tight tabular-nums">
                            {mark}%
                        </span>
                        <span className="mt-1 text-[0.65rem] tracking-[0.14em] uppercase">
                            Passing Mark
                        </span>
                    </p>
                </div>
                <div className="max-w-prose">
                    <h2 className="font-heading text-xl font-semibold tracking-tight">
                        About the Exam
                    </h2>
                    <p className="mt-3 text-sm leading-relaxed text-[#101426]/75 dark:text-[#FAFAF7]/75">
                        The CSC requires a general rating of at least 80.00.
                        Civio mock exams include only scored questions,
                        excluding the separate 20-item Examinee Descriptive
                        Questionnaire.
                    </p>
                    <p className="mt-2 text-sm leading-relaxed text-[#101426]/75 dark:text-[#FAFAF7]/75">
                        Civio is independent and not affiliated with the Civil
                        Service Commission.
                    </p>
                    <a
                        href={CSC_REFERENCE}
                        target="_blank"
                        rel="noreferrer"
                        className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-[#5B35F5] underline-offset-4 hover:underline dark:text-[#B6F72D]"
                    >
                        Official CSC Reference
                        <ArrowUpRight className="size-3.5" aria-hidden />
                    </a>
                </div>
            </div>
        </section>
    );
}

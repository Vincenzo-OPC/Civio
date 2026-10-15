import { formatSitting } from '@/lib/exam-dials';

const SIZE = 200;
const CENTER = SIZE / 2;
const TICK_OUTER = 92;
const ARC_RADIUS = 64;

const ARC_TONE = {
    calm: 'text-[var(--dial,var(--civio-violet,#5B35F5))]',
    amber: 'text-amber-700 dark:text-amber-300',
    red: 'text-[var(--civio-error,#e5484d)]',
    quiet: 'text-current',
} as const;

function polar(index: number, count: number, radius: number) {
    const angle = (index / count) * Math.PI * 2 - Math.PI / 2;

    return {
        x: CENTER + Math.cos(angle) * radius,
        y: CENTER + Math.sin(angle) * radius,
    };
}

function clockFace(seconds: number): string {
    const safe = Math.max(0, Math.floor(seconds));
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);

    return `${hours}:${String(minutes).padStart(2, '0')}`;
}

export interface TimeDialProps {
    /** Full sitting, in seconds. The ring is that sitting, not a score. */
    totalSeconds: number;
    /** Omit to draw the whole sitting. Set to draw time still left. */
    remainingSeconds?: number;
    /** Header countdown: the ring only. The numerals sit beside it. */
    compact?: boolean;
    /** Unselected sitting: full ring, quieter arc. */
    quiet?: boolean;
    tone?: 'calm' | 'amber' | 'red';
    /** Hide from the accessibility tree when nearby text already says the time. */
    decorative?: boolean;
    label?: string;
}

export function TimeDial({
    totalSeconds,
    remainingSeconds,
    compact = false,
    quiet = false,
    tone = 'calm',
    decorative = false,
    label,
}: TimeDialProps) {
    const countdown = remainingSeconds !== undefined;
    const total = Math.max(1, totalSeconds);
    const remaining = countdown
        ? Math.max(0, Math.min(total, remainingSeconds))
        : total;
    const fraction = countdown ? remaining / total : 1;
    const circumference = 2 * Math.PI * ARC_RADIUS;
    const dash = circumference * fraction;
    const tickCount = Math.max(12, Math.round(total / 60 / 5));
    const faceSeconds = countdown ? remaining : total;
    const arcTone = quiet ? ARC_TONE.quiet : ARC_TONE[tone];
    const drawIn = !compact && !countdown && !quiet;

    return (
        <svg
            viewBox={`0 0 ${SIZE} ${SIZE}`}
            className={
                compact
                    ? 'size-7 shrink-0 max-[380px]:hidden'
                    : 'mx-auto size-40 text-[#101426] dark:text-[#FAFAF7]'
            }
            role={decorative ? undefined : 'img'}
            aria-hidden={decorative ? true : undefined}
            aria-label={
                decorative
                    ? undefined
                    : (label ??
                      (countdown
                          ? `${clockFace(remaining)} left of ${formatSitting(total)}`
                          : formatSitting(total)))
            }
            style={{ ['--ring' as string]: String(circumference) }}
        >
            <circle
                cx={CENTER}
                cy={CENTER}
                r={ARC_RADIUS}
                fill="none"
                stroke="currentColor"
                strokeOpacity={0.14}
                strokeWidth={compact ? 18 : 7}
            />
            {compact
                ? null
                : Array.from({ length: tickCount }, (_, index) => {
                      const hour = index % 12 === 0;
                      const inner = polar(
                          index,
                          tickCount,
                          TICK_OUTER - (hour ? 12 : 6),
                      );
                      const outer = polar(index, tickCount, TICK_OUTER);
                      const spent = countdown && index / tickCount > fraction;

                      return (
                          <line
                              key={index}
                              className="civio-tick"
                              x1={inner.x}
                              y1={inner.y}
                              x2={outer.x}
                              y2={outer.y}
                              stroke="currentColor"
                              strokeOpacity={
                                  spent
                                      ? 0.16
                                      : hour
                                        ? 0.85
                                        : quiet
                                          ? 0.35
                                          : 0.62
                              }
                              strokeWidth={hour ? 1.7 : 1}
                              strokeLinecap="round"
                              style={{ animationDelay: `${index * 12}ms` }}
                          />
                      );
                  })}
            <circle
                className={`civio-arc ${drawIn ? 'civio-arc-draw' : ''} ${
                    countdown ? 'civio-arc-live' : ''
                } ${arcTone}`}
                cx={CENTER}
                cy={CENTER}
                r={ARC_RADIUS}
                fill="none"
                stroke="currentColor"
                strokeOpacity={quiet ? 0.45 : 1}
                strokeWidth={compact ? 18 : 7}
                strokeLinecap="round"
                strokeDasharray={`${dash} ${circumference}`}
                transform={`rotate(-90 ${CENTER} ${CENTER})`}
            />
            {compact ? null : (
                <text
                    x={CENTER}
                    y={CENTER + 12}
                    textAnchor="middle"
                    fill="currentColor"
                    fontSize="36"
                    fontWeight="600"
                    style={{
                        fontFamily:
                            'var(--font-heading), ui-sans-serif, system-ui, sans-serif',
                        fontVariantNumeric: 'tabular-nums',
                    }}
                >
                    {clockFace(faceSeconds)}
                </text>
            )}
        </svg>
    );
}

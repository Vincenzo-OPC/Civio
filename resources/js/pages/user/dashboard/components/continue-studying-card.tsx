import { Link } from '@inertiajs/react';
import { ArrowRight } from 'lucide-react';
import type { ExamTrack } from '@/lib/exam-countdown';
import { index as drillsIndex } from '@/routes/drills';
import { index as examsIndex } from '@/routes/exams';
import type { NextModuleItem, RecentAttemptItem } from '../types';

interface ContinueStudyingCardProps {
    nextModule?: NextModuleItem | null;
    latestAttempt?: RecentAttemptItem | null;
    /** Exam level picked in the countdown; a first mock starts at that level. */
    track?: ExamTrack;
}

/**
 * One dominant next action, chosen only from server data:
 * the next unfinished lesson, else more practice after a recent session,
 * else a first Study Mock at the learner's chosen exam level.
 */
export function continueStudyingTarget(
    nextModule?: NextModuleItem | null,
    latestAttempt?: RecentAttemptItem | null,
    track: ExamTrack = 'professional',
): {
    eyebrow: string;
    title: string;
    detail: string | null;
    href: string;
    cta: string;
} {
    if (nextModule) {
        return {
            eyebrow: 'Continue Studying',
            title: nextModule.title,
            detail: [
                nextModule.category_name,
                nextModule.estimated_minutes
                    ? `${nextModule.estimated_minutes} min`
                    : null,
            ]
                .filter(Boolean)
                .join(' · '),
            href: `/learn/${nextModule.slug}`,
            cta: 'Continue',
        };
    }

    if (latestAttempt) {
        return {
            eyebrow: 'Keep Practicing',
            title: 'Start a Practice Drill',
            detail: `Last session: ${latestAttempt.title}, ${latestAttempt.created_at_human}`,
            href: drillsIndex({ query: { from: '/dashboard' } }).url,
            cta: 'Start Drill',
        };
    }

    return {
        eyebrow: 'Get Started',
        title: 'Start a Study Mock',
        detail: `${track === 'subprofessional' ? 'Subprofessional, 145' : 'Professional, 150'} items. Choose Study Mode or Exam Mode next.`,
        href: examsIndex({ query: { start: track, from: '/dashboard' } }).url,
        cta: 'Start Mock',
    };
}

export function ContinueStudyingCard({
    nextModule,
    latestAttempt,
    track,
}: ContinueStudyingCardProps) {
    const target = continueStudyingTarget(nextModule, latestAttempt, track);

    return (
        <section
            aria-labelledby="continue-studying-title"
            className="dash-panel flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
            <div className="min-w-0">
                <p className="dash-eyebrow">{target.eyebrow}</p>
                <h2
                    id="continue-studying-title"
                    className="mt-1 font-heading text-xl font-semibold tracking-tight text-pretty sm:text-2xl"
                >
                    {target.title}
                </h2>
                {target.detail ? (
                    <p className="dash-muted mt-1 text-sm">{target.detail}</p>
                ) : null}
            </div>
            <Link
                href={target.href}
                className="dash-btn w-full shrink-0 sm:w-auto"
            >
                {target.cta}
                <ArrowRight className="size-4" aria-hidden />
            </Link>
        </section>
    );
}

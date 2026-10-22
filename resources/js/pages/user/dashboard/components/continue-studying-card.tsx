import { Link } from '@inertiajs/react';
import { ArrowRight } from 'lucide-react';
import { index as drillsIndex } from '@/routes/drills';
import { index as examsIndex } from '@/routes/exams';
import type { NextModuleItem, RecentAttemptItem } from '../types';

interface ContinueStudyingCardProps {
    nextModule?: NextModuleItem | null;
    latestAttempt?: RecentAttemptItem | null;
}

/**
 * One dominant next action, chosen only from server data:
 * the next unfinished lesson, else more practice after a recent session,
 * else a first Study Mock.
 */
export function continueStudyingTarget(
    nextModule?: NextModuleItem | null,
    latestAttempt?: RecentAttemptItem | null,
): { eyebrow: string; title: string; detail: string | null; href: string } {
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
        };
    }

    if (latestAttempt) {
        return {
            eyebrow: 'Keep Practicing',
            title: 'Start a Practice Drill',
            detail: `Last session: ${latestAttempt.title}, ${latestAttempt.created_at_human}`,
            href: drillsIndex({ query: { from: '/dashboard' } }).url,
        };
    }

    return {
        eyebrow: 'Get Started',
        title: 'Take a Study Mock',
        detail: 'Choose Study Mode or Exam Mode on the next screen.',
        href: examsIndex({ query: { from: '/dashboard' } }).url,
    };
}

export function ContinueStudyingCard({
    nextModule,
    latestAttempt,
}: ContinueStudyingCardProps) {
    const target = continueStudyingTarget(nextModule, latestAttempt);

    return (
        <section
            aria-labelledby="continue-studying-title"
            className="flex flex-col gap-4 rounded-2xl border border-[#E3E5EA] bg-[#FAFAF7] p-5 sm:flex-row sm:items-center sm:justify-between sm:p-6 dark:border-[#2a2a2a] dark:bg-black"
        >
            <div className="min-w-0">
                <p className="text-xs font-semibold tracking-[0.08em] text-[#5B35F5] uppercase dark:text-[#B3F52D]">
                    {target.eyebrow}
                </p>
                <h2
                    id="continue-studying-title"
                    className="mt-1 text-xl font-semibold tracking-tight text-pretty text-[#101426] sm:text-2xl dark:text-[#FAFAF7]"
                >
                    {target.title}
                </h2>
                {target.detail ? (
                    <p className="mt-1 text-sm text-[#101426]/65 dark:text-[#FAFAF7]/65">
                        {target.detail}
                    </p>
                ) : null}
            </div>
            <Link
                href={target.href}
                className="civio-action civio-action-primary inline-flex shrink-0 items-center justify-center gap-2 self-start sm:self-auto"
            >
                Continue
                <ArrowRight className="size-4" aria-hidden />
            </Link>
        </section>
    );
}

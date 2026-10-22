import { Deferred, Head, usePage } from '@inertiajs/react';
import { useEffect, useState } from 'react';
import { AnnouncementsBanner } from '@/components/domain/announcements-banner';
import { PageContainer } from '@/components/layout/page-container';
import { readTrack, TRACK_STORAGE_KEY } from '@/lib/exam-countdown';
import type { ExamTrack } from '@/lib/exam-countdown';
import { AiReadinessBentoCard } from '@/pages/user/dashboard/components/ai-readiness-bento-card';
import { ContinueStudyingCard } from '@/pages/user/dashboard/components/continue-studying-card';
import { DailyGoalStreakCard } from '@/pages/user/dashboard/components/daily-goal-streak-card';
import { DashboardHero } from '@/pages/user/dashboard/components/dashboard-hero';
import { ExamCountdown } from '@/pages/user/dashboard/components/exam-countdown';
import { SmartStudyLaunchers } from '@/pages/user/dashboard/components/smart-study-launchers';
import { StudyScheduleActivityCard } from '@/pages/user/dashboard/components/study-schedule-activity-card';
import { StudyTotalsCard } from '@/pages/user/dashboard/components/study-totals-card';
import type { Auth } from '@/types';
import type { DashboardProps } from './types';

export default function Dashboard({
    stats,
    aiAnalysis,
    dailyGoal,
    todayTasks = [],
    overdueTasksCount = 0,
    recentAttempts = [],
    nextModule,
    studyTotals,
}: DashboardProps) {
    const { auth } = usePage<{ auth: Auth }>().props;
    const firstName = auth?.user?.name ? auth.user.name.split(' ')[0] : null;
    // Exam level from the countdown picker; it also sets which mock a new
    // learner's primary action starts.
    const [track, setTrack] = useState<ExamTrack>(() => {
        try {
            return readTrack(
                typeof window === 'undefined'
                    ? null
                    : localStorage.getItem(TRACK_STORAGE_KEY),
            );
        } catch {
            return 'professional';
        }
    });

    useEffect(() => {
        const pendingExam = localStorage.getItem('pending_free_exam');

        if (pendingExam) {
            window.location.href = '/exams';
        }
    }, []);

    const primaryWeakness = aiAnalysis?.data?.critical_weaknesses?.[0];

    return (
        <PageContainer className="civio-dashboard gap-5 sm:gap-6">
            <Head title="Dashboard" />

            <AnnouncementsBanner />

            <DashboardHero
                firstName={firstName}
                motivationText={aiAnalysis?.data?.encouragement}
            />

            {/* Live countdown to 00:00 PHT on the next CSC-confirmed exam day */}
            <ExamCountdown
                sittings={stats?.examSittings ?? []}
                milestones={stats?.examMilestones ?? []}
                sourceUrl={stats?.examSourceUrl}
                source={stats?.examSource ?? null}
                track={track}
                onTrackChange={setTrack}
            />

            {/* The one primary action, from server data only. */}
            <ContinueStudyingCard
                nextModule={nextModule}
                latestAttempt={recentAttempts[0] ?? null}
                track={track}
            />

            {/* Paired cards stretch to equal row height on lg+ (md columns were too narrow beside the sidebar); natural height on mobile. */}
            <div
                data-dashboard-grid
                className="grid grid-cols-1 items-stretch gap-5 lg:grid-cols-2"
            >
                {/* Lite defers the analysis prop; show a text line until it lands. */}
                <Deferred
                    data="aiAnalysis"
                    fallback={
                        <p className="dash-panel dash-muted text-sm">
                            Loading your practice scores...
                        </p>
                    }
                >
                    <AiReadinessBentoCard aiAnalysis={aiAnalysis} />
                </Deferred>

                <DailyGoalStreakCard dailyGoal={dailyGoal} />

                <SmartStudyLaunchers
                    nextModule={nextModule}
                    primaryWeakness={primaryWeakness}
                />

                <StudyScheduleActivityCard
                    todayTasks={todayTasks}
                    overdueTasksCount={overdueTasksCount}
                    recentAttempts={recentAttempts}
                />

                {/* Counts from stored attempts; full width, no orphan column */}
                <StudyTotalsCard totals={studyTotals} />
            </div>
        </PageContainer>
    );
}

Dashboard.layout = {
    breadcrumbs: [
        {
            title: 'Dashboard',
            href: '/dashboard',
        },
    ],
};

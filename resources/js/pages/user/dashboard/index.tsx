import { Head, usePage } from '@inertiajs/react';
import { useEffect } from 'react';
import { AnnouncementsBanner } from '@/components/domain/announcements-banner';
import { PageContainer } from '@/components/layout/page-container';
import { ContinueStudyingCard } from '@/pages/user/dashboard/components/continue-studying-card';
import { DailyGoalStreakCard } from '@/pages/user/dashboard/components/daily-goal-streak-card';
import { DashboardHero } from '@/pages/user/dashboard/components/dashboard-hero';
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
    const firstName = auth?.user?.name ? auth.user.name.split(' ')[0] : 'User';

    useEffect(() => {
        const pendingExam = localStorage.getItem('pending_free_exam');

        if (pendingExam) {
            window.location.href = '/exams';
        }
    }, []);

    const primaryWeakness = aiAnalysis?.data?.critical_weaknesses?.[0];

    return (
        <PageContainer className="gap-5 sm:gap-6">
            <Head title="Dashboard" />

            {/* Global Announcements Banner */}
            <AnnouncementsBanner />

            {/* High-Impact Integrated Hero Banner */}
            <DashboardHero
                firstName={firstName}
                stats={stats}
                motivationText={aiAnalysis?.data?.encouragement}
                streak={dailyGoal?.streak}
            />

            {/* One dominant next action, from server data only. */}
            <ContinueStudyingCard
                nextModule={nextModule}
                latestAttempt={recentAttempts[0] ?? null}
            />

            <div className="grid grid-cols-1 items-start gap-5 sm:gap-6 md:grid-cols-2">
                {/* Recent sessions and today's study-plan tasks */}
                <StudyScheduleActivityCard
                    todayTasks={todayTasks}
                    overdueTasksCount={overdueTasksCount}
                    recentAttempts={recentAttempts}
                />

                {/* Counts from stored attempts; no readiness forecast */}
                <StudyTotalsCard totals={studyTotals} />

                <DailyGoalStreakCard dailyGoal={dailyGoal} />

                {/* Next steps */}
                <SmartStudyLaunchers
                    nextModule={nextModule}
                    primaryWeakness={primaryWeakness}
                />
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

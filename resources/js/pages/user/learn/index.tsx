import { Head, usePage, router } from '@inertiajs/react';
import { BookOpen, CheckCircle, BarChart } from 'lucide-react';
import React from 'react';
import { toast } from 'sonner';
import { PageContainer } from '@/components/layout/page-container';
import { PageHeader } from '@/components/layout/page-header';
import { HowItWorksModal } from '@/components/shared/how-it-works-modal';
import { connectRealtime } from '@/lib/realtime';
import type { Auth } from '@/types';
import { ModulesGrid } from './components/modules-grid';
import { SearchFilterRow } from './components/search-filter-row';
import { useLearnState } from './hooks/use-learn-state';
import type { LearnIndexProps } from './types';

const progressBarColors: Record<string, string> = {
    'General Information': 'bg-teal-600 dark:bg-teal-500',
    'Verbal Ability': 'bg-blue-600 dark:bg-blue-500',
    'Analytical Ability': 'bg-emerald-600 dark:bg-emerald-500',
    'Numerical Ability': 'bg-orange-600 dark:bg-orange-500',
    'Clerical Ability': 'bg-indigo-600 dark:bg-indigo-500',
};

export default function LearnIndex(props: LearnIndexProps) {
    const { modules = [], categories = [] } = props;
    const { auth, pusher } = usePage<{ auth: { user: Auth }; pusher?: any }>()
        .props;
    const isLoggedIn = !!auth?.user;

    React.useEffect(() => {
        if (!pusher?.key) {
            return;
        }

        return connectRealtime(pusher, (echo) => {
            echo.channel('learn-modules').listen(
                'LearnModulePublished',
                (e: any) => {
                    router.reload({
                        only: ['modules'],
                        onSuccess: () => {
                            toast.success(
                                `New study module available: ${e.module.title}`,
                                {
                                    duration: 8000,
                                },
                            );
                        },
                    });
                },
            );

            return () => {
                echo.disconnect();
            };
        });
    }, [pusher]);

    const activeCategories = React.useMemo(() => {
        return categories.filter((c) => c.name.toLowerCase() !== 'demographic');
    }, [categories]);

    const completedCount = modules.filter((m) => m.is_completed).length;
    const totalCount = modules.length;
    const progressPercent =
        totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

    const categoryStats = React.useMemo(() => {
        const stats: Record<string, { completed: number; total: number }> = {};
        modules.forEach((m) => {
            if (!stats[m.category]) {
                stats[m.category] = { completed: 0, total: 0 };
            }

            stats[m.category].total++;

            if (m.is_completed) {
                stats[m.category].completed++;
            }
        });

        return stats;
    }, [modules]);

    const {
        searchQuery,
        setSearchQuery,
        selectedCategory,
        setSelectedCategory,
        filteredModules,
        groupedModules,
    } = useLearnState(props);

    return (
        <>
            <Head>
                <title>Study Hub | Civio</title>
                <meta
                    name="description"
                    content="Practice notes for Numerical, Verbal, Analytical, Clerical, and General Information. Civio is not the Civil Service Commission."
                />
                <meta property="og:title" content="Study Hub | Civio" />
                <meta
                    property="og:description"
                    content="Practice notes for the exam subjects. These are not a CSC syllabus."
                />
            </Head>
            <PageContainer>
                {/* Header Banner */}
                <div className="mb-8 flex items-start gap-3">
                    <PageHeader
                        title="Study Hub"
                        description="Notes for the exam subjects. They are practice material, not a CSC syllabus."
                        tooltip="Access comprehensive study modules, lessons, formulas, and progress metrics for each major civil service topic."
                    />
                    {isLoggedIn && (
                        <div className="mt-1">
                            <HowItWorksModal
                                title="How the Study Hub Works"
                                tips={[
                                    {
                                        icon: <BookOpen className="size-4" />,
                                        title: 'Review Lessons',
                                        text: 'Read the notes for one subject, then drill that subject.',
                                    },
                                    {
                                        icon: (
                                            <CheckCircle className="size-4" />
                                        ),
                                        title: 'Track Progress',
                                        text: 'Click "Mark as Complete" inside any lesson to record your progress, update your overall progress bar, and display completed badges.',
                                    },
                                    {
                                        icon: <BarChart className="size-4" />,
                                        title: 'Smart Filtering',
                                        text: 'Filter lessons by specific categories to view individual completion percentages, or search keywords to find specific topics.',
                                    },
                                ]}
                            />
                        </div>
                    )}
                </div>

                {/* Overall Progress Card */}
                {isLoggedIn && totalCount > 0 && (
                    <div className="mb-6 rounded-xl border border-border bg-card p-5 shadow-2xs">
                        <div className="mb-3 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <span className="font-heading text-base font-bold text-foreground">
                                    Overall Study Progress
                                </span>
                                <span className="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-extrabold text-blue-700 dark:bg-blue-950/30 dark:bg-blue-950/40 dark:text-blue-400">
                                    {completedCount} / {totalCount} Completed
                                </span>
                            </div>
                            <span className="text-base font-black text-blue-600 dark:text-blue-400">
                                {progressPercent}%
                            </span>
                        </div>
                        <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                            <div
                                className="h-full rounded-full bg-blue-600 transition-all duration-500 dark:bg-blue-500"
                                style={{ width: `${progressPercent}%` }}
                            />
                        </div>

                        {/* Category Progress Grid */}
                        {(() => {
                            const visibleCategories = activeCategories.filter(
                                (cat) =>
                                    cat.name !== 'Clerical Ability' ||
                                    (categoryStats[cat.name]?.total ?? 0) > 0,
                            );

                            return (
                                <div
                                    className={`mt-5 grid grid-cols-1 gap-3 border-t border-border pt-4 sm:grid-cols-2 ${visibleCategories.length >= 5 ? 'lg:grid-cols-5' : 'lg:grid-cols-4'}`}
                                >
                                    {visibleCategories.map((cat) => {
                                        const stats = categoryStats[
                                            cat.name
                                        ] || {
                                            completed: 0,
                                            total: 0,
                                        };
                                        const pct =
                                            stats.total > 0
                                                ? Math.round(
                                                      (stats.completed /
                                                          stats.total) *
                                                          100,
                                                  )
                                                : 0;
                                        const barColor =
                                            progressBarColors[cat.name] ||
                                            'bg-slate-500 dark:bg-slate-400';

                                        return (
                                            <div
                                                key={cat.id}
                                                className="flex flex-col gap-1.5 rounded-lg border border-border/40 bg-slate-50/20 p-3.5 dark:bg-slate-900/10"
                                            >
                                                <div className="flex items-center justify-between text-sm font-bold">
                                                    <span
                                                        className="truncate text-muted-foreground"
                                                        title={cat.name}
                                                    >
                                                        {cat.name}
                                                    </span>
                                                    <span className="ml-1 shrink-0 font-extrabold text-foreground">
                                                        {pct}%
                                                    </span>
                                                </div>
                                                <div className="mt-1 h-2 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800/80">
                                                    <div
                                                        className={`${barColor} h-full rounded-full transition-all duration-500`}
                                                        style={{
                                                            width: `${pct}%`,
                                                        }}
                                                    />
                                                </div>
                                                <span className="mt-0.5 text-xs font-semibold text-muted-foreground/80">
                                                    {stats.completed} of{' '}
                                                    {stats.total} modules
                                                </span>
                                            </div>
                                        );
                                    })}
                                </div>
                            );
                        })()}
                    </div>
                )}

                {/* Search and Category Filter Row */}
                <SearchFilterRow
                    searchQuery={searchQuery}
                    setSearchQuery={setSearchQuery}
                    selectedCategory={selectedCategory}
                    setSelectedCategory={setSelectedCategory}
                    categories={activeCategories}
                    categoryStats={isLoggedIn ? categoryStats : undefined}
                    overallProgressPercent={
                        isLoggedIn ? progressPercent : undefined
                    }
                />

                {/* Modules Grid */}
                <ModulesGrid
                    filteredModules={filteredModules}
                    groupedModules={groupedModules}
                    categories={activeCategories}
                    searchQuery={searchQuery}
                />
            </PageContainer>
        </>
    );
}

// Register layout configuration
LearnIndex.layout = {
    breadcrumbs: [
        {
            title: 'Learn',
            href: '/learn',
        },
    ],
};

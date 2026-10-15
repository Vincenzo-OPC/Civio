import { Link } from '@inertiajs/react';
import {
    BookOpen,
    ClipboardList,
    History,
    Target,
    ArrowRight,
    HelpCircle,
    Award,
    Clock,
    CheckCircle2,
    Lightbulb,
    Info,
    LayoutDashboard,
    Calendar as CalendarIcon,
    TrendingUp,
    Sparkles,
} from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface ReviewerGuideTabsProps {
    showActions?: boolean;
    className?: string;
    tabsClassName?: string;
}

export function ReviewerGuideTabs({
    showActions = false,
    className = 'space-y-8',
    tabsClassName = 'flex border-b border-border overflow-x-auto',
}: ReviewerGuideTabsProps) {
    const [activeTab, setActiveTab] = useState<
        'features' | 'flow' | 'structure' | 'tips'
    >('features');

    const appFeatures = [
        {
            id: 'dashboard',
            title: 'Dashboard & Readiness Tracker',
            badge: 'Home Base',
            icon: LayoutDashboard,
            color: 'text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D] bg-blue-50 dark:bg-blue-950/40 border-blue-200 dark:border-blue-900/40',
            summary:
                'Scores from the mocks and drills you have finished, and a way back into the next one.',
            steps: [
                'A practice average is not a prediction. The published general passing rating is at least 80.00.',
                'Open the subject you missed most, then drill it.',
                'A streak only counts days you studied here. It is not part of the exam.',
            ],
            proTip: 'Spend 2 minutes on the dashboard at the start of every study session to decide whether to read concepts or run drills.',
            actionLabel: 'Go to Dashboard',
            actionUrl: '/dashboard',
        },
        {
            id: 'study-plan',
            title: 'Study Plan & Calendar',
            badge: 'Time Management',
            icon: CalendarIcon,
            color: 'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/40 border-indigo-200 dark:border-indigo-900/40',
            summary:
                'Set your target civil service examination date and schedule manageable daily study blocks.',
            steps: [
                'Set the exam date you are aiming for. The countdown uses that date.',
                'Put one subject on a day, such as Numerical on Monday.',
                'Mark a day complete when you finish it.',
            ],
            proTip: 'Thirty to forty-five minutes a day is easier to keep than one long weekend session.',
            actionLabel: 'Open Study Plan',
            actionUrl: '/study-schedules',
        },
        {
            id: 'study-hub',
            title: 'Study Hub (Learn Modules)',
            badge: 'Notes',
            icon: BookOpen,
            color: 'text-violet-600 dark:text-violet-400 bg-violet-50 dark:bg-violet-950/40 border-violet-200 dark:border-violet-900/40',
            summary:
                'Short notes for the exam subjects: definitions, formulas, and the laws that appear in General Information.',
            steps: [
                'Browse modules categorized by subject (General Information, Verbal, Analytical, Numerical, Clerical).',
                'Read bite-sized lessons with estimated reading times (typically 3–8 minutes each).',
                'Study interactive summaries and formula cheatsheets before attempting practice drills.',
            ],
            proTip: 'Republic Act 6713 and the Constitution are part of General Information. Civio does not promise that any topic is worth a fixed number of points.',
            actionLabel: 'Browse Study Hub',
            actionUrl: '/learn',
        },
        {
            id: 'drills',
            title: 'Custom Practice Drills',
            badge: 'Targeted Practice',
            icon: Target,
            color: 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-900/40',
            summary:
                'Untimed or rapid-fire practice sets with instant answer checking and detailed step-by-step solutions.',
            steps: [
                'Select exact categories or fine-grained subcategories you want to strengthen (e.g., Word Analogy or Number Sequence).',
                'Choose your question count and difficulty level.',
                'Receive immediate answer keys and full explanations right after submitting each item.',
            ],
            proTip: 'Always read the explanation even when you guess correctly — this solidifies the core logic for similar questions.',
            actionLabel: 'Start Practice Drill',
            actionUrl: '/drills',
        },
        {
            id: 'mock-exams',
            title: 'Exam Simulation',
            badge: 'Study Mode or Exam Mode',
            icon: ClipboardList,
            color: 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-900/40',
            summary:
                'Realistic exam simulations matching the exact question count, subtest distribution, and strict time limits.',
            steps: [
                'Select Professional (150 scored items, 3h 10m) or Subprofessional (145 scored items, 2h 40m). The unscored demographic items of the real exam are left out.',
                'Choose Study Mode (Show Explanation on every item, timer optional) or Exam Mode (always timed, answers locked until you submit).',
                'Use the interactive Question Palette on the right to track answered, skipped, and flagged items.',
                'Use the "Flag for Review" feature to mark difficult items and revisit them before final submission.',
            ],
            proTip: 'Train under strict timer discipline: you have about 76 seconds per item on the Professional mock.',
            actionLabel: 'Open a mock',
            actionUrl: '/exams',
        },
        {
            id: 'history',
            title: 'Attempt History & Review',
            badge: 'Error Analysis',
            icon: History,
            color: 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-900/40',
            summary:
                'A complete chronological log of all your completed drills and mock exams with comprehensive answer keys.',
            steps: [
                'View scores, time spent, and subtest breakdown for past attempts.',
                'Click "Review Answers" on any attempt to inspect every stem, your chosen answer, the correct option, and full explanation.',
                'Identify patterns in your wrong answers to prevent repeating the same mistakes.',
            ],
            proTip: 'Keep an error log of questions you missed twice and re-test those specific subcategories using Practice Drills.',
            actionLabel: 'View Attempt History',
            actionUrl: '/history',
        },
        {
            id: 'analytics',
            title: 'Performance Analytics',
            badge: 'Readiness Diagnostics',
            icon: TrendingUp,
            color: 'text-cyan-600 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/40 border-cyan-200 dark:border-cyan-900/40',
            summary:
                'Your practice scores by subject. CSC does not publish a per-subject cutoff.',
            steps: [
                'Compare subjects to see where practice is thin. This is a Civio view, not an official cutoff.',
                'A low percentage means you have missed more of those practice items. It is not an official rating.',
                'Review your average time per item if you want to check pacing.',
            ],
            proTip: 'The published general passing rating is at least 80.00. CSC does not publish a separate minimum for each subtest, so Civio does not treat 70% as an official rule.',
            actionLabel: 'Check Analytics',
            actionUrl: '/analytics',
        },
    ];

    const studySteps = [
        {
            phase: 'Phase 1',
            title: 'Diagnostic Benchmark',
            icon: ClipboardList,
            color: 'text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D] bg-blue-50 dark:bg-blue-950/30',
            description:
                'Begin by taking an initial diagnostic test to establish your baseline score and identify focus subcategories.',
            actionLabel: 'Take Diagnostic Exam',
            actionUrl: '/exams',
            tips: [
                'Choose Professional or Subprofessional level.',
                'Establish your starting score baseline before studying.',
            ],
        },
        {
            phase: 'Phase 2',
            title: 'Conceptual Study Hub',
            icon: BookOpen,
            color: 'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/30',
            description:
                'Read the Study Hub notes for subjects you missed. The notes are practice material, not a CSC syllabus.',
            actionLabel: 'Explore Study Hub',
            actionUrl: '/learn',
            tips: [
                'Focus on topics highlighted as focus areas in your dashboard.',
                'Use the interactive summaries to lock in key concepts and terms.',
            ],
        },
        {
            phase: 'Phase 3',
            title: 'Focused Practice Drills',
            icon: Target,
            color: 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30',
            description:
                'Strengthen weaker subject subcategories with Practice Drills. Create custom sets with active immediate explanations.',
            actionLabel: 'Launch Practice Drill',
            actionUrl: '/drills',
            tips: [
                'Target specific mathematical, verbal, or analytical subcategories.',
                'Read the instant visual explanations immediately after answering each question.',
            ],
        },
        {
            phase: 'Phase 4',
            title: 'Exam Mode Rehearsal',
            icon: Clock,
            color: 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/30',
            description:
                'Take Exam Mode at the real time limit: 150 scored items in 3 hours 10 minutes, or 145 in 2 hours 40 minutes. The clock is practice. It does not mean you will pass.',
            actionLabel: 'Open a mock',
            actionUrl: '/exams',
            tips: [
                'Simulate actual exam conditions in a quiet room without notes or calculators.',
                'On this mock you have about 76 seconds per scored item on Professional, and about 66 on Subprofessional.',
            ],
        },
        {
            phase: 'Phase 5',
            title: 'Mistake Curation & Analytics',
            icon: History,
            color: 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30',
            description:
                'Look at the subjects you missed and the time you spent. Then drill those subjects. The charts are your practice, not an official result.',
            actionLabel: 'Review Attempt History',
            actionUrl: '/history',
            tips: [
                'Review failed attempts once a week to verify you understand the correct logic.',
                'Re-run drills on subcategories where your score is below 80%.',
            ],
        },
    ];

    const examStructure = {
        professional: {
            title: 'Professional Exam Level',
            items: 170,
            scored: 150,
            time: '3 hours and 10 minutes',
            scope: [
                {
                    name: 'General Information',
                    lang: 'in English',
                    subcategories: [
                        'Philippine Constitution',
                        'Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713)',
                        'Peace and Human Rights Issues and Concepts',
                        'Environment Management and Protection',
                    ],
                },
                {
                    name: 'Verbal Ability',
                    lang: 'in English and Filipino',
                    subcategories: [
                        'Word meaning',
                        'Sentence completion',
                        'Error recognition',
                        'Sentence structure',
                        'Paragraph organization',
                        'Reading comprehension',
                    ],
                },
                {
                    name: 'Analytical Ability',
                    lang: 'in English',
                    subcategories: [
                        'Word analogy',
                        'Symbolic logic / abstract reasoning',
                        'Identifying assumptions and drawing conclusions',
                        'Data interpretation',
                    ],
                },
                {
                    name: 'Numerical Ability',
                    lang: 'in English',
                    subcategories: [
                        'Basic operations',
                        'Number sequence',
                        'Word problems',
                    ],
                },
            ],
        },
        subprofessional: {
            title: 'Subprofessional Exam Level',
            items: 165,
            scored: 145,
            time: '2 hours and 40 minutes',
            scope: [
                {
                    name: 'General Information',
                    lang: 'in English',
                    subcategories: [
                        'Philippine Constitution',
                        'Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713)',
                        'Peace and Human Rights Issues and Concepts',
                        'Environment Management and Protection',
                    ],
                },
                {
                    name: 'Verbal Ability',
                    lang: 'in English and Filipino',
                    subcategories: [
                        'Word meaning',
                        'Sentence completion',
                        'Error recognition',
                        'Sentence structure',
                        'Paragraph organization',
                        'Reading comprehension',
                    ],
                },
                {
                    name: 'Clerical Ability',
                    lang: 'in English',
                    subcategories: ['Filing', 'Spelling'],
                },
                {
                    name: 'Numerical Ability',
                    lang: 'in English',
                    subcategories: [
                        'Basic operations',
                        'Number sequence',
                        'Word problems',
                    ],
                },
            ],
        },
    };

    const generalTips = [
        {
            title: 'The passing rating',
            description:
                'The published general passing rating is at least 80.00. CSC does not publish a separate minimum for each subject. A drill score is not that rating.',
            icon: Award,
            color: 'border-l-emerald-500 text-emerald-600 dark:text-emerald-400',
        },
        {
            title: 'Time per item',
            description:
                'In Civio mocks you have about 76 seconds per item on Professional (150 items in 3h 10m) and about 66 seconds on Subprofessional (145 items in 2h 40m). Train your pace in Exam Mode.',
            icon: Clock,
            color: 'border-l-blue-500 text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D]',
        },
        {
            title: 'Analyze Explanations',
            description:
                'Getting questions wrong is part of study optimization. Make it a habit to hover or click on explanations to see the mathematical formula or grammatical rule applied.',
            icon: Lightbulb,
            color: 'border-l-indigo-500 text-indigo-600 dark:text-indigo-400',
        },
    ];

    return (
        <div className={className}>
            {/* Navigation Tabs */}
            <div className={tabsClassName}>
                <button
                    onClick={() => setActiveTab('features')}
                    className={`shrink-0 border-b-2 px-5 py-3 text-sm font-semibold transition-all ${
                        activeTab === 'features'
                            ? 'border-primary font-bold text-primary'
                            : 'border-transparent text-muted-foreground hover:text-foreground'
                    }`}
                >
                    Tools
                </button>
                <button
                    onClick={() => setActiveTab('flow')}
                    className={`shrink-0 border-b-2 px-5 py-3 text-sm font-semibold transition-all ${
                        activeTab === 'flow'
                            ? 'border-primary font-bold text-primary'
                            : 'border-transparent text-muted-foreground hover:text-foreground'
                    }`}
                >
                    Study order
                </button>
                <button
                    onClick={() => setActiveTab('structure')}
                    className={`shrink-0 border-b-2 px-5 py-3 text-sm font-semibold transition-all ${
                        activeTab === 'structure'
                            ? 'border-primary font-bold text-primary'
                            : 'border-transparent text-muted-foreground hover:text-foreground'
                    }`}
                >
                    Exam structure
                </button>
                <button
                    onClick={() => setActiveTab('tips')}
                    className={`shrink-0 border-b-2 px-5 py-3 text-sm font-semibold transition-all ${
                        activeTab === 'tips'
                            ? 'border-primary font-bold text-primary'
                            : 'border-transparent text-muted-foreground hover:text-foreground'
                    }`}
                >
                    Notes
                </button>
            </div>

            {/* Tab: App Features & How-To */}
            {activeTab === 'features' && (
                <div className="space-y-8">
                    <div className="flex items-start gap-3.5 rounded-2xl border border-blue-100 bg-blue-50/80 p-5 dark:border-blue-900/30 dark:bg-blue-950/20">
                        <Sparkles className="mt-0.5 size-5 shrink-0 text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D]" />
                        <div className="space-y-1">
                            <h3 className="text-sm font-bold text-blue-950 dark:text-blue-200">
                                How the tools work
                            </h3>
                            <p className="text-sm leading-relaxed text-blue-800/90 dark:text-[#B3F52D]/80">
                                Each tool does one job. Use a mock when you want
                                the clock. Use a drill when you want one
                                subject.
                            </p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                        {appFeatures.map((feature, idx) => {
                            const IconComponent = feature.icon;

                            return (
                                <Card
                                    key={feature.id}
                                    className="flex flex-col justify-between overflow-hidden border border-border bg-card p-6 shadow-xs transition duration-200 hover:shadow-md"
                                >
                                    <div className="space-y-5">
                                        {/* Header */}
                                        <div className="flex items-start justify-between gap-3">
                                            <div className="flex items-center gap-3">
                                                <div
                                                    className={`flex size-11 shrink-0 items-center justify-center rounded-xl border ${feature.color}`}
                                                >
                                                    <IconComponent className="size-5.5" />
                                                </div>
                                                <div>
                                                    <span className="text-xs font-medium text-muted-foreground">
                                                        {idx + 1}
                                                    </span>
                                                    <h3 className="font-heading text-lg font-semibold text-foreground">
                                                        {feature.title}
                                                    </h3>
                                                </div>
                                            </div>
                                            <span className="rounded-full border border-border bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
                                                {feature.badge}
                                            </span>
                                        </div>

                                        {/* Summary */}
                                        <p className="text-sm leading-relaxed text-muted-foreground">
                                            {feature.summary}
                                        </p>

                                        {/* Steps to Use */}
                                        <div className="space-y-2.5 rounded-xl border border-border/80 bg-muted/40 p-4">
                                            <span className="block text-xs font-medium text-foreground">
                                                How to use
                                            </span>
                                            <ul className="space-y-2 text-xs leading-relaxed text-muted-foreground">
                                                {feature.steps.map(
                                                    (step, sIdx) => (
                                                        <li
                                                            key={sIdx}
                                                            className="flex items-start gap-2"
                                                        >
                                                            <span className="mt-0.5 flex size-4 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-semibold text-primary">
                                                                {sIdx + 1}
                                                            </span>
                                                            <span>{step}</span>
                                                        </li>
                                                    ),
                                                )}
                                            </ul>
                                        </div>

                                        {/* Pro Tip */}
                                        <div className="flex items-start gap-2.5 rounded-xl border border-amber-200/80 bg-amber-50/70 p-3.5 text-xs text-amber-900 dark:border-amber-900/40 dark:bg-amber-950/20 dark:text-amber-300">
                                            <Lightbulb className="mt-0.5 size-4 shrink-0 text-amber-600 dark:text-amber-400" />
                                            <div>
                                                <strong className="font-bold">
                                                    Note:{' '}
                                                </strong>
                                                <span className="leading-relaxed">
                                                    {feature.proTip}
                                                </span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Action Link */}
                                    {showActions && (
                                        <div className="mt-6 border-t border-border pt-4">
                                            <Link
                                                href={feature.actionUrl}
                                                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-xs font-bold text-primary-foreground shadow-xs transition hover:bg-primary/90"
                                            >
                                                <span>
                                                    {feature.actionLabel}
                                                </span>
                                                <ArrowRight className="size-3.5" />
                                            </Link>
                                        </div>
                                    )}
                                </Card>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Tab: Reviewer Study Flow */}
            {activeTab === 'flow' && (
                <div className="space-y-6">
                    <div className="dark:bg-blue-950/30/20 flex items-start gap-3.5 rounded-xl border border-blue-100 bg-blue-50 p-5 dark:border-blue-900/30 dark:bg-blue-950/10">
                        <Info className="mt-0.5 size-5 shrink-0 text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D]" />
                        <div>
                            <h3 className="text-sm font-semibold text-blue-900 dark:text-[#B3F52D]">
                                Study order
                            </h3>
                            <p className="mt-1 text-sm leading-relaxed text-blue-700/95 dark:text-[#B3F52D]/90">
                                Start with a timed mock if you want to see which
                                subjects cost you marks. Then drill those
                                subjects. The four steps below are a study
                                order, not a promise of a score.
                            </p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 gap-3 sm:gap-6 md:grid-cols-2">
                        {studySteps.map((step, idx) => (
                            <Card
                                key={idx}
                                className="hover:border-slate-350 overflow-hidden border border-border bg-card transition duration-200 dark:hover:border-slate-700"
                            >
                                <div className="space-y-4 p-4 sm:p-6">
                                    <div className="flex items-center justify-between">
                                        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600 dark:bg-slate-900 dark:text-slate-400">
                                            {step.phase}
                                        </span>
                                        <div
                                            className={`rounded-lg p-2 ${step.color}`}
                                        >
                                            <step.icon className="size-5" />
                                        </div>
                                    </div>
                                    <div>
                                        <h3 className="font-heading text-lg font-semibold text-foreground">
                                            {step.title}
                                        </h3>
                                        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                                            {step.description}
                                        </p>
                                    </div>

                                    <div className="border-t border-border pt-4">
                                        <h4 className="mb-2 text-xs font-medium text-muted-foreground">
                                            Notes
                                        </h4>
                                        <ul className="space-y-1.5">
                                            {step.tips.map((tip, tIdx) => (
                                                <li
                                                    key={tIdx}
                                                    className="flex items-start gap-2 text-xs font-semibold text-foreground"
                                                >
                                                    <CheckCircle2 className="mt-0.5 size-3.5 shrink-0 text-emerald-500" />
                                                    <span>{tip}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    {showActions && (
                                        <div className="flex justify-end pt-2">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                asChild
                                                className="cursor-pointer gap-1.5 text-xs font-semibold"
                                            >
                                                <Link href={step.actionUrl}>
                                                    {step.actionLabel}
                                                    <ArrowRight className="size-3" />
                                                </Link>
                                            </Button>
                                        </div>
                                    )}
                                </div>
                            </Card>
                        ))}
                    </div>
                </div>
            )}

            {/* Tab: CSE Exam Structure */}
            {activeTab === 'structure' && (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 gap-4 sm:gap-8 lg:grid-cols-2">
                        {/* Professional Section */}
                        <Card className="space-y-6 border border-border bg-card p-4 sm:p-6">
                            <div className="space-y-1.5 border-b border-border pb-4">
                                <h3 className="flex items-center gap-2 font-heading text-xl font-semibold text-foreground">
                                    <Award className="size-5 text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D]" />
                                    {examStructure.professional.title}
                                </h3>
                                <p className="text-sm leading-relaxed text-muted-foreground">
                                    Qualifies eligibility for both first-level
                                    (clerical) and second-level
                                    (technical/scientific) government positions.
                                </p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-4 dark:border-slate-900/50 dark:bg-slate-900/20">
                                    <span className="block text-xs font-medium text-muted-foreground">
                                        Number of Items
                                    </span>
                                    <span className="text-2xl font-semibold text-slate-800 dark:text-white">
                                        {examStructure.professional.scored}{' '}
                                        scored
                                    </span>
                                    <span className="mt-1 block text-xs leading-relaxed font-normal text-muted-foreground">
                                        The paper is{' '}
                                        {examStructure.professional.items}{' '}
                                        items. This mock leaves out the unscored
                                        ones.
                                    </span>
                                </div>
                                <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-4 dark:border-slate-900/50 dark:bg-slate-900/20">
                                    <span className="block text-xs font-medium text-muted-foreground">
                                        Time Limit
                                    </span>
                                    <span className="text-lg font-semibold text-slate-800 dark:text-white">
                                        {examStructure.professional.time}
                                    </span>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <h4 className="text-xs font-medium text-muted-foreground">
                                    Subjects
                                </h4>
                                <div className="divide-y divide-border rounded-xl border border-border">
                                    {examStructure.professional.scope.map(
                                        (scope, idx) => (
                                            <div
                                                key={idx}
                                                className="space-y-2 p-3.5 transition hover:bg-slate-50/30 dark:hover:bg-slate-900/10"
                                            >
                                                <div className="flex items-baseline gap-2">
                                                    <span className="text-sm font-bold text-foreground">
                                                        {scope.name}
                                                    </span>
                                                    <span className="text-[10px] font-semibold text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D]">
                                                        ({scope.lang})
                                                    </span>
                                                </div>
                                                <ol className="ml-4 list-decimal space-y-0.5">
                                                    {scope.subcategories.map(
                                                        (sub, sIdx) => (
                                                            <li
                                                                key={sIdx}
                                                                className="text-xs leading-relaxed text-muted-foreground"
                                                            >
                                                                {sub}
                                                            </li>
                                                        ),
                                                    )}
                                                </ol>
                                            </div>
                                        ),
                                    )}
                                </div>
                            </div>
                        </Card>

                        {/* Subprofessional Section */}
                        <Card className="space-y-6 border border-border bg-card p-4 sm:p-6">
                            <div className="space-y-1.5 border-b border-border pb-4">
                                <h3 className="flex items-center gap-2 font-heading text-xl font-semibold text-foreground">
                                    <Award className="size-5 text-indigo-600 dark:text-indigo-400" />
                                    {examStructure.subprofessional.title}
                                </h3>
                                <p className="text-sm leading-relaxed text-muted-foreground">
                                    Qualifies eligibility exclusively for
                                    first-level government positions (clerical,
                                    custodial, trade services).
                                </p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-4 dark:border-slate-900/50 dark:bg-slate-900/20">
                                    <span className="block text-xs font-medium text-muted-foreground">
                                        Number of Items
                                    </span>
                                    <span className="text-2xl font-semibold text-slate-800 dark:text-white">
                                        {examStructure.subprofessional.scored}{' '}
                                        scored
                                    </span>
                                    <span className="mt-1 block text-xs leading-relaxed font-normal text-muted-foreground">
                                        The paper is{' '}
                                        {examStructure.subprofessional.items}{' '}
                                        items. This mock leaves out the unscored
                                        ones.
                                    </span>
                                </div>
                                <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-4 dark:border-slate-900/50 dark:bg-slate-900/20">
                                    <span className="block text-xs font-medium text-muted-foreground">
                                        Time Limit
                                    </span>
                                    <span className="text-lg font-semibold text-slate-800 dark:text-white">
                                        {examStructure.subprofessional.time}
                                    </span>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <h4 className="text-xs font-medium text-muted-foreground">
                                    Subjects
                                </h4>
                                <div className="divide-y divide-border rounded-xl border border-border">
                                    {examStructure.subprofessional.scope.map(
                                        (scope, idx) => (
                                            <div
                                                key={idx}
                                                className="space-y-2 p-3.5 transition hover:bg-slate-50/30 dark:hover:bg-slate-900/10"
                                            >
                                                <div className="flex items-baseline gap-2">
                                                    <span className="text-sm font-bold text-foreground">
                                                        {scope.name}
                                                    </span>
                                                    <span className="text-[10px] font-semibold text-[#5B35F5] dark:text-[#B3F52D] dark:text-[#B3F52D]">
                                                        ({scope.lang})
                                                    </span>
                                                </div>
                                                <ol className="ml-4 list-decimal space-y-0.5">
                                                    {scope.subcategories.map(
                                                        (sub, sIdx) => (
                                                            <li
                                                                key={sIdx}
                                                                className="text-xs leading-relaxed text-muted-foreground"
                                                            >
                                                                {sub}
                                                            </li>
                                                        ),
                                                    )}
                                                </ol>
                                            </div>
                                        ),
                                    )}
                                </div>
                            </div>
                        </Card>
                    </div>
                </div>
            )}

            {/* Tab: Smart Study Tips */}
            {activeTab === 'tips' && (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 gap-3 sm:gap-6 md:grid-cols-3">
                        {generalTips.map((tip, idx) => (
                            <Card
                                key={idx}
                                className={`border border-l-4 border-border bg-card p-4 sm:p-6 ${tip.color} space-y-4`}
                            >
                                <div className="flex items-center gap-3">
                                    <div className="rounded-lg bg-slate-100 p-2 dark:bg-slate-900">
                                        <tip.icon className="size-5 shrink-0" />
                                    </div>
                                    <h3 className="font-heading text-base leading-tight font-semibold text-foreground">
                                        {tip.title}
                                    </h3>
                                </div>
                                <p className="text-sm leading-relaxed text-muted-foreground">
                                    {tip.description}
                                </p>
                            </Card>
                        ))}
                    </div>

                    <Card className="space-y-4 border border-border bg-card p-4 sm:p-6">
                        <h3 className="flex items-center gap-2 font-heading text-lg font-semibold text-foreground">
                            <HelpCircle className="size-5 text-primary" />
                            Questions
                        </h3>
                        <div className="space-y-4 divide-y divide-border">
                            <div className="space-y-1.5 pt-2">
                                <span className="block text-xs font-bold text-foreground">
                                    Are these official CSC questions?
                                </span>
                                <span className="block text-xs leading-relaxed text-muted-foreground">
                                    No. They are practice questions written for
                                    Civio. They are not past papers. A score
                                    here is not your exam result.
                                </span>
                            </div>
                            <div className="space-y-1.5 pt-4">
                                <span className="block text-xs font-bold text-foreground">
                                    Can I practice with specific subcategories
                                    only?
                                </span>
                                <span className="block text-xs leading-relaxed text-muted-foreground">
                                    Yes. In Practice Drills you can pick one
                                    subject, or one subcategory such as Filing
                                    or the Constitution.
                                </span>
                            </div>
                        </div>
                    </Card>
                </div>
            )}
        </div>
    );
}

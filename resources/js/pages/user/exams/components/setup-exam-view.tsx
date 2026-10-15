import { Head, usePage } from '@inertiajs/react';
import {
    List,
    CheckCircle2,
    Clock,
    Timer,
    ArrowRight,
    BarChart,
    Target,
    Download,
} from 'lucide-react';
import React from 'react';
import { ExamLevelPicker } from '@/components/domain/exam-level-picker';
import { PageContainer } from '@/components/layout/page-container';
import { PageHeader } from '@/components/layout/page-header';
import { HowItWorksModal } from '@/components/shared/how-it-works-modal';
import type { ExamDialId } from '@/lib/exam-dials';
import type { Auth } from '@/types';
import type { SimulationDetails } from '../types';
import type { ExamMode } from '../utils/exam-mode';
import { EXAM_MODE_LABELS, EXAM_MODES } from '../utils/exam-mode';

const MODE_BLURBS: Record<ExamMode, string> = {
    study: 'Practice the full mock with Reveal, Dexter and Copy for AI on every item. The timer is your choice.',
    strict: 'Exam-day rehearsal: always timed, no Reveal, Dexter or Copy for AI. Answers unlock only after you submit.',
};

interface SetupExamViewProps {
    selectedExamId: number | null;
    setSelectedExamId: (id: number) => void;
    details: SimulationDetails;
    examMode: ExamMode;
    setExamMode: (mode: ExamMode) => void;
    studyTimed: boolean;
    setStudyTimed: (timed: boolean) => void;
    handleBeginExam: () => void;
    handlePrintExam: () => void;
    isPrinting?: boolean;
    customConfirmModal: React.ReactNode;
}

export function SetupExamView({
    selectedExamId,
    setSelectedExamId,
    details,
    examMode,
    setExamMode,
    studyTimed,
    setStudyTimed,
    handleBeginExam,
    handlePrintExam,
    isPrinting = false,
    customConfirmModal,
}: SetupExamViewProps) {
    const { auth } = usePage<{ auth: Auth }>().props;

    const onPrint = () => {
        handlePrintExam();
    };

    return (
        <>
            <Head title="Exam Simulation" />

            <PageContainer>
                {/* Header Information Section */}
                <div className="mb-8 flex items-start gap-3">
                    <PageHeader
                        title="Exam Simulation"
                        description="Pick your level, then choose Study Mock (learn as you go) or Strict Mock (exam-day rehearsal)."
                        tooltip="A full-length mock built on the Civil Service Exam format. Civio is not affiliated with the CSC."
                    />
                    <div className="mt-1">
                        <HowItWorksModal
                            title="How Exam Simulation Works"
                            tips={[
                                {
                                    icon: <Clock className="size-4" />,
                                    title: 'Two Modes',
                                    text: 'Study Mock keeps Reveal on every item and lets you turn the timer off. Strict Mock is always timed and cannot be paused.',
                                },
                                {
                                    icon: <BarChart className="size-4" />,
                                    title: 'Post-Exam Review',
                                    text: 'In a Strict Mock, answers stay locked until you submit the whole exam. Then use the review to study your mistakes.',
                                },
                                {
                                    icon: <Target className="size-4" />,
                                    title: 'Passing Target',
                                    text: 'Aim for a score of 80% or higher, which is the actual passing rate for the official Civil Service Exam.',
                                },
                            ]}
                        />
                    </div>
                </div>

                {/* Primary Column Grid Layout */}
                <div className="grid grid-cols-1 gap-3 sm:gap-6 lg:grid-cols-3">
                    {/* Left Panel: Level Selectors */}
                    <div className="flex flex-col gap-4 lg:col-span-2">
                        <ExamLevelPicker
                            value={
                                selectedExamId === 2
                                    ? 'subprofessional'
                                    : 'professional'
                            }
                            onChange={(id: ExamDialId) =>
                                setSelectedExamId(id === 'subprofessional' ? 2 : 1)
                            }
                        />

                        {/* Exam Simulation mode */}
                        <fieldset className="rounded-xl border-2 border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
                            <legend className="px-1 font-heading text-sm font-black tracking-tight text-slate-900 dark:text-white">
                                Mode
                            </legend>
                            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                                {EXAM_MODES.map((mode) => (
                                    <label
                                        key={mode}
                                        className={`flex cursor-pointer flex-col gap-1 rounded-lg border-2 p-3 ${
                                            examMode === mode
                                                ? 'border-[#5B35F5] bg-[#F4F5F2] dark:border-[#8b74ff] dark:bg-[#1a1e30]'
                                                : 'border-[#E3E5EA] dark:border-[#2c3148]'
                                        }`}
                                    >
                                        <span className="flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-white">
                                            <input
                                                type="radio"
                                                name="exam-mode"
                                                value={mode}
                                                checked={examMode === mode}
                                                onChange={() =>
                                                    setExamMode(mode)
                                                }
                                            />
                                            {EXAM_MODE_LABELS[mode]}
                                        </span>
                                        <span className="text-xs leading-relaxed text-slate-500 dark:text-slate-400">
                                            {MODE_BLURBS[mode]}
                                        </span>
                                    </label>
                                ))}
                            </div>
                            <label className="mt-3 flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300">
                                <input
                                    type="checkbox"
                                    checked={
                                        examMode === 'strict' || studyTimed
                                    }
                                    disabled={examMode === 'strict'}
                                    onChange={(e) =>
                                        setStudyTimed(e.target.checked)
                                    }
                                />
                                {examMode === 'strict'
                                    ? 'Timer on (always on in Strict Mock)'
                                    : 'Time this Study Mock'}
                            </label>
                        </fieldset>
                    </div>

                    {/* Right Panel: Simulation Overview */}
                    <div className="flex min-h-[380px] flex-col justify-between rounded-xl border border-[#E3E5EA] bg-[#FAFAF7] p-4 sm:p-6 dark:border-[#2c3148] dark:bg-[#101426]">
                        <div>
                            <h2 className="mb-4 border-b border-[#E3E5EA] pb-2 font-heading text-xl font-semibold tracking-tight text-[#101426] dark:border-[#2c3148] dark:text-[#FAFAF7]">
                                Simulation Overview
                            </h2>

                            {/* Simulation Specs List */}
                            <div className="mt-2 flex flex-col gap-4.5">
                                {/* Total Items */}
                                <div className="flex items-center justify-between text-xs font-semibold">
                                    <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                                        <List className="size-4 text-slate-400 dark:text-slate-500" />
                                        <span>Total Items</span>
                                    </div>
                                    <span className="font-bold text-slate-900 dark:text-white">
                                        {details.totalItems}
                                    </span>
                                </div>

                                {/* Scored Items */}
                                <div className="flex items-center justify-between text-xs font-semibold">
                                    <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                                        <CheckCircle2 className="size-4 text-slate-400 dark:text-slate-500" />
                                        <span>Scored Items</span>
                                    </div>
                                    <span className="font-bold text-slate-900 dark:text-white">
                                        {details.scoredItems}
                                    </span>
                                </div>

                                {/* Time Limit */}
                                <div className="flex items-center justify-between text-xs font-semibold">
                                    <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                                        <Clock className="size-4 text-slate-400 dark:text-slate-500" />
                                        <span>Time Limit</span>
                                    </div>
                                    <span className="font-bold text-slate-900 dark:text-white">
                                        {examMode === 'study' && !studyTimed
                                            ? 'Untimed'
                                            : details.timeLimit}
                                    </span>
                                </div>

                                {/* Target Pace */}
                                <div className="flex items-center justify-between text-xs font-semibold">
                                    <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                                        <Timer className="size-4 text-slate-400 dark:text-slate-500" />
                                        <span>Target Pace</span>
                                    </div>
                                    <span className="font-bold text-slate-900 dark:text-white">
                                        {details.targetPace}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="mt-6 flex gap-3">
                            <button
                                onClick={handleBeginExam}
                                className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-[#5B35F5] py-3 text-xs font-semibold text-white hover:bg-[#3D20C8] focus-visible:outline-none"
                            >
                                Begin {EXAM_MODE_LABELS[examMode]}
                                <ArrowRight className="size-4" />
                            </button>
                            {(auth.user?.role === 'admin' ||
                                auth.user?.can_download_pdf) && (
                                <button
                                    onClick={onPrint}
                                    disabled={isPrinting}
                                    title="Download PDF Exam Booklet"
                                    className="group flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-3 text-xs font-semibold text-slate-700 shadow-sm transition-all hover:border-blue-300 hover:bg-slate-50 hover:text-blue-600 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                                >
                                    {isPrinting ? (
                                        <div className="size-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
                                    ) : (
                                        <Download className="size-5 text-slate-500 transition-colors group-hover:text-blue-600 dark:text-slate-400" />
                                    )}
                                </button>
                            )}
                        </div>

                        <p className="mt-2 text-center text-[11px] leading-relaxed text-slate-500 dark:text-slate-400">
                            💡{' '}
                            <span className="font-semibold text-slate-700 dark:text-slate-300">
                                PDF Booklet:
                            </span>{' '}
                            Automatically generates a high-resolution, A4 PDF
                            exam booklet with answer key.
                        </p>
                    </div>
                </div>
            </PageContainer>
            {customConfirmModal}
        </>
    );
}

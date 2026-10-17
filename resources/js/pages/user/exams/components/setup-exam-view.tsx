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
    study: 'Practice at your own pace with explanations, question copying, and access to your preferred AI assistant. Choose whether to use a timer.',
    strict: 'Rehearse exam day under timed conditions, without explanations or AI assistance. Review your answers after submitting the exam.',
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
                        description="Pick a level, then choose Study Mode or Exam Mode."
                        tooltip="A full-length mock built on the Civil Service Exam format. Civio is not affiliated with the CSC."
                    />
                    <div className="mt-1">
                        <HowItWorksModal
                            title="How Exam Simulation Works"
                            tips={[
                                {
                                    icon: <Clock className="size-4" />,
                                    title: 'Two Modes',
                                    text: 'Study Mode keeps Show Explanation on every item and lets you turn the timer off. Exam Mode is always timed and cannot be paused.',
                                },
                                {
                                    icon: <BarChart className="size-4" />,
                                    title: 'Post-Exam Review',
                                    text: 'In Exam Mode, answers stay locked until you submit the whole exam. Then use the review to study your mistakes.',
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
                                setSelectedExamId(
                                    id === 'subprofessional' ? 2 : 1,
                                )
                            }
                        />

                        {/* Exam Simulation mode */}
                        <fieldset className="rounded-2xl border border-[#E3E5EA] bg-white p-5 dark:border-[#2a2a2a] dark:bg-[#141414]">
                            <legend className="sr-only">
                                Study Mode or Exam Mode
                            </legend>
                            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                                {EXAM_MODES.map((mode) => (
                                    <label
                                        key={mode}
                                        className={`flex cursor-pointer flex-col gap-1 rounded-xl border p-3 transition-colors ${
                                            examMode === mode
                                                ? 'border-2 border-[#5B35F5] bg-[#FAFAF7] dark:border-[#B3F52D] dark:bg-black'
                                                : 'border-[#E3E5EA] hover:border-[#5B35F5]/40 dark:border-[#2a2a2a]'
                                        }`}
                                    >
                                        <span className="flex items-center gap-2 text-sm font-semibold text-[#101426] dark:text-[#FAFAF7]">
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
                                    ? 'Always timed. You cannot turn this off.'
                                    : 'Time this Study Mode'}
                            </label>
                        </fieldset>
                    </div>

                    {/* Right Panel: Simulation Overview */}
                    <div className="flex min-h-[380px] flex-col justify-between rounded-xl border border-[#E3E5EA] bg-[#FAFAF7] p-4 sm:p-6 dark:border-[#2a2a2a] dark:bg-black">
                        <div>
                            <h2 className="mb-4 border-b border-[#E3E5EA] pb-2 font-heading text-xl font-semibold tracking-tight text-[#101426] dark:border-[#2a2a2a] dark:text-[#FAFAF7]">
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
                                    <span className="font-semibold text-[#101426] tabular-nums dark:text-[#FAFAF7]">
                                        {details.totalItems}
                                    </span>
                                </div>

                                {/* Scored Items */}
                                <div className="flex items-center justify-between text-xs font-semibold">
                                    <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                                        <CheckCircle2 className="size-4 text-slate-400 dark:text-slate-500" />
                                        <span>Scored Items</span>
                                    </div>
                                    <span className="font-semibold text-[#101426] tabular-nums dark:text-[#FAFAF7]">
                                        {details.scoredItems}
                                    </span>
                                </div>

                                {/* Time Limit */}
                                <div className="flex items-center justify-between text-xs font-semibold">
                                    <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                                        <Clock className="size-4 text-slate-400 dark:text-slate-500" />
                                        <span>Time Limit</span>
                                    </div>
                                    <span className="font-semibold text-[#101426] tabular-nums dark:text-[#FAFAF7]">
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
                                    <span className="font-semibold text-[#101426] tabular-nums dark:text-[#FAFAF7]">
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
                                    title="Download PDF & Answer Key"
                                    aria-label="Download PDF & Answer Key"
                                    className="group flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-3 text-xs font-semibold text-slate-700 shadow-sm transition-all hover:border-blue-300 hover:bg-slate-50 hover:text-[#5B35F5] disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                                >
                                    {isPrinting ? (
                                        <div className="size-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
                                    ) : (
                                        <Download className="size-4" />
                                    )}
                                    Download PDF &amp; Answer Key
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </PageContainer>
            {customConfirmModal}
        </>
    );
}

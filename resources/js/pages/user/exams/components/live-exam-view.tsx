import { Head, usePage } from '@inertiajs/react';
import {
    LayoutGrid,
    AlertCircle,
    Flag,
    ChevronLeft,
    ChevronRight,
    CheckCircle2,
    Lock,
    LogIn,
    Keyboard,
    Maximize2,
    Minimize2,
    Edit3,
    Strikethrough,
} from 'lucide-react';
import { useState, useMemo, useEffect, useCallback } from 'react';
import { toast } from 'sonner';
import { ReportIssueModal } from '@/components/domain/report-issue-modal';
import LiteModeToggle from '@/components/shared/lite-mode-toggle';
import { DarkModeToggle } from '@/components/shared/theme-toggle';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from '@/components/ui/dialog';

import { useLiteMode } from '@/hooks/use-lite-mode';
import type { AiHandoffAttemptState } from '@/lib/ai-handoff';
import { renderFormattedText } from '@/lib/exam-formatters';
import { combinedStudyBias } from '@/lib/guest-study-bias';
import { useContentShield } from '../hooks/use-content-shield';
import type { ExamClockSnapshot } from '../hooks/use-exam-timer';
import type { Question, SimulationDetails } from '../types';
import { answerOptionVisual } from '../utils/answer-state';
import type { ExamMode } from '../utils/exam-mode';
import { showsStudyTools, EXAM_MODE_LABELS } from '../utils/exam-mode';
import { WITHDRAWN_LIVE_NOTICE } from '../utils/retired-notice';
import { AskAssistantButton } from './ask-assistant-button';
import { CopyForAiButton } from './copy-for-ai-button';
import { ExamTimerDisplay } from './exam-timer-display';
import { LiteExamBody } from './lite-exam-body';
import QuestionPalettePanel from './question-palette-panel';
import { AnswerOption } from './session/answer-option';
import { AnswerReveal, readRevealTutor } from './session/answer-reveal';
import type { RevealTutorPayload } from './session/answer-reveal';
import { PauseOverlay } from './session/pause-overlay';

interface RevealedAnswer {
    questionId: number;
    letter: string;
    text: string;
    /** Correct option as an index into the displayed (shuffled) options. */
    displayIndex: number;
    explanation?: string | null;
    hasConflict?: boolean;
    tutor?: RevealTutorPayload | null;
}

interface LiveExamViewProps {
    details: SimulationDetails;
    isDrillSession?: boolean;
    activeQuestions: Question[];
    currentIdx: number;
    isTimed: boolean;
    /** Exam Simulation mode; Strict hides Reveal, Dexter and Copy for AI. */
    examMode?: ExamMode;
    timeLeft: number;
    itemElapsed: number;
    formatTime: (secs: number) => string;
    handleExitExam: () => void;
    setIsMobilePaletteOpen: (val: boolean) => void;
    toggleFlag: (idx: number) => void;
    flagged: Record<number, boolean>;
    answers: Record<number, number>;
    handleSelectOption: (idx: number) => void;
    handleQuestionNavigate: (idx: number) => void;
    isFreeAttempt: boolean;
    setShowRegisterModal: (val: boolean) => void;
    handleSubmitExam: (isTimeout: boolean) => void;
    selectedPaletteCategory: string;
    handleCategoryChange: (cat: string) => void;
    isMobilePaletteOpen: boolean;
    showLockedModal: boolean;
    setShowLockedModal: (val: boolean) => void;
    handleRegisterFromFreeExam: () => void;
    showRegisterModal: boolean;
    handleCancelFreeExam: () => void;
    customConfirmModal: React.ReactNode;
    isPaused?: boolean;
    canPause?: boolean;
    onPause?: () => void;
    onResume?: () => void;
    subscribeClock?: (listener: () => void) => () => void;
    getClockSnapshot?: () => ExamClockSnapshot;
    practiceBatchId?: string | null;
    examSessionId?: string | null;
}

export function LiveExamView({
    details,
    isDrillSession = false,
    activeQuestions,
    currentIdx,
    isTimed,
    examMode = 'study',
    timeLeft,
    itemElapsed,
    formatTime,
    handleExitExam,
    setIsMobilePaletteOpen,
    toggleFlag,
    flagged,
    answers,
    handleSelectOption: selectOption,
    handleQuestionNavigate,
    isFreeAttempt,
    setShowRegisterModal,
    handleSubmitExam,
    selectedPaletteCategory,
    handleCategoryChange,
    isMobilePaletteOpen,
    showLockedModal,
    setShowLockedModal,
    handleRegisterFromFreeExam,
    showRegisterModal,
    handleCancelFreeExam,
    customConfirmModal,
    isPaused = false,
    canPause = false,
    onPause,
    onResume,
    subscribeClock,
    getClockSnapshot,
    practiceBatchId = null,
    examSessionId = null,
}: LiveExamViewProps) {
    const activeQuestion = activeQuestions[currentIdx];
    // Withdrawn by Civio mid-mock: labelled, takes no new answer, not scored.
    const isWithdrawn = Boolean(activeQuestion?.withdrawn);
    const handleSelectOption = useCallback(
        (idx: number) => {
            if (!isWithdrawn) {
                selectOption(idx);
            }
        },
        [isWithdrawn, selectOption],
    );
    const studyTools = showsStudyTools(examMode, isDrillSession);
    const { lite } = useLiteMode();
    const [isReportModalOpen, setIsReportModalOpen] = useState(false);
    const [liveStatusFilter, setLiveStatusFilter] = useState<
        'all' | 'unanswered' | 'answered' | 'flagged'
    >('all');
    const [showKeyboardModal, setShowKeyboardModal] = useState(false);

    // Advanced UI/UX feature states
    const [eliminatedOptions, setEliminatedOptions] = useState<
        Record<number, Record<number, boolean>>
    >({});
    const [scratchpadNotes, setScratchpadNotes] = useState<string>(() => {
        return localStorage.getItem('exam_scratchpad_notes') || '';
    });
    const [isScratchpadOpen, setIsScratchpadOpen] = useState(false);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [isPaletteCollapsed, setIsPaletteCollapsed] = useState(true);
    const [toolsOpen, setToolsOpen] = useState(false);
    const [revealedAnswer, setRevealedAnswer] = useState<RevealedAnswer | null>(
        null,
    );

    // Structured state for Copy for AI. The answer key is only passed once
    // the learner has revealed this question; it is never fetched to copy.
    const liveHandoffAttempt = (questionId: number): AiHandoffAttemptState => {
        const revealed =
            revealedAnswer !== null && revealedAnswer.questionId === questionId;

        return {
            selectedDisplayIndex: answers[currentIdx],
            mode: isDrillSession ? 'study' : 'live',
            revealed,
            verifiedCorrectDisplayIndex: revealed
                ? revealedAnswer.displayIndex
                : undefined,
            verifiedExplanation: revealed
                ? revealedAnswer.explanation
                : undefined,
            questionNumber: currentIdx + 1,
            totalQuestions: activeQuestions.length,
            examLevel: 'Practice',
        };
    };

    const {
        isShielded,
        isResumeLocked,
        dismissShield,
        styleBlock,
        contentRef,
        wrapperProps,
    } = useContentShield({
        contentLabel: 'Exam',
        onCopyAttempt: (msg) => toast.error(msg),
    });

    // Auto-save scratchpad notes
    const handleScratchpadChange = (val: string) => {
        setScratchpadNotes(val);
        localStorage.setItem('exam_scratchpad_notes', val);
    };

    // Fullscreen toggle handler
    const toggleFullscreen = () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(() => {});
            setIsFullscreen(true);
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen().catch(() => {});
            }

            setIsFullscreen(false);
        }
    };

    useEffect(() => {
        const handleFsChange = () => {
            setIsFullscreen(!!document.fullscreenElement);
        };
        document.addEventListener('fullscreenchange', handleFsChange);

        return () =>
            document.removeEventListener('fullscreenchange', handleFsChange);
    }, []);

    // Toggle option strike-through (elimination)
    const toggleElimination = (
        e: React.MouseEvent,
        questionIdx: number,
        optionIdx: number,
    ) => {
        e.stopPropagation();
        const isCurrentlyEliminated =
            eliminatedOptions[questionIdx]?.[optionIdx];
        const willBeEliminated = !isCurrentlyEliminated;

        // If eliminating an option that is currently selected as answer, deselect it first
        if (willBeEliminated && answers[questionIdx] === optionIdx) {
            handleSelectOption(optionIdx);
        }

        setEliminatedOptions((prev) => {
            const qElim = prev[questionIdx] || {};

            return {
                ...prev,
                [questionIdx]: {
                    ...qElim,
                    [optionIdx]: willBeEliminated,
                },
            };
        });
    };

    const { user_reports_map = {} } = usePage<{
        user_reports_map?: Record<string, 'pending' | 'resolved' | 'dismissed'>;
    }>().props;

    const [localReportsMap, setLocalReportsMap] =
        useState<Record<string, 'pending' | 'resolved' | 'dismissed'>>(
            user_reports_map,
        );

    useEffect(() => {
        const handleReportSubmitted = (
            e: CustomEvent<{ flaggable_id: number }>,
        ) => {
            if (e.detail && e.detail.flaggable_id) {
                setLocalReportsMap((prev) => ({
                    ...prev,
                    [`App\\Models\\Question:${e.detail.flaggable_id}`]:
                        'pending',
                }));
            }
        };

        window.addEventListener(
            'report-submitted',
            handleReportSubmitted as EventListener,
        );

        return () => {
            window.removeEventListener(
                'report-submitted',
                handleReportSubmitted as EventListener,
            );
        };
    }, []);

    const reportStatus = activeQuestion
        ? localReportsMap[`App\\Models\\Question:${activeQuestion.id}`]
        : undefined;
    const isReported = reportStatus === 'pending';

    // Live statistics & pacing calculations
    const stats = useMemo(() => {
        let answered = 0;
        let unanswered = 0;
        let flaggedCount = 0;

        (activeQuestions || []).forEach((q, idx) => {
            if (flagged && flagged[idx]) {
                flaggedCount++;
            }

            const isDemographic =
                q.category === 'Demographic Profile' ||
                q.category?.toLowerCase().includes('demographic') ||
                q.isDemographic;

            if (isDemographic) {
                return;
            }

            const chosen = answers ? answers[idx] : undefined;

            if (chosen !== undefined && chosen !== null) {
                answered++;
            } else {
                unanswered++;
            }
        });

        const totalGraded = answered + unanswered;
        const progressPct =
            totalGraded > 0 ? Math.round((answered / totalGraded) * 100) : 0;

        // Target Pace: seconds available per remaining unanswered question
        const targetPace =
            unanswered > 0 ? Math.round(timeLeft / unanswered) : 0;

        let paceStatus: 'good' | 'warn' | 'behind' = 'good';

        if (targetPace < 20) {
            paceStatus = 'behind';
        } else if (targetPace < 40) {
            paceStatus = 'warn';
        }

        return {
            answered,
            unanswered,
            flagged: flaggedCount,
            totalGraded,
            progressPct,
            targetPace,
            paceStatus,
        };
    }, [activeQuestions, answers, flagged, timeLeft]);

    const onOptionClick = (optIdx: number) => {
        if (isPaused) {
            return;
        }

        handleSelectOption(optIdx);
    };

    // Navigation-only Keyboard Listener (security keys handled by useContentShield)
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (isPaused) {
                return;
            }

            if (e.key === 'Escape' && toolsOpen) {
                setToolsOpen(false);

                return;
            }

            if (
                ['INPUT', 'TEXTAREA', 'SELECT'].includes(
                    (e.target as HTMLElement)?.tagName,
                )
            ) {
                return;
            }

            if (e.key === 'ArrowRight' || e.key === ']' || e.key === 'n') {
                if (currentIdx < activeQuestions.length - 1) {
                    handleQuestionNavigate(currentIdx + 1);
                }
            } else if (
                e.key === 'ArrowLeft' ||
                e.key === '[' ||
                e.key === 'p'
            ) {
                if (currentIdx > 0) {
                    handleQuestionNavigate(currentIdx - 1);
                }
            } else if (e.key === 'f' || e.key === 'F') {
                toggleFlag(currentIdx);
            } else if (e.key === '?' || e.key === '/') {
                e.preventDefault();
                setShowKeyboardModal((prev) => !prev);
            } else if (
                [
                    '1',
                    '2',
                    '3',
                    '4',
                    '5',
                    'a',
                    'b',
                    'c',
                    'd',
                    'e',
                    'A',
                    'B',
                    'C',
                    'D',
                    'E',
                ].includes(e.key)
            ) {
                const optionMap: Record<string, number> = {
                    '1': 0,
                    a: 0,
                    A: 0,
                    '2': 1,
                    b: 1,
                    B: 1,
                    '3': 2,
                    c: 2,
                    C: 2,
                    '4': 3,
                    d: 3,
                    D: 3,
                    '5': 4,
                    e: 4,
                    E: 4,
                };
                const optIdx = optionMap[e.key];

                if (
                    optIdx !== undefined &&
                    activeQuestion?.options?.[optIdx] !== undefined
                ) {
                    if (e.altKey) {
                        e.preventDefault();
                        const isCurrentlyEliminated =
                            eliminatedOptions[currentIdx]?.[optIdx];
                        const willBeEliminated = !isCurrentlyEliminated;

                        if (
                            willBeEliminated &&
                            answers[currentIdx] === optIdx
                        ) {
                            handleSelectOption(optIdx);
                        }

                        setEliminatedOptions((prev) => ({
                            ...prev,
                            [currentIdx]: {
                                ...(prev[currentIdx] || {}),
                                [optIdx]: willBeEliminated,
                            },
                        }));
                    } else if (!eliminatedOptions[currentIdx]?.[optIdx]) {
                        handleSelectOption(optIdx);
                    }
                }
            }
        };

        window.addEventListener('keydown', handleKeyDown, { capture: true });

        return () =>
            window.removeEventListener('keydown', handleKeyDown, {
                capture: true,
            });
    }, [
        currentIdx,
        activeQuestions,
        activeQuestion,
        eliminatedOptions,
        handleQuestionNavigate,
        handleSelectOption,
        toggleFlag,
        answers,
        isPaused,
        toolsOpen,
    ]);

    // Reveal: fetch this item's key (server checks reveal rules) and map
    // it back to the displayed (shuffled) option order.
    const handleReveal = async () => {
        if (!activeQuestion || !studyTools || isPaused) {
            return;
        }

        try {
            const chosenDisplay = answers[currentIdx];
            const chosenOriginal =
                chosenDisplay === undefined
                    ? null
                    : (activeQuestion.originalOptionIndices?.[chosenDisplay] ??
                      chosenDisplay);
            const res = await fetch('/exams/reveal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN':
                        document
                            .querySelector('meta[name="csrf-token"]')
                            ?.getAttribute('content') || '',
                },
                body: JSON.stringify({
                    question_id: activeQuestion.id,
                    chosen_option: chosenOriginal,
                    weak_subcategories:
                        combinedStudyBias().weakSubcategories.slice(0, 20),
                    practice_batch_id: practiceBatchId,
                    exam_session_id: examSessionId,
                }),
            });
            const data = await res.json();

            if (data.success) {
                // The API key is stored against the original option order, while
                // the live exam shuffles choices for the learner. Convert the
                // original index back to the displayed index before rendering
                // the answer and its explanation.
                const originalIndex = Number(data.correct_option);
                const mappedIndex =
                    activeQuestion.originalOptionIndices?.indexOf(
                        originalIndex,
                    ) ?? -1;
                const displayedIndex =
                    mappedIndex >= 0 ? mappedIndex : originalIndex;
                const letter =
                    ['A', 'B', 'C', 'D', 'E'][displayedIndex] ||
                    String(displayedIndex + 1);
                setRevealedAnswer({
                    questionId: activeQuestion.id,
                    letter,
                    displayIndex: displayedIndex,
                    text: activeQuestion.options?.[displayedIndex] || '',
                    explanation: data.explanation,
                    hasConflict: data.has_conflict,
                    tutor: readRevealTutor(data.tutor),
                });
            } else {
                alert(data.message || 'Could not reveal answer');
            }
        } catch {
            alert('Reveal failed');
        }
    };

    return (
        <>
            <Head title={`Live Simulation: ${details.title}`} />
            <style>{styleBlock}</style>
            {isShielded && (
                <div className="fixed inset-0 z-[99999] flex flex-col items-center justify-center bg-card p-6 text-center opacity-100 select-none">
                    <div className="mx-auto flex max-w-2xl flex-col items-center gap-4 rounded-2xl border border-border/80 bg-background p-8 shadow-2xl">
                        <div className="flex size-14 items-center justify-center rounded-full bg-amber-500/10 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400">
                            <Lock className="size-7" />
                        </div>
                        <div className="space-y-2">
                            <h3 className="font-heading text-lg font-bold text-foreground">
                                Content Shield Active
                            </h3>
                            <p className="text-xs leading-relaxed font-semibold text-muted-foreground">
                                Exam content was hidden because window focus was
                                lost or external screen tools were detected.
                            </p>
                            {isResumeLocked && (
                                <p className="text-[11px] font-bold text-amber-600 dark:text-amber-400">
                                    Content stays locked while the exam window
                                    is not focused. Click back into this window,
                                    then resume.
                                </p>
                            )}
                        </div>
                        <button
                            type="button"
                            onClick={dismissShield}
                            disabled={isResumeLocked}
                            className={`mt-2 inline-flex items-center gap-2 rounded-xl px-6 py-2.5 text-xs font-bold text-white shadow-md transition focus:outline-none ${
                                isResumeLocked
                                    ? 'cursor-not-allowed bg-slate-400 opacity-60'
                                    : 'bg-[#5B35F5] hover:bg-[#4a2ad4]'
                            }`}
                        >
                            {isResumeLocked
                                ? 'Window Not Focused — Click to Focus'
                                : 'Resume Examination'}
                        </button>
                    </div>
                </div>
            )}
            <div
                ref={contentRef}
                {...wrapperProps}
                className={`civio-session fixed inset-0 z-50 flex flex-col transition-none select-none ${
                    isShielded
                        ? 'pointer-events-none invisible opacity-0'
                        : 'opacity-100'
                }`}
            >
                {isPaused && (
                    <PauseOverlay
                        strict={!canPause}
                        onResume={() => onResume?.()}
                    />
                )}
                {lite ? (
                    <LiteExamBody
                        title={details.title}
                        isDrillSession={isDrillSession}
                        question={activeQuestion}
                        questions={activeQuestions}
                        currentIdx={currentIdx}
                        answers={answers}
                        flagged={flagged}
                        answeredCount={stats.answered}
                        isTimed={isTimed}
                        timeLeft={timeLeft}
                        itemElapsed={itemElapsed}
                        formatTime={formatTime}
                        totalSeconds={details.timeLimitSecs}
                        subscribeClock={subscribeClock}
                        getClockSnapshot={getClockSnapshot}
                        onSelect={onOptionClick}
                        onNavigate={handleQuestionNavigate}
                        onToggleFlag={toggleFlag}
                        onSubmit={() => handleSubmitExam(false)}
                        onExit={handleExitExam}
                        showStudyTools={studyTools}
                        strict={!studyTools && !isDrillSession}
                        onReveal={handleReveal}
                        revealed={
                            revealedAnswer &&
                            revealedAnswer.questionId === activeQuestion?.id
                                ? revealedAnswer
                                : null
                        }
                        onHideReveal={() => setRevealedAnswer(null)}
                        copyAttempt={
                            studyTools && activeQuestion
                                ? liveHandoffAttempt(activeQuestion.id)
                                : null
                        }
                    />
                ) : (
                    <>
                        <header className="flex w-full flex-col border-b border-[var(--civio-line)] bg-[var(--civio-paper)]">
                            <div className="flex w-full items-center gap-1 px-2 py-1.5 sm:px-4">
                                <button
                                    onClick={handleExitExam}
                                    title={
                                        isDrillSession
                                            ? 'Exit Drill'
                                            : 'Exit Exam'
                                    }
                                    className="flex size-10 shrink-0 items-center justify-center rounded-lg text-[var(--civio-ink)]"
                                >
                                    <ChevronLeft className="size-5" />
                                    <span className="sr-only">
                                        {isDrillSession
                                            ? 'Exit Drill'
                                            : 'Exit Exam'}
                                    </span>
                                </button>

                                <div className="min-w-0 flex-1" />

                                <ExamTimerDisplay
                                    isTimed={isTimed}
                                    timeLeft={timeLeft}
                                    itemElapsed={itemElapsed}
                                    formatTime={formatTime}
                                    totalSeconds={details.timeLimitSecs}
                                    subscribeClock={subscribeClock}
                                    getClockSnapshot={getClockSnapshot}
                                />

                                <DarkModeToggle />

                                {activeQuestion && (
                                    <span className="group/hint relative">
                                        <button
                                            type="button"
                                            onClick={() =>
                                                toggleFlag(currentIdx)
                                            }
                                            aria-pressed={!!flagged[currentIdx]}
                                            aria-label={
                                                flagged[currentIdx]
                                                    ? 'Remove flag.'
                                                    : 'Flag for review.'
                                            }
                                            aria-describedby="exam-flag-hint"
                                            className={`flex size-10 shrink-0 items-center justify-center rounded-lg ${
                                                flagged[currentIdx]
                                                    ? 'text-[var(--civio-error)]'
                                                    : 'text-[var(--civio-ink)]/60'
                                            }`}
                                        >
                                            <Flag
                                                className={`size-4 ${
                                                    flagged[currentIdx]
                                                        ? 'fill-[var(--civio-error)]'
                                                        : ''
                                                }`}
                                            />
                                        </button>
                                        <span
                                            id="exam-flag-hint"
                                            role="tooltip"
                                            className="pointer-events-none absolute top-[calc(100%+6px)] right-0 z-30 hidden rounded-lg border border-[var(--civio-line)] bg-[var(--civio-paper)] px-2.5 py-1.5 text-[11px] leading-none font-medium whitespace-nowrap shadow-sm group-focus-within/hint:block group-hover/hint:block"
                                        >
                                            {flagged[currentIdx]
                                                ? 'Remove flag.'
                                                : 'Flag for review.'}
                                        </span>
                                    </span>
                                )}

                                <span className="group/hint relative">
                                    <button
                                        type="button"
                                        onClick={() => {
                                            if (window.innerWidth >= 1024) {
                                                setIsPaletteCollapsed(
                                                    (prev) => !prev,
                                                );
                                            } else {
                                                setIsMobilePaletteOpen(true);
                                            }
                                        }}
                                        aria-label="Jump to a question."
                                        aria-describedby="exam-list-hint"
                                        className="flex size-10 shrink-0 items-center justify-center rounded-lg text-[var(--civio-violet)]"
                                    >
                                        <LayoutGrid className="size-4" />
                                    </button>
                                    <span
                                        id="exam-list-hint"
                                        role="tooltip"
                                        className="pointer-events-none absolute top-[calc(100%+6px)] right-0 z-30 hidden rounded-lg border border-[var(--civio-line)] bg-[var(--civio-paper)] px-2.5 py-1.5 text-[11px] leading-none font-medium whitespace-nowrap shadow-sm group-focus-within/hint:block group-hover/hint:block"
                                    >
                                        Jump to a question.
                                    </span>
                                </span>
                            </div>

                            <div className="flex items-center justify-between gap-3 px-3 pb-1.5 text-xs sm:px-5">
                                <nav
                                    aria-label="Question context"
                                    className="min-w-0 flex-1 text-[var(--civio-ink)]"
                                >
                                    <ol className="flex min-w-0 items-baseline gap-1.5 leading-5">
                                        <li className="shrink-0 text-sm font-semibold">
                                            {isDrillSession
                                                ? 'Practice Drills'
                                                : EXAM_MODE_LABELS[examMode]}
                                        </li>
                                        {activeQuestion?.category && (
                                            <li className="flex min-w-0 items-baseline gap-1.5 text-[var(--civio-ink)]/70">
                                                <span
                                                    aria-hidden
                                                    className="text-[var(--civio-ink)]/35"
                                                >
                                                    /
                                                </span>
                                                <span className="truncate">
                                                    {activeQuestion.category}
                                                </span>
                                            </li>
                                        )}
                                        {activeQuestion?.subcategory && (
                                            <li className="hidden min-w-0 items-baseline gap-1.5 text-[var(--civio-ink)]/60 sm:flex">
                                                <span
                                                    aria-hidden
                                                    className="text-[var(--civio-ink)]/35"
                                                >
                                                    /
                                                </span>
                                                <span className="truncate">
                                                    {activeQuestion.subcategory}
                                                </span>
                                            </li>
                                        )}
                                    </ol>
                                    <span className="mt-0.5 block truncate text-[var(--civio-ink)]/55">
                                        {details.title}
                                    </span>
                                </nav>
                                <div className="flex shrink-0 items-center">
                                    <button
                                        type="button"
                                        onClick={() =>
                                            setToolsOpen((open) => !open)
                                        }
                                        aria-expanded={toolsOpen}
                                        className="h-8 rounded-lg px-2 font-semibold text-[var(--civio-ink)]/70"
                                    >
                                        Tools
                                    </button>
                                    {canPause && !isPaused && (
                                        <button
                                            type="button"
                                            onClick={() => onPause?.()}
                                            className="h-8 rounded-lg px-2 font-semibold"
                                        >
                                            Pause
                                        </button>
                                    )}
                                </div>
                            </div>

                            <div
                                aria-label={`Answered ${stats.progressPct} percent`}
                                className="h-1 w-full bg-[var(--civio-line)]"
                            >
                                <div
                                    className="h-full bg-[var(--civio-violet)]"
                                    style={{
                                        width: `${stats.progressPct}%`,
                                    }}
                                />
                            </div>

                            {toolsOpen && (
                                <div className="flex flex-wrap items-center gap-2 border-t border-[var(--civio-line)] px-3 py-2 sm:px-5">
                                    {isTimed && stats.unanswered > 0 && (
                                        <span className="text-xs text-[var(--civio-ink)]/70">
                                            About {stats.targetPace} seconds an
                                            item.
                                            {stats.paceStatus === 'behind'
                                                ? ' You are behind.'
                                                : stats.paceStatus === 'warn'
                                                  ? ' You are close.'
                                                  : ' You are on pace.'}
                                        </span>
                                    )}
                                    <button
                                        type="button"
                                        onClick={() =>
                                            setIsScratchpadOpen(true)
                                        }
                                        className="civio-action"
                                    >
                                        <Edit3 className="mr-1 inline size-3.5" />
                                        Notes
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() =>
                                            setShowKeyboardModal(true)
                                        }
                                        className="civio-action hidden sm:inline-flex"
                                    >
                                        <Keyboard className="mr-1 size-3.5" />
                                        Keys
                                    </button>
                                    <button
                                        type="button"
                                        onClick={toggleFullscreen}
                                        className="civio-action hidden sm:inline-flex"
                                    >
                                        {isFullscreen ? (
                                            <Minimize2 className="mr-1 size-3.5" />
                                        ) : (
                                            <Maximize2 className="mr-1 size-3.5" />
                                        )}
                                        Focus
                                    </button>
                                    <LiteModeToggle className="hidden sm:inline-flex" />
                                </div>
                            )}
                        </header>
                        {/* MAIN TWO-COLUMN SPLIT PANEL LAYOUT */}
                        <div className="flex flex-1 overflow-hidden">
                            {/* LEFT COLUMN: ACTIVE QUESTION CARD & OPTION SELECTORS */}
                            <div className="flex flex-1 flex-col justify-between overflow-y-auto p-4 sm:p-6 md:p-10">
                                <div className="mx-auto w-full max-w-[42rem]">
                                    {activeQuestion ? (
                                        <div className="flex flex-col gap-5">
                                            <p className="text-xs font-semibold tracking-[0.08em] text-[var(--civio-ink)]/60 uppercase tabular-nums">
                                                Question {currentIdx + 1}
                                                <span className="text-[var(--civio-ink)]/40">
                                                    {' '}
                                                    of {activeQuestions.length}
                                                </span>
                                            </p>
                                            <div className="max-w-[65ch] text-[1.0625rem] leading-[1.7] tracking-[-0.005em] text-pretty [overflow-wrap:anywhere] text-foreground md:text-xl md:leading-[1.65]">
                                                {renderFormattedText(
                                                    activeQuestion.stem,
                                                    true,
                                                )}
                                            </div>
                                            {isWithdrawn && (
                                                <p
                                                    role="status"
                                                    data-testid="withdrawn-live"
                                                    className="rounded-xl border border-amber-300/60 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-900 dark:border-amber-500/40 dark:bg-amber-950/40 dark:text-amber-200"
                                                >
                                                    {WITHDRAWN_LIVE_NOTICE}
                                                </p>
                                            )}
                                            <div className="flex flex-wrap items-center gap-3">
                                                <button
                                                    type="button"
                                                    disabled={isReported}
                                                    onClick={() =>
                                                        !isReported &&
                                                        setIsReportModalOpen(
                                                            true,
                                                        )
                                                    }
                                                    className="civio-action"
                                                >
                                                    {isReported
                                                        ? 'Reported'
                                                        : 'Report'}
                                                </button>
                                                {studyTools && (
                                                    <button
                                                        type="button"
                                                        onClick={() => {
                                                            if (
                                                                revealedAnswer?.questionId ===
                                                                activeQuestion.id
                                                            ) {
                                                                setRevealedAnswer(
                                                                    null,
                                                                );

                                                                return;
                                                            }

                                                            void handleReveal();
                                                        }}
                                                        className={
                                                            revealedAnswer?.questionId ===
                                                            activeQuestion.id
                                                                ? 'civio-action'
                                                                : 'civio-action civio-action-primary'
                                                        }
                                                    >
                                                        {revealedAnswer?.questionId ===
                                                        activeQuestion.id
                                                            ? 'Hide Explanation'
                                                            : 'Show Explanation'}
                                                    </button>
                                                )}
                                                {studyTools && (
                                                    <CopyForAiButton
                                                        question={
                                                            activeQuestion
                                                        }
                                                        attempt={liveHandoffAttempt(
                                                            activeQuestion.id,
                                                        )}
                                                        className="civio-action"
                                                    />
                                                )}
                                                {studyTools && (
                                                    <AskAssistantButton
                                                        question={
                                                            activeQuestion
                                                        }
                                                        attempt={liveHandoffAttempt(
                                                            activeQuestion.id,
                                                        )}
                                                        className="civio-action"
                                                    />
                                                )}
                                            </div>

                                            {studyTools &&
                                                revealedAnswer &&
                                                revealedAnswer.questionId ===
                                                    activeQuestion?.id && (
                                                    <AnswerReveal
                                                        letter={
                                                            revealedAnswer.letter
                                                        }
                                                        text={
                                                            revealedAnswer.text
                                                        }
                                                        explanation={
                                                            revealedAnswer.explanation
                                                        }
                                                        hasConflict={
                                                            revealedAnswer.hasConflict
                                                        }
                                                        tutor={
                                                            revealedAnswer.tutor
                                                        }
                                                        chosenIndex={
                                                            answers[
                                                                currentIdx
                                                            ] ?? null
                                                        }
                                                        correctIndex={
                                                            revealedAnswer.displayIndex
                                                        }
                                                        ask={{
                                                            question:
                                                                activeQuestion,
                                                            attempt:
                                                                liveHandoffAttempt(
                                                                    activeQuestion.id,
                                                                ),
                                                        }}
                                                    />
                                                )}

                                            {/* Options Grid selector stack */}
                                            <div
                                                className="flex flex-col"
                                                role="radiogroup"
                                            >
                                                {activeQuestion.options.map(
                                                    (opt, idx) => {
                                                        const label =
                                                            String.fromCharCode(
                                                                65 + idx,
                                                            );
                                                        const isEliminated =
                                                            !!eliminatedOptions[
                                                                currentIdx
                                                            ]?.[idx];
                                                        const revealedHere = !!(
                                                            revealedAnswer &&
                                                            revealedAnswer.questionId ===
                                                                activeQuestion.id
                                                        );
                                                        const choice =
                                                            answerOptionVisual({
                                                                optionIndex:
                                                                    idx,
                                                                selectedIndex:
                                                                    answers[
                                                                        currentIdx
                                                                    ],
                                                                revealed:
                                                                    revealedHere,
                                                                strict:
                                                                    !studyTools &&
                                                                    !isDrillSession,
                                                                correctIndex:
                                                                    revealedHere
                                                                        ? revealedAnswer.displayIndex
                                                                        : null,
                                                            });

                                                        return (
                                                            <AnswerOption
                                                                key={idx}
                                                                letter={label}
                                                                visual={
                                                                    choice.visual
                                                                }
                                                                status={
                                                                    choice.status
                                                                }
                                                                eliminated={
                                                                    isEliminated ||
                                                                    isWithdrawn
                                                                }
                                                                onSelect={() =>
                                                                    !isEliminated &&
                                                                    onOptionClick(
                                                                        idx,
                                                                    )
                                                                }
                                                                trailing={
                                                                    <span className="group/hint relative">
                                                                        <button
                                                                            type="button"
                                                                            onClick={(
                                                                                e,
                                                                            ) =>
                                                                                toggleElimination(
                                                                                    e,
                                                                                    currentIdx,
                                                                                    idx,
                                                                                )
                                                                            }
                                                                            aria-label={
                                                                                isEliminated
                                                                                    ? 'Restore this choice.'
                                                                                    : 'Cross out this choice.'
                                                                            }
                                                                            aria-describedby={`exam-cross-${currentIdx}-${idx}`}
                                                                            className="inline-flex shrink-0 items-center p-2 text-xs font-bold text-[var(--civio-ink)]/60"
                                                                        >
                                                                            <Strikethrough className="size-4" />
                                                                        </button>
                                                                        <span
                                                                            id={`exam-cross-${currentIdx}-${idx}`}
                                                                            role="tooltip"
                                                                            className="pointer-events-none absolute top-[calc(100%+6px)] right-0 z-30 hidden rounded-lg border border-[var(--civio-line)] bg-[var(--civio-paper)] px-2.5 py-1.5 text-[11px] leading-none font-medium whitespace-nowrap shadow-sm group-focus-within/hint:block group-hover/hint:block"
                                                                        >
                                                                            {isEliminated
                                                                                ? 'Restore this choice.'
                                                                                : 'Cross out this choice.'}
                                                                        </span>
                                                                    </span>
                                                                }
                                                            >
                                                                {renderFormattedText(
                                                                    opt,
                                                                    false,
                                                                    undefined,
                                                                    true,
                                                                )}
                                                            </AnswerOption>
                                                        );
                                                    },
                                                )}
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
                                            <AlertCircle className="mb-3 size-10 animate-pulse" />
                                            <span className="text-sm font-semibold">
                                                Generating questions slice...
                                            </span>
                                        </div>
                                    )}
                                </div>

                                {/* CORE CONTROL BUTTONS (PREV, NEXT, SUBMIT) */}
                                <div className="sticky bottom-0 z-10 mx-auto mt-6 flex w-full max-w-[42rem] items-center gap-3 border-t border-[var(--civio-line)] bg-[var(--civio-paper)] py-3">
                                    <button
                                        onClick={() =>
                                            handleQuestionNavigate(
                                                Math.max(0, currentIdx - 1),
                                            )
                                        }
                                        disabled={currentIdx === 0}
                                        className="civio-nav"
                                    >
                                        <ChevronLeft className="size-4" />
                                        Previous
                                    </button>

                                    {currentIdx < activeQuestions.length - 1 ? (
                                        <button
                                            onClick={() =>
                                                handleQuestionNavigate(
                                                    currentIdx + 1,
                                                )
                                            }
                                            className="civio-nav civio-nav-primary"
                                        >
                                            Next
                                            <ChevronRight className="size-4" />
                                        </button>
                                    ) : (
                                        <button
                                            onClick={() =>
                                                handleSubmitExam(false)
                                            }
                                            className="civio-nav civio-nav-primary"
                                        >
                                            <CheckCircle2 className="size-4" />
                                            Submit
                                        </button>
                                    )}
                                </div>
                            </div>

                            {/* RIGHT COLUMN: QUESTION PALETTE GRID */}
                            <QuestionPalettePanel
                                mode="exam"
                                questions={activeQuestions}
                                currentIdx={currentIdx}
                                answers={answers}
                                flagged={flagged}
                                onNavigate={handleQuestionNavigate}
                                selectedCategory={selectedPaletteCategory}
                                onCategoryChange={handleCategoryChange}
                                allowedCategories={details.allowedCategories}
                                isFreeAttempt={isFreeAttempt}
                                onSubmitExam={() => handleSubmitExam(false)}
                                liveStatusFilter={liveStatusFilter}
                                onLiveStatusChange={setLiveStatusFilter}
                                isMobile={false}
                                isCollapsed={isPaletteCollapsed}
                                onToggleCollapse={() =>
                                    setIsPaletteCollapsed((prev) => !prev)
                                }
                            />
                        </div>

                        {/* Mobile Question Palette Drawer */}
                        {isMobilePaletteOpen && (
                            <QuestionPalettePanel
                                mode="exam"
                                questions={activeQuestions}
                                currentIdx={currentIdx}
                                answers={answers}
                                flagged={flagged}
                                onNavigate={handleQuestionNavigate}
                                selectedCategory={selectedPaletteCategory}
                                onCategoryChange={handleCategoryChange}
                                allowedCategories={details.allowedCategories}
                                isFreeAttempt={isFreeAttempt}
                                onSubmitExam={() => handleSubmitExam(false)}
                                liveStatusFilter={liveStatusFilter}
                                onLiveStatusChange={setLiveStatusFilter}
                                isMobile={true}
                                onCloseMobile={() =>
                                    setIsMobilePaletteOpen(false)
                                }
                            />
                        )}
                    </>
                )}
                {customConfirmModal}

                {/* Keyboard Shortcuts Reference Dialog Modal */}
                <Dialog
                    open={showKeyboardModal}
                    onOpenChange={setShowKeyboardModal}
                >
                    <DialogContent className="sm:max-w-2xl">
                        <DialogHeader>
                            <DialogTitle className="flex items-center gap-2 font-heading text-lg font-bold">
                                <Keyboard className="size-5 text-[#5B35F5] dark:text-[#B3F52D]" />
                                Keyboard Shortcuts
                            </DialogTitle>
                            <DialogDescription>
                                Speed up your test-taking with these hotkeys.
                            </DialogDescription>
                        </DialogHeader>

                        <div className="mt-2 space-y-3">
                            <div className="flex items-center justify-between border-b border-border pb-2 text-xs font-semibold">
                                <span className="text-muted-foreground">
                                    Select Option
                                </span>
                                <div className="flex items-center gap-1">
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        1 - 5
                                    </kbd>
                                    <span className="text-muted-foreground">
                                        or
                                    </span>
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        A - E
                                    </kbd>
                                </div>
                            </div>

                            <div className="flex items-center justify-between border-b border-border pb-2 text-xs font-semibold">
                                <span className="text-muted-foreground">
                                    Next Question
                                </span>
                                <div className="flex items-center gap-1">
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        →
                                    </kbd>
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        ]
                                    </kbd>
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        N
                                    </kbd>
                                </div>
                            </div>

                            <div className="flex items-center justify-between border-b border-border pb-2 text-xs font-semibold">
                                <span className="text-muted-foreground">
                                    Previous Question
                                </span>
                                <div className="flex items-center gap-1">
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        ←
                                    </kbd>
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        [
                                    </kbd>
                                    <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                        P
                                    </kbd>
                                </div>
                            </div>

                            <div className="flex items-center justify-between border-b border-border pb-2 text-xs font-semibold">
                                <span className="text-muted-foreground">
                                    Toggle Flag for Review
                                </span>
                                <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                    F
                                </kbd>
                            </div>

                            <div className="flex items-center justify-between text-xs font-semibold">
                                <span className="text-muted-foreground">
                                    Open Shortcuts Cheatsheet
                                </span>
                                <kbd className="rounded border border-border bg-muted px-2 py-1 font-mono text-[11px] font-bold text-foreground">
                                    ?
                                </kbd>
                            </div>
                        </div>
                    </DialogContent>
                </Dialog>

                {/* Scratchpad Notes Dialog Modal */}
                <Dialog
                    open={isScratchpadOpen}
                    onOpenChange={setIsScratchpadOpen}
                >
                    <DialogContent className="sm:max-w-2xl">
                        <DialogHeader>
                            <DialogTitle className="flex items-center gap-2 font-heading text-lg font-bold">
                                <Edit3 className="size-5 text-amber-500" />
                                Exam Scratchpad & Rough Notes
                            </DialogTitle>
                            <DialogDescription>
                                Write down formulas, rough calculations, or
                                reasoning notes. Your notes auto-save locally.
                            </DialogDescription>
                        </DialogHeader>

                        <div className="mt-2 space-y-3">
                            <textarea
                                value={scratchpadNotes}
                                onChange={(e) =>
                                    handleScratchpadChange(e.target.value)
                                }
                                placeholder="Type your rough calculations or notes here..."
                                rows={8}
                                className="w-full resize-y rounded-xl border border-border bg-muted/30 p-3 font-mono text-xs font-medium text-foreground transition focus:border-amber-500 focus:ring-1 focus:ring-amber-500 focus:outline-none"
                            />
                            <div className="flex items-center justify-between text-xs text-muted-foreground">
                                <span>{scratchpadNotes.length} characters</span>
                                <button
                                    type="button"
                                    onClick={() => handleScratchpadChange('')}
                                    className="font-bold text-rose-600 transition hover:underline dark:text-rose-400"
                                >
                                    Clear Notes
                                </button>
                            </div>
                        </div>
                    </DialogContent>
                </Dialog>

                {/* Guest Free Attempt: Locked Question Modal */}
                {showLockedModal && (
                    <div
                        className="fixed inset-0 z-[100] flex animate-in items-center justify-center bg-slate-900/60 p-4 duration-200 fade-in"
                        onClick={() => setShowLockedModal(false)}
                    >
                        <div
                            className="relative flex max-h-[85dvh] w-[calc(100vw-2rem)] max-w-2xl animate-in flex-col overflow-y-auto rounded-xl border border-slate-200 bg-white p-4 shadow-xl duration-200 zoom-in-95 sm:w-full sm:p-6 dark:border-slate-800 dark:bg-slate-950"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="mb-1 flex items-center gap-2">
                                <Lock className="size-5 text-[#5B35F5] dark:text-[#B3F52D]" />
                                <h3 className="font-heading text-xl font-semibold tracking-tight text-slate-900 dark:text-white">
                                    Premium Feature Locked
                                </h3>
                            </div>
                            <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">
                                Register a free account to unlock all questions,
                                track your progress, and access more premium
                                features of the mock exam.
                            </p>
                            <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
                                <button
                                    type="button"
                                    onClick={() => setShowLockedModal(false)}
                                    className="rounded-lg border border-slate-200 px-5 py-2.5 text-xs font-bold text-slate-600 transition hover:bg-slate-50 dark:border-slate-800 dark:text-slate-400 dark:hover:bg-slate-900"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="button"
                                    onClick={handleRegisterFromFreeExam}
                                    className="group rounded-lg bg-[#5B35F5] px-5 py-2.5 text-xs font-bold text-white transition transition-all duration-300 hover:bg-[#4a2ad4] focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none active:scale-95"
                                >
                                    Register Now
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {/* Guest Free Attempt: Register / Continue Modal */}
                {showRegisterModal && (
                    <div
                        className="fixed inset-0 z-[100] flex animate-in items-center justify-center bg-slate-900/60 p-4 duration-200 fade-in"
                        onClick={() => setShowRegisterModal(false)}
                    >
                        <div
                            className="relative flex max-h-[85dvh] w-[calc(100vw-2rem)] max-w-2xl animate-in flex-col overflow-y-auto rounded-xl border border-slate-200 bg-white p-4 shadow-xl duration-200 zoom-in-95 sm:w-full sm:p-6 dark:border-slate-800 dark:bg-slate-950"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="mb-1 flex items-center gap-2">
                                <Lock className="size-5 text-[#5B35F5] dark:text-[#B3F52D]" />
                                <h3 className="font-heading text-xl font-semibold tracking-tight text-slate-900 dark:text-white">
                                    Free Preview Limit Reached
                                </h3>
                            </div>
                            <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">
                                You've completed the first 20 questions of the
                                free mock exam preview. Register a free account
                                to unlock the full exam, submit your answers,
                                and view your detailed scorecard.
                            </p>
                            <p className="mt-2 text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
                                ✓ Your progress will be saved and restored after
                                registration.
                            </p>
                            <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
                                <button
                                    type="button"
                                    onClick={handleCancelFreeExam}
                                    className="group rounded-lg border border-slate-200 px-5 py-2.5 text-xs font-bold text-slate-600 transition transition-all duration-300 hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none active:scale-95 dark:border-slate-800 dark:text-slate-400 dark:hover:bg-slate-900"
                                >
                                    Exit to Home
                                </button>
                                <button
                                    type="button"
                                    onClick={handleRegisterFromFreeExam}
                                    className="group flex items-center justify-center gap-2 rounded-lg bg-[#5B35F5] px-5 py-2.5 text-xs font-bold text-white shadow-sm transition transition-all duration-300 hover:bg-[#4a2ad4] focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none active:scale-95"
                                >
                                    <LogIn className="size-4" />
                                    Register Free Account
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {isReportModalOpen && activeQuestion && (
                    <ReportIssueModal
                        isOpen={isReportModalOpen}
                        onClose={() => setIsReportModalOpen(false)}
                        flaggableId={activeQuestion.id}
                        flaggableType="App\Models\Question"
                    />
                )}
            </div>
        </>
    );
}

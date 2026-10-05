import { setLayoutProps } from '@inertiajs/react';
import { useEffect } from 'react';
import {
    resolveOriginFromUrl,
    setSessionOrigin,
    getSessionOrigin,
    getOriginTitle,
} from '@/lib/smart-back';
import type {
    Question,
    SavedAttempt,
    ExamResults,
    CategoryScore,
    AttemptMetadata,
} from '../types';
import { isDemographicQuestion, EXAM_CONSTANTS } from '../utils/exam-utils';
import { shuffleOptionsForQuestion } from './use-exam-pool-builder';

interface UseExamHydrationProps {
    questions: Question[];
    savedAttempt?: SavedAttempt | null;
    auth?: any;
    isExamActive: boolean;
    isExamSubmitted: boolean;
    selectedExamId?: number | null;
    setSelectedExamId: (id: number | null) => void;
    setActiveQuestions: (qs: Question[]) => void;
    setCurrentIdx: (idx: number) => void;
    setAnswers: React.Dispatch<React.SetStateAction<Record<number, number>>>;
    setQuestionTimes: React.Dispatch<
        React.SetStateAction<Record<number, number>>
    >;
    setAnswerChanges: React.Dispatch<
        React.SetStateAction<Record<number, number>>
    >;
    setFlagged: React.Dispatch<React.SetStateAction<Record<number, boolean>>>;
    setIsExamActive: (val: boolean) => void;
    setIsExamSubmitted: (val: boolean) => void;
    setReviewScreenActive: (val: boolean) => void;
    setResults: (val: ExamResults | null) => void;
    setSessionTimeLimitSecs: (secs: number) => void;
    setTimeLeft: (secs: number) => void;
    setIsFreeAttempt: (val: boolean) => void;
    setSubmittedByTimer: (val: boolean) => void;
    setDrillCategoryId: (id: number | null) => void;
    setDrillCategoryName: (name: string | null) => void;
    setDrillSubcategories: (subcats: string[]) => void;
    setDrillLanguage: (lang: string) => void;
    setDrillQuestionCount: (count: number | 'all') => void;
    setIsTimed: (val: boolean) => void;
    buildFreshExamPool: (examId: number | null) => Question[];
    beginExamSession: (pool: Question[], examId: number | null) => void;
}

export function useExamHydration({
    questions,
    savedAttempt,
    auth,
    isExamActive,
    isExamSubmitted,
    setSelectedExamId,
    setActiveQuestions,
    setCurrentIdx,
    setAnswers,
    setQuestionTimes,
    setAnswerChanges,
    setFlagged,
    setIsExamActive,
    setIsExamSubmitted,
    setReviewScreenActive,
    setResults,
    setSessionTimeLimitSecs,
    setTimeLeft,
    setIsFreeAttempt,
    setSubmittedByTimer,
    setDrillCategoryId,
    setDrillCategoryName,
    setDrillSubcategories,
    setDrillLanguage,
    setDrillQuestionCount,
    setIsTimed,
    buildFreshExamPool,
    beginExamSession,
}: UseExamHydrationProps) {
    const fallbackQuestions: Question[] = questions;

    const remapIndexedRecord = <T,>(
        record: Record<number, T> | undefined,
        oldQuestions: Question[],
        newQuestions: Question[],
    ): Record<number, T> => {
        const remapped: Record<number, T> = {};

        newQuestions.forEach((question, newIdx) => {
            const oldIdx = oldQuestions.findIndex((q) => q.id === question.id);

            if (oldIdx >= 0 && record?.[oldIdx] !== undefined) {
                remapped[newIdx] = record[oldIdx];
            }
        });

        return remapped;
    };

    const scoredOnly = (pool: Question[]): Question[] =>
        pool.filter((q) => !isDemographicQuestion(q));

    // 1. Saved Attempt Hydration
    useEffect(() => {
        if (!savedAttempt) {
            return;
        }

        let rawLoadedQuestions: Question[] = [];

        if (savedAttempt.question_ids && savedAttempt.question_ids.length > 0) {
            rawLoadedQuestions = savedAttempt.question_ids
                .map((id) => questions.find((q) => q.id === id))
                .filter(Boolean) as Question[];
        }

        const loadedQuestions = scoredOnly(rawLoadedQuestions);
        // Prefer question-ID-keyed answers (Phase 0+). Fall back to legacy position keys.
        const restoredAnswers: Record<number, number> = {};
        const rawAnswers = savedAttempt.answers ?? {};
        const answerKeys = Object.keys(rawAnswers);
        const looksLikeQuestionIds = answerKeys.some((k) =>
            loadedQuestions.some((q) => String(q.id) === String(k)),
        );

        if (looksLikeQuestionIds) {
            loadedQuestions.forEach((question, newIdx) => {
                const byId =
                    rawAnswers[question.id as keyof typeof rawAnswers] ??
                    rawAnswers[String(question.id) as keyof typeof rawAnswers];
                if (byId !== undefined && byId !== null) {
                    restoredAnswers[newIdx] = Number(byId);
                }
            });
        } else {
            Object.assign(
                restoredAnswers,
                remapIndexedRecord(
                    rawAnswers as Record<number, number>,
                    rawLoadedQuestions,
                    loadedQuestions,
                ),
            );
        }
        const catScores = savedAttempt.cat_scores ?? {};
        const meta: AttemptMetadata = (catScores.metadata ??
            {}) as AttemptMetadata;
        const total = loadedQuestions.length;
        const correctCount = Math.min(meta.correct_count || 0, total);
        const skippedCount = Math.min(
            meta.skipped_count || 0,
            Math.max(0, total - correctCount),
        );
        const percentage =
            total > 0 ? Math.round((correctCount / total) * 100) : 0;
        const wrongCount = Math.max(0, total - correctCount - skippedCount);

        const isTimedSaved = meta.is_timed !== false;
        const isSubprofessional = meta.track === 'Subprofessional';
        const limitSecs = isTimedSaved
            ? isSubprofessional
                ? EXAM_CONSTANTS.SUBPROFESSIONAL_TIME_LIMIT_SECS
                : EXAM_CONSTANTS.PROFESSIONAL_TIME_LIMIT_SECS
            : 0;

        const storedDuration = Number(
            meta.duration_secs ?? (catScores as any).duration_secs ?? 0,
        );
        const elapsedSecs = isTimedSaved
            ? Math.min(limitSecs, Math.max(0, storedDuration))
            : storedDuration;

        const computedCatMap: Record<string, CategoryScore> = {};

        loadedQuestions.forEach((q, idx) => {
            const chosen = restoredAnswers[idx];
            const isCorrect = chosen === q.correct_option;

            if (isDemographicQuestion(q)) {
                return;
            }

            const catName = q.category || 'General Information';
            const subcatName = q.subcategory || 'General Concepts';

            if (!computedCatMap[catName]) {
                computedCatMap[catName] = { correct: 0, total: 0, subcats: {} };
            }

            if (!computedCatMap[catName].subcats[subcatName]) {
                computedCatMap[catName].subcats[subcatName] = {
                    correct: 0,
                    total: 0,
                };
            }

            computedCatMap[catName].total += 1;
            computedCatMap[catName].subcats[subcatName].total += 1;

            if (isCorrect) {
                computedCatMap[catName].correct += 1;
                computedCatMap[catName].subcats[subcatName].correct += 1;
            }
        });

        const activeCatMap = computedCatMap;

        const restoredResults: ExamResults = {
            score: percentage,
            total,
            percentage,
            correctCount,
            wrongCount,
            skippedCount,
            categoryScoreMap: activeCatMap,
            elapsedSecs,
        };

        const resolvedTrackId =
            meta.track === 'Subprofessional'
                ? 2
                : meta.track === 'Drill'
                  ? null
                  : 1;

        setSelectedExamId(resolvedTrackId);
        setActiveQuestions(loadedQuestions);
        setAnswers(restoredAnswers);
        setIsExamActive(false);
        setIsExamSubmitted(true);
        setResults(restoredResults);
        setSubmittedByTimer(false);

        if (meta.track === 'Drill') {
            setDrillCategoryName(meta.category_name || 'Practice Drill');
        }

        const isDrill = meta.track === 'Drill';
        const attemptTitle = isDrill
            ? `Drill: ${meta.category_name || 'Practice Drill'}`
            : `Exam Attempt #${savedAttempt.id}`;

        const origin = resolveOriginFromUrl(
            typeof window !== 'undefined' ? window.location.href : undefined,
        );
        const originTitle = origin ? origin.title : 'History';
        const originHref = origin ? origin.href : '/history';

        setLayoutProps({
            breadcrumbs: [
                { title: originTitle, href: originHref },
                { title: attemptTitle, href: '#' },
            ],
        });
    }, [
        savedAttempt,
        questions,
        setSelectedExamId,
        setActiveQuestions,
        setAnswers,
        setIsExamActive,
        setIsExamSubmitted,
        setResults,
        setSubmittedByTimer,
        setDrillCategoryName,
    ]);

    // 2. Auto-start deep links (?start= & ?drill=)
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const startType = params.get('start');
        const isDrillStart = params.get('drill') === 'true';
        const fromParam = params.get('from') || params.get('return_to');

        if (fromParam) {
            setSessionOrigin(fromParam);
        }

        if (startType && !savedAttempt) {
            // Explicit start= means a NEW mock — never resume an old localStorage
            // session (those often still carry Demographic Profile items).
            try {
                localStorage.removeItem('active_exam_session_v1');
                localStorage.removeItem('pending_free_exam');
            } catch {
                /* ignore */
            }

            const examId = startType === 'subprofessional' ? 2 : 1;
            const isFree = params.get('free_attempt') === '1';

            const url = new URL(window.location.href);
            url.searchParams.delete('start');
            url.searchParams.delete('free_attempt');
            window.history.replaceState({}, '', url.toString());

            if (isFree) {
                setIsFreeAttempt(true);
            }

            setSelectedExamId(examId);
            beginExamSession(buildFreshExamPool(examId), examId);
        } else if (isDrillStart && !savedAttempt && !isExamActive) {
            const catName =
                params.get('category_name') || 'General Information';
            const catId = params.get('category_id')
                ? Number(params.get('category_id'))
                : null;
            const qCountParam = params.get('question_count') || '30';
            const lang = params.get('language') || 'English';
            const isTimedParam = params.get('timed') !== 'false';
            let subcats: string[] = [];

            if (params.get('subcategories')) {
                try {
                    subcats = JSON.parse(params.get('subcategories')!);
                } catch {
                    /* ignore */
                }
            }

            const url = new URL(window.location.href);
            url.search = '';
            url.pathname = '/drills';
            window.history.replaceState({}, '', url.toString());

            const sourcePool = scoredOnly(
                questions.length > 0 ? questions : fallbackQuestions,
            );
            const customIdsParam = params.get('custom_question_ids');
            let pool: Question[] = [];

            if (customIdsParam) {
                try {
                    const parsedIds: number[] = JSON.parse(customIdsParam);
                    const idSet = new Set(parsedIds);
                    pool = sourcePool.filter((q) => idSet.has(q.id));
                } catch {
                    /* ignore */
                }
            }

            if (pool.length === 0) {
                pool = sourcePool.filter((q) => {
                    const catMatch =
                        q.category
                            .toLowerCase()
                            .includes(catName.toLowerCase()) ||
                        catName
                            .toLowerCase()
                            .includes(q.category.toLowerCase());
                    const subcatMatch =
                        subcats.length === 0 ||
                        subcats.some(
                            (subName) =>
                                q.subcategory
                                    .toLowerCase()
                                    .includes(subName.toLowerCase()) ||
                                subName
                                    .toLowerCase()
                                    .includes(q.subcategory.toLowerCase()),
                        );

                    let langMatch = true;

                    if (lang === 'English') {
                        langMatch = q.language === 'English' || !q.language;
                    } else if (lang === 'Filipino') {
                        langMatch = q.language === 'Filipino';
                    }

                    return catMatch && subcatMatch && langMatch;
                });
            }

            if (pool.length === 0) {
                pool = sourcePool.slice(0, 30);
            }

            const countLimit =
                qCountParam === 'all' ? pool.length : Number(qCountParam);
            const finalPool = pool
                .slice(0, Math.min(countLimit, pool.length))
                .map(shuffleOptionsForQuestion);
            const limitSecs = isTimedParam ? finalPool.length * 60 : 0;

            setDrillCategoryId(catId);
            setDrillCategoryName(
                catName.endsWith('Practice') || catName.endsWith('Drill')
                    ? catName
                    : `${catName} Practice`,
            );
            setDrillSubcategories(subcats);
            setDrillLanguage(lang);
            setDrillQuestionCount(
                qCountParam === 'all' ? 'all' : Number(qCountParam),
            );

            setSelectedExamId(null);
            setIsTimed(isTimedParam);
            setActiveQuestions(finalPool);
            setCurrentIdx(0);
            setAnswers({});
            setQuestionTimes({});
            setAnswerChanges({});
            setFlagged({});
            setSessionTimeLimitSecs(limitSecs);
            setTimeLeft(limitSecs);
            setIsExamActive(true);
            setIsExamSubmitted(false);
            setReviewScreenActive(false);
            setResults(null);
            setSubmittedByTimer(false);

            const sessionOrigin = getSessionOrigin() || fromParam;
            const originTitle = sessionOrigin
                ? getOriginTitle(sessionOrigin)
                : 'Practice';
            const originHref = sessionOrigin
                ? sessionOrigin.startsWith('/')
                    ? sessionOrigin
                    : `/${sessionOrigin}`
                : '/drills';

            setLayoutProps({
                breadcrumbs: [
                    { title: originTitle, href: originHref },
                    { title: `${catName} Active Practice`, href: '#' },
                ],
            });
        }
    }, [
        questions,
        fallbackQuestions,
        savedAttempt,
        isExamActive,
        beginExamSession,
        buildFreshExamPool,
        setIsFreeAttempt,
        setSelectedExamId,
        setDrillCategoryId,
        setDrillCategoryName,
        setDrillSubcategories,
        setDrillLanguage,
        setDrillQuestionCount,
        setIsTimed,
        setActiveQuestions,
        setCurrentIdx,
        setAnswers,
        setQuestionTimes,
        setAnswerChanges,
        setFlagged,
        setSessionTimeLimitSecs,
        setTimeLeft,
        setIsExamActive,
        setIsExamSubmitted,
        setReviewScreenActive,
        setResults,
        setSubmittedByTimer,
    ]);

    // 3. Restore guest free exam after registration
    useEffect(() => {
        if (
            !auth?.user ||
            questions.length === 0 ||
            isExamActive ||
            isExamSubmitted
        ) {
            return;
        }

        const savedState = localStorage.getItem('pending_free_exam');

        if (!savedState) {
            return;
        }

        try {
            const state = JSON.parse(savedState);
            localStorage.removeItem('pending_free_exam');

            const sourcePool = [...questions];
            const rawPool: Question[] =
                state.activeQuestions ||
                (state.questionIds || [])
                    .map((id: number) =>
                        sourcePool.find((q: Question) => q.id === id),
                    )
                    .filter(Boolean)
                    .map(shuffleOptionsForQuestion);
            const pool = scoredOnly(rawPool);
            const restoredAnswers = remapIndexedRecord<number>(
                state.answers as Record<number, number> | undefined,
                rawPool,
                pool,
            );
            const restoredTimes = remapIndexedRecord<number>(
                state.questionTimes as Record<number, number> | undefined,
                rawPool,
                pool,
            );
            const restoredChanges = remapIndexedRecord<number>(
                state.answerChanges as Record<number, number> | undefined,
                rawPool,
                pool,
            );

            if (pool.length === 0) {
                return;
            }

            setSelectedExamId(state.selectedExamId);
            setIsTimed(state.isTimed);
            setActiveQuestions(pool);
            setCurrentIdx(Math.min(state.currentIdx || 0, pool.length - 1));
            setAnswers(restoredAnswers);
            setQuestionTimes(restoredTimes);
            setAnswerChanges(restoredChanges);
            setFlagged({});
            setSessionTimeLimitSecs(state.sessionTimeLimitSecs);
            setTimeLeft(state.timeLeft);
            setIsFreeAttempt(false);
            setIsExamActive(true);
            setIsExamSubmitted(false);
            setReviewScreenActive(false);
            setResults(null);
            setSubmittedByTimer(false);
        } catch {
            localStorage.removeItem('pending_free_exam');
        }
    }, [
        auth?.user,
        questions,
        isExamActive,
        isExamSubmitted,
        setSelectedExamId,
        setIsTimed,
        setActiveQuestions,
        setCurrentIdx,
        setAnswers,
        setQuestionTimes,
        setAnswerChanges,
        setFlagged,
        setSessionTimeLimitSecs,
        setTimeLeft,
        setIsFreeAttempt,
        setIsExamActive,
        setIsExamSubmitted,
        setReviewScreenActive,
        setResults,
        setSubmittedByTimer,
    ]);
}

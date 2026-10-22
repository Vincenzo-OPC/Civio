export interface CategoryScore {
    name: string;
    correct: number;
    total: number;
    percentage: number;
}

export interface ChartDataPoint {
    score: number;
    label: string;
    date: string;
    track: string;
    detail: string;
    categoryScores?: CategoryScore[];
}

export interface SubtestThreshold {
    category: string;
    score: number;
    passed: boolean;
}

export interface SubcategoryAnalytics {
    id?: number;
    name: string;
    percentage: number;
    correct: number;
    total: number;
}

export interface PacingTrend {
    name: string;
    date: string;
    secondsPerQuestion: number;
    accuracy: number;
}

export interface AttemptBreakdown {
    name: string;
    date: string;
    Verbal: number | null;
    Clerical: number | null;
    General: number | null;
    Numerical: number | null;
    Analytical: number | null;
}

export interface AnalyticsCategory {
    name: string;
    percentage: number;
    color: string;
    correct: number;
    total: number;
    subcategories?: SubcategoryAnalytics[];
}

export interface AnalyticsStats {
    avgScore: number;
    totalExams: number;
    strongestArea: string;
    weakestArea: string;
    chartData: ChartDataPoint[];
    categories: AnalyticsCategory[];
    passingRate: number;
    totalDuration: string;
    avgDuration: string;
    totalQuestionsSolved: number;
    daysUntilExam?: number | null;
    examDate?: string | null;
    examDateRaw?: string | null;
    cseReadinessIndex?: number;
    subtestThresholds?: SubtestThreshold[];
    hasSubtestRisk?: boolean;
    percentileRank?: number | null;
    isIncompleteSyllabus?: boolean;
    coveredCategoriesCount?: number;
    mockExamCount?: number;
    filters?: {
        track: string;
        runs: string;
    };
    pacingTrend?: PacingTrend[];
    attemptBreakdowns?: AttemptBreakdown[];
    learning?: LearningSignals;
}

export interface AnalyticsProps {
    stats?: AnalyticsStats | null;
    aiAnalysis?: {
        status: 'no_data' | 'generating' | 'ready' | 'failed' | 'no_exam_date';
        data: any | null;
    };
}

/** Independent-only signals from LearningInsightsService. */
export interface LearningSignals {
    mastery: {
        name: string;
        correct: number;
        total: number;
        percentage: number;
    }[];
    timedSuggestions: string[];
    pace: { name: string; secondsPerItem: number; items: number }[];
    skills?: {
        subject: string;
        skill: string;
        subcategoryId: number;
        correct: number;
        total: number;
        percentage: number;
        stage: 'start' | 'building' | 'steady' | 'timed';
        next: string;
    }[];
    retention?: { checked: number; kept: number; percentage: number } | null;
}

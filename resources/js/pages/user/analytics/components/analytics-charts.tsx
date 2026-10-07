import type { AnalyticsCategory, ChartDataPoint, PacingTrend } from '../types';
import { PacingTrendChart } from './pacing-trend-chart';
import { QuestionVolumeChart } from './question-volume-chart';
import { ScoreHistoryChart } from './score-history-chart';
import { SubcategoryRadarChart } from './subcategory-radar-chart';
import { SubjectMasteryChart } from './subject-mastery-chart';

/**
 * All recharts-based panels in one lazily loaded chunk, so Lite mode (which
 * shows text tables instead) never downloads the chart library.
 */
export default function AnalyticsCharts({
    chartData,
    categories,
    pacingTrend,
    isDemoMode,
}: {
    chartData: ChartDataPoint[];
    categories: AnalyticsCategory[];
    pacingTrend: PacingTrend[];
    isDemoMode: boolean;
}) {
    return (
        <>
            {/* Row 1: Score History (Full Width) */}
            <ScoreHistoryChart chartData={chartData} isDemoMode={isDemoMode} />

            {/* Row 2: Subject Mastery (Radial) + Question Volume (Donut) */}
            <div className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
                <SubjectMasteryChart categories={categories} />
                <QuestionVolumeChart categories={categories} />
            </div>

            {/* Row 3: Weakest Subcategories (with inline drills) + Pacing Trend (with 54s benchmark) */}
            <div className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
                <SubcategoryRadarChart categories={categories} />
                <PacingTrendChart data={pacingTrend} />
            </div>
        </>
    );
}

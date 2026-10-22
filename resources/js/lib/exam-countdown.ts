// Exam-day countdown in Philippine time (Asia/Manila, UTC+8, no DST).
// The target is 00:00 PHT at the start of exam day, whatever the browser's
// own timezone is. The CSC calendar gives no start hour, so the UI says
// "Until exam day", never "Until exam starts".

export const PH_OFFSET_MS = 8 * 60 * 60 * 1000;
const DAY_MS = 24 * 60 * 60 * 1000;

export interface ExamSitting {
    date: string; // YYYY-MM-DD, a Philippine calendar day
    sitting: string;
    label: string;
}

export interface ExamMilestone extends ExamSitting {
    kind: 'filing_opens' | 'exam_day' | string;
}

export type ExamTrack = 'professional' | 'subprofessional';

export interface CountdownParts {
    days: number;
    hours: number;
    minutes: number;
    seconds: number;
}

export type CountdownState =
    | { phase: 'counting'; sitting: ExamSitting; parts: CountdownParts }
    | { phase: 'today'; sitting: ExamSitting }
    | { phase: 'none' };

/** Epoch ms of 00:00 Philippine time on the given YYYY-MM-DD. */
export function phMidnightMs(dateRaw: string): number {
    const [y, m, d] = dateRaw.split('-').map(Number);

    return Date.UTC(y, m - 1, d) - PH_OFFSET_MS;
}

/** The Philippine calendar day (YYYY-MM-DD) at the given instant. */
export function phToday(nowMs: number): string {
    return new Date(nowMs + PH_OFFSET_MS).toISOString().slice(0, 10);
}

export function splitMs(ms: number): CountdownParts {
    const total = Math.max(0, Math.floor(ms / 1000));

    return {
        days: Math.floor(total / 86400),
        hours: Math.floor((total % 86400) / 3600),
        minutes: Math.floor((total % 3600) / 60),
        seconds: total % 60,
    };
}

/**
 * Pick the next sitting and how long until its PH midnight. A sitting whose
 * PH day is under way reads "today"; once that day ends it is skipped and the
 * next confirmed sitting takes over.
 */
export function examCountdown(
    sittings: readonly ExamSitting[],
    nowMs: number,
): CountdownState {
    const sorted = [...sittings].sort((a, b) => a.date.localeCompare(b.date));

    for (const sitting of sorted) {
        const start = phMidnightMs(sitting.date);

        if (nowMs < start) {
            return {
                phase: 'counting',
                sitting,
                parts: splitMs(start - nowMs),
            };
        }

        if (nowMs < start + DAY_MS) {
            return { phase: 'today', sitting };
        }
    }

    return { phase: 'none' };
}

/** The first milestone whose PH day has not ended yet. */
export function nextMilestone(
    milestones: readonly ExamMilestone[],
    nowMs: number,
): ExamMilestone | null {
    const today = phToday(nowMs);

    return (
        [...milestones]
            .sort((a, b) => a.date.localeCompare(b.date))
            .find((m) => m.date >= today) ?? null
    );
}

export function milestoneText(m: ExamMilestone): string {
    if (m.kind === 'filing_opens') {
        const month = m.sitting.includes('August') ? 'August' : 'March';

        return `${month} CSE registration opens`;
    }

    return 'Exam day';
}

/** Long date in PH terms, e.g. "March 14, 2027", independent of browser zone. */
export function formatPhDate(dateRaw: string): string {
    return new Intl.DateTimeFormat('en-US', {
        timeZone: 'UTC',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    }).format(new Date(`${dateRaw}T00:00:00Z`));
}

export const TRACK_LABEL: Record<ExamTrack, string> = {
    professional: 'Professional',
    subprofessional: 'Subprofessional',
};

export const TRACK_STORAGE_KEY = 'civio_countdown_track';

export function readTrack(raw: string | null | undefined): ExamTrack {
    return raw === 'subprofessional' ? 'subprofessional' : 'professional';
}

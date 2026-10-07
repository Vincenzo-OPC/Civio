/**
 * Pure exam-clock helpers (no React, no DOM) so the urgency thresholds can be
 * unit-tested. Ported from the MSI desktop study build (2026-10-03 patch):
 *
 * - "Exam left" counts down from 3:10:00 (Professional) or 2:40:00
 *   (Subprofessional). Calm green while more than 10 minutes remain, amber in
 *   the last 10 minutes, red in the last 2 minutes. Time-up reuses the existing
 *   auto-submit.
 * - "This item" counts up and resets when the learner moves to another item.
 *   Calm green under 45s, amber from 45s through 75s, red after 75s.
 *
 * No sound and no flashing: tone only changes the chip colour.
 */

export type ClockTone = 'calm' | 'amber' | 'red';

export const EXAM_CLOCK_THRESHOLDS = {
    /** Exam clock turns amber at or below this many seconds left (10 min). */
    examAmberAtOrBelowSecs: 600,
    /** Exam clock turns red at or below this many seconds left (2 min). */
    examRedAtOrBelowSecs: 120,
    /** Item clock turns amber at or above this many seconds spent. */
    itemAmberFromSecs: 45,
    /** Item clock turns red once more than this many seconds are spent. */
    itemRedAfterSecs: 75,
} as const;

/** Official session lengths used by the strict mocks. */
export const EXAM_DURATION_SECS = {
    Professional: 3 * 3600 + 10 * 60, // 3:10:00
    Subprofessional: 2 * 3600 + 40 * 60, // 2:40:00
} as const;

export function examClockTone(timeLeftSecs: number): ClockTone {
    const left = Math.max(0, Math.floor(timeLeftSecs));

    if (left <= EXAM_CLOCK_THRESHOLDS.examRedAtOrBelowSecs) {
        return 'red';
    }

    if (left <= EXAM_CLOCK_THRESHOLDS.examAmberAtOrBelowSecs) {
        return 'amber';
    }

    return 'calm';
}

export function itemClockTone(elapsedSecs: number): ClockTone {
    const spent = Math.max(0, Math.floor(elapsedSecs));

    if (spent > EXAM_CLOCK_THRESHOLDS.itemRedAfterSecs) {
        return 'red';
    }

    if (spent >= EXAM_CLOCK_THRESHOLDS.itemAmberFromSecs) {
        return 'amber';
    }

    return 'calm';
}

/** H:MM:SS for the exam countdown (e.g. 3:10:00). */
export function formatExamLeft(secs: number): string {
    const safe = Math.max(0, Math.floor(secs));
    const h = Math.floor(safe / 3600);
    const m = Math.floor((safe % 3600) / 60);
    const s = safe % 60;

    return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

/** M:SS for the per-item clock (e.g. 1:05). */
export function formatItemElapsed(secs: number): string {
    const safe = Math.max(0, Math.floor(secs));
    const m = Math.floor(safe / 60);
    const s = safe % 60;

    return `${m}:${String(s).padStart(2, '0')}`;
}

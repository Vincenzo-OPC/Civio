import { EXAM_DURATION_SECS } from '@/lib/exam-clock';

/**
 * Scored mock sittings. The CSC paper adds a 20-item Examinee Descriptive
 * Questionnaire (170 and 165 on the official sheet). Civio times the scored
 * items only: 150 in 3 hr 10 min, and 145 in 2 hr 40 min.
 */
export const EXAM_DIALS = {
    professional: {
        id: 'professional',
        examId: 1,
        name: 'Professional',
        questions: 150,
        seconds: EXAM_DURATION_SECS.Professional,
        description:
            'For professional, technical, and scientific positions in government service.',
    },
    subprofessional: {
        id: 'subprofessional',
        examId: 2,
        name: 'Subprofessional',
        questions: 145,
        seconds: EXAM_DURATION_SECS.Subprofessional,
        description:
            'For clerical, trades, crafts, and custodial positions in government service.',
    },
} as const;

export type ExamDialId = keyof typeof EXAM_DIALS;

/**
 * Clock face. Twelve marks, not one mark per five minutes of the sitting.
 * A 3 hr 10 min sitting is 38 of those five-minute marks, and 38 is not a
 * multiple of 12, so the longer marks bunched up near 12 and left a gap.
 */
export const CLOCK_TICKS = 12;

export type ClockTickRole = 'hour' | 'cardinal';

export function clockTick(index: number): {
    angle: number;
    role: ClockTickRole;
} {
    const safe = ((index % CLOCK_TICKS) + CLOCK_TICKS) % CLOCK_TICKS;

    return {
        angle: (safe / CLOCK_TICKS) * 360,
        role: safe % 3 === 0 ? 'cardinal' : 'hour',
    };
}

/** "3 hr 10 min". The ring is this sitting, not a percent of a score. */
export function formatSitting(seconds: number): string {
    const safe = Math.max(0, Math.floor(seconds));
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);
    const parts: string[] = [];

    if (hours > 0) {
        parts.push(`${hours} hr`);
    }

    if (minutes > 0) {
        parts.push(`${minutes} min`);
    }

    return parts.join(' ') || '0 min';
}

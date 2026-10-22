/**
 * Dexter Rescue client guard (ADR-0003). The server is authoritative (gate,
 * 423 during an active Strict Mock); this guard makes sure the client never
 * even asks for answer-derived diagnostics in Exam (Strict) Mode, while a
 * Strict Mock is running, before an answer is graded, or for a right answer.
 *
 * Not imported by the exam page yet: the Rescue panel ships only after the
 * editorial pilot validates metadata and the gate is opened.
 */
export type RescueContext = {
    mode: 'study' | 'strict';
    strictMockActive: boolean;
    graded: boolean;
    correct: boolean | null;
};

export function canRequestRescue(ctx: RescueContext): boolean {
    return (
        ctx.mode === 'study' &&
        !ctx.strictMockActive &&
        ctx.graded &&
        ctx.correct === false
    );
}

export type RescuePayload = {
    state: 'idle' | 'explained';
    skill: string | null;
    diagnosis?: { code: string; label: string; method: string } | null;
};

/** Only a validated diagnosis may be labelled as one; otherwise say "why this option is wrong". */
export function rescueHeading(p: RescuePayload): string {
    return p.diagnosis ? p.diagnosis.label : 'Why this option is wrong';
}

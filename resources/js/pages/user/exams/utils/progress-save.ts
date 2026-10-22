import type { Question } from '../types';

type QuestionsSetter = (update: (prev: Question[]) => Question[]) => void;

/** Flag withdrawn items on screen; keeps the same array if nothing changes. */
export function markWithdrawn(
    setQuestions: QuestionsSetter | undefined,
    ids: number[],
): void {
    if (!setQuestions || ids.length === 0) {
        return;
    }

    setQuestions((prev) =>
        prev.some((q) => ids.includes(q.id) && !q.withdrawn)
            ? prev.map((q) =>
                  ids.includes(q.id) && !q.withdrawn
                      ? { ...q, withdrawn: true }
                      : q,
              )
            : prev,
    );
}

/**
 * One Strict-mock progress save, with recovery rules:
 * - 409 version conflict (another tab saved): re-read, retry once on the
 *   newer version, and hand back the merged server answers to hydrate.
 * - 409 because the mock was submitted or its deadline passed: closed.
 * - Items withdrawn mid-mock come back in withdrawn_ids on a successful save:
 *   the caller drops those local answers; the active ones in the same patch
 *   are saved. A 422 now means a malformed patch and is never retried.
 * No HTTP status (connection dropped): offline; the caller holds the answer
 *   and resends it on reconnect.
 * Anything else fails and the caller stops saving.
 */
export interface ProgressResponse {
    deadline_at: string | null;
    server_now: string;
    answers: Record<string, number | null>;
    save_version: number;
    submitted: boolean;
    withdrawn_ids?: number[];
}

export type ProgressPost = (
    payload: Record<string, unknown>,
) => Promise<ProgressResponse>;

export type SaveOutcome =
    | { kind: 'saved'; version: number; withdrawn: number[] }
    | {
          kind: 'merged';
          version: number;
          answers: ProgressResponse['answers'];
          withdrawn: number[];
      }
    | { kind: 'closed'; submitted: boolean }
    | { kind: 'offline' }
    | { kind: 'failed' };

export function httpStatusOf(error: unknown): number | null {
    const match = /status (\d{3})/.exec(
        error instanceof Error ? error.message : String(error),
    );

    return match ? Number(match[1]) : null;
}

export function isClosed(data: ProgressResponse): boolean {
    return (
        data.submitted ||
        (data.deadline_at !== null &&
            Date.parse(data.server_now) >= Date.parse(data.deadline_at))
    );
}

export async function saveProgressPatch(
    post: ProgressPost,
    sessionId: string,
    answers: Record<number, number | null>,
    expectedVersion: number,
): Promise<SaveOutcome> {
    if (Object.keys(answers).length === 0) {
        // Everything in the batch was withdrawn: nothing to send.
        return { kind: 'saved', version: expectedVersion, withdrawn: [] };
    }

    const patch = (version: number) =>
        post({
            exam_session_id: sessionId,
            expected_version: version,
            answers,
        });

    try {
        const data = await patch(expectedVersion);

        return {
            kind: 'saved',
            version: data.save_version,
            withdrawn: data.withdrawn_ids ?? [],
        };
    } catch (error) {
        const status = httpStatusOf(error);

        if (status === null) {
            return { kind: 'offline' };
        }

        if (status !== 409) {
            return { kind: 'failed' };
        }
    }

    try {
        const latest = await post({ exam_session_id: sessionId });

        if (isClosed(latest)) {
            return { kind: 'closed', submitted: latest.submitted };
        }

        if (latest.save_version === expectedVersion) {
            // Not a version conflict, yet the server refused: do not loop.
            return { kind: 'failed' };
        }

        const data = await patch(latest.save_version);

        return {
            kind: 'merged',
            version: data.save_version,
            answers: data.answers,
            withdrawn: data.withdrawn_ids ?? [],
        };
    } catch (error) {
        const status = httpStatusOf(error);

        if (status === null) {
            return { kind: 'offline' };
        }

        return { kind: 'failed' };
    }
}

/** Examinee-facing notices, kept here so they load with the save logic. */
export const progressNotices = {
    merged: 'Answers were updated from another tab or device. Check your choices.',
    offline:
        'Connection lost. Keep answering; your answers will be saved when you reconnect. The server deadline still applies.',
    reconnected: 'Reconnected. Your answers are saved.',
    saveFailed:
        'Save failed. Reload to recover server answers. Late submission uses saved answers only.',
    restored: (count: number) =>
        `Restored ${count} answer${count === 1 ? '' : 's'} made while offline. Saving now.`,
    superseded: (count: number) =>
        `${count} offline answer${count === 1 ? ' was' : 's were'} changed later on another tab or device; the newer choice is kept.`,
    lateDiscarded:
        'Time ran out before your offline answers reached the server. Only answers saved before the deadline count.',
    submitted: 'Mock submitted. Open its scorecard.',
    expired: 'Time is up. Submit to grade your saved answers.',
    withdrawn: (count: number) =>
        count === 1
            ? 'One item was withdrawn by Civio and will not be scored. Your answer to it was cleared; your other answers are saved.'
            : `${count} items were withdrawn by Civio and will not be scored. Your answers to them were cleared; your other answers are saved.`,
};

type AnswerMap = Record<number, number>;

export interface SaveState {
    pending: Map<number, number | null>;
    withdrawnIds: Set<number>;
    offline: { current: boolean };
    /** Last answers known to be on the server (original option indices). */
    server?: Record<number, number | null>;
    /** Strict session the pending answers belong to, for local persistence. */
    sessionId?: string | null;
    storage?: Pick<Storage, 'getItem' | 'setItem' | 'removeItem'> | null;
}

/** id -> [local original choice, server value it was based on] */
export type PendingEntries = Record<number, [number | null, number | null]>;

export const pendingKey = (sessionId: string) =>
    `civio_strict_pending:${sessionId}`;

function defaultStorage(): SaveState['storage'] {
    try {
        return globalThis.localStorage ?? null;
    } catch {
        return null;
    }
}

/**
 * Keep unsent answers across a reload. Each entry remembers the server value
 * it was made against so a resume can tell which copy is newer.
 */
export function persistPending(state: SaveState): void {
    const storage = state.storage ?? defaultStorage();

    if (!storage || !state.sessionId) {
        return;
    }

    try {
        const key = pendingKey(state.sessionId);

        if (state.pending.size === 0) {
            storage.removeItem(key);

            return;
        }

        const previous = readPending(state.sessionId, storage);
        const entries: PendingEntries = {};

        for (const [id, original] of state.pending) {
            entries[id] = [
                original,
                previous[id]?.[1] ?? state.server?.[id] ?? null,
            ];
        }

        storage.setItem(key, JSON.stringify(entries));
    } catch {
        /* storage full or blocked: in-memory copy still resends */
    }
}

export function readPending(
    sessionId: string,
    storage: SaveState['storage'] = defaultStorage(),
): PendingEntries {
    try {
        const raw = storage?.getItem(pendingKey(sessionId));
        const parsed: unknown = raw ? JSON.parse(raw) : {};
        const out: PendingEntries = {};

        if (parsed && typeof parsed === 'object') {
            for (const [id, entry] of Object.entries(parsed)) {
                if (
                    Array.isArray(entry) &&
                    entry.length === 2 &&
                    entry.every((v) => v === null || Number.isInteger(v)) &&
                    Number.isInteger(Number(id))
                ) {
                    out[Number(id)] = entry as [number | null, number | null];
                }
            }
        }

        return out;
    } catch {
        return {};
    }
}

export interface ResumeMerge {
    answers: Record<number, number | null>;
    /** Local answers that are newer than the server copy and must be sent. */
    resend: Record<number, number | null>;
    /** Local answers discarded because the server copy changed since. */
    superseded: number[];
}

/**
 * Three-way merge on reload. A local answer is newer when the server still
 * holds the value that answer was made against; otherwise the server wins.
 * After the deadline the server copy is final and nothing is resent.
 */
export function mergeResumed(
    server: ProgressResponse,
    local: PendingEntries,
    servedIds: number[],
): ResumeMerge {
    const answers: Record<number, number | null> = {};

    for (const [id, value] of Object.entries(server.answers)) {
        answers[Number(id)] = value;
    }

    const resend: Record<number, number | null> = {};
    const superseded: number[] = [];
    const served = new Set(servedIds);

    if (isClosed(server)) {
        return { answers, resend, superseded: Object.keys(local).map(Number) };
    }

    for (const [key, [mine, base]] of Object.entries(local)) {
        const id = Number(key);

        if (!served.has(id)) {
            continue;
        }

        const current = answers[id] ?? null;

        if (current === base) {
            if (mine !== current) {
                answers[id] = mine;
                resend[id] = mine;
            }
        } else if (current !== mine) {
            superseded.push(id);
        }
    }

    return { answers, resend, superseded };
}

export interface SaveUi {
    /** Exam answers are keyed by served position, not question id. */
    setAnswers: (update: (prev: AnswerMap) => AnswerMap) => void;
    /** Served questions in position order (current at call time). */
    questions: { current: Question[] };
    /** Marks items withdrawn mid-mock so the exam screen can label them. */
    setQuestions?: QuestionsSetter;
    /** Replace answers from the server's original-option map. */
    hydrate: (answers: ProgressResponse['answers']) => void;
    /** sonner's toast (or any object with these methods). */
    toast: Record<
        'info' | 'success' | 'warning' | 'error',
        (message: string) => unknown
    >;
    closed: (submitted: boolean) => void;
}

/**
 * Apply a save outcome to local state. Returns the new server version, or
 * null when it did not change. Throws on a hard failure.
 */
export function settleSave(
    outcome: SaveOutcome,
    sent: Record<number, number | null>,
    state: SaveState,
    ui: SaveUi,
): number | null {
    if (outcome.kind === 'offline') {
        for (const [id, original] of Object.entries(sent)) {
            state.pending.set(Number(id), original);
        }

        persistPending(state);

        if (!state.offline.current) {
            state.offline.current = true;
            ui.toast.warning(progressNotices.offline);
        }

        return null;
    }

    // A newer choice for an item may be waiting; clear only what was sent.
    for (const [id, original] of Object.entries(sent)) {
        if (state.pending.get(Number(id)) === original) {
            state.pending.delete(Number(id));
        }
    }

    persistPending(state);

    if (state.pending.size === 0 && state.offline.current) {
        state.offline.current = false;
        ui.toast.success(progressNotices.reconnected);
    }

    if (outcome.kind === 'failed') {
        throw new Error('save failed');
    }

    if (outcome.kind === 'closed') {
        state.pending.clear();
        persistPending(state);
        ui.closed(outcome.submitted);
        ui.toast.error(
            outcome.submitted
                ? progressNotices.submitted
                : progressNotices.expired,
        );

        return null;
    }

    if (outcome.kind === 'merged') {
        state.server = { ...outcome.answers };
        ui.hydrate({
            ...outcome.answers,
            ...Object.fromEntries(state.pending),
        });
        ui.toast.info(progressNotices.merged);
    }

    const ids = outcome.withdrawn;

    if (outcome.kind === 'saved') {
        state.server = { ...state.server, ...sent };
    }

    for (const id of ids) {
        delete state.server?.[id];
    }

    const fresh = ids.filter((id) => !state.withdrawnIds.has(id));

    for (const id of ids) {
        state.withdrawnIds.add(id);
        state.pending.delete(id);
    }

    markWithdrawn(ui.setQuestions, ids);

    if (ids.length > 0) {
        persistPending(state);
        const positions = ui.questions.current
            .map((q) => q.id)
            .flatMap((id, index) => (ids.includes(id) ? [index] : []));
        ui.setAnswers((prev) => {
            const next = { ...prev };

            for (const index of positions) {
                delete next[index];
            }

            return next;
        });
    }

    if (fresh.length > 0) {
        ui.toast.warning(progressNotices.withdrawn(fresh.length));
    }

    return outcome.version;
}

/** Drop items already known to be withdrawn before sending a patch. */
export function withoutWithdrawn(
    batch: Record<number, number | null>,
    withdrawnIds: Set<number>,
): Record<number, number | null> {
    return Object.fromEntries(
        Object.entries(batch).filter(([id]) => !withdrawnIds.has(Number(id))),
    );
}

/**
 * Prepare a resume: merge stored offline answers with the server copy, reset
 * the in-memory state, and list notices to show. Pure apart from storage.
 */
export function resumeFromServer(
    data: ProgressResponse,
    state: SaveState,
    servedIds: number[],
    setQuestions?: QuestionsSetter,
): {
    answers: Record<number, number | null>;
    resend: Record<number, number | null>;
    notices: Array<['info' | 'warning', string]>;
} {
    const local = state.sessionId
        ? readPending(state.sessionId, state.storage ?? defaultStorage())
        : {};
    const withdrawn = data.withdrawn_ids ?? [];

    for (const id of withdrawn) {
        state.withdrawnIds.add(id);
        delete local[id];
    }

    const merged = mergeResumed(data, local, servedIds);

    // A withdrawn item shows no answer: it will not be scored.
    for (const id of withdrawn) {
        delete merged.answers[id];
    }

    markWithdrawn(setQuestions, withdrawn);
    const closed = isClosed(data);
    state.server = { ...data.answers };
    state.pending.clear();

    for (const [id, original] of Object.entries(merged.resend)) {
        state.pending.set(Number(id), original);
    }

    persistPending(state);

    const notices: Array<['info' | 'warning', string]> = [];
    const restored = Object.keys(merged.resend).length;

    if (restored > 0) {
        notices.push(['info', progressNotices.restored(restored)]);
    } else if (closed && Object.keys(local).length > 0) {
        notices.push(['warning', progressNotices.lateDiscarded]);
    }

    if (!closed && merged.superseded.length > 0) {
        notices.push([
            'info',
            progressNotices.superseded(merged.superseded.length),
        ]);
    }

    return { answers: merged.answers, resend: merged.resend, notices };
}

/** A completed mock must never be offered for local resume. */
export function forgetLocalSession(): void {
    try {
        localStorage.removeItem('active_exam_session_v1');
    } catch {
        /* storage unavailable */
    }
}

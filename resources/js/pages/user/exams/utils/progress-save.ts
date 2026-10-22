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

function isClosed(data: ProgressResponse): boolean {
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
}

export interface SaveUi {
    setAnswers: (update: (prev: AnswerMap) => AnswerMap) => void;
    /** Replace answers from the server's original-option map. */
    hydrate: (answers: ProgressResponse['answers']) => void;
    notify: (
        level: 'info' | 'success' | 'warning' | 'error',
        message: string,
    ) => void;
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

        if (!state.offline.current) {
            state.offline.current = true;
            ui.notify('warning', progressNotices.offline);
        }

        return null;
    }

    // A newer choice for an item may be waiting; clear only what was sent.
    for (const [id, original] of Object.entries(sent)) {
        if (state.pending.get(Number(id)) === original) {
            state.pending.delete(Number(id));
        }
    }

    if (state.pending.size === 0 && state.offline.current) {
        state.offline.current = false;
        ui.notify('success', progressNotices.reconnected);
    }

    if (outcome.kind === 'failed') {
        throw new Error('save failed');
    }

    if (outcome.kind === 'closed') {
        state.pending.clear();
        ui.closed(outcome.submitted);
        ui.notify(
            'error',
            outcome.submitted
                ? progressNotices.submitted
                : progressNotices.expired,
        );

        return null;
    }

    if (outcome.kind === 'merged') {
        ui.hydrate({
            ...outcome.answers,
            ...Object.fromEntries(state.pending),
        });
        ui.notify('info', progressNotices.merged);
    }

    const ids = outcome.withdrawn;
    const fresh = ids.filter((id) => !state.withdrawnIds.has(id));

    for (const id of ids) {
        state.withdrawnIds.add(id);
        state.pending.delete(id);
    }

    if (ids.length > 0) {
        ui.setAnswers((prev) => {
            const next = { ...prev };

            for (const id of ids) {
                delete next[id];
            }

            return next;
        });
    }

    if (fresh.length > 0) {
        ui.notify('warning', progressNotices.withdrawn(fresh.length));
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

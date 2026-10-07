/**
 * Lite L2: queue offline answers and sync them when back online. Pure core
 * plus a small orchestrator with injected dependencies (store, network, bias).
 *
 * Every queued answer is re-graded on the server. Weak-topic stats are
 * updated only from the server's verdicts, never from the local grade.
 */
import type { StudyBiasInput } from '@/lib/guest-study-bias';
import type { CategoryScore, Question } from '@/pages/user/exams/types';
import { toOriginalIndex } from './grader';
import type {
    OfflinePackItem,
    QueuedAnswer,
    SyncResponse,
    SyncVerdict,
} from './types';

/** Matches SyncOfflineAttemptsRequest::MAX_ITEMS. */
export const SYNC_BATCH_SIZE = 200;

/** Keep the queue bounded on small phones. */
export const MAX_QUEUE = 2000;

export function newClientId(random: () => number = Math.random): string {
    const part = () =>
        Math.floor(random() * 0x100000000)
            .toString(36)
            .padStart(7, '0');

    return `${Date.now().toString(36)}-${part()}${part()}`;
}

/** Answers from a finished offline session, in original option order. */
export function answersFromSession(
    items: readonly OfflinePackItem[],
    questions: readonly Question[],
    answers: Readonly<Record<number, number>>,
    packVersions: Readonly<Record<string, string>>,
    now: Date,
    makeId: () => string = newClientId,
): QueuedAnswer[] {
    const out: QueuedAnswer[] = [];

    items.forEach((item, index) => {
        const display = answers[index];
        const question = questions[index];

        if (display === undefined || !question) {
            return;
        }

        out.push({
            client_id: makeId(),
            question_id: item.id,
            selected_option: toOriginalIndex(question, display),
            claimed_correct_option: item.correct_option,
            pack_version: packVersions[item.category] ?? null,
            answered_at: now.toISOString(),
        });
    });

    return out;
}

/** Append without duplicate client ids; oldest entries drop past MAX_QUEUE. */
export function enqueue(
    queue: readonly QueuedAnswer[],
    answers: readonly QueuedAnswer[],
): QueuedAnswer[] {
    const seen = new Set(queue.map((a) => a.client_id));
    const merged = [...queue];

    for (const answer of answers) {
        if (!seen.has(answer.client_id)) {
            seen.add(answer.client_id);
            merged.push(answer);
        }
    }

    return merged.slice(-MAX_QUEUE);
}

export function nextBatch(
    queue: readonly QueuedAnswer[],
    size: number = SYNC_BATCH_SIZE,
): QueuedAnswer[] {
    return queue.slice(0, size);
}

/** Drop every answer the server gave a verdict for (accepted or rejected). */
export function applyVerdicts(
    queue: readonly QueuedAnswer[],
    verdicts: readonly SyncVerdict[],
): QueuedAnswer[] {
    const done = new Set(verdicts.map((v) => v.client_id));

    return queue.filter((a) => !done.has(a.client_id));
}

/** Server bias block → input for recordGuestStudyBias('Drill', …). */
export function toBiasInput(bias: SyncResponse['bias']): StudyBiasInput {
    const scores = Array.isArray(bias.category_scores)
        ? {}
        : (bias.category_scores as Record<string, CategoryScore>);

    return {
        wrongIds: [...bias.wrong_ids],
        correctIds: [...bias.correct_ids],
        categoryScoreMap: scores,
    };
}

export interface SyncDeps {
    loadQueue: () => Promise<QueuedAnswer[]>;
    saveQueue: (queue: QueuedAnswer[]) => Promise<void>;
    post: (batch: QueuedAnswer[]) => Promise<SyncResponse>;
    recordBias: (input: StudyBiasInput) => void;
    isOnline: () => boolean;
}

export interface SyncSummary {
    sent: number;
    accepted: number;
    rejected: number;
    correct: number;
    remaining: number;
    error: string | null;
}

/** Send the queue in batches. Stops on the first network/server error. */
export async function syncQueue(deps: SyncDeps): Promise<SyncSummary> {
    let queue = await deps.loadQueue();
    const summary: SyncSummary = {
        sent: 0,
        accepted: 0,
        rejected: 0,
        correct: 0,
        remaining: queue.length,
        error: null,
    };

    while (queue.length > 0) {
        if (!deps.isOnline()) {
            summary.error = 'offline';
            break;
        }

        const batch = nextBatch(queue);
        let response: SyncResponse;

        try {
            response = await deps.post(batch);
        } catch (error) {
            summary.error =
                error instanceof Error ? error.message : 'sync failed';
            break;
        }

        const verdicts = response.results ?? [];

        if (verdicts.length === 0) {
            summary.error = 'empty response';
            break;
        }

        summary.sent += batch.length;

        for (const verdict of verdicts) {
            if (verdict.status === 'accepted') {
                summary.accepted++;
                summary.correct += verdict.correct ? 1 : 0;
            } else {
                summary.rejected++;
            }
        }

        if (verdicts.some((v) => v.status === 'accepted')) {
            deps.recordBias(toBiasInput(response.bias));
        }

        // Re-read: answers queued during the request must not be lost.
        queue = applyVerdicts(await deps.loadQueue(), verdicts);
        await deps.saveQueue(queue);
    }

    summary.remaining = queue.length;

    return summary;
}

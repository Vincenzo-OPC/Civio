import { expect, test } from '@playwright/test';
import {
    answerOnline,
    call,
    isProgress,
    pending,
    php,
    pick,
    progress,
    startStrict,
    toasts,
    waitForExam,
} from './helpers';

// One throwaway DB, one server: run the scenarios one at a time.
test.describe.configure({ mode: 'serial' });

test('offline answer survives closing the tab and reaches the server after reconnect', async ({
    context,
}) => {
    const { sid, q, p: first } = await startStrict(context);
    let p = first;
    expect((await answerOnline(p, 'Bravo', q[0].id, 1)).answers[q[0].id]).toBe(
        1,
    );

    await context.setOffline(true);
    await p.getByRole('button', { name: 'Next' }).click();
    await pick(p, 'Charlie');
    await expect
        .poll(async () => JSON.parse((await pending(p, sid)) ?? 'null'))
        .toEqual({ [q[1].id]: [2, null] });
    expect(await toasts(p)).toEqual(
        expect.arrayContaining([expect.stringMatching(/Connection lost/)]),
    );

    await p.close();
    await context.setOffline(false);
    p = await context.newPage();
    const resent = p.waitForResponse(
        (r) =>
            isProgress(r) &&
            (r.request().postData() ?? '').includes(`"${q[1].id}":2`),
        { timeout: 30_000 },
    );
    await p.goto('/exams');
    await expect(
        p.getByText(/Restored 1 answer made while offline/),
    ).toBeVisible({ timeout: 10_000 });
    await resent;

    const server = await progress(p, sid);
    expect(server.answers[q[0].id], 'online answer kept').toBe(1);
    expect(server.answers[q[1].id], 'offline answer saved after reopen').toBe(
        2,
    );
    expect(await pending(p, sid), 'local copy cleared').toBeNull();
});

test('two tabs: a stale tab save re-reads, retries once and keeps both answers', async ({
    context,
}) => {
    const { p: a, sid, q } = await startStrict(context);
    const b = await context.newPage();
    await b.goto('/exams'); // same browser session: resumes the same mock
    await waitForExam(b);
    await b.waitForTimeout(300);

    // Tab A saves first (version 0 -> 1). Tab B still holds version 0.
    expect((await answerOnline(a, 'Bravo', q[0].id, 1)).save_version).toBe(1);
    const conflict = b.waitForResponse(
        (r) => isProgress(r) && r.status() === 409,
    );
    const merged = b.waitForResponse(
        (r) =>
            isProgress(r) &&
            r.status() === 200 &&
            (r.request().postData() ?? '').includes('"expected_version":1'),
    );
    await b.getByRole('button', { name: 'Next' }).click();
    await pick(b, 'Charlie');
    await conflict;
    expect((await (await merged).json()).save_version).toBe(2);

    const server = await progress(a, sid);
    expect(server.answers[q[0].id], "tab A's answer survives").toBe(1);
    expect(server.answers[q[1].id], "tab B's answer saved after retry").toBe(2);
    await expect
        .poll(() => toasts(b))
        .toEqual(
            expect.arrayContaining([
                expect.stringMatching(/updated from another tab/),
            ]),
        );
});

test('deadline passes while offline: late answer refused, only saved answers graded', async ({
    context,
}) => {
    const { p, sid, q } = await startStrict(context);
    await answerOnline(p, 'Bravo', q[0].id, 1);
    php(
        `App\\Models\\ExamSession::whereKey('${sid}')->update(['deadline_at' => now()->addSeconds(4)]);`,
    );

    await context.setOffline(true);
    await p.getByRole('button', { name: 'Next' }).click();
    await pick(p, 'Bravo');
    await p.waitForTimeout(5500); // the deadline passes while offline
    const refused = p.waitForResponse(
        (r) => isProgress(r) && r.status() === 409,
    );
    await context.setOffline(false); // 'online' flush: the late save is refused
    await refused;
    await expect
        .poll(() => toasts(p))
        .toEqual(expect.arrayContaining([expect.stringMatching(/Time is up/)]));
    expect(await pending(p, sid), 'late answer not kept for resend').toBeNull();

    const server = await progress(p, sid);
    expect(server.answers[q[1].id], 'late answer never saved').toBeUndefined();

    // Even a final submit carrying the late answer grades saved answers only.
    const res = await call(p, '/exams/attempts', {
        exam_session_id: sid,
        question_ids: q.map((x) => x.id),
        answers: { [q[0].id]: 1, [q[1].id]: 1 },
    });
    expect(res.status).toBe(200);
    expect(res.body.answers[q[1].id], 'late answer not graded').toBeNull();
    expect(res.body.answers[q[0].id]).toBe(1);
});

test('double submit: exactly one attempt, the second is refused, refresh cannot resume', async ({
    context,
}) => {
    const { p, sid, q } = await startStrict(context);
    await answerOnline(p, 'Bravo', q[0].id, 1);
    const payload = {
        exam_session_id: sid,
        question_ids: q.map((x) => x.id),
        answers: { [q[0].id]: 1 },
    };
    const [r1, r2] = await Promise.all([
        call(p, '/exams/attempts', payload),
        call(p, '/exams/attempts', payload),
    ]);
    const statuses = [r1.status, r2.status].sort();
    expect(
        statuses.filter((s) => s === 200),
        'exactly one accepted',
    ).toHaveLength(1);
    expect([409, 429], 'second refused').toContain(
        statuses.find((s) => s !== 200),
    );
    const attempts = php(
        `echo App\\Models\\ExamAttempt::whereIn('id', App\\Models\\ExamSession::whereKey('${sid}')->pluck('exam_attempt_id'))->count();`,
    );
    expect(Number(attempts.split('\n').pop())).toBe(1);
    expect(
        (await call(p, '/exams/attempts', payload)).status,
        'a later retry is refused too',
    ).toBe(409);
    expect(
        (
            await call(p, '/exams/sessions/progress', {
                exam_session_id: sid,
                expected_version: 1,
                answers: { [q[1].id]: 0 },
            })
        ).status,
        'no saves after submit',
    ).toBe(409);

    // Refresh after submit: the page must not resume the completed mock.
    await p.reload();
    await p.waitForTimeout(2500);
    await expect(
        p.getByRole('button', { name: 'Next' }),
        'exam screen not resumed',
    ).toHaveCount(0);
    expect(
        await p.evaluate(() => localStorage.getItem('active_exam_session_v1')),
        'local resume copy cleared',
    ).toBeNull();
});

test('an item withdrawn mid-mock is marked on screen, live and after a reload, with no key', async ({
    context,
}) => {
    const { p, sid, q } = await startStrict(context);
    await answerOnline(p, 'Bravo', q[0].id, 1);
    php(
        `App\\Models\\Question::whereKey(${q[1].id})->update(['status' => 'retired']);`,
    );

    // Live: the next save reports the withdrawal and the item is marked.
    await p.getByRole('button', { name: 'Next' }).click();
    const saved = p.waitForResponse((r) => isProgress(r) && r.status() === 200);
    await pick(p, 'Charlie');
    const body = await (await saved).json();
    expect(body.withdrawn_ids).toContain(q[1].id);
    expect(JSON.stringify(body)).not.toMatch(/correct_option|explanation/);
    await expect(p.getByTestId('withdrawn-live')).toBeVisible();

    // Reload: the progress read lists it again and the mark comes back.
    await p.reload();
    await waitForExam(p);
    // The resume copy reopens on the item the candidate was on.
    await expect(p.getByText(/^Question 2 of/)).toBeVisible();
    await expect(p.getByTestId('withdrawn-live')).toBeVisible();
    const server = await progress(p, sid);
    expect(server.withdrawn_ids).toContain(q[1].id);
    expect(
        server.answers[q[1].id],
        'withdrawn answer not saved',
    ).toBeUndefined();
    expect(server.answers[q[0].id]).toBe(1);
});

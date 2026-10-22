// Strict mock browser <-> server checks (headless Chrome, local app, SQLite).
// See tests/E2E/README.md for setup. Exits non-zero on the first failure.
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';

const BASE = process.env.BASE_URL ?? 'http://127.0.0.1:8123';
const APP = process.env.APP_DIR ?? process.cwd();
const log = (...a) => console.log('[e2e]', ...a);
const browser = await chromium.launch({
    executablePath: process.env.CHROME ?? '/usr/bin/google-chrome',
    headless: true,
});

/** Run PHP against the same SQLite DB the server uses (test setup only). */
const php = (code) =>
    execFileSync('php', ['artisan', 'tinker', '--execute', code], {
        cwd: APP,
        env: process.env,
        encoding: 'utf8',
    }).trim();
const isProgress = (r) => r.url().endsWith('/exams/sessions/progress');

async function page(ctx) {
    const p = await ctx.newPage();
    p.on(
        'console',
        (m) =>
            m.type() === 'error' &&
            !/INTERNET_DISCONNECTED|409|422/.test(m.text()) &&
            log('console error', m.text().slice(0, 160)),
    );
    return p;
}
async function toasts(p) {
    return p.locator('[data-sonner-toast]').allInnerTexts();
}
async function call(p, url, body) {
    return p.evaluate(
        async ([url, body]) => {
            const token =
                document.querySelector('meta[name="csrf-token"]')?.content ??
                '';
            const r = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json',
                    'X-CSRF-TOKEN': token,
                },
                body: JSON.stringify(body),
            });
            return { status: r.status, body: await r.json().catch(() => null) };
        },
        [url, body],
    );
}
const progress = (p, sid) =>
    call(p, '/exams/sessions/progress', { exam_session_id: sid }).then(
        (r) => r.body,
    );
const pending = (p, sid) =>
    p.evaluate(
        (sid) => localStorage.getItem(`civio_strict_pending:${sid}`),
        sid,
    );
const pick = (p, label) =>
    p
        .locator('button', { hasText: new RegExp(`^[A-D]\\s*${label}$`) })
        .first()
        .click();

/** Start a Strict mock in a fresh guest context; returns the page and session. */
async function startStrict() {
    const ctx = await browser.newContext();
    const p = await page(ctx);
    await p.goto(`${BASE}/exams`);
    await p.getByRole('button', { name: 'ACCEPT' }).click();
    await p.getByText('Exam Mode', { exact: true }).click();
    const created = p.waitForResponse(
        (r) =>
            r.url().endsWith('/exams/sessions') &&
            r.request().method() === 'POST',
    );
    await p.getByRole('button', { name: /Begin/ }).first().click();
    const session = await (await created).json();
    assert.equal(session.mode, 'strict');
    for (const q of session.questions) {
        assert.ok(
            !('correct_option' in q) && !('explanation' in q),
            'no key before submit',
        );
    }
    await p
        .locator('button', { hasText: /Bravo$/ })
        .first()
        .waitFor();
    await p.waitForTimeout(500);
    return { ctx, p, sid: session.session_id, q: session.questions };
}
async function answerOnline(p, label, qid, value) {
    const saved = p.waitForResponse(
        (r) =>
            isProgress(r) &&
            (r.request().postData() ?? '').includes(`"${qid}":${value}`),
    );
    await pick(p, label);
    return (await saved).json();
}

const scenarios = {
    async 'offline answer survives closing the tab and reaches the server after reconnect'() {
        const { ctx, sid, q, p: first } = await startStrict();
        let p = first;
        assert.equal(
            (await answerOnline(p, 'Bravo', q[0].id, 1)).answers[q[0].id],
            1,
        );

        await ctx.setOffline(true);
        await p.getByRole('button', { name: 'Next' }).click();
        await pick(p, 'Charlie');
        await p.waitForTimeout(800);
        assert.deepEqual(JSON.parse(await pending(p, sid)), {
            [q[1].id]: [2, null],
        });
        assert.ok(
            (await toasts(p)).some((t) => /Connection lost/.test(t)),
            'offline notice',
        );

        await p.close();
        await ctx.setOffline(false);
        p = await page(ctx);
        const resent = p.waitForResponse(
            (r) =>
                isProgress(r) &&
                (r.request().postData() ?? '').includes(`"${q[1].id}":2`),
            { timeout: 30000 },
        );
        await p.goto(`${BASE}/exams`);
        await p
            .getByText(/Restored 1 answer made while offline/)
            .waitFor({ timeout: 10000 });
        await resent;
        const server = await progress(p, sid);
        assert.equal(server.answers[q[0].id], 1, 'online answer kept');
        assert.equal(
            server.answers[q[1].id],
            2,
            'offline answer saved after reopen',
        );
        assert.equal(await pending(p, sid), null, 'local copy cleared');
        await ctx.close();
    },

    async 'two tabs: a stale tab save re-reads, retries once and keeps both answers'() {
        const { ctx, p: a, sid, q } = await startStrict();
        const b = await page(ctx);
        await b.goto(`${BASE}/exams`); // same browser session: resumes the same mock
        await b
            .locator('button', { hasText: /Bravo$/ })
            .first()
            .waitFor();
        await b.waitForTimeout(800);

        // Tab A saves first (version 0 -> 1). Tab B still holds version 0.
        assert.equal(
            (await answerOnline(a, 'Bravo', q[0].id, 1)).save_version,
            1,
        );
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
        const m = await (await merged).json();
        assert.equal(m.save_version, 2);

        const server = await progress(a, sid);
        assert.equal(server.answers[q[0].id], 1, "tab A's answer survives");
        assert.equal(
            server.answers[q[1].id],
            2,
            "tab B's answer saved after retry",
        );
        await b.waitForTimeout(300);
        assert.ok(
            (await toasts(b)).some((t) => /updated from another tab/.test(t)),
            'merge notice in tab B',
        );
        await ctx.close();
    },

    async 'deadline passes while offline: late answer refused, only saved answers graded'() {
        const { ctx, p, sid, q } = await startStrict();
        await answerOnline(p, 'Bravo', q[0].id, 1);
        php(
            `App\\Models\\ExamSession::whereKey('${sid}')->update(['deadline_at' => now()->addSeconds(4)]);`,
        );

        await ctx.setOffline(true);
        await p.getByRole('button', { name: 'Next' }).click();
        await pick(p, 'Bravo');
        await p.waitForTimeout(5500); // deadline passes while offline
        const refused = p.waitForResponse(
            (r) => isProgress(r) && r.status() === 409,
        );
        await ctx.setOffline(false); // 'online' flush: server refuses the late save
        await refused;
        await p.waitForTimeout(500);
        assert.ok(
            (await toasts(p)).some((t) => /Time is up/.test(t)),
            'deadline notice',
        );
        assert.equal(
            await pending(p, sid),
            null,
            'late answer not kept for resend',
        );

        const server = await progress(p, sid);
        assert.equal(
            server.answers[q[1].id],
            undefined,
            'late answer never saved',
        );
        // Even a final submit carrying the late answer grades saved answers only.
        const res = await call(p, '/exams/attempts', {
            exam_session_id: sid,
            question_ids: q.map((x) => x.id),
            answers: { [q[0].id]: 1, [q[1].id]: 1 },
        });
        assert.equal(res.status, 200);
        assert.equal(res.body.answers[q[1].id], null, 'late answer not graded');
        assert.equal(res.body.answers[q[0].id], 1);
        await ctx.close();
    },

    async 'double submit: exactly one attempt, the second is refused, refresh cannot resume'() {
        const { ctx, p, sid, q } = await startStrict();
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
        log('double submit statuses', statuses.join(','));
        assert.equal(
            statuses.filter((s) => s === 200).length,
            1,
            'exactly one accepted',
        );
        assert.ok(
            [409, 429].includes(statuses.find((s) => s !== 200)),
            'second refused',
        );
        assert.equal(
            Number(
                php(
                    `echo App\\Models\\ExamAttempt::whereIn('id', App\\Models\\ExamSession::whereKey('${sid}')->pluck('exam_attempt_id'))->count();`,
                )
                    .split('\n')
                    .pop(),
            ),
            1,
        );
        assert.equal(
            (await call(p, '/exams/attempts', payload)).status,
            409,
            'a later retry is refused too',
        );
        assert.equal(
            (
                await call(p, '/exams/sessions/progress', {
                    exam_session_id: sid,
                    expected_version: 1,
                    answers: { [q[1].id]: 0 },
                })
            ).status,
            409,
            'no saves after submit',
        );

        // Refresh after submit: the page must not resume the completed mock.
        await p.reload();
        await p.waitForTimeout(2500);
        assert.equal(
            await p.getByRole('button', { name: 'Next' }).count(),
            0,
            'exam screen not resumed',
        );
        assert.equal(
            await p.evaluate(() =>
                localStorage.getItem('active_exam_session_v1'),
            ),
            null,
            'local resume copy cleared',
        );
        await ctx.close();
    },
};

let failed = 0;
for (const [name, run] of Object.entries(scenarios)) {
    try {
        await run();
        log('PASS', name);
    } catch (error) {
        failed++;
        log('FAIL', name, '\n', error?.stack ?? error);
    }
}
await browser.close();
log(failed === 0 ? 'ALL PASS' : `${failed} FAILED`);
process.exit(failed === 0 ? 0 : 1);

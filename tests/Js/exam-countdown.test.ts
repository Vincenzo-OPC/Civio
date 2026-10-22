import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { afterEach, beforeEach, describe, it, mock } from 'node:test';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import {
    examCountdown,
    formatPhDate,
    milestoneText,
    nextMilestone,
    phMidnightMs,
    readTrack,
} from '../../resources/js/lib/exam-countdown';
import type {
    ExamMilestone,
    ExamSitting,
} from '../../resources/js/lib/exam-countdown';

const MARCH: ExamSitting = {
    date: '2027-03-14',
    sitting: '14 March 2027 CSE-PPT',
    label: 'Exam day (Professional and Subprofessional)',
};
const AUGUST: ExamSitting = {
    date: '2027-08-08',
    sitting: '08 August 2027 CSE-PPT',
    label: 'Exam day (Professional and Subprofessional)',
};
const SITTINGS = [MARCH, AUGUST];
const MILESTONES: ExamMilestone[] = [
    { ...MARCH, date: '2026-11-02', label: 'Filing opens', kind: 'filing_opens' },
    { ...MARCH, kind: 'exam_day' },
    { ...AUGUST, date: '2027-05-10', label: 'Filing opens', kind: 'filing_opens' },
    { ...AUGUST, kind: 'exam_day' },
];

const at = (iso: string) => Date.parse(iso);

describe('exam countdown target is 00:00 Philippine time', () => {
    it('March 14 2027 starts at 2027-03-13T16:00Z', () => {
        assert.equal(phMidnightMs('2027-03-14'), at('2027-03-13T16:00:00Z'));
    });

    it('counts the March sitting from Oct 22 2026, 20:30 PHT', () => {
        const s = examCountdown(SITTINGS, at('2026-10-22T20:30:00+08:00'));
        assert.equal(s.phase, 'counting');
        assert.ok(s.phase === 'counting');
        assert.equal(s.sitting.date, '2027-03-14');
        assert.deepEqual(s.parts, { days: 142, hours: 3, minutes: 30, seconds: 0 });
    });

    it('does not depend on the browser timezone (America/Los_Angeles)', () => {
        const prev = process.env.TZ;
        process.env.TZ = 'America/Los_Angeles';
        try {
            const now = at('2027-03-13T15:59:59Z');
            const s = examCountdown(SITTINGS, now);
            assert.ok(s.phase === 'counting');
            assert.deepEqual(s.parts, { days: 0, hours: 0, minutes: 0, seconds: 1 });
            assert.equal(formatPhDate('2027-03-14'), 'March 14, 2027');
        } finally {
            process.env.TZ = prev;
        }
    });
});

describe('midnight and exam-day rollover', () => {
    it('flips to Exam Day Today at PH midnight', () => {
        const s = examCountdown(SITTINGS, at('2027-03-14T00:00:00+08:00'));
        assert.equal(s.phase, 'today');
    });

    it('stays Exam Day Today until 23:59:59 PHT', () => {
        const s = examCountdown(SITTINGS, at('2027-03-14T23:59:59+08:00'));
        assert.equal(s.phase, 'today');
    });

    it('moves to the August sitting when the PH exam day ends', () => {
        const s = examCountdown(SITTINGS, at('2027-03-15T00:00:00+08:00'));
        assert.ok(s.phase === 'counting');
        assert.equal(s.sitting.date, '2027-08-08');
    });

    it('shows no countdown after the last confirmed sitting', () => {
        assert.equal(
            examCountdown(SITTINGS, at('2027-08-09T00:00:00+08:00')).phase,
            'none',
        );
        assert.equal(examCountdown([], Date.now()).phase, 'none');
    });
});

describe('milestones', () => {
    it('walks Nov 2 -> Mar 14 -> May 10 -> Aug 8 in PH days', () => {
        const pick = (iso: string) => nextMilestone(MILESTONES, at(iso));
        assert.equal(pick('2026-10-22T12:00:00+08:00')?.date, '2026-11-02');
        assert.equal(milestoneText(pick('2026-10-22T12:00:00+08:00')!), 'March CSE registration opens');
        assert.equal(pick('2026-11-03T00:00:00+08:00')?.date, '2027-03-14');
        assert.equal(pick('2027-03-15T00:00:00+08:00')?.date, '2027-05-10');
        assert.equal(milestoneText(pick('2027-03-15T00:00:00+08:00')!), 'August CSE registration opens');
        assert.equal(pick('2027-05-11T00:00:00+08:00')?.date, '2027-08-08');
        assert.equal(pick('2027-08-09T00:00:00+08:00'), null);
    });
});

describe('Professional / Subprofessional selection', () => {
    it('defaults to Professional and accepts Subprofessional', () => {
        assert.equal(readTrack(null), 'professional');
        assert.equal(readTrack('junk'), 'professional');
        assert.equal(readTrack('subprofessional'), 'subprofessional');
    });
});

describe('ExamCountdown component', async () => {
    const { ExamCountdown } = await import(
        '../../resources/js/pages/user/dashboard/components/exam-countdown'
    );
    const render = (now: string, sittings = SITTINGS) =>
        renderToStaticMarkup(
            createElement(ExamCountdown, {
                sittings,
                milestones: MILESTONES,
                sourceUrl: 'https://csc.gov.ph/x',
                source: 'csc',
                initialNow: at(now),
            }),
        );

    it('renders days, hours, minutes, seconds, date, track picker and milestone', () => {
        const html = render('2026-10-22T20:30:00+08:00');
        for (const unit of ['Days', 'Hours', 'Mins', 'Secs']) {
            assert.match(html, new RegExp(`data-unit="${unit}"`));
        }
        assert.match(html, /Until exam day/);
        assert.doesNotMatch(html, /Until exam starts/);
        assert.match(html, /March 14, 2027/);
        assert.match(html, /role="radio" aria-checked="true"[^>]*>Professional/);
        assert.match(html, />Subprofessional</);
        assert.match(html, /November 2, 2026 · March CSE registration opens/);
        assert.doesNotMatch(html, /November 22/);
    });

    it('says Exam Day Today on exam day and has no ticking digits', () => {
        const html = render('2027-03-14T09:00:00+08:00');
        assert.match(html, /Exam Day Today/);
        assert.doesNotMatch(html, /data-unit=/);
    });

    it('handles no confirmed future exam', () => {
        const html = render('2027-08-10T00:00:00+08:00');
        assert.match(html, /No confirmed CSC exam date yet/);
    });

    it('stays readable on mobile: four-column grid, no fixed widths below sm', () => {
        const html = render('2026-10-22T20:30:00+08:00');
        assert.match(html, /grid grid-cols-4/);
        assert.match(html, /text-2xl/);
        assert.doesNotMatch(html, /\bw-\[\d+px\]/);
    });
});

describe('countdown updates without reload', () => {
    beforeEach(() => mock.timers.enable({ apis: ['setInterval', 'Date'], now: at('2026-10-22T20:30:00+08:00') }));
    afterEach(() => mock.timers.reset());

    it('the component ticks once a second via setInterval', () => {
        const src = readFileSync(
            new URL('../../resources/js/pages/user/dashboard/components/exam-countdown.tsx', import.meta.url),
            'utf8',
        );
        assert.match(src, /setInterval\(\(\) => setNow\(Date\.now\(\)\), 1000\)/);
        assert.doesNotMatch(src, /T00:00:00`\)/);

        let now = Date.now();
        const id = setInterval(() => (now = Date.now()), 1000);
        const before = examCountdown(SITTINGS, now);
        mock.timers.tick(3000);
        const after = examCountdown(SITTINGS, now);
        clearInterval(id);
        assert.ok(before.phase === 'counting' && after.phase === 'counting');
        assert.equal(before.parts.seconds, 0);
        assert.equal(after.parts.seconds, 57);
    });
});

describe('dashboard layout', () => {
    const page = readFileSync(
        new URL('../../resources/js/pages/user/dashboard/index.tsx', import.meta.url),
        'utf8',
    );
    it('renders DailyGoalStreakCard, SmartStudyLaunchers and ExamCountdown once each', () => {
        assert.equal(page.match(/<DailyGoalStreakCard\b/g)?.length, 1);
        assert.equal(page.match(/<SmartStudyLaunchers\b/g)?.length, 1);
        assert.equal(page.match(/<ExamCountdown\b/g)?.length, 1);
    });
    it('the hero no longer shows a days-only exam date', () => {
        const hero = readFileSync(
            new URL('../../resources/js/pages/user/dashboard/components/dashboard-hero.tsx', import.meta.url),
            'utf8',
        );
        assert.doesNotMatch(hero, /days left/);
    });
});

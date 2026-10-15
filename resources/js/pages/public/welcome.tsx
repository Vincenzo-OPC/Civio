import { Head, Link, router, usePage } from '@inertiajs/react';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';
import type { Auth } from '@/types';

const SAMPLE = {
    stem: 'Which sentence is clearest?',
    options: [
        'The report was finished by the clerk before noon.',
        'The clerk finished the report before noon.',
        'Before noon, it was the report that the clerk finished.',
        'Finished was the report, by the clerk, before noon.',
    ],
};

export default function Welcome() {
    const { auth } = usePage<{ auth: Auth }>().props;

    const startExam = (track: 'professional' | 'subprofessional') => {
        const guest = auth?.user ? '' : '&free_attempt=1';
        router.visit(`/exams?start=${track}${guest}`);
    };

    return (
        <>
            <Head title="Prepare for the Civil Service Exam">
                <meta
                    name="description"
                    content="Practice Civil Service Exam questions with timed mocks and explanations. Civio is an independent reviewer, not the Civil Service Commission."
                />
            </Head>
            <SiteHeader activeNav="home" />
            <main className="bg-[var(--civio-paper,#fafaf7)] text-[var(--civio-ink,#101426)]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-12">
                    <header className="flex flex-col gap-3">
                        <h1 className="font-heading text-3xl font-semibold tracking-tight sm:text-5xl">
                            Prepare for the Civil Service Exam.
                        </h1>
                        <p className="text-base leading-relaxed text-[var(--civio-ink,#101426)]/75 sm:text-lg">
                            Timed mocks for the Professional and Subprofessional
                            exams. The explanation comes after you answer.
                        </p>
                    </header>

                    <div className="grid gap-3 sm:grid-cols-3">
                        <button
                            type="button"
                            onClick={() => startExam('professional')}
                            className="rounded-xl bg-[var(--civio-violet,#5b35f5)] px-4 py-4 text-left text-white"
                        >
                            <span className="block text-sm font-semibold">
                                Start Pro
                            </span>
                            <span className="mt-1 block text-xs text-white/80">
                                150 items · 3h 10m
                            </span>
                        </button>
                        <button
                            type="button"
                            onClick={() => startExam('subprofessional')}
                            className="rounded-xl border border-[var(--civio-line,#e3e5ea)] bg-white px-4 py-4 text-left dark:bg-transparent"
                        >
                            <span className="block text-sm font-semibold">
                                Start Sub Pro
                            </span>
                            <span className="mt-1 block text-xs opacity-70">
                                145 items · 2h 40m
                            </span>
                        </button>
                        <Link
                            href="/exams"
                            className="rounded-xl border border-[var(--civio-line,#e3e5ea)] bg-white px-4 py-4 text-left dark:bg-transparent"
                        >
                            <span className="block text-sm font-semibold">
                                Continue Studying
                            </span>
                            <span className="mt-1 block text-xs opacity-70">
                                Resume a mock or open the exam setup
                            </span>
                        </Link>
                    </div>

                    <p className="text-sm">
                        <Link
                            href="/drills"
                            className="font-semibold text-[var(--civio-violet,#5b35f5)] underline-offset-4 hover:underline"
                        >
                            Practice Drills
                        </Link>
                        <span className="mx-2 opacity-40">·</span>
                        <Link
                            href="/learn"
                            className="font-semibold underline-offset-4 hover:underline"
                        >
                            Study Hub
                        </Link>
                    </p>

                    <section
                        aria-label="Question interface preview"
                        className="rounded-2xl border border-[var(--civio-line,#e3e5ea)] bg-white p-4 sm:p-6 dark:bg-transparent"
                    >
                        <p className="text-xs font-semibold tracking-wide opacity-60">
                            Interface preview · not a scored item
                        </p>
                        <p className="mt-3 text-lg leading-relaxed">
                            {SAMPLE.stem}
                        </p>
                        <div className="mt-4 flex flex-col" role="list">
                            {SAMPLE.options.map((option, index) => (
                                <div
                                    key={option}
                                    role="listitem"
                                    className={`flex min-h-12 items-start gap-3 border-b border-[var(--civio-line,#e3e5ea)] py-3 ${
                                        index === 1
                                            ? 'text-[var(--civio-violet,#5b35f5)]'
                                            : ''
                                    }`}
                                >
                                    <span
                                        className={`flex size-7 shrink-0 items-center justify-center border text-xs font-bold ${
                                            index === 1
                                                ? 'border-[var(--civio-violet,#5b35f5)] bg-[var(--civio-violet,#5b35f5)] text-white'
                                                : 'border-[var(--civio-line,#e3e5ea)]'
                                        }`}
                                    >
                                        {String.fromCharCode(65 + index)}
                                    </span>
                                    <span className="text-base leading-relaxed">
                                        {option}
                                        {index === 1 && (
                                            <span className="mt-1 block text-xs font-semibold">
                                                Selected
                                            </span>
                                        )}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </section>

                    <section className="grid gap-4 text-sm leading-relaxed sm:grid-cols-2">
                        <p>
                            <strong className="font-semibold">
                                Professional.
                            </strong>{' '}
                            150 scored items, 3 hours 10 minutes. For
                            professional, technical, and supervisory posts.
                        </p>
                        <p>
                            <strong className="font-semibold">
                                Subprofessional.
                            </strong>{' '}
                            145 scored items, 2 hours 40 minutes. For clerical,
                            trades, and custodial posts.
                        </p>
                    </section>

                    <p className="text-xs leading-relaxed opacity-70">
                        The published general passing rating is at least 80.00.
                        Civio is not the Civil Service Commission and is not an
                        official CSC reviewer. Practice scores are not a
                        prediction of your exam result.
                    </p>
                </div>
            </main>
            <SiteFooter />
        </>
    );
}

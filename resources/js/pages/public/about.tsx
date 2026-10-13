import { Head, Link } from '@inertiajs/react';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';

export default function About() {
    return (
        <>
            <Head title="About">
                <meta
                    name="description"
                    content="Civio is an independent study app for the Philippine Civil Service Exam. It is not the Civil Service Commission."
                />
            </Head>
            <SiteHeader activeNav="about" />
            <main className="bg-[var(--civio-paper,#fafaf7)] text-[var(--civio-ink,#101426)]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-12">
                    <header className="flex flex-col gap-3">
                        <p className="text-sm font-semibold text-[var(--civio-violet,#5b35f5)]">
                            Civio
                        </p>
                        <h1 className="font-heading text-3xl font-semibold tracking-tight sm:text-4xl">
                            A study app. Not the Commission.
                        </h1>
                        <p className="text-base leading-relaxed text-[var(--civio-ink,#101426)]/75 sm:text-lg">
                            Civio is for people preparing for the Philippine
                            Civil Service Exam. It is not affiliated with,
                            endorsed by, or connected to the Civil Service
                            Commission.
                        </p>
                    </header>

                    <section className="grid gap-4 text-sm leading-relaxed sm:grid-cols-2">
                        <p>
                            <strong className="font-semibold">
                                Professional.
                            </strong>{' '}
                            150 scored items, 3 hours 10 minutes.
                        </p>
                        <p>
                            <strong className="font-semibold">
                                Subprofessional.
                            </strong>{' '}
                            145 scored items, 2 hours 40 minutes.
                        </p>
                    </section>

                    <section className="flex flex-col gap-3 text-sm leading-relaxed">
                        <p>
                            The published general passing rating is at least
                            80.00. CSC does not publish a separate minimum for
                            each subtest. A practice score is not a prediction
                            of your result.
                        </p>
                        <p>
                            You can study without an account. Dexter is the
                            tutor in the app. He checks an item against its
                            stored key. He does not speak for the Commission.
                        </p>
                        <p>
                            The questions are written for practice. They are not
                            past CSC papers, and none of them carry an official
                            source badge.
                        </p>
                    </section>

                    <p className="text-sm">
                        <Link
                            href="/exams?start=professional&free_attempt=1"
                            className="font-semibold text-[var(--civio-violet,#5b35f5)] underline-offset-4 hover:underline"
                        >
                            Start Pro
                        </Link>
                        <span className="mx-2 opacity-40">·</span>
                        <Link
                            href="/exams?start=subprofessional&free_attempt=1"
                            className="font-semibold underline-offset-4 hover:underline"
                        >
                            Start Sub Pro
                        </Link>
                        <span className="mx-2 opacity-40">·</span>
                        <Link
                            href="/guide"
                            className="font-semibold underline-offset-4 hover:underline"
                        >
                            Exam guide
                        </Link>
                    </p>
                </div>
            </main>
            <SiteFooter />
        </>
    );
}

About.layout = undefined;

import { Head, Link } from '@inertiajs/react';
import ExamFormat from '@/components/domain/exam-format';
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
            <main className="bg-[#FAFAF7] text-[#101426] dark:bg-[#101426] dark:text-[#FAFAF7]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-12">
                    <header className="flex flex-col gap-3">
                        <p className="text-sm font-semibold text-[#5B35F5] dark:text-[#C4B6FF]">
                            Civio
                        </p>
                        <h1 className="font-heading text-3xl font-semibold tracking-tight sm:text-4xl">
                            A study app. Not the Commission.
                        </h1>
                        <p className="text-base leading-relaxed opacity-75 sm:text-lg">
                            Civio is for people preparing for the Philippine
                            Civil Service Exam. It is not affiliated with,
                            endorsed by, or connected to the Civil Service
                            Commission.
                        </p>
                    </header>

                    <ExamFormat />

                    <section className="flex flex-col gap-3 text-sm leading-relaxed">
                        <h2 className="font-heading text-xl font-semibold tracking-tight">
                            How an Explanation Is Chosen
                        </h2>
                        <p>
                            Show Explanation does not call a chat model. If a
                            rule can recompute the item, and that result is the
                            stored answer, Civio teaches from the rule. If not,
                            it shows the explanation already saved on the
                            question.
                        </p>
                        <p>
                            Step-by-Step, Exam Tip, Common Mistake, and Diagram
                            appear only when that part exists. Copy Question and
                            Ask send the item out. They do not grade it. A
                            Exam Mode hides all of these until you submit.
                        </p>
                    </section>

                    <section className="flex flex-col gap-3 text-sm leading-relaxed">
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
                            className="font-semibold text-[#5B35F5] underline-offset-4 hover:underline dark:text-[#C4B6FF]"
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

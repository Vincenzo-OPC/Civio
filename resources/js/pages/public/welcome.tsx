import { Head, Link, router, usePage } from '@inertiajs/react';
import { useState } from 'react';
import ExamFormat from '@/components/domain/exam-format';
import { ExamLevelPicker } from '@/components/domain/exam-level-picker';
import { ExamScreenPreview } from '@/components/domain/exam-screen-preview';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';
import type { ExamDialId } from '@/lib/exam-dials';
import type { Auth } from '@/types';

export default function Welcome() {
    const { auth } = usePage<{ auth: Auth }>().props;
    const [level, setLevel] = useState<ExamDialId>('professional');

    const startExam = () => {
        const guest = auth?.user ? '' : '&free_attempt=1';
        router.visit(`/exams?start=${level}${guest}`);
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
            <main className="bg-[#FAFAF7] text-[#101426] dark:bg-[#101426] dark:text-[#FAFAF7]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-12">
                    <header className="flex flex-col gap-2">
                        <h1 className="font-heading text-3xl font-semibold tracking-tight sm:text-5xl">
                            Choose Your Exam
                        </h1>
                        <p className="max-w-[32rem] text-base leading-relaxed opacity-75 sm:text-lg">
                            A full mock. The explanation comes after you answer.
                        </p>
                    </header>

                    <ExamLevelPicker value={level} onChange={setLevel} />

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                        <button
                            type="button"
                            onClick={startExam}
                            className="inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-[#5B35F5] px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-[#4a2ad4] focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAFAF7] focus-visible:outline-none sm:w-auto dark:focus-visible:ring-offset-[#101426]"
                        >
                            Set Up Mock Exam
                        </button>
                        <Link
                            href="/exams"
                            className="inline-flex min-h-11 w-full items-center justify-center rounded-xl border-2 border-[#E3E5EA] bg-white px-5 py-3 text-sm font-semibold transition-colors hover:border-[#5B35F5]/40 focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAFAF7] focus-visible:outline-none sm:w-auto dark:border-[#2c3148] dark:bg-transparent dark:hover:border-[#A594FF]/50 dark:focus-visible:ring-[#A594FF] dark:focus-visible:ring-offset-[#101426]"
                        >
                            Continue Studying
                        </Link>
                    </div>

                    <p className="text-sm">
                        <Link
                            href="/drills"
                            className="font-semibold text-[#5B35F5] underline-offset-4 hover:underline dark:text-[#C4B6FF]"
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

                    <ExamScreenPreview />

                    <ExamFormat />
                </div>
            </main>
            <SiteFooter />
        </>
    );
}

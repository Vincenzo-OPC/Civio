import { Head, Link, router, usePage } from '@inertiajs/react';
import { BookOpen, Target, Timer } from 'lucide-react';
import { useState } from 'react';
import ExamFormat from '@/components/domain/exam-format';
import { ExamLevelPicker } from '@/components/domain/exam-level-picker';
import { ExamScreenPreview } from '@/components/domain/exam-screen-preview';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';
import { EXAM_DIALS } from '@/lib/exam-dials';
import type { ExamDialId } from '@/lib/exam-dials';
import type { Auth } from '@/types';

const MODES = [
    {
        name: 'Study Mode',
        description:
            'Practice at your own pace with instant feedback and detailed explanations.',
        href: '/exams',
        icon: BookOpen,
    },
    {
        name: 'Exam Mode',
        description:
            'Experience a timed mock exam with answers and results revealed after submission.',
        href: '/exams',
        icon: Timer,
    },
    {
        name: 'Practice Drills',
        description:
            'Strengthen specific skills with focused practice by subject and topic.',
        href: '/drills',
        icon: Target,
    },
] as const;

export default function Welcome() {
    const { auth } = usePage<{ auth: Auth }>().props;
    const [level, setLevel] = useState<ExamDialId>('professional');
    const name = EXAM_DIALS[level].name;

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
            <div className="civio-glass-stage">
                <div className="civio-glass-wash" aria-hidden />
                <div className="relative">
                    <SiteHeader activeNav="home" />
                    <main>
                        <div className="mx-auto flex w-full max-w-3xl flex-col gap-10 px-4 py-8 sm:px-6 sm:py-12">
                            <header
                                id="choose-exam"
                                className="civio-rise flex flex-col gap-3"
                            >
                                <p className="text-xs font-semibold tracking-[0.18em] text-[#5B35F5] dark:text-[#B3F52D]">
                                    PHILIPPINE CIVIL SERVICE EXAM
                                </p>
                                <h1 className="font-heading text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
                                    Choose Your Exam.
                                </h1>
                                <p className="max-w-2xl text-sm leading-relaxed text-[#101426]/75 sm:text-base dark:text-[#FAFAF7]/75">
                                    Civio: An independent platform helping
                                    Filipinos prepare for public service through
                                    accessible, reliable Civil Service Exam
                                    education.
                                </p>
                            </header>

                            <ExamLevelPicker
                                value={level}
                                onChange={setLevel}
                            />

                            <div
                                className="civio-rise flex flex-col gap-3 sm:flex-row sm:items-center"
                                style={{ animationDelay: '180ms' }}
                            >
                                <button
                                    type="button"
                                    onClick={startExam}
                                    className="inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-[#5B35F5] px-5 py-3 text-sm font-semibold text-white transition-[transform,background-color,filter] duration-200 hover:bg-[#4a2ad4] focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAFAF7] focus-visible:outline-none active:scale-[0.98] motion-reduce:transform-none sm:w-auto dark:bg-[#B3F52D] dark:text-[#0A0A0A] dark:hover:brightness-95 dark:focus-visible:ring-[#B3F52D] dark:focus-visible:ring-offset-black"
                                >
                                    Continue with {name}
                                </button>
                                <Link
                                    href="/drills"
                                    className="civio-glass inline-flex min-h-11 w-full items-center justify-center rounded-xl border border-white/70 px-5 py-3 text-sm font-semibold transition-colors hover:border-[#5B35F5]/40 focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FAFAF7] focus-visible:outline-none sm:w-auto dark:border-white/10 dark:hover:border-[#B3F52D]/60 dark:focus-visible:ring-[#B3F52D] dark:focus-visible:ring-offset-black"
                                >
                                    Practice by Topic
                                </Link>
                            </div>

                            <section
                                aria-label="Practice Modes"
                                className="flex flex-col gap-4"
                            >
                                <h2 className="font-heading text-xl font-semibold tracking-tight">
                                    Practice Modes
                                </h2>
                                <div className="grid gap-3 sm:grid-cols-3">
                                    {MODES.map((mode) => {
                                        const Icon = mode.icon;

                                        return (
                                            <Link
                                                key={mode.name}
                                                href={
                                                    mode.href === '/drills'
                                                        ? '/drills'
                                                        : mode.name ===
                                                            'Study Mode'
                                                          ? `/exams?start=${level}${auth?.user ? '' : '&free_attempt=1'}`
                                                          : '/exams'
                                                }
                                                className="civio-glass flex flex-col gap-3 rounded-2xl border border-white/70 p-4 transition-[transform,border-color,box-shadow] duration-200 hover:-translate-y-0.5 hover:border-[#5B35F5]/40 hover:shadow-sm focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:outline-none motion-reduce:transform-none dark:border-white/10 dark:hover:border-[#B3F52D]/60"
                                            >
                                                <Icon
                                                    className="size-5 text-[#5B35F5] dark:text-[#B3F52D]"
                                                    aria-hidden
                                                />
                                                <span className="font-heading text-base font-semibold tracking-tight">
                                                    {mode.name}
                                                </span>
                                                <span className="text-sm leading-relaxed text-[#101426]/75 dark:text-[#FAFAF7]/75">
                                                    {mode.description}
                                                </span>
                                            </Link>
                                        );
                                    })}
                                </div>
                            </section>

                            <section
                                aria-label="How Civio Helps"
                                className="flex flex-col gap-3"
                            >
                                <h2 className="font-heading text-xl font-semibold tracking-tight">
                                    How Civio Helps
                                </h2>
                                <ul className="flex flex-col gap-3 text-sm leading-relaxed text-[#101426]/80 dark:text-[#FAFAF7]/80">
                                    <li>
                                        <span className="font-semibold text-[#101426] dark:text-[#FAFAF7]">
                                            Practice.
                                        </span>{' '}
                                        Full mocks and focused drills for
                                        Professional and Subprofessional.
                                    </li>
                                    <li>
                                        <span className="font-semibold text-[#101426] dark:text-[#FAFAF7]">
                                            Learn.
                                        </span>{' '}
                                        An explanation after you answer, and a
                                        list of questions you missed.
                                    </li>
                                    <li>
                                        <span className="font-semibold text-[#101426] dark:text-[#FAFAF7]">
                                            Improve.
                                        </span>{' '}
                                        Saved progress and your practice
                                        history. Smart Review reminds a
                                        signed-in learner to try a missed
                                        question again.
                                    </li>
                                    <li>
                                        <span className="font-semibold text-[#101426] dark:text-[#FAFAF7]">
                                            Study anywhere.
                                        </span>{' '}
                                        A lighter layout on a slow connection,
                                        and offline drills for selected topics.
                                    </li>
                                </ul>
                                <p className="text-sm leading-relaxed text-[#101426]/70 dark:text-[#FAFAF7]/70">
                                    Civio is not the Civil Service Commission. A
                                    practice score is not your exam result.
                                    Smart Review needs a connection.
                                </p>
                            </section>

                            <ExamScreenPreview />

                            <ExamFormat />
                        </div>
                    </main>
                    <SiteFooter />
                </div>
            </div>
        </>
    );
}

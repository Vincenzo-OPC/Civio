import { Head } from '@inertiajs/react';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';

const CSC_ANNOUNCEMENTS =
    'https://www.csc.gov.ph/examination-advisories/examination-announcement-no-05-s-2026-calendar-of-civil-service-examinations-pen-and-paper-test-for-cy-2027';

const CHECKLIST = [
    'Your Notice of School Assignment or room assignment, if the CSC advisory asks for it.',
    'A valid ID that matches the name on your application.',
    'The writing materials the advisory names (usually pencils, an eraser and a black ballpen).',
    'Clothing that follows the dress code in the advisory.',
    'Water and a light snack. Leave your phone and calculator outside the room as instructed.',
    'Leave early. Plan to arrive well before the reporting time.',
];

export default function ExamDay() {
    return (
        <>
            <Head title="Exam-day guide">
                <meta
                    name="description"
                    content="A short exam-day checklist for the Civil Service Exam pen-and-paper test, with links to the official CSC announcements."
                />
            </Head>
            <SiteHeader activeNav="exam-day" />
            <main className="bg-[#FAFAF7] text-[#101426] dark:bg-black dark:text-[#FAFAF7]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 sm:px-6 sm:py-12">
                    <h1 className="font-heading text-3xl font-semibold tracking-tight">
                        Exam-day guide
                    </h1>
                    <p className="text-base leading-relaxed opacity-75">
                        Civio is not the Civil Service Commission. The official
                        rules are in the CSC examination announcement and the
                        exam advisory, which CSC posts about two weeks before
                        exam day. Always follow those over this page.
                    </p>
                    <p className="text-base">
                        <a
                            href={CSC_ANNOUNCEMENTS}
                            className="font-semibold underline"
                            rel="noopener noreferrer"
                            target="_blank"
                        >
                            CSC exam calendar for 2027 (csc.gov.ph)
                        </a>{' '}
                        ·{' '}
                        <a
                            href="https://www.csc.gov.ph/"
                            className="font-semibold underline"
                            rel="noopener noreferrer"
                            target="_blank"
                        >
                            csc.gov.ph
                        </a>
                    </p>
                    <section className="flex flex-col gap-2">
                        <h2 className="text-xl font-semibold">Bring and do</h2>
                        <ul className="list-disc pl-5 leading-relaxed">
                            {CHECKLIST.map((item) => (
                                <li key={item}>{item}</li>
                            ))}
                        </ul>
                    </section>
                    <section className="flex flex-col gap-2">
                        <h2 className="text-xl font-semibold">
                            During the test
                        </h2>
                        <ul className="list-disc pl-5 leading-relaxed">
                            <li>
                                Answer what you know first, mark hard items,
                                then return.
                            </li>
                            <li>
                                Check every 10 items that your answer-sheet
                                number matches the question.
                            </li>
                            <li>
                                Shade answers fully and erase changes cleanly.
                            </li>
                            <li>
                                Listen to the proctor&apos;s instructions on
                                time limits and guessing.
                            </li>
                        </ul>
                    </section>
                    <p className="text-sm opacity-60">
                        Links checked 22 October 2026.
                    </p>
                </div>
            </main>
            <SiteFooter />
        </>
    );
}

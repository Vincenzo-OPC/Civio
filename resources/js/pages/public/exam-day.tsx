import { Head } from '@inertiajs/react';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';

const ANN_03 =
    'https://www.csc.gov.ph/examination-advisories/examination-announcement-no-03-s-2026-conduct-of-career-service-examination-pen-and-paper-test-cse-ppt-for-professional-and-subprofessional-levels-09-august-2026';
const ANN_05 =
    'https://www.csc.gov.ph/examination-advisories/examination-announcement-no-05-s-2026-calendar-of-civil-service-examinations-pen-and-paper-test-for-cy-2027';

/** Each fact is tied to the CSC source it came from. */
const SECTIONS: {
    title: string;
    items: string[];
    source: 'ann03' | 'ann05';
}[] = [
    {
        title: 'Dates for 2027',
        source: 'ann05',
        items: [
            'CSE Professional and Subprofessional (pen and paper): 14 March 2027. Filing opens 2 November 2026 and continues until slots are filled or CSC says otherwise.',
            'Second 2027 exam: 8 August 2027, with filing from 10 May 2027.',
            'Target release of the March results: 11 May 2027. CSC posts the detailed announcement about 3 weeks before filing opens and an advisory about 2 weeks before exam day.',
        ],
    },
    {
        title: 'Who may apply',
        source: 'ann03',
        items: [
            'Filipino citizen, at least 18 years old on the date of filing, of good moral character.',
            'Not convicted by final judgment of the offenses CSC lists, and not dishonorably discharged or dismissed for cause from government service.',
            'Has not taken the same level within 3 months before the exam date, and has not already passed that level.',
        ],
    },
    {
        title: 'What to file',
        source: 'ann03',
        items: [
            'Application Form (CS Form No. 100, Revised 2023) for your level, from a CSC office or csc.gov.ph.',
            'Four identical passport-size colored ID photos (white background, taken within 3 months, hand-held name tag with handwritten signature over printed name). Read the full photo rules in the announcement.',
            'Original and photocopy of an accepted ID (for example PhilID/ePhilID, passport, driver’s license, UMID, voter’s ID, PRC, postal, school or company ID; the full list is in the announcement).',
            'Examination fee of PhP 500.00 (2026 announcement; confirm in the March 2027 announcement).',
            'Filing is through CSC eServe, OCSEAS or a CSC office, depending on the region. Ask the CSC Regional or Field Office where you will take the exam.',
        ],
    },
    {
        title: 'What the Subprofessional test covers',
        source: 'ann03',
        items: [
            'General Information (English): Philippine Constitution; R.A. 6713; peace and human rights; environment management and protection.',
            'Verbal Ability (English and Filipino): word meaning, sentence completion, error recognition, sentence structure, paragraph organization, reading comprehension.',
            'Numerical Ability: basic operations, number sequence, word problems.',
            'Clerical Ability: filing and spelling. (Analytical Ability is in the Professional test only.)',
            'Passing grade: a general rating of at least 80.00.',
        ],
    },
    {
        title: 'Not allowed at your seat or on you',
        source: 'ann03',
        items: [
            'Calculators of any kind, including watch calculators.',
            'Phones, smart watches, camera pens or glasses, and any other gadget or recording device.',
            'Books, dictionaries or any printed material.',
            'Scratch work on any loose paper, your skin or your clothing.',
            'Photos or videos of the test booklet, answer sheet, other examinees or the room, before, during or after the exam, and posting any test question.',
            'Tearing pages, copying questions or answers, comparing answers, crib sheets, or taking the booklet or answer sheet out of the room.',
            'Breaking these rules cancels your exam and may be punished under R.A. 9416, the Anti-Cheating Law.',
        ],
    },
    {
        title: 'Results',
        source: 'ann03',
        items: [
            'Only the List of Passers on the CSC website is official. Individual ratings are generated through OCSERGS on csc.gov.ph.',
        ],
    },
];

const SOURCE_LABEL = {
    ann03: {
        href: ANN_03,
        label: 'CSC Examination Announcement No. 03, s. 2026',
    },
    ann05: {
        href: ANN_05,
        label: 'CSC Examination Announcement No. 05, s. 2026',
    },
} as const;

export default function ExamDay() {
    return (
        <>
            <Head title="Exam-day guide">
                <meta
                    name="description"
                    content="Civil Service Exam pen-and-paper guide: 2027 dates, who may apply, what to file, scope, prohibited items and results, each cited to the official CSC announcement."
                />
            </Head>
            <SiteHeader activeNav="exam-day" />
            <main className="bg-[#FAFAF7] text-[#101426] dark:bg-black dark:text-[#FAFAF7]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 sm:px-6 sm:py-12">
                    <h1 className="font-heading text-3xl font-semibold tracking-tight">
                        Exam-day guide
                    </h1>
                    <p className="text-base leading-relaxed opacity-75">
                        Civio is not the Civil Service Commission. This page
                        summarizes CSC&apos;s own announcements. The March 2027
                        announcement and exam advisory were not out yet when
                        this page was written, so some details come from the
                        August 2026 announcement. If anything differs, the CSC
                        announcement wins.
                    </p>
                    {SECTIONS.map((section) => (
                        <section
                            key={section.title}
                            className="flex flex-col gap-2"
                        >
                            <h2 className="text-xl font-semibold">
                                {section.title}
                            </h2>
                            <ul className="list-disc pl-5 leading-relaxed">
                                {section.items.map((item) => (
                                    <li key={item}>{item}</li>
                                ))}
                            </ul>
                            <p className="text-sm opacity-70">
                                Source:{' '}
                                <a
                                    href={SOURCE_LABEL[section.source].href}
                                    className="underline"
                                    rel="noopener noreferrer"
                                    target="_blank"
                                >
                                    {SOURCE_LABEL[section.source].label}
                                </a>
                            </p>
                        </section>
                    ))}
                    <section className="flex flex-col gap-2">
                        <h2 className="text-xl font-semibold">
                            On the day (study tips, not CSC rules)
                        </h2>
                        <ul className="list-disc pl-5 leading-relaxed">
                            <li>
                                Bring the ID you filed with and anything the
                                exam advisory asks for. Leave early.
                            </li>
                            <li>
                                Answer what you know first, mark hard items,
                                then return.
                            </li>
                            <li>
                                Every 10 items, check that the answer-sheet
                                number matches the question.
                            </li>
                            <li>Follow the proctor&apos;s instructions.</li>
                        </ul>
                    </section>
                    <p className="text-sm opacity-60">
                        Sources checked 22 October 2026 on{' '}
                        <a
                            href="https://www.csc.gov.ph/"
                            className="underline"
                            rel="noopener noreferrer"
                            target="_blank"
                        >
                            csc.gov.ph
                        </a>
                        .
                    </p>
                </div>
            </main>
            <SiteFooter />
        </>
    );
}

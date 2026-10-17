import { Head, Link } from '@inertiajs/react';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';

type DateStatus = 'confirmed' | 'target' | 'unconfirmed';

type CseDate = {
    sitting: string;
    label: string;
    date: string | null;
    status: DateStatus;
    note: string | null;
    source_title: string;
    source_url: string;
    last_checked: string;
};

type Props = {
    dates: CseDate[];
    lastChecked: string;
};

const STATUS_LABEL: Record<DateStatus, string> = {
    confirmed: 'Confirmed',
    target: 'CSC target',
    unconfirmed: 'Unconfirmed',
};

function formatDay(iso: string): string {
    return new Date(`${iso}T00:00:00+08:00`).toLocaleDateString('en-PH', {
        weekday: 'short',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        timeZone: 'Asia/Manila',
    });
}

export default function CseDates({ dates, lastChecked }: Props) {
    const sittings = [...new Set(dates.map((d) => d.sitting))];

    return (
        <>
            <Head title="CSE 2027 Dates">
                <meta
                    name="description"
                    content="Civil Service Exam 2027 filing, exam and results dates, each linked to its official CSC source."
                />
            </Head>
            <SiteHeader activeNav="cse-dates" />
            <main className="bg-[#FAFAF7] text-[#101426] dark:bg-black dark:text-[#FAFAF7]">
                <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-12">
                    <header className="flex flex-col gap-3">
                        <h1 className="font-heading text-3xl font-semibold tracking-tight sm:text-4xl">
                            CSE 2027 Dates
                        </h1>
                        <p className="text-base leading-relaxed opacity-75">
                            Every date links to the CSC page it came from. Last
                            checked {formatDay(lastChecked)}. Civio is not the
                            Civil Service Commission, so confirm on csc.gov.ph
                            before you file.
                        </p>
                    </header>

                    {sittings.map((sitting) => (
                        <section
                            key={sitting}
                            className="flex flex-col gap-3"
                            aria-labelledby={`sitting-${sitting}`}
                        >
                            <h2
                                id={`sitting-${sitting}`}
                                className="font-heading text-xl font-semibold tracking-tight"
                            >
                                {sitting}
                            </h2>
                            <ul className="flex flex-col divide-y divide-black/10 dark:divide-white/15">
                                {dates
                                    .filter((d) => d.sitting === sitting)
                                    .map((d) => (
                                        <li
                                            key={d.label}
                                            className="flex flex-col gap-1 py-3"
                                        >
                                            <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
                                                <span className="font-semibold">
                                                    {d.label}
                                                </span>
                                                <span className="tabular-nums">
                                                    {d.date
                                                        ? formatDay(d.date)
                                                        : 'No date published'}
                                                </span>
                                            </div>
                                            <p className="text-sm opacity-75">
                                                <span
                                                    className={
                                                        d.status === 'confirmed'
                                                            ? 'font-semibold text-[#5B35F5] dark:text-[#B3F52D]'
                                                            : 'font-semibold'
                                                    }
                                                >
                                                    {STATUS_LABEL[d.status]}
                                                </span>
                                                {d.note ? ` · ${d.note}` : ''}
                                            </p>
                                            <a
                                                href={d.source_url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-sm underline-offset-4 hover:underline"
                                            >
                                                Source: {d.source_title}
                                            </a>
                                        </li>
                                    ))}
                            </ul>
                        </section>
                    ))}

                    <p className="text-sm">
                        <Link
                            href="/exams?start=subprofessional&free_attempt=1"
                            className="font-semibold text-[#5B35F5] underline-offset-4 hover:underline dark:text-[#B3F52D]"
                        >
                            Practice Sub Pro
                        </Link>
                        <span className="mx-2 opacity-40">·</span>
                        <Link
                            href="/exams?start=professional&free_attempt=1"
                            className="font-semibold underline-offset-4 hover:underline"
                        >
                            Practice Pro
                        </Link>
                    </p>
                </div>
            </main>
            <SiteFooter />
        </>
    );
}

CseDates.layout = undefined;

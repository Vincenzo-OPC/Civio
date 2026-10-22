import { Link } from '@inertiajs/react';
import AppLogo from './app-logo';

const FOOTER_LINKS = [
    { href: '/cse-2027-dates', label: 'CSE 2027 Dates' },
    { href: '/exam-day', label: 'Exam Day' },
    { href: '/terms', label: 'Terms' },
    { href: '/privacy', label: 'Privacy' },
    { href: '/support', label: 'Support' },
] as const;

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="w-full border-t border-[#E3E5EA] bg-[#FAFAF7] text-[#101426] dark:border-[#2a2a2a] dark:bg-black dark:text-[#FAFAF7]">
            <div className="mx-auto flex w-full max-w-3xl flex-col gap-4 px-4 py-6 sm:px-6">
                <Link href="/" className="inline-flex w-fit" aria-label="Civio">
                    <AppLogo />
                </Link>
                <div className="flex items-end justify-between gap-4">
                    <div className="flex flex-col gap-2 text-sm">
                        <p>© {currentYear} Civio. All rights reserved.</p>
                        <nav aria-label="Footer" className="flex gap-4">
                            {FOOTER_LINKS.map(({ href, label }) => (
                                <Link
                                    key={href}
                                    href={href}
                                    className="underline-offset-4 hover:underline"
                                >
                                    {label}
                                </Link>
                            ))}
                        </nav>
                    </div>
                </div>
            </div>
        </footer>
    );
}

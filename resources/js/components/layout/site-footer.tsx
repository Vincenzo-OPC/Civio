import { Link } from '@inertiajs/react';
import AppLogo from './app-logo';

const FOOTER_LINKS = [
    { href: '/terms', label: 'Terms' },
    { href: '/privacy', label: 'Privacy' },
    { href: '/support', label: 'Support' },
] as const;

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="w-full border-t border-[var(--civio-line,#e3e5ea)] bg-[var(--civio-paper,#fafaf7)] text-[var(--civio-ink,#101426)]">
            <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 sm:px-6">
                <div className="flex flex-col gap-3">
                    <Link
                        href="/"
                        className="inline-flex items-center text-base font-semibold"
                    >
                        <AppLogo />
                    </Link>
                    <p className="text-sm leading-relaxed text-[var(--civio-ink,#101426)]/70">
                        Practice for the Civil Service Exam. Civio is not the
                        Civil Service Commission.
                    </p>
                </div>

                <p className="text-sm leading-relaxed text-[var(--civio-ink,#101426)]/75">
                    Civio is an independent study app. It is not affiliated
                    with, endorsed by, or connected to the Civil Service
                    Commission or any Philippine government agency. The items
                    and explanations are for practice. A score here is not your
                    exam result.
                </p>

                <div className="flex flex-col gap-3 text-sm sm:flex-row sm:items-center sm:justify-between">
                    <p>© {currentYear} Civio</p>
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
        </footer>
    );
}

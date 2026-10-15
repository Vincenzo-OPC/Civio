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
        <footer className="w-full border-t border-[#E3E5EA] bg-[#FAFAF7] text-[#101426] dark:border-[#2c3148] dark:bg-[#101426] dark:text-[#FAFAF7]">
            <div className="mx-auto flex w-full max-w-3xl flex-col gap-4 px-4 py-6 sm:px-6">
                <Link href="/" className="inline-flex w-fit" aria-label="Civio">
                    <AppLogo />
                </Link>
                <div className="flex items-end justify-between gap-4">
                    <div className="flex flex-col gap-2 text-sm">
                        <p>© {currentYear} Civio. All Rights Reserved.</p>
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
                    <img
                        src="/images/bir-registered-2025.png"
                        alt="BIR registered, 2025"
                        width={960}
                        height={540}
                        className="h-14 w-auto shrink-0"
                    />
                </div>
            </div>
        </footer>
    );
}

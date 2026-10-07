import { Link } from '@inertiajs/react';
import type { LucideIcon } from 'lucide-react';
import { Mail, Scale, ShieldAlert, ShieldCheck } from 'lucide-react';

import AppLogo from './app-logo';

interface FooterLinkItem {
    readonly href: string;
    readonly label: string;
    readonly icon: LucideIcon;
}

const FOOTER_LINKS: readonly FooterLinkItem[] = [
    { href: '/terms', label: 'Terms of Service', icon: Scale },
    { href: '/privacy', label: 'Privacy Policy', icon: ShieldCheck },
    { href: '/support', label: 'Contact Support', icon: Mail },
];

const footerLinkClass =
    'group inline-flex items-center gap-1.5 underline decoration-border underline-offset-4 transition-all duration-300 hover:text-foreground hover:decoration-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none active:scale-95';

const disclaimerTextClass =
    'text-sm leading-relaxed font-medium text-amber-950/80 dark:text-slate-300';

function FooterBranding() {
    return (
        <div className="flex flex-col gap-3 lg:col-span-4">
            <Link
                href="/"
                className="group flex items-center gap-2 text-base font-black tracking-tight text-foreground transition-all duration-300 hover:opacity-90 focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none active:scale-95"
            >
                <AppLogo />
            </Link>

            <p className="max-w-2xl text-sm leading-relaxed font-medium text-muted-foreground">
                An interactive reviewer platform designed to help Filipino
                examinees strengthen core competencies for Professional and
                Sub-Professional Civil Service Examination preparation.
            </p>
        </div>
    );
}

function FooterDisclaimer() {
    return (
        <div className="shadow-3xs rounded-2xl border border-amber-500/20 bg-amber-500/5 p-5 lg:col-span-8 dark:bg-amber-950/10">
            <div className="flex gap-3">
                <ShieldAlert className="mt-0.5 size-5 shrink-0 text-amber-600 dark:text-amber-400" />

                <div className="flex flex-col gap-2">
                    <span className="text-xs font-black tracking-wider text-amber-800 uppercase dark:text-amber-400">
                        Legal Disclaimer & Educational Use Only
                    </span>

                    <p className={disclaimerTextClass}>
                        Civio is an independent educational learning platform
                        created solely for examination preparation and reviewer
                        practice simulation.{' '}
                        <strong>
                            This platform is NOT affiliated with, authorized,
                            endorsed by, or officially connected to the Civil
                            Service Commission (CSC)
                        </strong>{' '}
                        or any government agency in the Philippines.
                    </p>

                    <p className={disclaimerTextClass}>
                        All mock examinations, reviewer materials, explanations,
                        and practice content are independently created for
                        educational purposes only. Some questions and learning
                        modules may be AI-assisted or AI-generated.
                    </p>
                </div>
            </div>
        </div>
    );
}

function FooterNav() {
    return (
        <nav
            aria-label="Footer"
            className="order-1 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 md:order-2"
        >
            {FOOTER_LINKS.map(({ href, label, icon: Icon }) => (
                <Link key={href} href={href} className={footerLinkClass}>
                    <Icon className="size-3.5" />
                    {label}
                </Link>
            ))}
        </nav>
    );
}

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="w-full border-t border-border bg-card text-card-foreground">
            <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 items-start gap-4 sm:gap-8 lg:grid-cols-12">
                    <FooterBranding />
                    <FooterDisclaimer />
                </div>

                <div className="my-8 h-px w-full bg-border" />

                <div className="flex flex-col items-center justify-between gap-5 text-xs font-semibold text-muted-foreground md:flex-row">
                    <div className="order-3 text-center md:order-1 md:text-left">
                        © {currentYear} Civio
                    </div>

                    <FooterNav />
                </div>
            </div>
        </footer>
    );
}

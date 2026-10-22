import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface DashPanelProps {
    id: string;
    title: string;
    subtitle?: string;
    footer?: ReactNode;
    className?: string;
    children: ReactNode;
}

/**
 * Shared learner-dashboard card: one header, a body that takes the spare
 * height in an equal-height grid row, and a footer pinned to the bottom so
 * paired cards line up top and bottom without fixed heights.
 */
export function DashPanel({
    id,
    title,
    subtitle,
    footer,
    className,
    children,
}: DashPanelProps) {
    return (
        <section
            aria-labelledby={id}
            className={cn('dash-panel flex h-full flex-col', className)}
        >
            <header>
                <h2 id={id} className="dash-title">
                    {title}
                </h2>
                {subtitle ? (
                    <p className="dash-muted mt-0.5 text-sm">{subtitle}</p>
                ) : null}
            </header>
            <div className="@container mt-4 flex flex-1 flex-col">
                {children}
            </div>
            {footer ? (
                <footer className="mt-5 flex items-center justify-between gap-3 border-t border-(--dash-line) pt-4">
                    {footer}
                </footer>
            ) : null}
        </section>
    );
}

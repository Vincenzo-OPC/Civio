import LiteModeToggle from '@/components/shared/lite-mode-toggle';

interface DashboardHeroProps {
    /** Null for guests: they get an honest, non-personal greeting. */
    firstName: string | null;
    motivationText?: string | null;
}

/** Compact page heading. The next action lives in ContinueStudyingCard. */
export function DashboardHero({
    firstName,
    motivationText,
}: DashboardHeroProps) {
    const motivation =
        motivationText ||
        'Practice scores here are not a Civil Service Commission rating.';

    return (
        <header className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
                <h1 className="font-heading text-2xl font-semibold tracking-tight text-balance sm:text-[28px] sm:leading-9">
                    {firstName
                        ? `Welcome Back, ${firstName}`
                        : 'Start Your CSE Review'}
                </h1>
                <p className="dash-muted mt-1 max-w-2xl text-sm leading-relaxed">
                    {motivation}
                </p>
            </div>
            <div className="shrink-0">
                <LiteModeToggle />
            </div>
        </header>
    );
}

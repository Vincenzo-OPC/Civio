import { useLiteMode } from '@/hooks/use-lite-mode';
import { cn } from '@/lib/utils';

/** Small "Lite" switch for the dashboard and exam headers. */
export default function LiteModeToggle({ className }: { className?: string }) {
    const { lite, toggle } = useLiteMode();

    return (
        <button
            type="button"
            role="switch"
            aria-checked={lite}
            onClick={toggle}
            title={
                lite
                    ? 'Lite mode is on. Tap to turn it off.'
                    : 'Turn on Lite mode for slow or prepaid data.'
            }
            className={cn(
                'inline-flex min-h-9 items-center gap-1.5 rounded-full border px-3 text-xs font-medium',
                lite
                    ? 'border-emerald-600 bg-emerald-50 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200'
                    : 'border-slate-300 text-slate-600 dark:border-slate-600 dark:text-slate-300',
                className,
            )}
        >
            <span
                aria-hidden="true"
                className={cn(
                    'h-2 w-2 rounded-full',
                    lite ? 'bg-emerald-600' : 'bg-slate-400',
                )}
            />
            Lite {lite ? 'on' : 'off'}
        </button>
    );
}

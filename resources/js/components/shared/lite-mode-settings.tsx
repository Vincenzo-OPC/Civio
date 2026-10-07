import { useState } from 'react';
import { useLiteMode } from '@/hooks/use-lite-mode';
import type { LitePreference } from '@/lib/lite-mode';
import { readOfflineOptIn, writeOfflineOptIn } from '@/lib/lite-mode';
import { cn } from '@/lib/utils';

const OPTIONS: { value: LitePreference; label: string }[] = [
    { value: 'auto', label: 'Auto' },
    { value: 'on', label: 'On' },
    { value: 'off', label: 'Off' },
];

/** Settings > Appearance: Lite mode preference plus the offline opt-in. */
export default function LiteModeSettings() {
    const { lite, preference, setPreference } = useLiteMode();
    const [offline, setOffline] = useState(() =>
        typeof window === 'undefined' ? false : readOfflineOptIn(),
    );

    return (
        <section className="space-y-3" aria-labelledby="lite-mode-heading">
            <div>
                <h2 id="lite-mode-heading" className="text-sm font-medium">
                    Lite mode
                </h2>
                <p className="text-sm text-muted-foreground">
                    For slow or prepaid data. Turns off animations, charts,
                    pictures and live updates, and uses a text-first exam
                    screen. Auto turns it on when your phone asks to save data
                    or the connection is slow (3G or worse).
                </p>
            </div>

            <div
                role="radiogroup"
                aria-label="Lite mode"
                className="inline-flex gap-1 rounded-lg bg-slate-100 p-1 dark:bg-slate-800"
            >
                {OPTIONS.map(({ value, label }) => (
                    <button
                        key={value}
                        type="button"
                        role="radio"
                        aria-checked={preference === value}
                        onClick={() => setPreference(value)}
                        className={cn(
                            'min-h-11 rounded-md px-4 text-sm',
                            preference === value
                                ? 'bg-white dark:bg-slate-700 dark:text-slate-100'
                                : 'text-slate-500 hover:bg-slate-200/60 dark:text-slate-400 dark:hover:bg-slate-700/60',
                        )}
                    >
                        {label}
                    </button>
                ))}
            </div>

            <p className="text-sm" aria-live="polite">
                Lite is <strong>{lite ? 'on' : 'off'}</strong> right now.
            </p>

            <label className="flex items-start gap-2 text-sm">
                <input
                    type="checkbox"
                    className="mt-1 h-4 w-4"
                    checked={offline}
                    onChange={(event) => {
                        setOffline(event.target.checked);
                        writeOfflineOptIn(event.target.checked);
                    }}
                />
                <span>
                    Keep the app cached for offline use while Lite is on. This
                    downloads about 0.5 MB once. Takes effect on the next page
                    load.
                </span>
            </label>
        </section>
    );
}

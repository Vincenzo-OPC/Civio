import { Moon, Sun } from 'lucide-react';
import { useAppearance } from '@/hooks/use-appearance';

/** One click between light and dark. No system option. */
export function ThemeToggle({ className = '' }: { className?: string }) {
    const { resolvedAppearance, updateAppearance } = useAppearance();
    const isDark = resolvedAppearance === 'dark';

    return (
        <button
            type="button"
            onClick={() => updateAppearance(isDark ? 'light' : 'dark')}
            aria-pressed={isDark}
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            title={isDark ? 'Light mode' : 'Dark mode'}
            className={`flex size-9 shrink-0 items-center justify-center rounded-lg text-[#101426] dark:text-[#FAFAF7] ${className}`}
        >
            {isDark ? <Sun className="size-4" /> : <Moon className="size-4" />}
            <span className="sr-only">
                {isDark ? 'Light mode' : 'Dark mode'}
            </span>
        </button>
    );
}

export const DarkModeToggle = ThemeToggle;

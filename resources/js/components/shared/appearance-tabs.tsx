import type { LucideIcon } from 'lucide-react';
import { Moon, Sun } from 'lucide-react';
import type { HTMLAttributes } from 'react';
import type { Appearance } from '@/hooks/use-appearance';
import { useAppearance } from '@/hooks/use-appearance';
import { cn } from '@/lib/utils';

export default function AppearanceToggleTab({
    className = '',
    ...props
}: HTMLAttributes<HTMLDivElement>) {
    const { appearance, resolvedAppearance, updateAppearance } =
        useAppearance();
    const selected = appearance === 'system' ? resolvedAppearance : appearance;

    const tabs: { value: Appearance; icon: LucideIcon; label: string }[] = [
        { value: 'light', icon: Sun, label: 'Light' },
        { value: 'dark', icon: Moon, label: 'Dark' },
    ];

    return (
        <div
            className={cn(
                'inline-flex gap-1 rounded-lg bg-[#F4F5F2] p-1 dark:bg-[#1a1e30]',
                className,
            )}
            {...props}
        >
            {tabs.map(({ value, icon: Icon, label }) => (
                <button
                    key={value}
                    onClick={() => updateAppearance(value)}
                    className={cn(
                        'flex items-center rounded-md px-3.5 py-1.5 transition-colors',
                        selected === value
                            ? 'bg-white shadow-xs dark:bg-[#101426] dark:text-[#FAFAF7]'
                            : 'text-[#101426]/60 hover:text-[#101426] dark:text-[#FAFAF7]/60 dark:hover:text-[#FAFAF7]',
                    )}
                >
                    <Icon className="-ml-1 h-4 w-4" />
                    <span className="ml-1.5 text-sm">{label}</span>
                </button>
            ))}
        </div>
    );
}

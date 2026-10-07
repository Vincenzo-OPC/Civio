/** Small Online / Offline pill (Lite L2 offline drills). */
export function OnlineBadge({ online }: { online: boolean }) {
    return (
        <span
            role="status"
            className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                online
                    ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200'
                    : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-200'
            }`}
        >
            {online ? 'Online' : 'Offline'}
        </span>
    );
}

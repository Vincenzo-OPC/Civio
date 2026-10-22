/** Keep the server's absolute deadline while allowing a different device clock. */
export function localDeadline(
    deadline: string,
    serverNow: string,
    localNow: number,
): number {
    return localNow + Date.parse(deadline) - Date.parse(serverNow);
}

export function secondsUntil(deadline: number, now: number): number {
    return Math.max(0, Math.ceil((deadline - now) / 1000));
}

/**
 * Which countdown warning (if any) is due. Uses thresholds rather than exact
 * seconds: a throttled background tab can jump straight past 600 or 60.
 */
export function dueTimerWarning(
    secondsLeft: number,
    warned10Min: boolean,
    warned1Min: boolean,
): '10m' | '1m' | null {
    if (secondsLeft <= 60 && secondsLeft > 0 && !warned1Min) {
        return '1m';
    }

    if (secondsLeft <= 600 && secondsLeft > 60 && !warned10Min) {
        return '10m';
    }

    return null;
}

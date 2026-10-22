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

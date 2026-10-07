/**
 * Lite mode (L1): a lighter Civio for slow or metered connections.
 *
 * Auto-on when the browser asks for less data (Save-Data) or reports a slow
 * connection (slow-2g / 2g / 3g). The user can force it on or off in
 * Settings > Appearance or from the dashboard and exam headers.
 *
 * Lite adds the `lite` class to <html> (CSS turns off animations, blur,
 * shadows and decorative images, and uses system fonts) and sets the
 * `civio_lite` cookie so the server can skip or defer heavy props and
 * realtime config.
 */

export type LitePreference = 'auto' | 'on' | 'off';

export type ConnectionInfo = {
    saveData?: boolean;
    effectiveType?: string;
};

export const LITE_STORAGE_KEY = 'civio_lite_pref';
export const LITE_COOKIE = 'civio_lite';
export const LITE_CLASS = 'lite';
/** Lite skips the PWA precache unless the user opts into offline use. */
export const LITE_OFFLINE_KEY = 'civio_lite_offline';

const SLOW_TYPES = new Set(['slow-2g', '2g', '3g']);

/** Pure: should Lite switch on by itself for this connection? */
export function detectLite(connection?: ConnectionInfo | null): boolean {
    if (!connection) {
        return false;
    }

    if (connection.saveData === true) {
        return true;
    }

    return SLOW_TYPES.has(String(connection.effectiveType ?? '').toLowerCase());
}

/** Pure: the stored preference wins; "auto" follows the connection. */
export function resolveLite(
    preference: LitePreference,
    connection?: ConnectionInfo | null,
): boolean {
    if (preference === 'on') {
        return true;
    }

    if (preference === 'off') {
        return false;
    }

    return detectLite(connection);
}

export function parsePreference(value: unknown): LitePreference {
    return value === 'on' || value === 'off' ? value : 'auto';
}

type ClassTarget = {
    classList: { toggle: (name: string, force?: boolean) => unknown };
};

/** Pure-ish: toggles the `lite` class on the given element (normally <html>). */
export function applyLiteClass(
    target: ClassTarget | null | undefined,
    on: boolean,
): void {
    target?.classList.toggle(LITE_CLASS, on);
}

/** Pure: register the service worker (and its precache) in this mode? */
export function shouldRegisterServiceWorker(
    lite: boolean,
    offlineOptIn: boolean,
): boolean {
    return !lite || offlineOptIn;
}

export function readOfflineOptIn(): boolean {
    try {
        return localStorage.getItem(LITE_OFFLINE_KEY) === '1';
    } catch {
        return false;
    }
}

export function writeOfflineOptIn(on: boolean): void {
    try {
        localStorage.setItem(LITE_OFFLINE_KEY, on ? '1' : '0');
    } catch {
        /* ignore */
    }
}

// ---- browser store (useSyncExternalStore-friendly) ----

type NetworkConnection = ConnectionInfo & {
    addEventListener?: (type: 'change', cb: () => void) => void;
};

const listeners = new Set<() => void>();
let preference: LitePreference = 'auto';
let active = false;
let initialized = false;

function connection(): NetworkConnection | null {
    if (typeof navigator === 'undefined') {
        return null;
    }

    return (
        (navigator as Navigator & { connection?: NetworkConnection })
            .connection ?? null
    );
}

function writeCookie(on: boolean): void {
    if (typeof document === 'undefined') {
        return;
    }

    document.cookie = `${LITE_COOKIE}=${on ? '1' : '0'};path=/;max-age=${365 * 24 * 60 * 60};SameSite=Lax`;
}

function recompute(): void {
    const next = resolveLite(preference, connection());

    active = next;

    if (typeof document !== 'undefined') {
        applyLiteClass(document.documentElement, next);
    }

    writeCookie(next);
    listeners.forEach((listener) => listener());
}

export function initializeLiteMode(): void {
    if (typeof window === 'undefined' || initialized) {
        return;
    }

    initialized = true;

    try {
        preference = parsePreference(localStorage.getItem(LITE_STORAGE_KEY));
    } catch {
        preference = 'auto';
    }

    recompute();
    connection()?.addEventListener?.('change', () => {
        if (preference === 'auto') {
            recompute();
        }
    });
}

export function isLiteActive(): boolean {
    return active;
}

export function getLitePreference(): LitePreference {
    return preference;
}

export function setLitePreference(next: LitePreference): void {
    preference = next;

    try {
        localStorage.setItem(LITE_STORAGE_KEY, next);
    } catch {
        /* private mode: the cookie still carries it for this visit */
    }

    recompute();
}

export function subscribeLite(listener: () => void): () => void {
    listeners.add(listener);

    return () => listeners.delete(listener);
}

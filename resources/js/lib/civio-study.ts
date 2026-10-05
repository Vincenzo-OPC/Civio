import { usePage } from '@inertiajs/react';

type CivioShared = {
    guestUnlimited?: boolean;
    contentShield?: boolean;
};

function isLocalStudyHost(): boolean {
    if (typeof window === 'undefined') {
        return false;
    }
    const host = window.location.hostname;
    const port = window.location.port;
    // Covers localhost, 127.0.0.1, ::1, and common Docker/internal hosts on any port (including :8080)
    return (
        host === 'localhost' ||
        host === '127.0.0.1' ||
        host === '[::1]' ||
        host.endsWith('.local') ||
        host.includes('docker') ||
        host.includes('hiraya') ||
        port === '8080' ||
        port === '3000' ||
        port === '5173'
    );
}

/**
 * Local-study guest policy: env CIVIO_GUEST_UNLIMITED (via Inertia)
 * plus localhost/127.0.0.1 fallback so Docker study never hard-blocks.
 */
export function isGuestUnlimitedFromProps(civio?: CivioShared | null): boolean {
    if (civio?.guestUnlimited === true) {
        return true;
    }

    if (isLocalStudyHost()) {
        return true;
    }

    return false;
}

export function useGuestUnlimited(): boolean {
    const props = usePage().props as { civio?: CivioShared };
    return isGuestUnlimitedFromProps(props?.civio);
}

/**
 * Content shield: OFF when CIVIO_CONTENT_SHIELD=false (Inertia) OR localhost.
 * Default ON only for non-local hosts when prop is missing/true (production).
 */
export function isContentShieldEnabledFromProps(
    civio?: CivioShared | null,
): boolean {
    if (isLocalStudyHost()) {
        return false;
    }
    if (civio?.contentShield === false) {
        return false;
    }
    if (civio?.contentShield === true) {
        return true;
    }
    // Missing prop on non-local: default OFF for study (copy/paste allowed). Production can force true via env.
    return false;
}

export function useContentShieldEnabled(): boolean {
    const props = usePage().props as { civio?: CivioShared };
    return isContentShieldEnabledFromProps(props?.civio);
}
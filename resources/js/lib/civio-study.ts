import { usePage } from '@inertiajs/react';

type CivioShared = {
    guestUnlimited?: boolean;
    contentShield?: boolean;
};

/**
 * Local-study guest policy: env CIVIO_GUEST_UNLIMITED (via Inertia)
 * plus localhost/127.0.0.1 fallback so Docker study never hard-blocks.
 */
export function isGuestUnlimitedFromProps(civio?: CivioShared | null): boolean {
    if (civio?.guestUnlimited === true) {
        return true;
    }

    if (typeof window !== 'undefined') {
        const host = window.location.hostname;
        if (host === 'localhost' || host === '127.0.0.1') {
            return true;
        }
    }

    return false;
}

export function useGuestUnlimited(): boolean {
    const props = usePage().props as { civio?: CivioShared };
    return isGuestUnlimitedFromProps(props?.civio);
}

export function useContentShieldEnabled(): boolean {
    const props = usePage().props as { civio?: CivioShared };
    // Default ON unless explicitly disabled; localhost still hard-bypasses in useContentShield.
    if (props?.civio?.contentShield === false) {
        return false;
    }
    return true;
}

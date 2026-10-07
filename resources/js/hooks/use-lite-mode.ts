import { useCallback, useSyncExternalStore } from 'react';
import type { LitePreference } from '@/lib/lite-mode';
import {
    getLitePreference,
    isLiteActive,
    setLitePreference,
    subscribeLite,
} from '@/lib/lite-mode';

export type UseLiteModeReturn = {
    /** Lite is on right now (forced on, or auto-detected). */
    readonly lite: boolean;
    readonly preference: LitePreference;
    readonly setPreference: (next: LitePreference) => void;
    /** Flip Lite on/off explicitly (used by the header controls). */
    readonly toggle: () => void;
};

export function useLiteMode(): UseLiteModeReturn {
    const lite = useSyncExternalStore(subscribeLite, isLiteActive, () => false);
    const preference = useSyncExternalStore(
        subscribeLite,
        getLitePreference,
        () => 'auto' as LitePreference,
    );

    const toggle = useCallback(() => {
        setLitePreference(isLiteActive() ? 'off' : 'on');
    }, []);

    return { lite, preference, setPreference: setLitePreference, toggle };
}
